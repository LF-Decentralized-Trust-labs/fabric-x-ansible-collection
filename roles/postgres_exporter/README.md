# hyperledger.fabricx.postgres_exporter

The role `hyperledger.fabricx.postgres_exporter` can be used to run a [Prometheus Postgres Exporter](https://github.com/prometheus-community/postgres_exporter) to collect PostgreSQL metrics.

The role allows to run Postgres Exporter as **container only** (binary is not currently supported).

The role supports running one exporter per database instance.

## Table of Contents <!-- omit in toc -->

- [Postgres Exporter Metrics](#postgres-exporter-metrics)
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
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)

## Postgres Exporter Metrics

When the `prometheus_postgres_exporters` variable is set, Prometheus scrapes the following main metric families from each PostgreSQL instance:

- **pg_up** – Database availability (1 = up, 0 = down)
- **pg_connections** – Current number of active connections
- **pg_database_size_bytes** – Database size in bytes
- **pg_stat_activity** – Information about active queries and sessions
- **pg*stat_database* metrics** – Transaction counts, commit/rollback rates, tuple reads/inserts/updates/deletes
- **pg*stat_replication* metrics** – Replication lag and streaming replication state
- **pg_locks** – Lock counts by type and mode
- **pg*index* metrics** – Index usage and size
- **pg*table* metrics** – Table size and row counts
- **pg*stat_bgwriter* metrics** – Background writer activity (checkpoints, buffers written)
- **pg*stat_statements* metrics** (if extension is enabled) – Query execution counts, total/mean execution time, I/O stats
- **pg_cache_hit_ratio** – Calculated metric for cache efficiency

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate the crypto material needed to run Postgres Exporter with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` fetches the TLS certificate of a Postgres Exporter running with TLS:

```yaml
- name: Fetch the TLS certificate of Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for Postgres Exporter:

```yaml
- name: Remove the Postgres Exporter crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` transfers the Postgres Exporter configuration files on the remote node:

```yaml
- name: Transfer the Postgres Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Postgres Exporter configuration files on the remote node:

```yaml
- name: Remove the Postgres Exporter configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/rm
```

### start

The task `start` allows to start the Postgres Exporter.

```yaml
- name: Start Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: start
```

### stop

The task `stop` allows to stop the Postgres Exporter.

```yaml
- name: Stop Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Postgres Exporter.

```yaml
- name: Teardown the Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down and wipe all configuration files of a Postgres Postgres Exporter.

```yaml
- name: Wipe the Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Postgres Exporter.

```yaml
- name: Fetch the Postgres Exporter logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Postgres Exporter components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Postgres Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: ping
```
