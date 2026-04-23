#!/usr/bin/env python3
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Local wrapper around ``aar-doc`` generation.

This collection uses ``aar-doc`` for two separate tasks:

1. render role READMEs from ``meta/argument_specs.yaml``
2. render ``defaults/main.yaml`` from the same argument specs

This wrapper is used as the collection's single entrypoint for both commands.
README generation works with the upstream CLI plus a custom Jinja template,
while defaults generation needs a few behavior changes that are not exposed by
``aar-doc`` as CLI settings:

- keep very long single-line defaults on one line instead of re-wrapping them
- preserve the original ruamel scalar style for multiline defaults
- prepend the repository license header to generated defaults files

The second point matters for Jinja expressions declared in YAML with explicit
block scalar styles such as ``>-`` in ``argument_specs.yaml``. Without this
wrapper, ``aar-doc`` normalizes multiline strings into literal blocks and the
generated defaults lose the original folded style choice.

The wrapper therefore monkey-patches the small parts of ``aar_doc.defaults``
that turn parsed argument spec values into the final YAML output.
"""

from os import linesep
from pathlib import Path

import aar_doc.defaults as _d
import aar_doc.markdown as _m
from ruamel.yaml.scalarstring import FoldedScalarString, ScalarString, SingleQuotedScalarString

LICENSE_HEADER = "\n".join(
    [
        "#",
        "# Copyright IBM Corp. All Rights Reserved.",
        "#",
        "# SPDX-License-Identifier: Apache-2.0",
        "#",
    ],
) + "\n"
_ORIGINAL_WRITE_MARKDOWN = _m.write_markdown

# ``aar-doc`` uses a module-level ``ruamel.yaml.YAML`` instance for dumping the
# generated defaults. Setting an effectively unlimited width prevents long
# single-line Jinja expressions from being wrapped onto multiple physical lines.
_d.yaml.best_width = 99999
_d.yaml.width = 99999


def _add_default_preserving_scalar_style(self, name, value, description, depth=0):
    """Store defaults without discarding ruamel scalar subclasses.

    Upstream ``aar-doc`` strips string defaults with ``value.strip()``. That is
    fine for plain Python strings, but for ruamel scalar subclasses it also
    drops the style information that tells the YAML dumper whether the source
    value originally came from ``>-``, ``|``, etc.

    Here we rebuild the same scalar subclass after trimming whitespace so the
    resulting ``RoleDefault`` still carries the original YAML style.
    """
    if isinstance(value, ScalarString):
        value = type(value)(str(value).strip())
    elif isinstance(value, str):
        value = value.strip()

    if self._overwrite:
        self._defaults[name] = _d.RoleDefault(name, value, description, depth)
    else:
        self._defaults.setdefault(name, _d.RoleDefault(name, value, description, depth))


def _safe_quote_recursive_preserving_scalar_style(self, value):
    """Apply the same quoting rules as ``aar-doc`` without flattening styles.

    ``aar-doc`` walks every generated default recursively before dumping it:

    - quote YAML-sensitive strings such as ``yes`` / ``no`` and values
      containing ``:``
    - render multiline strings as block scalars

    The upstream implementation converts every multiline string to a literal
    block. For this collection we want to keep ruamel scalar subclasses
    untouched when they already carry an explicit style from the source YAML.

    For plain Python strings that happen to contain newlines we still choose a
    folded block (``>-``), which keeps the generated defaults compact while
    remaining readable.
    """
    if isinstance(value, list):
        return [self.safe_quote_recursive(v) for v in value]
    if isinstance(value, dict):
        for key, item in value.items():
            value[key] = self.safe_quote_recursive(item)
        return value
    if isinstance(value, ScalarString):
        if "\n" in str(value):
            return value
        value = str(value)
    if isinstance(value, str):
        if value in ("yes", "no"):
            return SingleQuotedScalarString(value)
        if "\n" in value:
            return FoldedScalarString(value)
        if ":" in value:
            return SingleQuotedScalarString(value)
    return value


def _write_defaults_with_license_header(output_file_path, role_path, role_defaults):
    """Write generated defaults with the collection license header."""
    if output_file_path.name == "README.md":
        output = role_path / "defaults" / "main.yml"
    elif output_file_path.is_absolute():
        output = output_file_path
    else:
        output = role_path / "defaults" / output_file_path
    output = Path(output).resolve()

    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as defaults_file:
        defaults_file.write(LICENSE_HEADER)
        defaults_file.writelines(
            ["---" + linesep, "# Automatically generated by aar-doc" + linesep],
        )
        _d.yaml.dump(role_defaults, defaults_file)


def _write_markdown_without_leading_blank_line(ctx, content):
    """Normalize generated Markdown before delegating to aar-doc."""
    _ORIGINAL_WRITE_MARKDOWN(ctx, content.lstrip("\n"))

    output = ctx.obj["config"]["output_file"].expanduser()
    if "/" not in str(output):
        output = ctx.obj["config"]["role_path"] / output
    output = Path(output).resolve()

    normalized = output.read_text(encoding="utf-8").lstrip("\n")
    output.write_text(normalized, encoding="utf-8")


# Replace the two upstream methods used during defaults generation with the
# style-preserving versions above. The rest of ``aar-doc`` remains unchanged.
_d.RoleDefaultsManager.add_default = _add_default_preserving_scalar_style
_d.RoleDefaultsManager.safe_quote_recursive = _safe_quote_recursive_preserving_scalar_style
_d.write_defaults = _write_defaults_with_license_header
_m.write_markdown = _write_markdown_without_leading_blank_line

from aar_doc.cli import app  # noqa: E402
import aar_doc.cli as _cli  # noqa: E402

_cli.write_markdown = _write_markdown_without_leading_blank_line

# Re-export the original Typer application so this wrapper can be invoked as a
# drop-in replacement for the ``aar-doc`` CLI.
app()
