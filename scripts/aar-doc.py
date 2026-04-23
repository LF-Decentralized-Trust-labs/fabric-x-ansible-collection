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

import ast
import json
import re
from os import linesep
from pathlib import Path

import aar_doc.core as _c
import aar_doc.defaults as _d
from ruamel.yaml.scalarstring import (DoubleQuotedScalarString,
                                      FoldedScalarString, ScalarString,
                                      SingleQuotedScalarString)

LICENSE_HEADER = "\n".join(
    [
        "#",
        "# Copyright IBM Corp. All Rights Reserved.",
        "#",
        "# SPDX-License-Identifier: Apache-2.0",
        "#",
    ],
) + "\n"

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
    if isinstance(value, SingleQuotedScalarString):
        # Convert single-quoted scalars to double-quoted so the output uses " consistently.
        value = DoubleQuotedScalarString(str(value).strip())
    elif isinstance(value, ScalarString):
        # For any other ruamel scalar subclass (e.g. FoldedScalarString), preserve the
        # original style by re-instantiating with the same type after stripping whitespace.
        value = type(value)(str(value).strip())
    elif isinstance(value, str):
        # Plain Python strings just need leading/trailing whitespace removed.
        value = value.strip()

    if self._overwrite:
        # Always replace the entry when overwrite mode is active.
        self._defaults[name] = _d.RoleDefault(name, value, description, depth)
    else:
        # In non-overwrite mode, only store the value if the key doesn't exist yet.
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
        # Recurse into each list element independently.
        return [self.safe_quote_recursive(v) for v in value]
    if isinstance(value, dict):
        # Recurse into each dict value in-place; keys are always plain strings.
        for key, item in value.items():
            value[key] = self.safe_quote_recursive(item)
        return value
    if isinstance(value, ScalarString):
        if "\n" in str(value):
            # Multi-line ruamel scalars already carry the correct block style — leave them alone.
            return value
        # Single-line ruamel scalar: strip the wrapper so the plain-string checks below apply.
        value = str(value)
    if isinstance(value, str):
        if value in ("yes", "no"):
            # YAML interprets bare yes/no as booleans, so quote them to preserve string semantics.
            return DoubleQuotedScalarString(value)
        if "\n" in value:
            # Multi-line plain string: use a folded block scalar (>-) for readability.
            return FoldedScalarString(value)
        if ":" in value or len(value) == 0:
            # Strings containing ":" would break YAML parsing if unquoted; empty strings need quotes too.
            return DoubleQuotedScalarString(value)
    # All other values (numbers, booleans, None) are returned as-is.
    return value


def _write_defaults_with_license_header(output_file_path, role_path, role_defaults):
    """Write generated defaults with the collection license header."""
    # aar-doc passes README.md as the output path when generating defaults alongside docs;
    # in that case redirect the output to defaults/main.yml inside the role directory.
    if output_file_path.name == "README.md":
        output = role_path / "defaults" / "main.yml"
    elif output_file_path.is_absolute():
        # An absolute path is used as-is.
        output = output_file_path
    else:
        # A relative path is resolved relative to the role's defaults/ directory.
        output = role_path / "defaults" / output_file_path
    output = Path(output).resolve()

    # Create the parent directory if it doesn't exist yet.
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as defaults_file:
        # Write the Apache-2.0 license header first.
        defaults_file.write(LICENSE_HEADER)
        # Write the YAML document start marker and the "do not edit" banner.
        defaults_file.writelines(
            [
                "---" + linesep,
                linesep,
                "# Automatically generated by aar-doc. DO NOT EDIT MANUALLY." + linesep,
                linesep,
            ],
        )
        # Serialize the collected role defaults into the file using ruamel.
        _d.yaml.dump(role_defaults, defaults_file)


def _extract_c_example(text):
    """Extract the value inside the last C(...) from an Example description line.

    Matches ``C(<value>)`` optionally followed by a period at end of string.
    Returns the captured group as a string, or ``None`` when no match is found.
    """
    m = re.search(r"C\(([^)]+)\)\.?\s*$", str(text))
    return m.group(1) if m else None


def _yaml_render_obj(obj, indent):
    """Recursively render a Python object as YAML lines at the given indent level.

    Returns a list of strings (without trailing newlines).  The first element
    is always a non-empty line; callers that want the block to start on the
    *next* line (after a ``: ``) should prepend an empty string.
    """
    prefix = " " * indent
    lines = []
    if isinstance(obj, dict):
        for key, val in obj.items():
            if isinstance(val, (dict, list)):
                nested = _yaml_render_obj(val, indent + 2)
                lines.append(f"{prefix}{key}:")
                lines.extend(nested)
            elif isinstance(val, str):
                lines.append(f'{prefix}{key}: "{val}"')
            else:
                lines.append(f"{prefix}{key}: {val}")
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                nested = _yaml_render_obj(item, indent + 2)
                # First nested line gets the "- " prefix; remainder are indented.
                first = nested[0] if nested else ""
                rest = nested[1:]
                lines.append(f"{prefix}- {first.lstrip()}")
                lines.extend(rest)
            elif isinstance(item, str):
                lines.append(f'{prefix}- "{item}"')
            else:
                lines.append(f"{prefix}- {item}")
    return lines


