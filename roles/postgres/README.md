# hyperledger.fabricx.postgres

The role `hyperledger.fabricx.postgres` can be used to run a PostgreSQL DB.

The role allows to run Postgres as **container only** (binary is not currently supported).

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

## Variables

| Variable                        | Default                                              | Description                                  |
| ------------------------------- | ---------------------------------------------------- | -------------------------------------------- |
| `postgres_registry_endpoint`    | `$POSTGRES_REGISTRY_ENDPOINT` or `docker.io/library` | Container registry endpoint                  |
| `postgres_image_name`           | `postgres`                                           | Container image name                         |
| `postgres_image_tag`            | `16.4`                                               | Container image tag                          |
| `postgres_image`                | `{{ registry }}/{{ name }}:{{ tag }}`                | Full container image reference               |
| `postgres_container_name`       | `{{ inventory_hostname }}`                           | Name given to the container                  |
| `postgres_remote_config_dir`    | `{{ remote_config_dir }}`                            | Configuration directory on the remote node   |
| `postgres_remote_data_dir`      | `{{ remote_data_dir }}`                              | Data directory on the remote node            |
| `postgres_container_config_dir` | `/var/lib/postgresql/config`                         | Configuration directory inside the container |
| `postgres_container_data_dir`   | `/var/lib/postgresql/data`                           | Data directory inside the container          |
| `postgres_use_tls`              | `false`                                              | Enable TLS                                   |
| `postgres_use_mtls`             | `false`                                              | Enable mutual TLS                            |
| `postgres_tls_private_key_file` | `server.key`                                         | TLS private key file name                    |
| `postgres_tls_cert_file`        | `server.crt`                                         | TLS certificate file name                    |

## Tasks

### crypto/setup

The task `crypto/setup` transfers or generates the crypto material needed to run a Postgres DB with TLS. The task supports 3 operating modes:

- with `openssl` (see [hyperledger.fabricx.openssl](../openssl/README.md)) if the DB runs without an Hyperledger Fabric-X peer organization definition;
- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Generate the TLS keypair for Postgres DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` allows to fetch the TLS certificate of a Postgres DB on the control node, so that it could be shared with the clients later.

```yaml
- name: Fetch the Postgres DB TLS certificate
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for Postgres on the remote node:

```yaml
- name: Remove the Postgres crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` transfers the Postgres configuration files on the remote node. When mTLS is enabled and `postgres_mtls_clients` is defined, it also transfers the `pg_hba.conf` to enforce mutual TLS connections:

```yaml
- name: Transfer the Postgres configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Postgres configuration files on the remote node:

```yaml
- name: Remove the Postgres configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/rm
```

### start

The task `start` allows to start the Postgres DB.

```yaml
- name: Start the Postgres DB
  vars:
    postgres_port: 5432
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: start
```

### stop

The task `stop` allows to stop the Postgres DB.

```yaml
- name: Stop the Postgres DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Postgres DB, and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown the Postgres DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Postgres DB, and remove all the artifacts (configuration files and all the runtime-generated artifacts).

```yaml
- name: Wipe the Postgres DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Postgres DB components from the remote hosts to the control node.

```yaml
- name: Fetch the Postgres DB logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Postgres DB components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Postgres DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: ping
```
