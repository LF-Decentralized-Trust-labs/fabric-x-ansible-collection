# hyperledger.fabricx.node_exporter

> Runs a Prometheus Node Exporter to collect machine state metrics (RAM, disk, CPU, network).

<!-- @depends_on: hyperledger.fabricx.openssl -->

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
    - [get_host_set](#get_host_set)
- [Variables](#variables)

## Depends On

| Role                                                  | Reason                     |
| ----------------------------------------------------- | -------------------------- |
| [`hyperledger.fabricx.openssl`](../openssl/README.md) | TLS certificate generation |

## Tasks

### Crypto

| Task                                      | Description                   |
| ----------------------------------------- | ----------------------------- |
| [crypto/setup](./tasks/crypto/setup.yaml) | Generates TLS crypto material |
| [crypto/fetch](./tasks/crypto/fetch.yaml) | Fetches TLS certificate       |
| [crypto/rm](./tasks/crypto/rm.yaml)       | Removes TLS crypto material   |

#### crypto/setup

Generates the crypto material needed to run Node Exporter with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the TLS certificate of a Node Exporter running with TLS:

```yaml
- name: Fetch the TLS certificate of Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for Node Exporter:

```yaml
- name: Remove the Node Exporter crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                           |
| ----------------------------------------------- | ------------------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers Node Exporter configuration |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration                 |

#### config/transfer

Transfers the Node Exporter configuration files on the remote node:

```yaml
- name: Transfer the Node Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/transfer
```

#### config/rm

Removes the Node Exporter configuration files on the remote node:

```yaml
- name: Remove the Node Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/rm
```

### Lifecycle

| Task                                      | Description                    |
| ----------------------------------------- | ------------------------------ |
| [start](./tasks/start.yaml)               | Starts Node Exporter container |
| [stop](./tasks/stop.yaml)                 | Stops Node Exporter container  |
| [teardown](./tasks/teardown.yaml)         | Removes container              |
| [wipe](./tasks/wipe.yaml)                 | Removes all data               |
| [fetch_logs](./tasks/fetch_logs.yaml)     | Collects logs                  |
| [ping](./tasks/ping.yaml)                 | Health check                   |
| [get_host_set](./tasks/get_host_set.yaml) | Gets host information          |

#### start

Starts the Node Exporter container:

```yaml
- name: Start Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: start
```

#### stop

Stops the Node Exporter container:

```yaml
- name: Stop Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: stop
```

#### teardown

Removes the Node Exporter container:

```yaml
- name: Teardown Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: teardown
```

#### wipe

Removes all Node Exporter data:

```yaml
- name: Wipe Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: wipe
```

#### fetch_logs

Collects Node Exporter logs:

```yaml
- name: Fetch Node Exporter logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: fetch_logs
```

#### ping

Health check for Node Exporter:

```yaml
- name: Ping Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: ping
```

#### get_host_set

Gets host information:

```yaml
- name: Get host set
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: get_host_set
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
