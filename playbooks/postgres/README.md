# PostgreSQL Playbooks

The `postgres` playbooks operate the PostgreSQL databases shared across the network. A database can back any component (Fabric CA, committer, Block Explorer), so every playbook here targets `all` and selects hosts by inventory variable rather than by group.

## Table of Contents <!-- omit in toc -->

- [Playbooks flow](#playbooks-flow)
- [generate\_crypto.yaml](#generate_cryptoyaml)
- [configs.yaml](#configsyaml)
- [start.yaml](#startyaml)
- [stop.yaml](#stopyaml)
- [teardown.yaml](#teardownyaml)
- [wipe.yaml](#wipeyaml)
- [ping.yaml](#pingyaml)
- [fetch\_crypto.yaml](#fetch_cryptoyaml)
- [fetch\_logs.yaml](#fetch_logsyaml)

## Playbooks flow

```mermaid
flowchart LR
  CRYPTO[generate_crypto] --> CONFIGS[configs]
  CONFIGS --> START[start]
  START --> PING[ping]
  PING --> STOP[stop]
  STOP --> TEARDOWN[teardown]
  TEARDOWN --> WIPE[wipe]
```

## generate_crypto.yaml

[`generate_crypto.yaml`](./generate_crypto.yaml) generates TLS crypto material for every PostgreSQL database in the inventory: cryptogen transfer or Fabric CA enrollment depending on inventory configuration. The Fabric CA databases generate their own crypto directly (see [`fabric_ca_server.generate_crypto`](../fabric_ca_server/README.md)) so it can run before a Fabric CA server exists to enroll against; running this playbook too is harmless, since it is a no-op for hosts whose crypto already exists.

```shell
ansible-playbook hyperledger.fabricx.postgres.generate_crypto --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default. Use `target_hosts` to restrict to a subset.
- Nuance: only hosts that define `postgres_port` participate. Hosts enrolling through Fabric CA require a reachable, already-started Fabric CA server.

## configs.yaml

[`configs.yaml`](./configs.yaml) transfers PostgreSQL configuration files (mTLS `pg_hba.conf` rules, Kubernetes ConfigMaps) for every database in the inventory.

```shell
ansible-playbook hyperledger.fabricx.postgres.configs --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default.
- Nuance: only hosts that define `postgres_port` participate.

## start.yaml

[`start.yaml`](./start.yaml) starts every PostgreSQL database in the inventory in a single pass, ahead of the components that depend on them. Run it before starting the committer or the Block Explorer.

```shell
ansible-playbook hyperledger.fabricx.postgres.start --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default. Use `target_hosts` to restrict to a subset.
- Nuance: only hosts that define `postgres_port` participate; every other host is skipped. This lets one playbook serve Fabric CA, committer, and Block Explorer databases regardless of which groups they live in.

## stop.yaml

[`stop.yaml`](./stop.yaml) stops every PostgreSQL database in the inventory. Run it after stopping the components that depend on them.

```shell
ansible-playbook hyperledger.fabricx.postgres.stop --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default.
- Nuance: only hosts that define `postgres_port` participate.

## teardown.yaml

[`teardown.yaml`](./teardown.yaml) removes runtime state for every PostgreSQL database in the inventory. Run it after tearing down the components that depend on them and before removing container networks.

```shell
ansible-playbook hyperledger.fabricx.postgres.teardown --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default.
- Nuance: only hosts that define `postgres_port` participate.

## wipe.yaml

[`wipe.yaml`](./wipe.yaml) removes all PostgreSQL artifacts, including generated configuration and crypto, from every database host in the inventory.

```shell
ansible-playbook hyperledger.fabricx.postgres.wipe --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default.
- Nuance: only hosts that define `postgres_port` participate.

## ping.yaml

[`ping.yaml`](./ping.yaml) checks that every PostgreSQL database port in the inventory is reachable. Run it before pinging the components that depend on them.

```shell
ansible-playbook hyperledger.fabricx.postgres.ping --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default.
- Nuance: only hosts that define `postgres_port` participate.

## fetch_crypto.yaml

[`fetch_crypto.yaml`](./fetch_crypto.yaml) fetches every PostgreSQL database's crypto material into the configured artifacts directory for inspection, reuse, or debugging.

```shell
ansible-playbook hyperledger.fabricx.postgres.fetch_crypto --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default.
- Nuance: only hosts that define `postgres_port` participate.

## fetch_logs.yaml

[`fetch_logs.yaml`](./fetch_logs.yaml) fetches every PostgreSQL database's logs from targeted hosts into the configured output directory.

```shell
ansible-playbook hyperledger.fabricx.postgres.fetch_logs --extra-vars '{"target_hosts": "all"}'
```

Properties:

- Target hosts: `all` by default.
- Nuance: only hosts that define `postgres_port` participate.
