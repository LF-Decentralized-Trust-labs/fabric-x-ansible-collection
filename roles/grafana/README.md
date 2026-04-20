# hyperledger.fabricx.grafana

> Runs a Grafana instance to visualize Fabric-X component metrics in container or Kubernetes mode.

<!-- @depends_on: hyperledger.fabricx.openssl, hyperledger.fabricx.prometheus -->

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
    - [fetch\_logs](#fetch_logs)
    - [ping](#ping)
- [Variables](#variables)

## Depends On

| Role                                                        | Reason                     |
| ----------------------------------------------------------- | -------------------------- |
| [`hyperledger.fabricx.openssl`](../openssl/README.md)       | TLS certificate generation |
| [`hyperledger.fabricx.prometheus`](../prometheus/README.md) | Metrics data source        |

## Tasks

### Crypto

| Task                                      | Description                   |
| ----------------------------------------- | ----------------------------- |
| [crypto/setup](./tasks/crypto/setup.yaml) | Generates TLS crypto material |
| [crypto/fetch](./tasks/crypto/fetch.yaml) | Fetches TLS certificate       |
| [crypto/rm](./tasks/crypto/rm.yaml)       | Removes TLS crypto material   |

#### crypto/setup

Generates the crypto material needed to run Grafana with TLS using [openssl](../openssl/README.md). When `grafana_use_k8s` is enabled, it also applies the Kubernetes Secret that holds the admin credentials and optional TLS material:

```yaml
- name: Setup the crypto material for Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the TLS certificate of a Grafana running with TLS:

```yaml
- name: Fetch the TLS certificate of Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for Grafana:

```yaml
- name: Remove the Grafana crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                     |
| ----------------------------------------------- | ------------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers Grafana configuration |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration           |

#### config/transfer

Transfers the Grafana configuration files on the remote node. When `grafana_use_k8s` is enabled, it also applies the Kubernetes ConfigMap used by the Deployment:

```yaml
- name: Transfer the Grafana configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/transfer
```

#### config/rm

Removes the Grafana configuration files on the remote node:

```yaml
- name: Remove the Grafana configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/rm
```

### Lifecycle

| Task                                  | Description                                          |
| ------------------------------------- | ---------------------------------------------------- |
| [start](./tasks/start.yaml)           | Starts Grafana in the selected deployment mode       |
| [stop](./tasks/stop.yaml)             | Stops Grafana container mode                         |
| [teardown](./tasks/teardown.yaml)     | Removes the workload in the selected deployment mode |
| [wipe](./tasks/wipe.yaml)             | Removes all data                                     |
| [fetch_logs](./tasks/fetch_logs.yaml) | Collects logs                                        |
| [ping](./tasks/ping.yaml)             | Health check                                         |

#### start

Starts Grafana in the selected deployment mode. Set `grafana_use_k8s: true` to deploy a Service and Deployment on Kubernetes; set `grafana_k8s_use_node_port: true` as well when you also want the NodePort Service. Otherwise the role starts the container-based deployment:

```yaml
- name: Start Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: start
```

#### stop

Stops the Grafana container when container mode is enabled:

```yaml
- name: Stop Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: stop
```

#### teardown

Removes the Grafana container or Kubernetes workload:

```yaml
- name: Teardown Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: teardown
```

#### wipe

Removes all Grafana data:

```yaml
- name: Wipe Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: wipe
```

#### fetch_logs

Collects Grafana logs from the container or Kubernetes pod, depending on the selected deployment mode:

```yaml
- name: Fetch Grafana logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: fetch_logs
```

#### ping

Health check for Grafana:

```yaml
- name: Ping Grafana
  vars:
    grafana_web_port: 3000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: ping
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
