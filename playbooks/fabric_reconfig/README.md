# fabric_reconfig Playbooks

The `fabric_reconfig` playbooks perform a live channel-config update against a running Fabric-X network. v1 scope: changing one party's Assembler endpoint. The workflow is split across three playbooks to support out-of-band, per-party signing across separate trust domains.

**Fetch/sign/submit are driven by `hyperledger.fabricx.fx_reconfig_client`**, a small Go client this collection builds and vendors because the ordering (Fabric-X-Orderer) team does not yet have CLI tooling of its own for this -- confirmed directly with them, and consistent with their own in-progress `reconfig.md` guide. Expect these steps to be pointed at their CLI once it exists; see `fx_reconfig_client`'s role docs for the exact protocol details (Deliver/Broadcast against `orderer.AtomicBroadcast`).

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

[`prepare.yaml`](./prepare.yaml) fetches the current channel config from an Assembler, renders the desired config from inventory (the target party's Assembler endpoint, edited in place), checks whether anything actually changed, computes the `ConfigUpdate`, and wraps it into an unsigned `ConfigUpdateEnvelope`.

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
- Nuance: ends the play with no further action when the rendered config is identical to the current one (see `diff_check` in the role).
- Output: `{{ fabric_reconfig_artifacts_dir }}/unsigned_config_update_envelope.pb`, to be handed to each required signer.

## sign.yaml

[`sign.yaml`](./sign.yaml) is run independently by each party listed in `fabric_reconfig_required_signers`, against that party's own admin identity, producing one `ConfigSignature` over the pending update.

```shell
ansible-playbook hyperledger.fabricx.fabric_reconfig.sign \
  -e fabric_reconfig_signing_party=2 \
  -e fabric_reconfig_signer_mspid=Org2MSP \
  -e fabric_reconfig_signer_cert=/path/to/org2-admin-cert.pem \
  -e fabric_reconfig_signer_key=/path/to/org2-admin-key.pem
```

Properties:

- Target hosts: `localhost`.
- Nuance: requires `unsigned_config_update_envelope.pb` from `prepare` to already exist under `fabric_reconfig_artifacts_dir`.
- Output: `{{ fabric_reconfig_artifacts_dir }}/signature_party<id>.pb` and its decoded JSON form.

## submit.yaml

[`submit.yaml`](./submit.yaml) splices every collected `ConfigSignature` into the `ConfigUpdateEnvelope`, wraps and signs the final broadcast-ready `Envelope`, submits it to every Router in the network, re-fetches the config to confirm it landed, and restarts only the reconfigured Assembler.

```shell
ansible-playbook hyperledger.fabricx.fabric_reconfig.submit \
  -e fabric_reconfig_required_signers='[1,2,3]' \
  -e fabric_reconfig_submitter_mspid=Org1MSP \
  -e fabric_reconfig_submitter_cert=/path/to/org1-admin-cert.pem \
  -e fabric_reconfig_submitter_key=/path/to/org1-admin-key.pem
```

Properties:

- Target hosts: `localhost` for collect/submit/verify, then `fabric_x_orderers` for the restart stage.
- No `fabric_reconfig_target_host` to pass: the reconfigured Assembler's `inventory_hostname` is derived from `fabric_reconfig_target_party` via inventory.
- Nuance: submission targets **every Router** in `fabric_x_orderers` (confirmed with the ordering team: `BroadcastTxClient.SendTx`), not a single Router. The required ack quorum defaults to `SendTx`'s own fault-tolerance formula (tolerate up to 1/3 Router failures); override with `fx_reconfig_client_quorum` if needed.
- Nuance: only the reconfigured Assembler is stopped and started; every other node in `fabric_x_orderers` relaunches itself dynamically once the update lands and needs no Ansible-driven restart. The restart stage runs immediately after verify succeeds -- the ordering team's own `reconfig.md` guide confirms nodes can enter a "pending-admin" state first, but does not yet document an externally observable signal for it (their own TODO, not something we missed).

> [!WARNING]
> A verification failure after submit usually means the update was rejected (for example a stale config version at the consensus layer), not a generic error. Re-run from `prepare` rather than retrying `submit` directly.
