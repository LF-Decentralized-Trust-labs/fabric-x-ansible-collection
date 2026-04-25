# local/fabric-x-cryptogen.yaml

[`fabric-x-cryptogen.yaml`](../../local/fabric-x-cryptogen.yaml) runs the local container topology without Fabric CA services. Crypto material is generated on the control node with `cryptogen`.

Use it for fast, repeatable local tests where Fabric CA enrollment is not under test.

## Table of Contents <!-- omit in toc -->

- [Network Diagram](#network-diagram)
- [Inventory Specs](#inventory-specs)
- [What Makes This Inventory Different](#what-makes-this-inventory-different)

## Network Diagram

The diagram below summarizes this inventory's Fabric-X services and how they fit together.

![local Fabric-X cryptogen inventory](../../../images/fabric-x-cryptogen.drawio.png)

## Inventory Specs

The Fabric-X services, PostgreSQL, load generator, and monitoring stack run as local containers. `cryptogen` runs on the control node and writes artifacts below `cryptogen_artifacts_dir`.

This inventory deploys these logical services on the local machine:

- No Fabric CA servers or Fabric CA databases.
- 4 orderer groups. Each group has 1 router, 1 consenter, 1 assembler, and 1 batcher.
- 1 committer with validator, verifier, coordinator, sidecar, query service, and PostgreSQL storage.
- 1 load generator.
- Monitoring with node exporter, PostgreSQL exporter, Prometheus, and Grafana.

```mermaid
flowchart TD
  all --> control_node_crypto["cryptogen artifacts"]
  all --> network
  network --> fabric_x
  all --> load_generators
  all --> monitoring
  fabric_x --> fabric_x_orderers
  fabric_x --> fabric_x_committer
  fabric_x_orderers --> orderer_groups["fabric_x_orderer_1..4"]
  fabric_x_committer --> committer_services["validator, verifier, coordinator, sidecar, query service"]
  fabric_x_committer --> committer_db["committer-db PostgreSQL"]
  control_node_crypto -.-> fabric_x_orderers
  control_node_crypto -.-> fabric_x_committer
```

## What Makes This Inventory Different

Fabric CA is omitted entirely. Certificates and keys are generated centrally before the local container services consume them.

This keeps setup quick and deterministic, but it is not a production certificate lifecycle because private keys are generated on the control node.
