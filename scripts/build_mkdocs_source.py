#!/usr/bin/env python3
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Generate the MkDocs source tree from the repository README files."""

import re
import shutil
import sys
from pathlib import Path
from posixpath import relpath
from urllib.parse import quote, urlsplit

# GitHub URLs produced for links that point to repository files we do not copy
# into the MkDocs source tree.
REPO_URL = "https://github.com/LF-Decentralized-Trust-labs/fabric-x-ansible-collection"
GITHUB_BRANCH = "main"

# Generated MkDocs input directory. This path is intentionally ignored by git
# and rebuilt whenever docs are served or deployed.
# pathlib.Path overloads the "/" operator for path joining, so expressions like
# Path("docs") / "mkdocs" mean "docs/mkdocs", not division.
DOCS_ROOT = Path("docs") / "mkdocs"

# Matches normal Markdown links and images, for example:
#   [Roles](./roles/README.md)
#   ![Network](./examples/images/fabric-x.drawio.png)
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")

# Matches links that wrap an image, for example:
#   [![License](https://img.shields.io/...)](LICENSE)
# The regular expression above cannot handle this nested bracket shape.
NESTED_IMAGE_LINK_RE = re.compile(r"(\[!\[[^\]]*\]\([^)]+\)\]\()([^)\s]+)(\))")
TABLE_OF_CONTENTS_RE = re.compile(
    r"(?ms)^## Table of Contents <!-- omit in toc -->\n\n.*?(?=^## )",
)


def is_external_link(target: str) -> bool:
    """Return True when a Markdown link target should be left untouched."""
    # In-page anchors already make sense after copying the Markdown file.
    if target.startswith("#"):
        return True

    # Links with a URL scheme or host, such as https://, mailto:, or //example,
    # are not repository-relative links and should not be rewritten.
    parsed = urlsplit(target)
    return bool(parsed.scheme or parsed.netloc)


def split_anchor(target: str) -> tuple[str, str]:
    """Split a local Markdown target into path and optional anchor parts."""
    # Keep anchors attached to whatever URL we produce later.
    if "#" not in target:
        return target, ""
    path, anchor = target.split("#", 1)
    return path, f"#{anchor}"


def remove_manual_table_of_contents(text: str) -> str:
    """Remove GitHub-oriented manual TOCs from generated MkDocs pages."""
    # MkDocs Material already renders page headings in the right-hand table of
    # contents, so the copied GitHub TOC is redundant and can render poorly.
    return TABLE_OF_CONTENTS_RE.sub("", text)


def normalize_repo_target(repo_root: Path, source_file: Path, link_path: str) -> tuple[Path, bool] | None:
    """Resolve a local link from source_file to a repository-relative path."""
    # Empty local paths are pure anchors and are handled before this function.
    if not link_path:
        return None

    # Resolve the link from the original source README location, not from the
    # generated docs/mkdocs location.
    source_dir = source_file.parent
    resolved = (source_dir / link_path).resolve()

    # Ignore links that escape the repository root.
    try:
        repo_path = resolved.relative_to(repo_root)
    except ValueError:
        return None

    # Directory links that contain README.md are treated as documentation pages,
    # so a source link to roles/cryptogen can map to roles/cryptogen/README.md.
    if resolved.is_dir():
        if (resolved / "README.md").exists():
            return repo_path / "README.md", True

        # Directories without README.md are repository source directories, so
        # they should become GitHub tree links.
        return repo_path, True

    # Existing files are either copied docs/assets or GitHub blob links,
    # depending on whether they appear in the maps built below.
    if resolved.exists():
        return repo_path, False

    # Support extensionless directory-style links where the raw path does not
    # exist in the generated tree but path/README.md does exist in the repo.
    readme_candidate = resolved / "README.md"
    if readme_candidate.exists():
        return repo_path / "README.md", False

    # Leave unresolved local paths as repository paths. MkDocs will not receive
    # them directly; they become GitHub links, which keeps the site focused on
    # selected Markdown pages.
    return repo_path, False


def relative_site_link(source_site_file: Path, target_site_file: Path, anchor: str = "") -> str:
    """Build a relative MkDocs link between generated site files."""
    # All site paths here are relative to docs/mkdocs.
    source_dir = source_site_file.parent.as_posix() or "."

    # Link to the generated Markdown file itself, not to the clean directory
    # URL. MkDocs validates source Markdown against actual files and will render
    # index.md links as clean URLs in the built site.
    link = relpath(target_site_file.as_posix(), source_dir)
    return f"{link}{anchor}"


def github_link(repo_path: Path, is_directory: bool = False, anchor: str = "") -> str:
    """Build a GitHub blob link for a repository-relative path."""
    # Quote path segments so special characters remain valid in a URL.
    quoted = quote(repo_path.as_posix())

    # GitHub uses /tree/ for directories and /blob/ for files.
    view = "tree" if is_directory else "blob"
    return f"{REPO_URL}/{view}/{GITHUB_BRANCH}/{quoted}{anchor}"


def rewrite_links(
    text: str,
    repo_root: Path,
    source_repo_file: Path,
    source_site_file: Path,
    doc_page_map: dict[Path, Path],
    asset_map: dict[Path, Path],
) -> str:
    """Rewrite relative Markdown links for the generated MkDocs tree."""

    def replace(match):
        prefix, target, suffix = match.groups()

        # External links and in-page anchors are already valid.
        if is_external_link(target):
            return match.group(0)

        # Separate the local file path from a possible #section anchor.
        path_part, anchor = split_anchor(target)

        # Resolve the link against the original README's repo location.
        normalized = normalize_repo_target(repo_root, source_repo_file, path_part)
        if normalized is None:
            return match.group(0)
        repo_target, is_directory = normalized

        # If the target is one of the copied Markdown docs, link inside MkDocs.
        if repo_target in doc_page_map:
            new_target = relative_site_link(source_site_file, doc_page_map[repo_target], anchor)

        # If the target is one of the copied assets, link to the copied asset.
        elif repo_target in asset_map:
            new_target = relative_site_link(source_site_file, asset_map[repo_target], anchor)

        # Everything else is repo source, so link to GitHub instead of copying it.
        else:
            new_target = github_link(repo_target, is_directory, anchor)
        return f"{prefix}{new_target}{suffix}"

    # Rewrite nested image links first so the normal link regex does not consume
    # only the inner image URL.
    text = NESTED_IMAGE_LINK_RE.sub(replace, text)
    return MARKDOWN_LINK_RE.sub(replace, text)


def discover_doc_pages(repo_root: Path) -> dict[Path, Path]:
    """Return source README paths mapped to generated MkDocs paths."""
    # Fixed documentation pages that are not discovered automatically from the repository.
    pages = {
        # The root README becomes the MkDocs index page.
        Path("README.md"): Path("index.md"),
        # Examples README
        Path("examples") / "README.md": Path("examples") / "index.md",
        # Playbooks README
        Path("playbooks") / "README.md": Path("playbooks") / "index.md",
        # Roles README
        Path("roles") / "README.md": Path("roles") / "index.md",
        # Inventory documentation overview
        Path("examples") / "inventory" / "README.md": Path("examples") / "inventory" / "index.md",
    }

    # Add per-inventory Markdown pages. These pages sit beside the example
    # inventory YAML files and document each deployment variant.
    inventory_docs_dir = repo_root / "examples" / "inventory" / "docs"
    if inventory_docs_dir.exists():
        for page in sorted(inventory_docs_dir.rglob("*.md")):
            repo_page = page.relative_to(repo_root)
            if repo_page in pages:
                continue
            pages[repo_page] = repo_page

    # Add README pages for supported playbook namespaces.
    for readme in sorted((repo_root / "playbooks").glob("*/README.md")):
        namespace = readme.parent.name
        pages[Path("playbooks") / namespace / "README.md"] = (
            Path("playbooks") / namespace / "index.md"
        )

    # Add to the static pages all the role README.md that are currently present in the repository.
    for readme in sorted((repo_root / "roles").glob("*/README.md")):
        role_name = readme.parent.name
        pages[Path("roles") / role_name / "README.md"] = Path("roles") / role_name / "index.md"
    return pages


def discover_assets(repo_root: Path) -> dict[Path, Path]:
    """Return source asset paths mapped to generated MkDocs asset paths."""
    assets = {}

    # Copy all public image assets used by the existing example READMEs.
    images_dir = repo_root / "examples" / "images"
    if images_dir.exists():
        for asset in sorted(images_dir.rglob("*")):
            if asset.is_file():
                # Keep asset paths unchanged under docs/mkdocs so existing image
                # links remain intuitive after rewriting.
                repo_path = asset.relative_to(repo_root)
                assets[repo_path] = repo_path
    return assets


def build_docs(repo_root: Path) -> None:
    """Build docs/mkdocs from selected repository docs."""
    repo_root = Path(repo_root).resolve()
    docs_root = repo_root / DOCS_ROOT

    # Clean existing docs/mkdocs tree before regeneration.
    if docs_root.exists():
        shutil.rmtree(docs_root)
    docs_root.mkdir(parents=True)

    # These maps are the source of truth for deciding whether a local link is
    # an internal MkDocs link, a copied asset, or a GitHub source link.
    doc_page_map = discover_doc_pages(repo_root)
    asset_map = discover_assets(repo_root)

    # Copy every selected README into its generated MkDocs location after
    # rewriting links from the perspective of the original source file.
    for source_repo_file, target_site_file in sorted(doc_page_map.items()):
        source_file = repo_root / source_repo_file
        if not source_file.exists():
            print(f"WARNING: expected doc page not found, skipping: {source_repo_file}", file=sys.stderr)
            continue
        target_file = docs_root / target_site_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        text = source_file.read_text(encoding="utf-8")
        text = remove_manual_table_of_contents(text)
        rewritten = rewrite_links(
            text,
            repo_root,
            source_file,
            target_site_file,
            doc_page_map,
            asset_map,
        )
        target_file.write_text(rewritten, encoding="utf-8")

    # Copy binary/static assets after Markdown generation. No rewriting is
    # needed for asset contents.
    for source_repo_file, target_site_file in sorted(asset_map.items()):
        source_file = repo_root / source_repo_file
        target_file = docs_root / target_site_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)


def main():
    # The script lives in scripts/, so parents[1] is the repository root.
    build_docs(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
