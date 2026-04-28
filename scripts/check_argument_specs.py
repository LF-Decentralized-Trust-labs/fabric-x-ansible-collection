#!/usr/bin/env python3
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Check that argument_specs.yaml entrypoints and tasks/ files are in exact sync.

For every role under roles/:
  - Reads meta/argument_specs.yaml and extracts the entrypoint names
    (all top-level keys under ``argument_specs:`` except ``role-options``,
    which is a shared variable catalog, not a callable task).
  - Walks tasks/ and collects relative slash-paths (without .yaml extension),
    excluding ``main`` (not reachable via tasks_from:).
  - Reports any mismatches:
      ghost       — declared in argument_specs but no matching task file found
      undocumented — task file exists but not declared in argument_specs

Exits 0 if all roles are clean, 1 if any mismatch is found.

Usage:
    python3 scripts/check_argument_specs.py [--roles-dir PATH]
"""

import argparse
import sys
from pathlib import Path

import yaml

# ANSI color codes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color

# Top-level keys under argument_specs: that are NOT callable entrypoints.
# ``role-options`` is a dedicated section used to collect all role variables
# via YAML anchors (&name) so they can be aliased (*name) into real entrypoints.
NON_ENTRYPOINT_KEYS = {"role-options"}


class SpecError(Exception):
    """Raised when argument_specs.yaml cannot be parsed or has an unexpected shape."""


def extract_spec_tasks(argument_specs_path):
    """Return the set of callable entrypoint names from argument_specs.yaml.

    Raises SpecError for malformed YAML or unexpected document shape.
    """
    try:
        with argument_specs_path.open() as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise SpecError(f"invalid YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise SpecError("argument_specs.yaml must be a YAML mapping at the top level")

    specs = data.get("argument_specs")
    if specs is None:
        raise SpecError("missing top-level 'argument_specs' key")
    if not isinstance(specs, dict):
        raise SpecError("'argument_specs' must be a mapping")

    result = set()
    for key in specs:
        if not isinstance(key, str):
            raise SpecError(f"non-string key in argument_specs: {key!r}")
        if key not in NON_ENTRYPOINT_KEYS:
            result.add(key)
    return result


def extract_file_tasks(tasks_dir):
    """Return slash-paths of task files under tasks/, excluding main.

    Only .yaml files are expected; .yml files are flagged as violations of the
    repo convention that all task files use the .yaml extension.

    Returns a tuple (task_paths, yml_violations) where:
      task_paths     — set of slash-paths (suffix stripped)
      yml_violations — list of Path objects whose suffix is .yml
    """
    task_paths = set()
    yml_violations = []
    if not tasks_dir.is_dir():
        return task_paths, yml_violations
    for f in tasks_dir.rglob("*"):
        if not f.is_file():
            continue
        if f.suffix == ".yml":
            yml_violations.append(f)
        elif f.suffix == ".yaml":
            slash_path = f.relative_to(tasks_dir).with_suffix("").as_posix()
            if slash_path != "main":
                task_paths.add(slash_path)
    return task_paths, yml_violations


def check_role(role_dir):
    """Check a single role. Returns True if clean, False if any mismatch."""
    specs_file = role_dir / "meta" / "argument_specs.yaml"

    if not specs_file.exists():
        print(f"{YELLOW}[SKIP]{NC}   {role_dir.name}: no argument_specs.yaml found")
        return True

    try:
        spec_tasks = extract_spec_tasks(specs_file)
    except SpecError as exc:
        print(f"{RED}[FAIL]{NC}   {role_dir.name}: {exc}")
        return False

    file_tasks, yml_violations = extract_file_tasks(role_dir / "tasks")

    ghost = sorted(spec_tasks - file_tasks)
    undocumented = sorted(file_tasks - spec_tasks)

    if not ghost and not undocumented and not yml_violations:
        print(f"{GREEN}[OK]{NC}     {role_dir.name}")
        return True

    print(f"{RED}[FAIL]{NC}   {role_dir.name}")
    if ghost:
        print("  In argument_specs but no task file found (ghost entries):")
        for entry in ghost:
            print(f"    - {entry}")
    if undocumented:
        print("  Task file exists but not declared in argument_specs (undocumented):")
        for entry in undocumented:
            print(f"    + {entry}")
    if yml_violations:
        print("  Task files with .yml extension (must use .yaml):")
        for path in sorted(yml_violations):
            print(f"    ! {path.relative_to(role_dir)}")
    return False


def main():
    script_dir = Path(__file__).resolve().parent
    default_roles_dir = script_dir.parent / "roles"

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--roles-dir",
        type=Path,
        default=default_roles_dir,
        help=f"Path to the roles directory (default: {default_roles_dir})",
    )
    args = parser.parse_args()
    roles_dir = args.roles_dir

    if not roles_dir.is_dir():
        print(f"{RED}Error:{NC} roles directory not found: {roles_dir}", file=sys.stderr)
        sys.exit(1)

    role_dirs = sorted(p for p in roles_dir.iterdir() if p.is_dir())

    if not role_dirs:
        print(f"{YELLOW}Warning:{NC} no roles found in {roles_dir}", file=sys.stderr)
        sys.exit(0)

    print(f"Checking argument_specs alignment for {len(role_dirs)} role(s) in: {roles_dir}\n")

    failures = 0
    for role_dir in role_dirs:
        if not check_role(role_dir):
            failures += 1

    print()
    if failures == 0:
        print(f"{GREEN}All {len(role_dirs)} role(s) passed.{NC}")
    else:
        print(f"{RED}{failures} of {len(role_dirs)} role(s) failed.{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
