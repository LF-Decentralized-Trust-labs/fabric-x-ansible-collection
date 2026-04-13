# hyperledger.fabricx.committer

> Runs Fabric-X Committer components (`validator`, `verifier`, `coordinator`, `sidecar`, `query-service`).

<!-- @depends_on: hyperledger.fabricx.cryptogen, hyperledger.fabricx.fabric_ca, hyperledger.fabricx.orderer, hyperledger.fabricx.fxconfig, hyperledger.fabricx.postgres, hyperledger.fabricx.yugabyte -->

## Table of Contents <!-- omit in toc -->

- [Depends On](#depends-on)
- [Tasks](#tasks)
  - [Crypto](#crypto)
    - [crypto/setup](#cryptosetup)
    - [crypto/fetch](#cryptofetch)
    - [crypto/rm](#cryptorm)
  - [Config](#config)
    - [config/transfer](#configtransfer)
    - [config/rm](#configrm)
  - [Lifecycle](#lifecycle)
    - [start](#start)
    - [stop](#stop)
    - [teardown](#teardown)
    - [wipe](#wipe)
    - [fetch_logs](#fetch_logs)
    - [ping](#ping)
    - [get_metrics](#get_metrics)
- [Variables](#variables)

## Depends On

| Role                                                      | Reason                                                    |
| --------------------------------------------------------- | --------------------------------------------------------- |
| [`hyperledger.fabricx.cryptogen`](../cryptogen/README.md) | Crypto material (cryptogen mode)                          |
| [`hyperledger.fabricx.fabric_ca`](../fabric_ca/README.md) | Crypto material (Fabric-CA mode)                          |
| [`hyperledger.fabricx.orderer`](../orderer/README.md)     | Coordinator ↔ assembler relationship                      |
| [`hyperledger.fabricx.fxconfig`](../fxconfig/README.md)   | Generates node configuration                              |
| [`hyperledger.fabricx.postgres`](../postgres/README.md)   | Database backend (when `postgres_port` defined)           |
| [`hyperledger.fabricx.yugabyte`](../yugabyte/README.md)   | Database backend (when `yugabyte_component_type` defined) |

## Tasks

### Crypto

| Task                                      | Description                             |
| ----------------------------------------- | --------------------------------------- |
| [crypto/setup](./tasks/crypto/setup.yaml) | Generates/transfers crypto material     |
| [crypto/fetch](./tasks/crypto/fetch.yaml) | Fetches TLS certificate to control node |
| [crypto/rm](./tasks/crypto/rm.yaml)       | Removes crypto material                 |

#### crypto/setup

Generates and/or transfers the crypto material needed to run a Fabric-X Committer component. Supports two modes:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Setup the crypto material for Fabric-X Committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the Fabric-X Committer TLS certificate on the control node. This operation is important for sharing the TLS CA certificate with clients that need to establish a trusted connection to the committer.

```yaml
- name: Fetch the Fabric-X Committer TLS certificate
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the TLS crypto material generated for a Fabric-X Committer component:

```yaml
- name: Remove the Fabric-X Committer crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                   |
| ----------------------------------------------- | ----------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers configuration files |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration         |

#### config/transfer

Transfers the configuration files for a Fabric-X Committer component on the remote node. The component type is determined by the `committer_component_type` variable (`validator`, `verifier`, `coordinator`, `sidecar`, or `query-service`):

```yaml
- name: Transfer the Fabric-X Committer configuration files
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/transfer
```

#### config/rm

Removes the configuration files for a Fabric-X Committer component:

```yaml
- name: Remove the Fabric-X Committer configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/rm
```

### Lifecycle

| Task                                    | Description                 |
| --------------------------------------- | --------------------------- |
| [start](./tasks/start.yaml)             | Starts committer components |
| [stop](./tasks/stop.yaml)               | Stops committer components  |
| [teardown](./tasks/teardown.yaml)       | Removes runtime components  |
| [wipe](./tasks/wipe.yaml)               | Removes all data            |
| [fetch_logs](./tasks/fetch_logs.yaml)   | Collects logs               |
| [ping](./tasks/ping.yaml)               | Health check                |
| [get_metrics](./tasks/get_metrics.yaml) | Retrieves metrics           |

#### start

Starts the Fabric-X Committer component. The component type is determined by the `committer_component_type` variable:

```yaml
- name: Start Fabric-X Committer
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: start
```

#### stop

Stops the Fabric-X Committer component:

```yaml
- name: Stop Fabric-X Committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: stop
```

#### teardown

Removes the Fabric-X Committer component:

```yaml
- name: Teardown Fabric-X Committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: teardown
```

#### wipe

Removes all Fabric-X Committer data:

```yaml
- name: Wipe Fabric-X Committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: wipe
```

#### fetch_logs

Collects Fabric-X Committer logs:

```yaml
- name: Fetch Fabric-X Committer logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: fetch_logs
```

#### ping

Health check for Fabric-X Committer:

```yaml
- name: Ping Fabric-X Committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: ping
```

#### get_metrics

Retrieves Fabric-X Committer metrics:

```yaml
- name: Get Fabric-X Committer metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: get_metrics
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
