# hyperledger.fabricx.armageddon

> Runs the `armageddon` CLI tool for genesis block and shared config generation.

<!-- @depends_on: hyperledger.fabricx.cryptogen -->

## Table of Contents <!-- omit in toc -->

- [Depends On](#depends-on)
- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Config](#config)
  - [Lifecycle](#lifecycle)

## Depends On

| Role                                                      | Reason                                          |
| --------------------------------------------------------- | ----------------------------------------------- |
| [`hyperledger.fabricx.cryptogen`](../cryptogen/README.md) | Genesis block generation requires crypto output |

## Prerequisites

- `go` to be installed (when using binary mode)

## Tasks

### Config

| Task                                      | Description                  |
| ----------------------------------------- | ---------------------------- |
| [config/build](./tasks/config/build.yaml) | Generates shared_config.yaml |

#### config/build

Generates the `shared_config.yaml` configuration file used to build the `shared_config.binpb` protobuf.

```yaml
- name: Generate shared_config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: config/build
```

### Lifecycle

| Task                                                      | Description                   |
| --------------------------------------------------------- | ----------------------------- |
| [create_shared_config](./tasks/create_shared_config.yaml) | Generates shared_config.binpb |

#### create_shared_config

Generates the `shared_config.binpb` serialized protobuf containing all necessary configuration to bootstrap the Fabric-X Orderer.

```yaml
- name: Generate shared_config.binpb
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: create_shared_config
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
