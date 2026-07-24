# hyperledger.fabricx.fabric_reconfig

> Performs a live channel-config update against a running Fabric-X network (v1 scope: changing one party's Assembler endpoint), split across fetch/render/compute, per-party out-of-band signing, and submit/verify/restart stages.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [main](#main)
  - [resolve\_identity](#resolve_identity)
  - [resolve\_tls\_ca](#resolve_tls_ca)
  - [fetch\_current\_config](#fetch_current_config)
  - [render\_desired\_config](#render_desired_config)
  - [diff\_check](#diff_check)
  - [build\_config\_update](#build_config_update)
  - [build\_unsigned\_envelope](#build_unsigned_envelope)
  - [sign](#sign)
  - [collect\_and\_merge\_signatures](#collect_and_merge_signatures)
  - [submit](#submit)
  - [verify](#verify)
  - [handle\_restart](#handle_restart)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.fabric_reconfig
```

## Tasks

### main

> Validate reconfig inputs

Assert that exactly one party is targeted for this run.

```yaml
- name: Validate reconfig inputs
  vars:
    # PartyID whose Assembler endpoint is being changed. Only one party may be reconfigured per run.
    fabric_reconfig_target_party: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: main
```

### resolve_identity

> Resolve an admin identity from a PartyID (internal helper)

Included via `include_tasks` by `fetch_current_config`, `sign`, `submit`, and `verify` to derive an admin identity's MSP ID, cert, key, and TLS client cert/key from a PartyID and the standard cryptogen crypto material layout. Not intended to be run as its own entry point.

```yaml
- name: Resolve an admin identity from a PartyID (internal helper)
  vars:
    # Control-node directory holding cryptogen-generated crypto material, used to auto-derive admin identities and TLS CA certs by PartyID.
    cryptogen_artifacts_dir: "string"
    # PartyID to resolve an admin identity for, from inventory and the standard cryptogen crypto material layout.
    fabric_reconfig_identity_party: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: resolve_identity
```

### resolve_tls_ca

> Auto-derive a TLS CA bundle from inventory (internal helper)

Included via `include_tasks` by `fetch_current_config`, `submit`, and `verify`. When `fabric_reconfig_tls_ca` is unset and the network uses TLS, builds one PEM bundle covering every orderer org's TLS CA cert. Not intended to be run as its own entry point.

```yaml
- name: Auto-derive a TLS CA bundle from inventory (internal helper)
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # Control-node directory holding cryptogen-generated crypto material, used to auto-derive admin identities and TLS CA certs by PartyID.
    cryptogen_artifacts_dir: "string"
    # Path to a TLS CA certificate (or bundle) PEM file trusted for Assembler/Router connections. Leave unset to auto-derive: when `orderer_use_tls` is true, a bundle covering every orderer org's TLS CA cert is built from inventory; when false, connections are made in plaintext.
    fabric_reconfig_tls_ca: ""
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: resolve_tls_ca
```

### fetch_current_config

> Fetch and extract the current channel config

Resolves `fabric_reconfig_fetch_party`'s Assembler endpoint from inventory, fetches the current config block via `hyperledger.fabricx.fx_reconfig_client` (Deliver API), decodes it with `configtxlator`, and extracts `.data.data[0].payload.data.config` into `current_config.json`.

```yaml
- name: Fetch and extract the current channel config
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # Channel identifier for `fabric_reconfig_channel_id`.
    channel_id: "string"
    # Channel identifier used for the reconfig update.
    fabric_reconfig_channel_id: "{{ channel_id }}"
    # PartyID whose Assembler is used as the fetch source for the current config. Defaults to `fabric_reconfig_target_party`.
    fabric_reconfig_fetch_party: 1000
    # PartyID whose Assembler endpoint is being changed. Only one party may be reconfigured per run.
    fabric_reconfig_target_party: 1000
    # PartyID whose admin identity is used to authenticate fetch/verify requests (must satisfy the channel's Readers policy; any party admin qualifies). Defaults to `fabric_reconfig_target_party`. Ignored once `fabric_reconfig_reader_cert` is set explicitly.
    fabric_reconfig_reader_party: 1000
    # MSP ID of the reader identity. Leave unset to auto-derive from `fabric_reconfig_reader_party` and inventory (cryptogen layout). Set explicitly for fabric-ca-based or non-standard deployments.
    fabric_reconfig_reader_mspid: ""
    # Path to the reader identity's certificate PEM file. Leave unset to auto-derive; see `fabric_reconfig_reader_mspid`.
    fabric_reconfig_reader_cert: ""
    # Path to the reader identity's private key PEM file. Leave unset to auto-derive; see `fabric_reconfig_reader_mspid`.
    fabric_reconfig_reader_key: ""
    # Path to a TLS CA certificate (or bundle) PEM file trusted for Assembler/Router connections. Leave unset to auto-derive: when `orderer_use_tls` is true, a bundle covering every orderer org's TLS CA cert is built from inventory; when false, connections are made in plaintext.
    fabric_reconfig_tls_ca: ""
    # Override the TLS server name verified against the remote endpoint's certificate SANs. Needed whenever the dial address doesn't literally match a SAN entry -- for example a port-forwarded/NATed address such as 127.0.0.1 dialing a container whose certificate only lists its LAN IPs. Leave unset to derive it from the dial address.
    fabric_reconfig_tls_server_name: ""
    # Path to the reader identity's TLS client certificate PEM file. Required when the target network enforces mTLS (`orderer_use_mtls`): the Assembler's Deliver API rejects requests that don't bind a client TLS cert hash. Leave unset to auto-derive alongside `fabric_reconfig_reader_mspid`, or for TLS deployments that don't require a client certificate.
    fabric_reconfig_reader_tls_client_cert: ""
    # Path to the reader identity's TLS client private key PEM file.
    fabric_reconfig_reader_tls_client_key: ""
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: fetch_current_config
```

### render_desired_config

> Render the desired config from current_config.json

Run `files/apply_endpoint_change.py` against `current_config.json` to produce `desired_config.json` with `fabric_reconfig_target_party`'s Assembler endpoint changed to `fabric_reconfig_new_host`:`fabric_reconfig_new_port`.

```yaml
- name: Render the desired config from current_config.json
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # PartyID whose Assembler endpoint is being changed. Only one party may be reconfigured per run.
    fabric_reconfig_target_party: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: render_desired_config
```

### diff_check

> Idempotency check between current and desired config

Compare `current_config.json` and `desired_config.json` as parsed JSON structures; end the play with no further action when they are identical.

```yaml
- name: Idempotency check between current and desired config
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # PartyID whose Assembler endpoint is being changed. Only one party may be reconfigured per run.
    fabric_reconfig_target_party: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: diff_check
```

### build_config_update

> Compute the ConfigUpdate

Encode `current_config.json` and `desired_config.json` to protobuf and run `configtxlator compute_update` to produce `config_update.pb`.

```yaml
- name: Compute the ConfigUpdate
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # Channel identifier for `fabric_reconfig_channel_id`.
    channel_id: "string"
    # Channel identifier used for the reconfig update.
    fabric_reconfig_channel_id: "{{ channel_id }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: build_config_update
```

### build_unsigned_envelope

> Wrap the ConfigUpdate into an unsigned ConfigUpdateEnvelope

Wrap `config_update.pb` into a `common.ConfigUpdateEnvelope` with an empty `signatures` list, ready to hand off to each required party for out-of-band signing.

```yaml
- name: Wrap the ConfigUpdate into an unsigned ConfigUpdateEnvelope
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # PartyIDs whose `sign` output must be collected before `submit` will proceed. Must satisfy the channel's block validation policy majority requirement.
    fabric_reconfig_required_signers: [1000, 2000]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: build_unsigned_envelope
```

### sign

> Produce one ConfigSignature for the pending update

Decodes the unsigned envelope produced by `build_unsigned_envelope`, isolates the ConfigUpdate bytes, and signs them via `hyperledger.fabricx.fx_reconfig_client` (a signature over `signature_header || config_update`, matching Fabric's ConfigSignature construction).

```yaml
- name: Produce one ConfigSignature for the pending update
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # PartyID of the admin identity running the `sign` entry point in this invocation.
    fabric_reconfig_signing_party: 1000
    # MSP ID of the signing party's admin identity. Leave unset to auto-derive from `fabric_reconfig_signing_party` and inventory (cryptogen layout). Set explicitly for fabric-ca-based or non-standard deployments.
    fabric_reconfig_signer_mspid: ""
    # Path to the signing party's admin certificate PEM file. Leave unset to auto-derive; see `fabric_reconfig_signer_mspid`.
    fabric_reconfig_signer_cert: ""
    # Path to the signing party's admin private key PEM file. Leave unset to auto-derive; see `fabric_reconfig_signer_mspid`.
    fabric_reconfig_signer_key: ""
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: sign
```

### collect_and_merge_signatures

> Merge collected ConfigSignatures into the ConfigUpdateEnvelope

Splice each `fabric_reconfig_required_signers` party's `signature_party<id>.json` into the unsigned envelope's `signatures` list and re-encode `signed_config_update_envelope.pb`.

```yaml
- name: Merge collected ConfigSignatures into the ConfigUpdateEnvelope
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # PartyIDs whose `sign` output must be collected before `submit` will proceed. Must satisfy the channel's block validation policy majority requirement.
    fabric_reconfig_required_signers: [1000, 2000]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: collect_and_merge_signatures
```

### submit

> Wrap, sign, and submit the final Envelope

Wraps and signs the outer Envelope via `hyperledger.fabricx.fx_reconfig_client`, then resolves every Router in `fabric_x_orderers` from inventory and broadcasts the signed Envelope to all of them. Confirmed with the ordering team: submission targets ALL Routers (`BroadcastTxClient.SendTx`), not a single Router. Quorum defaults to `BroadcastTxClient.SendTx`'s own fault-tolerance formula; see `hyperledger.fabricx.fx_reconfig_client`.

```yaml
- name: Wrap, sign, and submit the final Envelope
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # Channel identifier for `fabric_reconfig_channel_id`.
    channel_id: "string"
    # Channel identifier used for the reconfig update.
    fabric_reconfig_channel_id: "{{ channel_id }}"
    # PartyID whose Assembler endpoint is being changed. Only one party may be reconfigured per run.
    fabric_reconfig_target_party: 1000
    # PartyID whose admin identity signs and submits the outer Envelope. Defaults to `fabric_reconfig_target_party`. Ignored once `fabric_reconfig_submitter_cert` is set explicitly.
    fabric_reconfig_submitter_party: 1000
    # MSP ID of the submitting party's admin identity (signs the outer Envelope). Leave unset to auto-derive from `fabric_reconfig_submitter_party` and inventory (cryptogen layout). Set explicitly for fabric-ca-based or non-standard deployments.
    fabric_reconfig_submitter_mspid: ""
    # Path to the submitting party's admin certificate PEM file. Leave unset to auto-derive; see `fabric_reconfig_submitter_mspid`.
    fabric_reconfig_submitter_cert: ""
    # Path to the submitting party's admin private key PEM file. Leave unset to auto-derive; see `fabric_reconfig_submitter_mspid`.
    fabric_reconfig_submitter_key: ""
    # Path to a TLS CA certificate (or bundle) PEM file trusted for Assembler/Router connections. Leave unset to auto-derive: when `orderer_use_tls` is true, a bundle covering every orderer org's TLS CA cert is built from inventory; when false, connections are made in plaintext.
    fabric_reconfig_tls_ca: ""
    # Override the TLS server name verified against the remote endpoint's certificate SANs. Needed whenever the dial address doesn't literally match a SAN entry -- for example a port-forwarded/NATed address such as 127.0.0.1 dialing a container whose certificate only lists its LAN IPs. Leave unset to derive it from the dial address.
    fabric_reconfig_tls_server_name: ""
    # Path to the submitting party's TLS client certificate PEM file. Required when the target network enforces mTLS (`orderer_use_mtls`). Leave unset to auto-derive alongside `fabric_reconfig_submitter_mspid`, or for TLS deployments that don't require a client certificate.
    fabric_reconfig_submitter_tls_client_cert: ""
    # Path to the submitting party's TLS client private key PEM file.
    fabric_reconfig_submitter_tls_client_key: ""
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: submit
```

### verify

> Confirm the update landed on-chain

Resolves `fabric_reconfig_fetch_party`'s Assembler endpoint from inventory, re-fetches the config the same way `fetch_current_config` does, and compares the result against `desired_config.json`. A mismatch there usually means the submission was rejected (for example a stale config version at the consensus layer); re-run from `fetch_current_config` rather than treating it as a generic error.

```yaml
- name: Confirm the update landed on-chain
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # Channel identifier for `fabric_reconfig_channel_id`.
    channel_id: "string"
    # Channel identifier used for the reconfig update.
    fabric_reconfig_channel_id: "{{ channel_id }}"
    # PartyID whose Assembler is used as the fetch source for the current config. Defaults to `fabric_reconfig_target_party`.
    fabric_reconfig_fetch_party: 1000
    # PartyID whose Assembler endpoint is being changed. Only one party may be reconfigured per run.
    fabric_reconfig_target_party: 1000
    # PartyID whose admin identity is used to authenticate fetch/verify requests (must satisfy the channel's Readers policy; any party admin qualifies). Defaults to `fabric_reconfig_target_party`. Ignored once `fabric_reconfig_reader_cert` is set explicitly.
    fabric_reconfig_reader_party: 1000
    # MSP ID of the reader identity. Leave unset to auto-derive from `fabric_reconfig_reader_party` and inventory (cryptogen layout). Set explicitly for fabric-ca-based or non-standard deployments.
    fabric_reconfig_reader_mspid: ""
    # Path to the reader identity's certificate PEM file. Leave unset to auto-derive; see `fabric_reconfig_reader_mspid`.
    fabric_reconfig_reader_cert: ""
    # Path to the reader identity's private key PEM file. Leave unset to auto-derive; see `fabric_reconfig_reader_mspid`.
    fabric_reconfig_reader_key: ""
    # Path to a TLS CA certificate (or bundle) PEM file trusted for Assembler/Router connections. Leave unset to auto-derive: when `orderer_use_tls` is true, a bundle covering every orderer org's TLS CA cert is built from inventory; when false, connections are made in plaintext.
    fabric_reconfig_tls_ca: ""
    # Override the TLS server name verified against the remote endpoint's certificate SANs. Needed whenever the dial address doesn't literally match a SAN entry -- for example a port-forwarded/NATed address such as 127.0.0.1 dialing a container whose certificate only lists its LAN IPs. Leave unset to derive it from the dial address.
    fabric_reconfig_tls_server_name: ""
    # Path to the reader identity's TLS client certificate PEM file. Required when the target network enforces mTLS (`orderer_use_mtls`): the Assembler's Deliver API rejects requests that don't bind a client TLS cert hash. Leave unset to auto-derive alongside `fabric_reconfig_reader_mspid`, or for TLS deployments that don't require a client certificate.
    fabric_reconfig_reader_tls_client_cert: ""
    # Path to the reader identity's TLS client private key PEM file.
    fabric_reconfig_reader_tls_client_key: ""
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: verify
```

### handle_restart

> Restart the reconfigured Assembler

Stop and start only the reconfigured party's Assembler (resolved from inventory via `fabric_reconfig_target_party`). Every other node in `fabric_x_orderers` relaunches itself dynamically once the update lands and needs no Ansible-driven restart. Run against `hosts: fabric_x_orderers`; the per-host `when` guard makes it a no-op everywhere except the reconfigured Assembler. NOT blocked, but unconfirmed: stops and starts immediately after submit/verify succeed. The ordering team's test harness waits for a node to enter "pending admin state" first; we don't yet know an externally observable signal for that. See the debug note this task emits.

```yaml
- name: Restart the reconfigured Assembler
  vars:
    # PartyID whose Assembler endpoint is being changed. Only one party may be reconfigured per run.
    fabric_reconfig_target_party: 1000
    # Fabric-X orderer sub-component running on this host, set per-host in inventory by `hyperledger.fabricx.orderer`. `handle_restart` only acts when this is `assembler`.
    orderer_component_type: "string"
    # Deployment mode (`bin` or `container`) `hyperledger.fabricx.orderer` was started with for this host.
    orderer_deployment_mode: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: handle_restart
```
