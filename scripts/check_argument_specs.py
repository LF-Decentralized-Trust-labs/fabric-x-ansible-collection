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
      unused anchor — YAML anchor is defined but never aliased
      uncataloged option — entrypoint option is missing from role-options

Exits 0 if all roles are clean, 1 if any mismatch is found.

Usage:
    python3 scripts/check_argument_specs.py [--roles-dir PATH]
"""

import argparse
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, TemplateAssertionError, TemplateSyntaxError, meta
from yaml.events import AliasEvent

# ANSI color codes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color

# Top-level keys under argument_specs: that are NOT callable entrypoints.
# ``role-options`` is a dedicated section used to collect all role variables
# via YAML anchors (&name) so they can be aliased (*name) into real entrypoints.
NON_ENTRYPOINT_KEYS = {"role-options"}

# Fields that Ansible treats as Jinja expressions even when they are not wrapped
# in ``{{ ... }}``.
BARE_EXPRESSION_KEYS = {
    "changed_when",
    "delegate_to",
    "failed_when",
    "loop",
    "until",
    "when",
}

# These expression fields commonly accept lists whose items are still
# expressions. A literal loop list, however, is data rather than expression
# syntax, so its plain string items must not be parsed as variables.
BARE_EXPRESSION_LIST_KEYS = BARE_EXPRESSION_KEYS - {"loop"}

# Variables provided by Ansible/Jinja at runtime rather than by role callers.
BUILTIN_VARS = {
    "ansible_check_mode",
    "ansible_config_file",
    "ansible_diff_mode",
    "ansible_host",
    "ansible_facts",
    "ansible_forks",
    "ansible_inventory_sources",
    "ansible_limit",
    "ansible_play_batch",
    "ansible_play_hosts",
    "ansible_play_hosts_all",
    "ansible_play_name",
    "ansible_play_role_names",
    "ansible_playbook_python",
    "ansible_role_names",
    "ansible_run_tags",
    "ansible_skip_tags",
    "ansible_verbosity",
    "ansible_version",
    "environment",
    "group_names",
    "groups",
    "hostvars",
    "inventory_dir",
    "inventory_file",
    "inventory_hostname",
    "inventory_hostname_short",
    "item",
    "localhost",
    "lookup",
    "omit",
    "play_hosts",
    "playbook_dir",
    "query",
    "role_name",
    "role_names",
    "role_path",
    "vars",
}

JINJA_ENV = Environment()
UNKNOWN_FILTER_RE = re.compile(r"No filter named '([^']+)'")
UNKNOWN_TEST_RE = re.compile(r"No test named '([^']+)'")


def passthrough_filter(value, *args, **kwargs):
    """Placeholder for Ansible filters unknown to plain Jinja."""
    return value


def passthrough_test(value, *args, **kwargs):
    """Placeholder for Ansible tests unknown to plain Jinja."""
    return bool(value)


class SpecError(Exception):
    """Raised when argument_specs.yaml cannot be parsed or has an unexpected shape."""


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


def load_argument_specs(argument_specs_path):
    """Return the parsed argument_specs mapping.

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
    return specs


def extract_spec_options(specs):
    """Return direct option names for each callable entrypoint."""
    result = {}
    for entrypoint, spec in specs.items():
        if not isinstance(entrypoint, str):
            raise SpecError(f"non-string key in argument_specs: {entrypoint!r}")
        if entrypoint in NON_ENTRYPOINT_KEYS:
            continue
        if spec is None:
            result[entrypoint] = set()
            continue
        if not isinstance(spec, dict):
            raise SpecError(f"argument_specs.{entrypoint!r} must be a mapping")
        options = spec.get("options", {})
        if options is None:
            result[entrypoint] = set()
            continue
        if not isinstance(options, dict):
            raise SpecError(f"argument_specs.{entrypoint}.options must be a mapping")
        option_names = set()
        for option in options:
            if not isinstance(option, str):
                raise SpecError(
                    f"non-string key in argument_specs.{entrypoint}.options: {option!r}"
                )
            option_names.add(option)
        result[entrypoint] = option_names
    return result


def parse_jinja_variables(value, source):
    """Return undeclared variables referenced by one Jinja template string."""
    while True:
        try:
            ast = JINJA_ENV.parse(value)
            return meta.find_undeclared_variables(ast)
        except TemplateAssertionError as exc:
            filter_match = UNKNOWN_FILTER_RE.search(str(exc))
            if filter_match:
                JINJA_ENV.filters[filter_match.group(1)] = passthrough_filter
                continue
            test_match = UNKNOWN_TEST_RE.search(str(exc))
            if test_match:
                JINJA_ENV.tests[test_match.group(1)] = passthrough_test
                continue
            raise SpecError(f"invalid Jinja in {source}: {exc}") from exc
        except TemplateSyntaxError as exc:
            raise SpecError(f"invalid Jinja in {source}: {exc}") from exc


