# hyperledger.fabricx.fx_reconfig_client

> Builds and runs the fx-reconfig-client CLI, a small Fabric orderer.AtomicBroadcast client used to fetch, sign, and submit live channel-config updates against a Fabric-X network.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [build](#build)
  - [fetch\_config](#fetch_config)
  - [extract\_config\_update](#extract_config_update)
  - [sign\_config\_update](#sign_config_update)
  - [merge\_signatures](#merge_signatures)
  - [build\_envelope](#build_envelope)
  - [broadcast](#broadcast)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.fx_reconfig_client
```

## Tasks

### build

> Build the fx-reconfig-client binary on the control node

Build the `fx-reconfig-client` binary from the vendored Go source tree in `files/src` on the control node. Delegates to the shared `hyperledger.fabricx.go` role's `build` entry point; no git clone is involved since the source lives in this role. The compiled executable is written to `cli_bin_dir` and reused by every other entry point in this role.

```yaml
- name: Build the fx-reconfig-client binary on the control node
  vars:
    # Directory used as the `fx-reconfig-client` binary destination.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the build and CLI-invocation entry points.
    fx_reconfig_client_bin_name: fx-reconfig-client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fx_reconfig_client
    tasks_from: build
```

### fetch_config

> Fetch the current channel config block from an Assembler

Run `fx-reconfig-client fetch-config` to pull the latest channel config block from an Assembler over the standard Deliver API. Mirrors `peer channel fetch config`'s own resolution against a classic orderer -- pulls the newest block, reads its `LAST_CONFIG` metadata pointer, then (unless the newest block already is the config block) pulls that block by number. The seek request must be signed by an identity the channel's Readers policy accepts (any party admin qualifies).

```yaml
- name: Fetch the current channel config block from an Assembler
  vars:
    # Directory used as the `fx-reconfig-client` binary destination.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the build and CLI-invocation entry points.
    fx_reconfig_client_bin_name: fx-reconfig-client
    # Channel identifier for `fx_reconfig_client_channel_id`.
    channel_id: "string"
    # Channel identifier passed to `fetch_config` and `build_envelope`.
    fx_reconfig_client_channel_id: "{{ channel_id }}"
    # MSP ID of the signing identity used to authenticate the request or produce a signature.
    fx_reconfig_client_mspid: "string"
    # Path to the signing identity's certificate PEM file.
    fx_reconfig_client_cert: "string"
    # Path to the signing identity's private key PEM file (EC, SEC1 or PKCS8 encoded).
    fx_reconfig_client_key: "string"
    # Path to the remote endpoint's TLS CA certificate PEM file. Leave unset to dial in plaintext (no-TLS deployments).
    fx_reconfig_client_tls_ca: ""
    # Path to the client's mTLS certificate PEM file. Only required when the remote endpoint enforces mTLS.
    fx_reconfig_client_tls_client_cert: ""
    # Path to the client's mTLS private key PEM file. Only required when the remote endpoint enforces mTLS.
    fx_reconfig_client_tls_client_key: ""
    # Override the TLS server name verified against the remote endpoint's certificate SANs. Needed whenever the dial address doesn't literally match a SAN entry -- for example a port-forwarded/NATed address such as 127.0.0.1 dialing a container whose certificate only lists its LAN IPs. Leave unset to derive it from the dial address.
    fx_reconfig_client_tls_server_name: ""
    # Assembler address to fetch the config block from, as `host:port`.
    fx_reconfig_client_assembler_endpoint: "string"
    # Path to write the raw `common.Block` proto bytes.
    fx_reconfig_client_fetch_config_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fx_reconfig_client
    tasks_from: fetch_config
```

### extract_config_update

> Read the ConfigUpdate bytes out of a ConfigUpdateEnvelope, unchanged

Run `fx-reconfig-client extract-config-update` to copy the `config_update` bytes field straight out of a `common.ConfigUpdateEnvelope`, with no re-encoding. This matters because `config_update` is itself an opaque bytes field holding a marshaled `common.ConfigUpdate`, which embeds several protobuf map fields. Producing a copy to sign by decoding the envelope to JSON and re-encoding a fresh `common.ConfigUpdate` is not guaranteed to reproduce identical bytes across separate configtxlator invocations (each is a fresh process, and Go's map iteration order is randomized per process), which would make the signature fail to verify. Reading the field directly out of the already-built envelope sidesteps that risk.

```yaml
- name: Read the ConfigUpdate bytes out of a ConfigUpdateEnvelope, unchanged
  vars:
    # Directory used as the `fx-reconfig-client` binary destination.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the build and CLI-invocation entry points.
    fx_reconfig_client_bin_name: fx-reconfig-client
    # Path to a `common.ConfigUpdateEnvelope` proto to read the `config_update` field out of, unchanged.
    fx_reconfig_client_config_update_envelope_input: "string"
    # Path to write the extracted raw `common.ConfigUpdate` proto bytes.
    fx_reconfig_client_extract_config_update_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fx_reconfig_client
    tasks_from: extract_config_update
```

### sign_config_update

> Produce one ConfigSignature for a ConfigUpdate

Run `fx-reconfig-client sign-config-update` to produce a single `common.ConfigSignature` over a raw `common.ConfigUpdate` proto, using the same signing-bytes construction (`signature_header || config_update`) Fabric itself verifies against. Intended to be run independently by each required party against their own admin identity; the resulting signature is later spliced into the `ConfigUpdateEnvelope.signatures` list.

```yaml
- name: Produce one ConfigSignature for a ConfigUpdate
  vars:
    # Directory used as the `fx-reconfig-client` binary destination.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the build and CLI-invocation entry points.
    fx_reconfig_client_bin_name: fx-reconfig-client
    # MSP ID of the signing identity used to authenticate the request or produce a signature.
    fx_reconfig_client_mspid: "string"
    # Path to the signing identity's certificate PEM file.
    fx_reconfig_client_cert: "string"
    # Path to the signing identity's private key PEM file (EC, SEC1 or PKCS8 encoded).
    fx_reconfig_client_key: "string"
    # Path to the raw `common.ConfigUpdate` proto bytes to sign.
    fx_reconfig_client_config_update_file: "string"
    # Path to write the resulting `common.ConfigSignature` proto bytes.
    fx_reconfig_client_sign_config_update_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fx_reconfig_client
    tasks_from: sign_config_update
```

### merge_signatures

> Splice ConfigSignatures into an unsigned ConfigUpdateEnvelope

Run `fx-reconfig-client merge-signatures` to append each collected `common.ConfigSignature` to an unsigned `common.ConfigUpdateEnvelope`'s `signatures` list, entirely in-process (no configtxlator/JSON round trip). The envelope's `config_update` bytes are carried over unchanged from the input file.

```yaml
- name: Splice ConfigSignatures into an unsigned ConfigUpdateEnvelope
  vars:
    # Directory used as the `fx-reconfig-client` binary destination.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the build and CLI-invocation entry points.
    fx_reconfig_client_bin_name: fx-reconfig-client
    # Path to the unsigned `common.ConfigUpdateEnvelope` proto to splice signatures into.
    fx_reconfig_client_unsigned_envelope_file: "string"
    # Paths to each collected party's `common.ConfigSignature` proto file, in the order they should be spliced in.
    fx_reconfig_client_signature_files: ["entry1", "entry2"]
    # Path to write the resulting, fully-signed `common.ConfigUpdateEnvelope` proto bytes.
    fx_reconfig_client_merge_signatures_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fx_reconfig_client
    tasks_from: merge_signatures
```

### build_envelope

> Wrap and sign a ConfigUpdateEnvelope into a broadcast-ready Envelope

Run `fx-reconfig-client build-envelope` to wrap a (fully signed) `common.ConfigUpdateEnvelope` into a `common.Envelope`, signed once by the submitting identity. Produces the same shape `peer channel update` builds internally via `protoutil.CreateSignedEnvelope` with header type `CONFIG_UPDATE`.

```yaml
- name: Wrap and sign a ConfigUpdateEnvelope into a broadcast-ready Envelope
  vars:
    # Directory used as the `fx-reconfig-client` binary destination.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the build and CLI-invocation entry points.
    fx_reconfig_client_bin_name: fx-reconfig-client
    # Channel identifier for `fx_reconfig_client_channel_id`.
    channel_id: "string"
    # Channel identifier passed to `fetch_config` and `build_envelope`.
    fx_reconfig_client_channel_id: "{{ channel_id }}"
    # MSP ID of the signing identity used to authenticate the request or produce a signature.
    fx_reconfig_client_mspid: "string"
    # Path to the signing identity's certificate PEM file.
    fx_reconfig_client_cert: "string"
    # Path to the signing identity's private key PEM file (EC, SEC1 or PKCS8 encoded).
    fx_reconfig_client_key: "string"
    # Path to the raw, fully-signed `common.ConfigUpdateEnvelope` proto bytes.
    fx_reconfig_client_config_update_envelope_file: "string"
    # Path to write the resulting broadcast-ready `common.Envelope` proto bytes.
    fx_reconfig_client_build_envelope_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fx_reconfig_client
    tasks_from: build_envelope
```

### broadcast

> Submit a signed Envelope to a set of Routers

Run `fx-reconfig-client broadcast` to send an already-signed `common.Envelope` to every given Router endpoint over the standard Broadcast API, in parallel, and require at least `fx_reconfig_client_quorum` SUCCESS acks. Confirmed with the ordering team: submission targets ALL Routers in the network (`BroadcastTxClient.SendTx`), not a single Router.

```yaml
- name: Submit a signed Envelope to a set of Routers
  vars:
    # Directory used as the `fx-reconfig-client` binary destination.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the build and CLI-invocation entry points.
    fx_reconfig_client_bin_name: fx-reconfig-client
    # Path to the remote endpoint's TLS CA certificate PEM file. Leave unset to dial in plaintext (no-TLS deployments).
    fx_reconfig_client_tls_ca: ""
    # Path to the client's mTLS certificate PEM file. Only required when the remote endpoint enforces mTLS.
    fx_reconfig_client_tls_client_cert: ""
    # Path to the client's mTLS private key PEM file. Only required when the remote endpoint enforces mTLS.
    fx_reconfig_client_tls_client_key: ""
    # Override the TLS server name verified against the remote endpoint's certificate SANs. Needed whenever the dial address doesn't literally match a SAN entry -- for example a port-forwarded/NATed address such as 127.0.0.1 dialing a container whose certificate only lists its LAN IPs. Leave unset to derive it from the dial address.
    fx_reconfig_client_tls_server_name: ""
    # Path to the signed `common.Envelope` proto bytes to submit.
    fx_reconfig_client_envelope_file: "string"
    # Router addresses to broadcast to, each as `host:port`. Confirmed with the ordering team: a config transaction is submitted to ALL Routers in the network (`BroadcastTxClient.SendTx`), not a single Router.
    fx_reconfig_client_router_endpoints: ["entry1", "entry2"]
    # Minimum number of SUCCESS acks required. `0` (the default) mirrors `BroadcastTxClient.SendTx`'s own fault-tolerance formula: for N >= 3 endpoints, tolerate up to floor(N/3) failures (quorum = N - floor(N/3)); for N < 3, require all endpoints to ack.
    fx_reconfig_client_quorum: 0
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fx_reconfig_client
    tasks_from: broadcast
```
