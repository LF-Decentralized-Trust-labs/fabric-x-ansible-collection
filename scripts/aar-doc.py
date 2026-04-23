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

# Replace the two upstream methods used during defaults generation with the
# style-preserving versions above. The rest of ``aar-doc`` remains unchanged.
_d.RoleDefaultsManager.add_default = _add_default_preserving_scalar_style
_d.RoleDefaultsManager.safe_quote_recursive = _safe_quote_recursive_preserving_scalar_style
_d.write_defaults = _write_defaults_with_license_header

from aar_doc.cli import app  # noqa: E402

# Re-export the original Typer application so this wrapper can be invoked as a
# drop-in replacement for the ``aar-doc`` CLI.
app()
