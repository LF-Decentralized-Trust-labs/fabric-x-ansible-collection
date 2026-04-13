# hyperledger.fabricx.loadgen

> Runs a Load Generator to test Fabric-X network throughput.

<!-- @depends_on: hyperledger.fabricx.cryptogen, hyperledger.fabricx.fabric_ca -->

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
    - [limit_rate](#limit_rate)
- [Variables](#variables)

## Depends On

| Role                                                      | Reason                           |
| --------------------------------------------------------- | -------------------------------- |
| [`hyperledger.fabricx.cryptogen`](../cryptogen/README.md) | Crypto material (cryptogen mode) |
| [`hyperledger.fabricx.fabric_ca`](../fabric_ca/README.md) | Crypto material (Fabric-CA mode) |

## Tasks

### Crypto

| Task                                      | Description                         |
| ----------------------------------------- | ----------------------------------- |
| [crypto/setup](./tasks/crypto/setup.yaml) | Generates/transfers crypto material |
| [crypto/fetch](./tasks/crypto/fetch.yaml) | Fetches certificates                |
| [crypto/rm](./tasks/crypto/rm.yaml)       | Removes crypto material             |

#### crypto/setup

Generates and/or transfers the crypto material needed to run a Fabric-X Loadgen component. Supports two modes:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Setup the crypto material for Fabric-X Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the Fabric-X Loadgen certificates on the control node. This operation is important for the generation of the genesis block on the control node in case the Loadgen user is set as **Meta Namespace Admin** (with the `meta_namespace_admin` flag).

```yaml
- name: Fetch the Fabric-X Loadgen certificates
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for a Fabric-X Loadgen:

```yaml
- name: Remove the Fabric-X Loadgen crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                            |
| ----------------------------------------------- | -------------------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers load generator configuration |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration                  |

#### config/transfer

Transfers the Loadgen configuration files on the remote node:

```yaml
- name: Transfer the Loadgen configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/transfer
```

#### config/rm

Removes the Loadgen configuration files on the remote node:

```yaml
- name: Remove the Loadgen configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/rm
```

### Lifecycle

| Task                                    | Description           |
| --------------------------------------- | --------------------- |
| [start](./tasks/start.yaml)             | Starts load generator |
| [stop](./tasks/stop.yaml)               | Stops load generator  |
| [teardown](./tasks/teardown.yaml)       | Removes runtime       |
| [wipe](./tasks/wipe.yaml)               | Removes all data      |
| [fetch_logs](./tasks/fetch_logs.yaml)   | Collects logs         |
| [ping](./tasks/ping.yaml)               | Health check          |
| [get_metrics](./tasks/get_metrics.yaml) | Retrieves metrics     |
| [limit_rate](./tasks/limit_rate.yaml)   | Limits request rate   |

#### start

Starts the Loadgen component:

```yaml
- name: Start Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: start
```

#### stop

Stops the Loadgen component:

```yaml
- name: Stop Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: stop
```

#### teardown

Removes the Loadgen component:

```yaml
- name: Teardown Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: teardown
```

#### wipe

Removes all Loadgen data:

```yaml
- name: Wipe Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: wipe
```

#### fetch_logs

Collects Loadgen logs:

```yaml
- name: Fetch Loadgen logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: fetch_logs
```

#### ping

Health check for Loadgen:

```yaml
- name: Ping Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: ping
```

#### get_metrics

Retrieves Loadgen metrics:

```yaml
- name: Get Loadgen metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: get_metrics
```

#### limit_rate

Limits the request rate of Loadgen:

```yaml
- name: Limit Loadgen rate
  vars:
    loadgen_rate: 100
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: limit_rate
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
