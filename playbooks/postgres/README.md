# PostgreSQL Playbooks

The `postgres` playbooks operate the PostgreSQL databases shared across the network. A database can back any component (Fabric CA, committer, Block Explorer), so every playbook here targets `all` and selects hosts by inventory variable rather than by group.

## Table of Contents <!-- omit in toc -->

- [Playbooks flow](#playbooks-flow)
- [start.yaml](#startyaml)
- [stop.yaml](#stopyaml)
- [teardown.yaml](#teardownyaml)
- [wipe.yaml](#wipeyaml)
- [ping.yaml](#pingyaml)

## Playbooks flow

```mermaid
flowchart LR
  START[start] --> PING[ping]
  PING --> STOP[stop]
  STOP --> TEARDOWN[teardown]
  TEARDOWN --> WIPE[wipe]
```

## start.yaml

[`start.yaml`](./start.yaml) starts every PostgreSQL database in the inventory in a single pass, ahead of the components that depend on them. Run it before starting the committer or the Block Explorer. The Fabric CA playbooks start their own CA databases directly (see [`fabric_ca_server.start`](../fabric_ca_server/README.md)) so a scoped `make generate-crypto` run doesn't reach into every database in the network; running this playbook too is harmless, since starting an already-running database is a no-op.

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
