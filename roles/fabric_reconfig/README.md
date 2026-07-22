# hyperledger.fabricx.fabric_reconfig

> Performs a live channel-config update against a running Fabric-X network (v1 scope: changing one party's Assembler endpoint), split across fetch/render/compute, per-party out-of-band signing, and submit/verify/restart stages.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [main](#main)
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

### fetch_current_config

> Fetch and extract the current channel config

Resolves `fabric_reconfig_fetch_party`'s Assembler endpoint from inventory, then BLOCKED: fails with the exact fetch operation the ordering team's not-yet-built CLI needs to perform (see role description).

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
    # MSP ID of the identity used to fetch the current config (must satisfy the channel's Readers policy; any party admin qualifies).
    fabric_reconfig_reader_mspid: "string"
    # Path to the reader identity's certificate PEM file.
    fabric_reconfig_reader_cert: "string"
    # Path to the reader identity's private key PEM file.
    fabric_reconfig_reader_key: "string"
    # Path to the Assembler/Router TLS CA certificate PEM file. Leave unset for plaintext (no-TLS) deployments.
    fabric_reconfig_tls_ca: ""
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

Decodes the unsigned envelope produced by `build_unsigned_envelope` and isolates the ConfigUpdate bytes to sign, then BLOCKED: fails with the exact signing operation the ordering team's not-yet-built CLI needs to perform (see role description).

```yaml
- name: Produce one ConfigSignature for the pending update
  vars:
    # Base build directory for `fabric_reconfig_artifacts_dir`.
    config_build_dir: "string"
    # Working directory on the control node for every intermediate and final artifact produced by this role.
    fabric_reconfig_artifacts_dir: "{{ config_build_dir }}/fabric-reconfig-artifacts"
    # PartyID of the admin identity running the `sign` entry point in this invocation.
    fabric_reconfig_signing_party: 1000
    # MSP ID of the signing party's admin identity.
    fabric_reconfig_signer_mspid: "string"
    # Path to the signing party's admin certificate PEM file.
    fabric_reconfig_signer_cert: "string"
    # Path to the signing party's admin private key PEM file.
    fabric_reconfig_signer_key: "string"
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

Resolves `fabric_reconfig_submitting_party`'s Router endpoint from inventory, then BLOCKED: fails with the exact wrap/sign/submit operation the ordering team's not-yet-built CLI needs to perform (see role description). Submission is intended to target only the submitting party's Router, matching Fabric-X's own `BroadcastClient.SendTxTo` usage for config transactions in their test harness -- not a fan-out to every Router -- but this is inferred, not confirmed with the ordering team.

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
    # PartyID whose Router the final signed Envelope is submitted to.
    fabric_reconfig_submitting_party: 1000
    # MSP ID of the submitting party's admin identity (signs the outer Envelope).
    fabric_reconfig_submitter_mspid: "string"
    # Path to the submitting party's admin certificate PEM file.
    fabric_reconfig_submitter_cert: "string"
    # Path to the submitting party's admin private key PEM file.
    fabric_reconfig_submitter_key: "string"
    # Path to the Assembler/Router TLS CA certificate PEM file. Leave unset for plaintext (no-TLS) deployments.
    fabric_reconfig_tls_ca: ""
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_reconfig
    tasks_from: submit
```

### verify

> Confirm the update landed on-chain

Resolves `fabric_reconfig_fetch_party`'s Assembler endpoint from inventory, then BLOCKED: fails with the same fetch operation as `fetch_current_config` (see role description). Once fetch works, this compares the result against `desired_config.json`. A mismatch there usually means the submission was rejected (for example a stale config version at the consensus layer); re-run from `fetch_current_config` rather than treating it as a generic error.

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
    # MSP ID of the identity used to fetch the current config (must satisfy the channel's Readers policy; any party admin qualifies).
    fabric_reconfig_reader_mspid: "string"
    # Path to the reader identity's certificate PEM file.
    fabric_reconfig_reader_cert: "string"
    # Path to the reader identity's private key PEM file.
    fabric_reconfig_reader_key: "string"
    # Path to the Assembler/Router TLS CA certificate PEM file. Leave unset for plaintext (no-TLS) deployments.
    fabric_reconfig_tls_ca: ""
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
