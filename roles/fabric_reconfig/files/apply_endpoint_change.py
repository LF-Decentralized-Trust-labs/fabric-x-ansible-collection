#!/usr/bin/env python3
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Apply an Assembler endpoint change to a decoded Fabric-X channel config.

Takes the JSON produced by `configtxlator proto_decode --type common.Config`
and produces a modified copy with one party's Assembler endpoint changed.
Fabric-X's party topology (ordererpb.SharedConfig) is embedded as the
Metadata bytes of the standard common.ConsensusType ConfigValue, at
channel_group.groups.Orderer.values.ConsensusType.value.metadata.

Whether that metadata field surfaces as already-decoded JSON or as an opaque
base64 string depends on whether the deployed configtxlator build registers
fabric-x-common's ordererext protolator extension. This script only handles
the decoded-JSON case, which it can do with plain JSON patching -- no
Fabric-X-specific tooling needed. If the metadata is still opaque bytes at
this point, editing it requires either the ordering team's own tooling or a
proto-level decoder we don't have a sanctioned source for; this script stops
and says so rather than guessing.
"""

import argparse
import copy
import json
import sys
from pathlib import Path

METADATA_PATH = ("channel_group", "groups", "Orderer", "values", "ConsensusType", "value", "metadata")


def get_nested(data, path):
    node = data
    for key in path:
        node = node[key]
    return node


def patch_decoded_metadata(metadata, party, host, port):
    for party_config in metadata["PartiesConfig"]:
        if int(party_config["PartyID"]) == party:
            party_config["AssemblerConfig"]["host"] = host
            party_config["AssemblerConfig"]["port"] = port
            return
    raise SystemExit(f"party {party} not found in PartiesConfig")


def apply_endpoint_change(current_config, party, host, port):
    desired_config = copy.deepcopy(current_config)
    metadata = get_nested(desired_config, METADATA_PATH)

    if not isinstance(metadata, dict):
        raise SystemExit(
            "BLOCKED: channel_group.groups.Orderer.values.ConsensusType.value.metadata is "
            f"{type(metadata).__name__}, not decoded JSON. This configtxlator build does not "
            "structurally decode Fabric-X's SharedConfig metadata (no ordererext protolator "
            "extension registered), and we don't have sanctioned tooling from the ordering "
            "team to edit it as opaque bytes. Ask the ordering team how they expect this to "
            "be edited."
        )

    patch_decoded_metadata(metadata, party, host, port)
    return desired_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current", required=True, type=Path, help="Path to the decoded current common.Config JSON")
    parser.add_argument("--desired", required=True, type=Path, help="Path to write the modified common.Config JSON")
    parser.add_argument("--party", required=True, type=int, help="PartyID whose Assembler endpoint is changing")
    parser.add_argument("--host", required=True, help="New Assembler host")
    parser.add_argument("--port", required=True, type=int, help="New Assembler port")
    args = parser.parse_args()

    current_config = json.loads(args.current.read_text())
    desired_config = apply_endpoint_change(current_config, args.party, args.host, args.port)
    args.desired.write_text(json.dumps(desired_config, indent=2))

    print(f"wrote {args.desired} (party {args.party} Assembler -> {args.host}:{args.port})")


if __name__ == "__main__":
    sys.exit(main())