def _to_yaml_sequence(value_str, indent=6):
    """Parse a stringified list and render it as a YAML block sequence.

    Each item is placed on its own line prefixed with ``- `` at the given
    indentation level so that the output aligns correctly inside the YAML
    code blocks produced by the role README template (vars are at 4 spaces,
    so sequence items sit at 6 spaces by default).

    The returned string starts with ``\\n`` so the caller's ``: `` suffix
    becomes a blank scalar and the items follow on subsequent lines.
    Falls back to the original string when parsing fails or the value is
    not a list.
    """
    try:
        obj = ast.literal_eval(value_str)
    except (ValueError, SyntaxError):
        try:
            obj = json.loads(value_str)
        except (ValueError, json.JSONDecodeError):
            return value_str
    if not isinstance(obj, list):
        return value_str
    return "\n" + "\n".join(_yaml_render_obj(obj, indent))


def _to_yaml_dict(value_str, indent=6):
    """Parse a stringified dict and render it as a recursive YAML block mapping.

    Each key-value pair is placed on its own line at the given indentation
    level. Nested dicts and lists are expanded recursively using the same
    block style rather than being serialised as compact JSON.

    String values are single-quoted; other scalar values are rendered as-is.

    The returned string starts with ``\\n`` so the caller's ``: `` suffix
    becomes a blank scalar and the mapping follows on subsequent lines.
    Falls back to the original string when parsing fails or the value is
    not a dict.
    """
    try:
        obj = ast.literal_eval(value_str)
    except (ValueError, SyntaxError):
        try:
            obj = json.loads(value_str)
        except (ValueError, json.JSONDecodeError):
            return value_str
    if not isinstance(obj, dict):
        return value_str
    return "\n" + "\n".join(_yaml_render_obj(obj, indent))


def _render_default_value(value, indent="      "):
    """Render a role default value as a YAML-compatible string.

    - ``true`` / ``false`` for Python booleans.
    - Multiline strings become a folded block scalar (``>-``).
    - Strings containing YAML-sensitive characters are double-quoted.
    - Dicts and lists are expanded as YAML block mappings / sequences;
      nesting is handled recursively with two extra spaces per level.
    - Any other type is coerced to its string representation.
    """
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        if "\n" in value:
            lines = value.split("\n")
            return ">-\n" + "\n".join(f"{indent}{line}" for line in lines)
        if not value:
            return '""'
        if any(c in value for c in ("{", ":", "#", "[", "]")):
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        return value
    if isinstance(value, dict):
        if not value:
            return "{}"
        inner = indent + "  "
        lines = [
            f"{indent}{k}: {_render_default_value(v, inner)}"
            for k, v in value.items()
        ]
        return "\n" + "\n".join(lines)
    if isinstance(value, (list, tuple)):
        inner = indent + "  "
        lines = [
            f"{indent}- {_render_default_value(item, inner)}"
            for item in value
        ]
        return "\n" + "\n".join(lines)
    return str(value)


def _render_default(value):
    """Jinja2 filter: render a role default value as YAML.

    Prepends a single space when the result is an inline scalar so that the
    template can use ``{{ var_name }}:{{ var.default | render_default }}``
    without leaving a trailing space on block-scalar key lines.
    """
    result = _render_default_value(value)
    return result if result.startswith("\n") else f" {result}"


def _render_placeholder(var, indent=6):
    """Jinja2 filter: render a placeholder YAML value for a variable without a default.

    Extracts the last ``Example: C(...)`` from the variable description and
    formats it according to the variable type.  Falls back to generic
    type-based placeholders when no example is present.
    """
    var_type = var.get("type", "str")
    desc = var.get("description", [])
    desc_list = [desc] if isinstance(desc, str) else (desc or [])

    # Collect the last ``Example: C(...)`` found across all description lines.
    example_val = None
    for line in desc_list:
        if isinstance(line, str) and "Example: C(" in line:
            extracted = _extract_c_example(line)
            if extracted is not None:
                example_val = extracted

    if example_val is not None:
        if var_type in ("str", "path"):
            return f' "{example_val}"'
        if var_type == "list":
            return _to_yaml_sequence(example_val, indent)
        if var_type == "dict":
            return _to_yaml_dict(example_val, indent)
        return f" {example_val}"

    # Generic fallback placeholders when no example is present.
    if var_type in ("int", "float"):
        return " 1000"
    if var_type == "bool":
        return " false"
    if var_type == "list":
        elements = var.get("elements", "str")
        if elements in ("int", "float"):
            return " [1000, 2000]"
        if elements == "bool":
            return " [true, false]"
        if elements == "dict":
            return " [{}]"
        return ' ["entry1", "entry2"]'
    if var_type == "dict":
        return " {}"
    return ' "string"'


_orig_env_init = _c.jinja2.Environment.__init__


def _env_init_with_extras(self, *args, **kwargs):
    _orig_env_init(self, *args, **kwargs)
    self.filters["render_default"] = _render_default
    self.filters["render_placeholder"] = _render_placeholder


_c.jinja2.Environment.__init__ = _env_init_with_extras
_d.RoleDefaultsManager.add_default = _add_default_preserving_scalar_style
_d.RoleDefaultsManager.safe_quote_recursive = _safe_quote_recursive_preserving_scalar_style
_d.write_defaults = _write_defaults_with_license_header

from aar_doc.cli import app  # noqa: E402

app()
