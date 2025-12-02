# hyperledger.fabricx.elasticsearch

The role `hyperledger.fabricx.elasticsearch` can be used to run an ElasticSearch container.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate the crypto material needed to run ElasticSearch with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` fetches the TLS certificate of a ElasticSearch running with TLS:

```yaml
- name: Fetch the TLS certificate of ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for ElasticSearch:

```yaml
- name: Remove the ElasticSearch crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/rm
```

### config/rm

The task `config/rm` removes the ElasticSearch configuration files on the remote node:

```yaml
- name: Remove the ElasticSearch configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: config/rm
```

### start

The task `start` allows to start an ElasticSearch container:

```yaml
- name: Start an ElasticSearch container
  vars:
    elasticsearch_http_port: 9200
    elasticsearch_transport_port: 9300
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: start
```

### stop

The task `stop` allows to stop an ElasticSearch container.

```yaml
- name: Stop ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down an ElasticSearch container and remove all the data stored by the container on the persistent volume.

```yaml
- name: Teardown ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down an ElasticSearch container and remove all the data stored by the container on the persistent volume.

```yaml
- name: Wipe ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from an ElasticSearch container.

```yaml
- name: Fetch ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping an ElasticSearch container. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: ping
```
