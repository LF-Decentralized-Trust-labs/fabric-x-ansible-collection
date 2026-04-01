# hyperledger.fabricx.node_exporter

The role `hyperledger.fabricx.node_exporter` can be used to run a Prometheus Node Exporter node to collect general metrics about the machine state such as RAM consumption, disk usage, network bandwidth, CPU load and so on.

The role allows to run Node Exporter as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)
  - [get\_host\_set](#get_host_set)

## Variables

| Variable                             | Default                                                | Description                                  |
| ------------------------------------ | ------------------------------------------------------ | -------------------------------------------- |
| `node_exporter_registry_endpoint`    | `$NODE_EXPORTER_REGISTRY_ENDPOINT` or `docker.io/prom` | Container registry endpoint                  |
| `node_exporter_image_name`           | `node-exporter`                                        | Container image name                         |
| `node_exporter_image_tag`            | `latest`                                               | Container image tag                          |
| `node_exporter_image`                | `{{ registry }}/{{ name }}:{{ tag }}`                  | Full container image reference               |
| `node_exporter_container_name`       | `node-exporter`                                        | Name given to the container                  |
| `node_exporter_remote_config_dir`    | `{{ remote_deploy_dir }}/node-exporter/config`         | Configuration directory on the remote node   |
| `node_exporter_container_config_dir` | `/var/config`                                          | Configuration directory inside the container |
| `node_exporter_web_config_file`      | `web-config.yaml`                                      | Web configuration file name                  |
| `node_exporter_root_fs_flags`        | `ro,rslave`                                            | Mount flags for the root filesystem volume   |
| `node_exporter_use_tls`              | `false`                                                | Enable TLS                                   |
| `node_exporter_tls_private_key_file` | `server.key`                                           | TLS private key file name                    |
| `node_exporter_tls_cert_file`        | `server.crt`                                           | TLS certificate file name                    |

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate the crypto material needed to run Node Exporter with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` fetches the TLS certificate of a Node Exporter running with TLS:

```yaml
- name: Fetch the TLS certificate of Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for Node Exporter:

```yaml
- name: Remove the Node Exporter crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` transfers the Node Exporter configuration files on the remote node:

```yaml
- name: Transfer the Node Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Node Exporter configuration files on the remote node:

```yaml
- name: Remove the Node Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/rm
```

### start

The task `start` allows to bootstrap Node Exporter.

```yaml
- name: Start Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: start
```

### stop

The task `stop` allows to stop Node Exporter without deleting the associated content on disk.

```yaml
- name: Stop Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down Node Exporter deleting the associated content on disk.

```yaml
- name: Teardown Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down and wipe all configuration files of a Node Exporter.

```yaml
- name: Wipe the Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Node Exporter instance.

```yaml
- name: Fetch the Node Exporter logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Node Exporter instance on its opened port. It is useful to check whether the instance is running or if it is not running/reachable.

```yaml
- name: Ping Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: ping
```

### get_host_set

The task `get_host_set` generates a set without duplicates of Ansible machines by setting them in the dynamic group `node_exporter_hosts`. This group can be used to run the Node Exporter tasks preventing duplication (i.e. start one Node Exporter instance per machine instead of being per-host).

```yaml
- name: Get the set of hosts in node_exporter_hosts
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: get_host_set
```
