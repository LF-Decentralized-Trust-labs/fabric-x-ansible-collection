# hyperledger.fabricx.orderer

> Runs Fabric-X Orderer components (`consensus`, `batcher`, `assembler`, `router`).

<!-- @depends_on: hyperledger.fabricx.cryptogen, hyperledger.fabricx.fabric_ca, hyperledger.fabricx.fxconfig -->

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
| [`hyperledger.fabricx.cryptogen`](../cryptogen/README.md) | Crypto material required before starting (cryptogen mode) |
| [`hyperledger.fabricx.fabric_ca`](../fabric_ca/README.md) | Crypto material required before starting (Fabric-CA mode) |
| [`hyperledger.fabricx.fxconfig`](../fxconfig/README.md)   | Generates node configuration                              |

## Tasks

### Crypto

| Task                                      | Description                          |
| ----------------------------------------- | ------------------------------------ |
| [crypto/setup](./tasks/crypto/setup.yaml) | Generates/transfers crypto material  |
| [crypto/fetch](./tasks/crypto/fetch.yaml) | Fetches certificates to control node |
| [crypto/rm](./tasks/crypto/rm.yaml)       | Removes crypto material              |

#### crypto/setup

Generates and/or transfers the crypto material needed to run a Fabric-X Orderer component. Supports two modes:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

In Kubernetes mode, this task additionally creates a Secret containing all crypto material for the component.

```yaml
- name: Setup the crypto material for Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the Fabric-X Orderer certificates on the control node. This operation is important for the generation of the genesis block on the control node, which will embed the certificates of the orderers.

```yaml
- name: Fetch the Fabric-X Orderer certificates
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for a Fabric-X Orderer. In Kubernetes mode, this also deletes the Secret.

```yaml
- name: Remove the Fabric-X Orderer crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                   |
| ----------------------------------------------- | ----------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers configuration files |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration         |

#### config/transfer

Transfers the configuration files for a Fabric-X Orderer component on the remote node. The component type is determined by the `orderer_component_type` variable (`consensus`, `batcher`, `assembler`, or `router`):

```yaml
- name: Transfer the Fabric-X Orderer configuration files
  vars:
    orderer_component_type: router # or consensus, batcher, assembler
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer
```

#### config/rm

Removes the configuration files for a Fabric-X Orderer component:

```yaml
- name: Remove the Fabric-X Orderer configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/rm
```

### Lifecycle

| Task                                    | Description                |
| --------------------------------------- | -------------------------- |
| [start](./tasks/start.yaml)             | Starts orderer components  |
| [stop](./tasks/stop.yaml)               | Stops orderer components   |
| [teardown](./tasks/teardown.yaml)       | Removes runtime components |
| [wipe](./tasks/wipe.yaml)               | Removes all data           |
| [fetch_logs](./tasks/fetch_logs.yaml)   | Collects logs              |
| [ping](./tasks/ping.yaml)               | Health check               |
| [get_metrics](./tasks/get_metrics.yaml) | Retrieves metrics          |

#### start

Starts the Fabric-X Orderer component. The component type is determined by the `orderer_component_type` variable:

```yaml
- name: Start Fabric-X Orderer
  vars:
    orderer_component_type: router # or consensus, batcher, assembler
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: start
```

#### stop

Stops the Fabric-X Orderer component:

```yaml
- name: Stop Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: stop
```

#### teardown

Removes the Fabric-X Orderer component:

```yaml
- name: Teardown Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: teardown
```

#### wipe

Removes all Fabric-X Orderer data:

```yaml
- name: Wipe Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: wipe
```

#### fetch_logs

Collects Fabric-X Orderer logs:

```yaml
- name: Fetch Fabric-X Orderer logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: fetch_logs
```

#### ping

Health check for Fabric-X Orderer:

```yaml
- name: Ping Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: ping
```

#### get_metrics

Retrieves Fabric-X Orderer metrics:

```yaml
- name: Get Fabric-X Orderer metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: get_metrics
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
