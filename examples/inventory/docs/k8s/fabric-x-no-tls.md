# k8s/fabric-x-no-tls.yaml

[`fabric-x-no-tls.yaml`](../../k8s/fabric-x-no-tls.yaml) deploys the Kubernetes sample with TLS and mTLS disabled.

Use it for local-cluster debugging when plaintext endpoints are deliberate and the goal is to remove certificate handling from the test.

!!! warning

    This inventory is meant for debugging only. It disables both TLS encryption and mTLS client authentication.

## Table of Contents <!-- omit in toc -->

- [Network Diagram](#network-diagram)
- [Inventory Details](#inventory-details)

## Network Diagram

The diagram below summarizes this inventory's Fabric-X services and how they fit together.

![Kubernetes Fabric-X no TLS inventory](../../../images/fabric-x-k8s.drawio.png)

## Inventory Details

Fabric CA, CA databases, orderer, committer, PostgreSQL, load generator, node exporter, Prometheus, and Grafana use Kubernetes task paths. External access follows the same NodePort pattern as [`fabric-x.yaml`](./fabric-x.md).

This inventory deploys the same service layout as the default Kubernetes sample:

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
  network --> plaintext["TLS and mTLS disabled"]
```

TLS-related variables are intentionally omitted for the Kubernetes services in this inventory. Service traffic is unencrypted, and mTLS client certificate checks are disabled.
