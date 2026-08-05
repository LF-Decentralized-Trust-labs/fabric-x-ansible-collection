# fxconfig Playbooks

The `fxconfig` playbooks prepare and submit Fabric-X configuration transactions, including namespace creation. `fxconfig` is a control-plane tool that uses generated artifacts, endorser information from the inventory, and runtime endpoints.

## Table of Contents <!-- omit in toc -->

- [Playbooks flow](#playbooks-flow)
- [binaries.yaml](#binariesyaml)
- [configs.yaml](#configsyaml)
- [create_namespaces.yaml](#create_namespacesyaml)
- [wipe.yaml](#wipeyaml)

## Playbooks flow

```mermaid
flowchart LR
  BIN[binaries] --> CONFIGS[configs]
  CONFIGS --> CREATE[create_namespaces]
  CREATE -. cleanup .-> WIPE[wipe]
```

## binaries.yaml

[`binaries.yaml`](./binaries.yaml) prepares the `fxconfig` CLI used for configuration transactions. It handles control-node install/build decisions first, then ensures remote hosts that declare `fxconfig_use_bin: true` have the binary available by transfer, local build, or install.

```shell
ansible-playbook hyperledger.fabricx.fxconfig.binaries
```

Properties:

- Target hosts: `localhost` for control-node build/install decisions, then `all` by default for remote binary setup.
- Binary activation: only hosts with `fxconfig_use_bin: true` run the remote binary setup step.
- Build location: set `bin_build_on_control_node: true` with `fxconfig_build_bin: true` to build on the control node and transfer the result to remote hosts. In that case, `go` must be installed on the control node. If `fxconfig_build_bin: true` is set without `bin_build_on_control_node`, the build happens on each remote binary host and `go` is needed there.

## configs.yaml

[`configs.yaml`](./configs.yaml) renders and transfers `fxconfig` configuration for hosts that declare namespace and user data. It selects the endorser identity, discovers the orderer router, committer query service, and committer sidecar endpoints, and writes the local configuration that later namespace operations use.

```shell
ansible-playbook hyperledger.fabricx.fxconfig.configs
```

Properties:

- Target hosts: `all` by default.
- Nuance: run this during setup after core crypto and genesis/config artifacts exist and before namespace creation.

## create_namespaces.yaml

[`create_namespaces.yaml`](./create_namespaces.yaml) first lists the namespaces already committed to the Fabric-X network together with their current on-chain version, then compares each declared namespace's policy against a fingerprint recorded from the last run to decide whether it needs to be created, updated, or left alone. It groups inventory definitions, creates or updates unsigned transactions on the control node, asks the relevant organizations to endorse them, merges the endorsements, submits the finalized transactions, and records the applied fingerprint.

```shell
ansible-playbook hyperledger.fabricx.fxconfig.create_namespaces
```

Properties:

- Target hosts: `all` by default, with transaction construction and submission coordinated by the `fxconfig` role.
- Reconciliation: a namespace absent from the chain is created. A namespace already on chain whose recorded fingerprint does not exactly match its declared policy — including having no recorded fingerprint at all — is updated, using the namespace's current on-chain version as the compare-and-swap token fxconfig requires. This is how changing a namespace's `policy` in the inventory and re-running this playbook applies the change, and it also means the very first run against a namespace that already existed on chain before this reconciliation was in place submits one update for it. No `version` field is needed in the inventory.
- Idempotency: a namespace whose declared policy still matches its recorded fingerprint is skipped across creation, endorsement, merge, and submission.
- Known limitation: a namespace policy changed out-of-band (not through this playbook) is not detected, since reconciliation compares against the last fingerprint *this playbook* recorded, not the actual on-chain policy bytes.

> [!WARNING]
> Run this after the network is started and the required committer endpoints are reachable. Running it too early fails by design because namespace transactions must be endorsed and submitted through live Fabric-X endpoints.

## wipe.yaml

[`wipe.yaml`](./wipe.yaml) removes generated `fxconfig` files from targeted hosts so namespace/configuration artifacts can be rebuilt cleanly during another setup or debug cycle.

```shell
ansible-playbook hyperledger.fabricx.fxconfig.wipe
```

Properties:

- Target hosts: `all` by default.
- Nuance: removes generated `fxconfig` files so namespace/configuration artifacts can be rebuilt cleanly.