def is_jinja_template(value):
    """Return True when a string contains explicit Jinja delimiters."""
    return "{{" in value or "{%" in value or "{#" in value


def extract_string_vars(value, source, parse_bare_expression=False):
    """Return variables from a task string value."""
    if is_jinja_template(value):
        return parse_jinja_variables(value, source)
    if parse_bare_expression and value.strip():
        return parse_jinja_variables(f"{{{{ {value} }}}}", source)
    return set()


def collect_task_local_vars(value):
    """Return variables produced locally by tasks instead of supplied by callers."""
    locals_ = set()
    if isinstance(value, list):
        for item in value:
            locals_.update(collect_task_local_vars(item))
        return locals_
    if not isinstance(value, dict):
        return locals_

    register = value.get("register")
    if isinstance(register, str):
        locals_.add(register)

    loop_control = value.get("loop_control")
    if isinstance(loop_control, dict):
        loop_var = loop_control.get("loop_var")
        if isinstance(loop_var, str):
            locals_.add(loop_var)
        index_var = loop_control.get("index_var")
        if isinstance(index_var, str):
            locals_.add(index_var)

    task_vars = value.get("vars")
    if isinstance(task_vars, dict):
        locals_.update(key for key in task_vars if isinstance(key, str))

    set_fact = value.get("ansible.builtin.set_fact")
    if isinstance(set_fact, dict):
        locals_.update(key for key in set_fact if isinstance(key, str))

    block = value.get("block")
    if isinstance(block, list):
        locals_.update(collect_task_local_vars(block))

    for nested_key in ("rescue", "always"):
        nested_tasks = value.get(nested_key)
        if isinstance(nested_tasks, list):
            locals_.update(collect_task_local_vars(nested_tasks))

    return locals_


def is_builtin_var(variable):
    """Return True for variables provided by Ansible rather than role callers."""
    return variable in BUILTIN_VARS or variable.startswith("ansible_")


def collect_vars_from_value(value, source, parent_key=None):
    """Recursively extract Jinja/Ansible expression variables from task data."""
    variables = set()
    if isinstance(value, str):
        variables.update(
            extract_string_vars(
                value,
                source,
                parse_bare_expression=parent_key in BARE_EXPRESSION_KEYS,
            )
        )
    elif isinstance(value, list):
        child_parent_key = parent_key if parent_key in BARE_EXPRESSION_LIST_KEYS else None
        for item in value:
            variables.update(collect_vars_from_value(item, source, child_parent_key))
    elif isinstance(value, dict):
        for key, item in value.items():
            variables.update(collect_vars_from_value(item, source, key))
    return variables


def extract_task_vars(task_file):
    """Return role argument variables referenced by a task file."""
    try:
        with task_file.open() as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise SpecError(f"invalid YAML in {task_file}: {exc}") from exc

    if data is None:
        return set()
    if not isinstance(data, list):
        raise SpecError(f"{task_file} must contain a YAML task list")

    local_vars = collect_task_local_vars(data)
    variables = collect_vars_from_value(data, task_file.as_posix())
    return {
        variable
        for variable in variables - local_vars
        if not is_builtin_var(variable)
    }


def extract_role_local_vars(tasks_dir):
    """Return variables produced by any task file in a role."""
    local_vars = set()
    if not tasks_dir.is_dir():
        return local_vars
    for task_file in sorted(tasks_dir.rglob("*.yaml")):
        try:
            with task_file.open() as fh:
                data = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            raise SpecError(f"invalid YAML in {task_file}: {exc}") from exc
        if data is None:
            continue
        if not isinstance(data, list):
            raise SpecError(f"{task_file} must contain a YAML task list")
        local_vars.update(collect_task_local_vars(data))
    return local_vars


def extract_collection_local_vars(roles_dir):
    """Return variables produced by task files across all roles."""
    local_vars = set()
    if not roles_dir.is_dir():
        return local_vars
    for tasks_dir in sorted(roles_dir.glob("*/tasks")):
        if tasks_dir.is_dir():
            local_vars.update(extract_role_local_vars(tasks_dir))
    return local_vars


def extract_missing_task_options(role_dir, spec_options, collection_local_vars=None):
    """Return task variables missing from the matching argument_specs options."""
    tasks_dir = role_dir / "tasks"
    missing = []
    if not tasks_dir.is_dir():
        return missing
    local_vars = extract_role_local_vars(tasks_dir)
    if collection_local_vars is None:
        collection_local_vars = extract_collection_local_vars(role_dir.parent)
    local_vars.update(collection_local_vars)

    for task_file in sorted(tasks_dir.rglob("*.yaml")):
        entrypoint = task_file.relative_to(tasks_dir).with_suffix("").as_posix()
        if entrypoint == "main" or entrypoint not in spec_options:
            continue
        task_vars = extract_task_vars(task_file) - local_vars
        for variable in sorted(task_vars - spec_options[entrypoint]):
            missing.append((entrypoint, variable))
    return missing


