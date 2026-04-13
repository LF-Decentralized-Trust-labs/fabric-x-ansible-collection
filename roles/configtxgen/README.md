# hyperledger.fabricx.configtxgen

> Runs the `configtxgen` CLI tool to generate Fabric-X genesis blocks.

<!-- @depends_on: hyperledger.fabricx.cryptogen -->

## Table of Contents <!-- omit in toc -->

- [Depends On](#depends-on)
- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Config](#config)
    - [config/build](#configbuild)
  - [Lifecycle](#lifecycle)
    - [start](#start)
- [Variables](#variables)

## Depends On

| Role                                                      | Reason                                          |
| --------------------------------------------------------- | ----------------------------------------------- |
| [`hyperledger.fabricx.cryptogen`](../cryptogen/README.md) | Genesis block generation requires crypto output |

## Prerequisites

- `go` to be installed (when using binary mode)

## Tasks

### Config

| Task                                      | Description             |
| ----------------------------------------- | ----------------------- |
| [config/build](./tasks/config/build.yaml) | Generates configtx.yaml |

#### config/build

Generates the `configtx.yaml` configuration file used to build the genesis block.

```yaml
- name: Generate configtx.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: config/build
```

### Lifecycle

| Task                        | Description             |
| --------------------------- | ----------------------- |
| [start](./tasks/start.yaml) | Generates genesis block |

#### start

Runs `configtxgen` to generate the genesis block for bootstrapping the Fabric-X network.

```yaml
- name: Generate the genesis block for Fabric-X
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: start
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
