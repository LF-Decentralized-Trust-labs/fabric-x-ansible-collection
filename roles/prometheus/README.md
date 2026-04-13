# hyperledger.fabricx.prometheus

> Runs a Prometheus metrics collector.

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

Generates the crypto material needed to run Prometheus with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the TLS certificate of Prometheus running with TLS:

```yaml
- name: Fetch the TLS certificate of Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for Prometheus:

```yaml
- name: Remove the Prometheus crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                        |
| ----------------------------------------------- | ---------------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers Prometheus configuration |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration              |

#### config/transfer

Transfers the Prometheus configuration files on the remote node:

```yaml
- name: Transfer the Prometheus configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: config/transfer
```

#### config/rm

Removes the Prometheus configuration files on the remote node:

```yaml
- name: Remove the Prometheus configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: config/rm
```

### Lifecycle

| Task                                  | Description                 |
| ------------------------------------- | --------------------------- |
| [start](./tasks/start.yaml)           | Starts Prometheus container |
| [stop](./tasks/stop.yaml)             | Stops Prometheus container  |
| [teardown](./tasks/teardown.yaml)     | Removes container           |
| [wipe](./tasks/wipe.yaml)             | Removes all data            |
| [fetch_logs](./tasks/fetch_logs.yaml) | Collects logs               |
| [ping](./tasks/ping.yaml)             | Health check                |

#### start

Starts the Prometheus container:

```yaml
- name: Start Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: start
```

#### stop

Stops the Prometheus container:

```yaml
- name: Stop Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: stop
```

#### teardown

Removes the Prometheus container:

```yaml
- name: Teardown Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: teardown
```

#### wipe

Removes all Prometheus data:

```yaml
- name: Wipe Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: wipe
```

#### fetch_logs

Collects Prometheus logs:

```yaml
- name: Fetch Prometheus logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: fetch_logs
```

#### ping

Health check for Prometheus:

```yaml
- name: Ping Prometheus
  vars:
    prometheus_port: 9090
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: ping
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
