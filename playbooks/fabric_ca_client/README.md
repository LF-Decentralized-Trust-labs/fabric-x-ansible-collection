# Fabric CA Client Playbooks

The `fabric_ca_client` playbooks prepare the Fabric CA client binary used by enrollment and registration tasks. There is no separate long-running Fabric CA client service.

```mermaid
flowchart LR
  BIN[binaries]
```

## binaries.yaml

[`binaries.yaml`](./binaries.yaml) prepares the Fabric CA client wherever enrollment or registration tasks may need it. It can install or build the client on the control node, then transfer, install, or build it on remote Fabric CA servers and component hosts whose organizations enroll through Fabric CA.

```shell
ansible-playbook hyperledger.fabricx.fabric_ca_client.binaries
```

Properties:

- Target hosts: `localhost` for control-node build/install decisions, then `all` by default for remote binary setup.
- Binary activation: only hosts with `fabric_ca_client_use_bin: true` run the remote binary setup step.
- Build location: set `bin_build_on_control_node: true` with `fabric_ca_client_build_bin: true` to build on the control node and transfer the result to remote hosts. In that case, `go` must be installed on the control node. If `fabric_ca_client_build_bin: true` is set without `bin_build_on_control_node`, the build happens on each remote binary host and `go` is needed there.
- Nuance: run this before Fabric CA enrollment and registration when your inventory uses Fabric CA client binary mode. The example binary wrapper imports it before component crypto generation.
