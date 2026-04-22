#!/usr/bin/env python3
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Local wrapper around ``aar-doc`` defaults generation.

This collection uses ``aar-doc`` for two separate tasks:

1. render role READMEs from ``meta/argument_specs.yaml``
2. render ``defaults/main.yaml`` from the same argument specs

The README generation works as-is with custom Jinja templates, but the
defaults generation needs two small behavior changes that are not exposed by
``aar-doc`` as CLI settings:

- keep very long single-line defaults on one line instead of re-wrapping them
- preserve the original ruamel scalar style for multiline defaults

The second point matters for Jinja expressions declared in YAML with explicit
block scalar styles such as ``>-`` in ``argument_specs.yaml``. Without this
wrapper, ``aar-doc`` normalizes multiline strings into literal blocks and the
generated defaults lose the original folded style choice.

The wrapper therefore monkey-patches the small parts of ``aar_doc.defaults``
that turn parsed argument spec values into the final YAML output.
"""

import aar_doc.defaults as _d
from ruamel.yaml.scalarstring import FoldedScalarString, ScalarString, SingleQuotedScalarString

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


# Replace the two upstream methods used during defaults generation with the
# style-preserving versions above. The rest of ``aar-doc`` remains unchanged.
_d.RoleDefaultsManager.add_default = _add_default_preserving_scalar_style
_d.RoleDefaultsManager.safe_quote_recursive = _safe_quote_recursive_preserving_scalar_style

from aar_doc.cli import app  # noqa: E402

# Re-export the original Typer application so this wrapper can be invoked as a
# drop-in replacement for the ``aar-doc`` CLI.
app()
