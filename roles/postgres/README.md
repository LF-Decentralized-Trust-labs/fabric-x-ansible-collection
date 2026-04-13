# hyperledger.fabricx.postgres

> Runs a PostgreSQL database instance as a container.

<!-- @depends_on: hyperledger.fabricx.openssl, hyperledger.fabricx.cryptogen, hyperledger.fabricx.fabric_ca -->

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

| Role                                                      | Reason                                           |
| --------------------------------------------------------- | ------------------------------------------------ |
| [`hyperledger.fabricx.openssl`](../openssl/README.md)     | TLS key/cert generation (without org definition) |
| [`hyperledger.fabricx.cryptogen`](../cryptogen/README.md) | TLS crypto material (cryptogen mode)             |
| [`hyperledger.fabricx.fabric_ca`](../fabric_ca/README.md) | TLS crypto material (Fabric-CA mode)             |

## Tasks

### Crypto

| Task                                      | Description                             |
| ----------------------------------------- | --------------------------------------- |
| [crypto/setup](./tasks/crypto/setup.yaml) | Generates/transfers TLS crypto material |
| [crypto/fetch](./tasks/crypto/fetch.yaml) | Fetches TLS certificate to control node |
| [crypto/rm](./tasks/crypto/rm.yaml)       | Removes TLS crypto material             |

#### crypto/setup

Generates/transfers the crypto material needed to run a Postgres DB with TLS. Supports 3 operating modes:

- with `openssl` (see [hyperledger.fabricx.openssl](../openssl/README.md)) if the DB runs without an Hyperledger Fabric-X peer organization definition;
- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Generate the TLS keypair for Postgres DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/setup
```

#### crypto/fetch

Fetches the TLS certificate of a Postgres DB on the control node, so that it could be shared with the clients later:

```yaml
- name: Fetch the Postgres DB TLS certificate
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/fetch
```

#### crypto/rm

Removes the crypto material generated for Postgres on the remote node:

```yaml
- name: Remove the Postgres crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/rm
```

### Config

| Task                                            | Description                        |
| ----------------------------------------------- | ---------------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers PostgreSQL configuration |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration              |

#### config/transfer

Transfers the Postgres configuration files on the remote node:

```yaml
- name: Transfer the Postgres configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/transfer
```

#### config/rm

Removes the Postgres configuration files on the remote node:

```yaml
- name: Remove the Postgres configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/rm
```

### Lifecycle

| Task                                  | Description                 |
| ------------------------------------- | --------------------------- |
| [start](./tasks/start.yaml)           | Starts PostgreSQL container |
| [stop](./tasks/stop.yaml)             | Stops PostgreSQL container  |
| [teardown](./tasks/teardown.yaml)     | Removes container           |
| [wipe](./tasks/wipe.yaml)             | Removes all data            |
| [fetch_logs](./tasks/fetch_logs.yaml) | Collects logs               |
| [ping](./tasks/ping.yaml)             | Health check                |

#### start

Starts the Postgres container:

```yaml
- name: Start Postgres
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: start
```

#### stop

Stops the Postgres container:

```yaml
- name: Stop Postgres
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: stop
```

#### teardown

Removes the Postgres container:

```yaml
- name: Teardown Postgres
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: teardown
```

#### wipe

Removes all Postgres data:

```yaml
- name: Wipe Postgres
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: wipe
```

#### fetch_logs

Collects Postgres logs:

```yaml
- name: Fetch Postgres logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: fetch_logs
```

#### ping

Health check for Postgres:

```yaml
- name: Ping Postgres
  vars:
    postgres_port: 5432
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: ping
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
