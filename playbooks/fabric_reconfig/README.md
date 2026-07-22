# fabric_reconfig Playbooks

The `fabric_reconfig` playbooks perform a live channel-config update against a running Fabric-X network. v1 scope: changing one party's Assembler endpoint. The workflow is split across three playbooks to support out-of-band, per-party signing across separate trust domains.

**Deliberately incomplete today.** The ordering (Fabric-X-Orderer) team does not yet have a CLI or script to fetch a config block, sign a `ConfigUpdate`, or submit the final transaction -- confirmed directly with them. Rather than reimplementing that protocol logic ourselves, `fetch_current_config`, `sign`, and `submit` resolve everything they can from inventory and then stop with `ansible.builtin.fail`, describing the exact operation still needed (endpoint, identity, expected input/output). Everything before those stops is real and runs today; those three steps are a deliberate, visible boundary, not a bug.

## Table of Contents <!-- omit in toc -->

- [Playbooks flow](#playbooks-flow)
- [prepare.yaml](#prepareyaml)
- [sign.yaml](#signyaml)
- [submit.yaml](#submityaml)

## Playbooks flow

```mermaid
flowchart LR
  PREPARE[prepare] -. unsigned envelope .-> SIGN[sign]
  SIGN -. ConfigSignature per party .-> SUBMIT[submit]
```

`prepare` runs once, on the control node. `sign` runs once per required signer, independently, against that party's own admin identity -- it can run on the same control node or a different one, as long as it can reach the unsigned envelope artifact and that party's private key. `submit` runs once, after every required signature has been collected back onto the node running `submit`.

## prepare.yaml

[`prepare.yaml`](./prepare.yaml) resolves the fetch-source Assembler from inventory, then **stops (BLOCKED)** at the point where it needs an ordering-team fetch-config CLI. Once that exists, this playbook will fetch the current channel config, render the desired config from inventory (the target party's Assembler endpoint, edited in place), check whether anything actually changed, compute the `ConfigUpdate`, and wrap it into an unsigned `ConfigUpdateEnvelope`.

```shell
ansible-playbook hyperledger.fabricx.fabric_reconfig.prepare \
  -e fabric_reconfig_target_party=1 \
  -e fabric_reconfig_reader_mspid=Org1MSP \
  -e fabric_reconfig_reader_cert=/path/to/admin-cert.pem \
  -e fabric_reconfig_reader_key=/path/to/admin-key.pem
```

Properties:

- Target hosts: `localhost`.
- No `fabric_reconfig_new_host`/`fabric_reconfig_new_port` to pass: the new Assembler endpoint is derived from the target party's Assembler entry in inventory -- edit `ansible_host`/`orderer_rpc_port` there before running this.
- Nuance: ends the play with no further action when the rendered config is identical to the current one (see `diff_check` in the role) -- once fetch is unblocked.
- Currently stops at `fetch_current_config` with a `BLOCKED` message (see above).

## sign.yaml

[`sign.yaml`](./sign.yaml) decodes the unsigned envelope and isolates the `ConfigUpdate` bytes to sign, then **stops (BLOCKED)** at the point where it needs an ordering-team signing CLI. Once that exists, this playbook is run independently by each party listed in `fabric_reconfig_required_signers`, against that party's own admin identity, producing one `ConfigSignature` over the pending update.

```shell
ansible-playbook hyperledger.fabricx.fabric_reconfig.sign \
  -e fabric_reconfig_signing_party=2 \
  -e fabric_reconfig_signer_mspid=Org2MSP \
  -e fabric_reconfig_signer_cert=/path/to/org2-admin-cert.pem \
  -e fabric_reconfig_signer_key=/path/to/org2-admin-key.pem
```

Properties:

- Target hosts: `localhost`.
- Nuance: requires `unsigned_config_update_envelope.pb` from `prepare` to already exist under `fabric_reconfig_artifacts_dir` -- which itself requires `prepare` to be unblocked first.
- Currently stops with a `BLOCKED` message describing the exact ConfigSignature to produce.

## submit.yaml

[`submit.yaml`](./submit.yaml) resolves the submitting party's Router from inventory, then **stops (BLOCKED)** at the point where it needs an ordering-team wrap/sign/submit CLI. Once that exists, this playbook will splice every collected `ConfigSignature` into the `ConfigUpdateEnvelope`, wrap and sign the final broadcast-ready `Envelope`, submit it, re-fetch the config to confirm it landed, and restart only the reconfigured Assembler.

```shell
ansible-playbook hyperledger.fabricx.fabric_reconfig.submit \
  -e fabric_reconfig_required_signers='[1,2,3]' \
  -e fabric_reconfig_submitting_party=1 \
  -e fabric_reconfig_submitter_mspid=Org1MSP \
  -e fabric_reconfig_submitter_cert=/path/to/org1-admin-cert.pem \
  -e fabric_reconfig_submitter_key=/path/to/org1-admin-key.pem
```

Properties:

- Target hosts: `localhost` for collect/submit/verify, then `fabric_x_orderers` for the restart stage.
- No `fabric_reconfig_target_host` to pass: the reconfigured Assembler's `inventory_hostname` is derived from `fabric_reconfig_target_party` via inventory.
- Nuance (once unblocked): submission is intended to target only the submitting party's Router (matching Fabric-X's own `BroadcastClient.SendTxTo` usage for config transactions), not every Router in the network -- inferred from their test harness, not confirmed with the ordering team.
- Nuance: only the reconfigured Assembler is stopped and started; every other node in `fabric_x_orderers` relaunches itself dynamically once the update lands and needs no Ansible-driven restart. The restart stage runs immediately after verify succeeds -- the ordering team's own test harness waits for a "pending admin state" first, and we don't yet know an externally observable signal for that.
- Currently stops with a `BLOCKED` message at the wrap/sign/submit step, before the restart stage is ever reached.

> [!WARNING]
> A verification failure after submit (once unblocked) usually means the update was rejected (for example a stale config version at the consensus layer), not a generic error. Re-run from `prepare` rather than retrying `submit` directly.
