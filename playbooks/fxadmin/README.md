# fxadmin Playbooks

The `fxadmin` playbooks drive live Fabric-X channel reconfigurations: fetch the current channel configuration, patch it, collect endorsements from the organization admins, and submit the resulting transaction. `fxadmin` signs with the identity declared in the host's `organization.user`, reusing the MSP already produced by the crypto setup of that host.

## Supported reconfiguration flows

Add a row here whenever a new flow lands.

| Flow                               | Playbook                                                             | Changes                                                                                          |
| ---------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Change an orderer Assembler's port | [`reconfigure_assembler_port.yaml`](#reconfigure_assembler_portyaml) | The Assembler's org-level `Endpoints` entry and its `ConsensusType.metadata.PartiesConfig` entry |

## Table of Contents <!-- omit in toc -->

- [Supported reconfiguration flows](#supported-reconfiguration-flows)
- [Playbooks flow](#playbooks-flow)
- [binaries.yaml](#binariesyaml)
- [configs.yaml](#configsyaml)
- [reconfigure_assembler_port.yaml](#reconfigure_assembler_portyaml)
- [wipe.yaml](#wipeyaml)

## Playbooks flow

```mermaid
flowchart LR
  CRYPTO[crypto generation] --> BIN[binaries] --> CONFIGS[configs]
  CONFIGS --> RECONFIG[reconfigure_assembler_port]
  RECONFIG -. cleanup .-> WIPE[wipe]
```

All playbooks act on the **admin hosts**: the hosts whose `organization.user` has `type: admin` (the orderer consenters in the sample inventories), narrowed by `target_hosts`.

## binaries.yaml

[`binaries.yaml`](./binaries.yaml) builds the `fxadmin` CLI on the control node and delivers it to every admin host.

```shell
ansible-playbook hyperledger.fabricx.fxadmin.binaries
```

Properties:

- Binary activation: only runs when `fxadmin_use_bin: true`.
- Build location: with `bin_build_on_control_node: true` the binary is built once on the control node and transferred; otherwise each admin host installs it with `go install`.

## configs.yaml

[`configs.yaml`](./configs.yaml) renders the `fxadmin` admin configuration (MSP identity and TLS/mTLS material) on every admin host.

```shell
ansible-playbook hyperledger.fabricx.fxadmin.configs
```

Properties:

- Nuance: run this after the crypto generation and before any reconfiguration flow.

## reconfigure_assembler_port.yaml

[`reconfigure_assembler_port.yaml`](./reconfigure_assembler_port.yaml) changes the port of one orderer Assembler in the channel configuration. Every admin host endorses the update, and the first admin host submits it and waits until it commits.

```shell
make reconfigure-assembler-port ASSEMBLER_HOST=orderer-assembler-1 NEW_PORT=7065
```

Properties:

- `target_hosts` (`TARGET_HOSTS`, default `all`) must cover at least one admin host per organization, otherwise the playbook fails.
- Apply: the playbook does **not** restart the Assembler. Afterwards set `orderer_rpc_port` of the assembler host to the new port in the inventory and run `make <assembler_host> configs restart`.
- Nuance: run this on a started network, after `binaries.yaml` and `configs.yaml`. `jq` must be installed on the control node.

## wipe.yaml

[`wipe.yaml`](./wipe.yaml) removes the `fxadmin` binary and configuration from every admin host.

```shell
ansible-playbook hyperledger.fabricx.fxadmin.wipe
```
