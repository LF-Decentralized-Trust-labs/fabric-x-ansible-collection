# hyperledger.fabricx.elasticsearch

> Runs an ElasticSearch container for log storage.

<!-- @depends_on: hyperledger.fabricx.openssl -->

## Table of Contents <!-- omit in toc -->

- [Depends On](#depends-on)
- [Tasks](#tasks)
  - [Crypto](#crypto)
    - [crypto/setup](#cryptosetup)
    - [crypto/fetch](#cryptofetch)
    - [crypto/rm](#cryptorm)
  - [Config](#config)
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

Generates the crypto material needed to run ElasticSearch with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the TLS certificate of a ElasticSearch running with TLS:

```yaml
- name: Fetch the TLS certificate of ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for ElasticSearch:

```yaml
- name: Remove the ElasticSearch crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/rm
```

### Config

| Task                                | Description           |
| ----------------------------------- | --------------------- |
| [config/rm](./tasks/config/rm.yaml) | Removes configuration |

#### config/rm

Removes the ElasticSearch configuration files on the remote node:

```yaml
- name: Remove the ElasticSearch configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: config/rm
```

### Lifecycle

| Task                                  | Description                    |
| ------------------------------------- | ------------------------------ |
| [start](./tasks/start.yaml)           | Starts ElasticSearch container |
| [stop](./tasks/stop.yaml)             | Stops ElasticSearch container  |
| [teardown](./tasks/teardown.yaml)     | Removes container              |
| [wipe](./tasks/wipe.yaml)             | Removes all data               |
| [fetch_logs](./tasks/fetch_logs.yaml) | Collects logs                  |
| [ping](./tasks/ping.yaml)             | Health check                   |

#### start

Starts the ElasticSearch container:

```yaml
- name: Start ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: start
```

#### stop

Stops the ElasticSearch container:

```yaml
- name: Stop ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: stop
```

#### teardown

Removes the ElasticSearch container:

```yaml
- name: Teardown ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: teardown
```

#### wipe

Removes all ElasticSearch data:

```yaml
- name: Wipe ElasticSearch
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: wipe
```

#### fetch_logs

Collects ElasticSearch logs:

```yaml
- name: Fetch ElasticSearch logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: fetch_logs
```

#### ping

Health check for ElasticSearch:

```yaml
- name: Ping ElasticSearch
  vars:
    elasticsearch_port: 9200
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: ping
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
