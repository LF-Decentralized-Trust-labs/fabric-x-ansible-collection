# hyperledger.fabricx.node_exporter

The role `hyperledger.fabricx.node_exporter` can be used to run a Prometheus Node Exporter node to collect general metrics about the machine state such as RAM consumption, disk usage, network bandwidth, CPU load and so on.

The role allows to run Node Exporter as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [get\_host\_set](#get_host_set)

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

### config/transfer

The task `config/transfer` transfers the Node Exporter configuration files:

```yaml
- name: Transfer the Node Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Node Exporter configuration files:

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

### get_host_set

The task `get_host_set` generates a set without duplicates of Ansible machines by setting them in the dynamic group `node_exporter_hosts`. This group can be used to run the Node Exporter tasks preventing duplication (i.e. start one Node Exporter instance per machine instead of being per-host).

```yaml
- name: Get the set of hosts in node_exporter_hosts
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: get_host_set
```
