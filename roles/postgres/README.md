# hyperledger.fabricx.postgres

The role `hyperledger.fabricx.postgres` can be used to run a PostgreSQL DB.

The role allows to run Postgres as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [crypto/transfer](#cryptotransfer)
  - [crypto/fetch](#cryptofetch)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)

## Tasks

### crypto/transfer

The task `crypto/transfer` allows to generate the crypto material needed to run a Postgres DB with TLS. The task uses `openssl` (see [hyperledger.fabricx.openssl](../openssl/README.md)) to generate a TLS keypair and a self-signed certificate which can be shared with the client to perform a connection secured with TLS.

```yaml
- name: Generate the TLS keypair for Postgres DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/transfer
```

### crypto/fetch

The task `crypto/fetch` allows to fetch the TLS certificate of a Postgres DB on the control node, so that it could be shared with the clients later.

```yaml
- name: Fetch the Postgres DB TLS certificate
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/fetch
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