def extract_unused_anchors(argument_specs_path):
    """Return YAML anchors defined in argument_specs.yaml but never aliased.

    Returns a list of tuples (anchor_name, line, column). Lines and columns are
    one-based so they match what editors and terminal output normally show.

    Raises SpecError for malformed YAML.
    """
    definitions = []
    aliases = set()
    try:
        with argument_specs_path.open() as fh:
            for event in yaml.parse(fh):
                anchor = getattr(event, "anchor", None)
                if not anchor:
                    continue
                if isinstance(event, AliasEvent):
                    aliases.add(anchor)
                else:
                    definitions.append(
                        (
                            anchor,
                            event.start_mark.line + 1,
                            event.start_mark.column + 1,
                        )
                    )
    except yaml.YAMLError as exc:
        raise SpecError(f"invalid YAML: {exc}") from exc

    return [
        (anchor, line, column)
        for anchor, line, column in definitions
        if anchor not in aliases
    ]


def extract_uncataloged_options(specs, spec_options):
    """Return entrypoint options that are not declared under role-options.

    YAML merge keys are resolved by safe_load(), so a merged option is checked
    by its final option name instead of by the raw ``<<`` merge key.

    Returns a list of tuples (entrypoint, option_name).

    Raises SpecError for unexpected document shape.
    """
    role_options = specs.get("role-options")
    if not isinstance(role_options, dict):
        raise SpecError("'argument_specs.role-options' must be a mapping")

    catalog_options = role_options.get("options")
    if not isinstance(catalog_options, dict):
        raise SpecError("'argument_specs.role-options.options' must be a mapping")

    for option in catalog_options:
        if not isinstance(option, str):
            raise SpecError(f"non-string key in role-options.options: {option!r}")

    uncataloged = []
    for entrypoint, options in spec_options.items():
        for option in options:
            if option not in catalog_options:
                uncataloged.append((entrypoint, option))
    return uncataloged


def check_role(role_dir, collection_local_vars=None):
    """Check a single role. Returns True if clean, False if any mismatch."""
    specs_file = role_dir / "meta" / "argument_specs.yaml"

    if not specs_file.exists():
        print(f"{YELLOW}[SKIP]{NC}   {role_dir.name}: no argument_specs.yaml found")
        return True

    try:
        specs = load_argument_specs(specs_file)
        spec_options = extract_spec_options(specs)
        spec_tasks = set(spec_options)
        unused_anchors = extract_unused_anchors(specs_file)
        uncataloged_options = extract_uncataloged_options(specs, spec_options)
    except SpecError as exc:
        print(f"{RED}[FAIL]{NC}   {role_dir.name}: {exc}")
        return False

    file_tasks, yml_violations = extract_file_tasks(role_dir / "tasks")

    ghost = sorted(spec_tasks - file_tasks)
    undocumented = sorted(file_tasks - spec_tasks)
    try:
        missing_task_options = extract_missing_task_options(
            role_dir,
            spec_options,
            collection_local_vars,
        )
    except SpecError as exc:
        print(f"{RED}[FAIL]{NC}   {role_dir.name}: {exc}")
        return False

    if (
        not ghost
        and not undocumented
        and not yml_violations
        and not unused_anchors
        and not uncataloged_options
        and not missing_task_options
    ):
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
    if unused_anchors:
        print("  Unused YAML anchors in argument_specs.yaml:")
        for anchor, line, column in sorted(unused_anchors):
            print(f"    &{anchor} at meta/argument_specs.yaml:{line}:{column}")
    if uncataloged_options:
        print("  Entrypoint options missing from role-options:")
        for entrypoint, option in sorted(uncataloged_options):
            print(f"    + {entrypoint}: {option}")
    if missing_task_options:
        print("  Task variables missing from argument_specs options:")
        for entrypoint, option in sorted(missing_task_options):
            print(f"    + {entrypoint}: {option}")
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

    try:
        collection_local_vars = extract_collection_local_vars(roles_dir)
    except SpecError as exc:
        print(f"{RED}[FAIL]{NC}   {exc}")
        sys.exit(1)

    failures = 0
    for role_dir in role_dirs:
        if not check_role(role_dir, collection_local_vars):
            failures += 1

    print()
    if failures == 0:
        print(f"{GREEN}All {len(role_dirs)} role(s) passed.{NC}")
    else:
        print(f"{RED}{failures} of {len(role_dirs)} role(s) failed.{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
