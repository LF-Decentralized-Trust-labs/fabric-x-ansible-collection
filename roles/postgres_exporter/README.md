# hyperledger.fabricx.postgres_exporter

> Runs a [Prometheus Postgres Exporter](https://github.com/prometheuscommunity/postgres_exporter) to collect PostgreSQL metrics.

<!-- @depends_on: hyperledger.fabricx.openssl, hyperledger.fabricx.postgres -->

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

| Role                                                    | Reason                       |
| ------------------------------------------------------- | ---------------------------- |
| [`hyperledger.fabricx.openssl`](../openssl/README.md)   | TLS certificate generation   |
| [`hyperledger.fabricx.postgres`](../postgres/README.md) | Database instance to monitor |

## Tasks

### Crypto

| Task                                      | Description                   |
| ----------------------------------------- | ----------------------------- |
| [crypto/setup](./tasks/crypto/setup.yaml) | Generates TLS crypto material |
| [crypto/fetch](./tasks/crypto/fetch.yaml) | Fetches TLS certificate       |
| [crypto/rm](./tasks/crypto/rm.yaml)       | Removes TLS crypto material   |

#### crypto/setup

Generates the crypto material needed to run Postgres Exporter with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the TLS certificate of a Postgres Exporter running with TLS:

```yaml
- name: Fetch the TLS certificate of Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for Postgres Exporter:

```yaml
- name: Remove the Postgres Exporter crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                      |
| ----------------------------------------------- | -------------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers exporter configuration |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration            |

#### config/transfer

Transfers the Postgres Exporter configuration files on the remote node:

```yaml
- name: Transfer the Postgres Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/transfer
```

#### config/rm

Removes the Postgres Exporter configuration files on the remote node:

```yaml
- name: Remove the Postgres Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/rm
```

### Lifecycle

| Task                                  | Description               |
| ------------------------------------- | ------------------------- |
| [start](./tasks/start.yaml)           | Starts exporter container |
| [stop](./tasks/stop.yaml)             | Stops exporter container  |
| [teardown](./tasks/teardown.yaml)     | Removes container         |
| [wipe](./tasks/wipe.yaml)             | Removes all data          |
| [fetch_logs](./tasks/fetch_logs.yaml) | Collects logs             |
| [ping](./tasks/ping.yaml)             | Health check              |

#### start

Starts the Postgres Exporter container:

```yaml
- name: Start Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: start
```

#### stop

Stops the Postgres Exporter container:

```yaml
- name: Stop Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: stop
```

#### teardown

Removes the Postgres Exporter container:

```yaml
- name: Teardown Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: teardown
```

#### wipe

Removes all Postgres Exporter data:

```yaml
- name: Wipe Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: wipe
```

#### fetch_logs

Collects Postgres Exporter logs:

```yaml
- name: Fetch Postgres Exporter logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: fetch_logs
```

#### ping

Health check for Postgres Exporter:

```yaml
- name: Ping Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: ping
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
