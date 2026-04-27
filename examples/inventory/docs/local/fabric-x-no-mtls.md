# local/fabric-x-no-mtls.yaml

[`fabric-x-no-mtls.yaml`](../../local/fabric-x-no-mtls.yaml) is the local container sample with TLS enabled and mTLS disabled.

Use it when you need encrypted local traffic but want to remove client certificate authentication from Fabric-X service-to-service calls.

!!! warning

    This inventory is meant for debugging only. It disables mTLS client authentication between Fabric-X services.

## Table of Contents <!-- omit in toc -->

- [Network Diagram](#network-diagram)
- [Inventory Details](#inventory-details)

## Network Diagram

The diagram below summarizes this inventory's Fabric-X services and how they fit together.

![local Fabric-X no mTLS inventory](../../../images/fabric-x.drawio.png)

## Inventory Details

All long-running services run as local containers. Ansible connects locally and uses the same container runtime paths as [`fabric-x.yaml`](./fabric-x.md).

This inventory deploys the same service layout as the default local sample:

- 5 Fabric CA servers and 5 PostgreSQL databases for Fabric CA state.
- 4 orderer groups. Each group has 1 router, 1 consenter, 1 assembler, and 1 batcher.
- 1 committer with validator, verifier, coordinator, sidecar, query service, and PostgreSQL storage.
- 1 load generator.
- Monitoring with node exporter, PostgreSQL exporter, Prometheus, and Grafana.

```mermaid
flowchart TD
  all --> network
  network --> fabric_cas
  network --> fabric_x
  all --> load_generators
  all --> monitoring
  fabric_cas --> fabric_ca_servers
  fabric_cas --> fabric_ca_dbs
  fabric_x --> fabric_x_orderers
  fabric_x --> fabric_x_committer
  fabric_x_orderers --> orderer_groups["fabric_x_orderer_1..4"]
  fabric_x_committer --> committer_services["validator, verifier, coordinator, sidecar, query service"]
  fabric_x_committer --> committer_db["committer-db PostgreSQL"]
  fabric_x --> mtls["mTLS disabled"]
```

TLS remains enabled for Fabric CA, PostgreSQL, orderer, committer, load generator, and monitoring components that declare TLS variables. The `orderer_use_mtls` and `committer_use_mtls` variables are omitted, so Fabric-X services do not require client certificates from each other.

This is useful for isolating TLS certificate, hostname, or endpoint problems from mTLS client-authentication problems.
