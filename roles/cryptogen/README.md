# hyperledger.fabricx.cryptogen

> Generates crypto material for Hyperledger Fabric-X networks using the `cryptogen` CLI tool.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Config](#config)
    - [config/build](#configbuild)
  - [Lifecycle](#lifecycle)
    - [start](#start)
    - [fetch](#fetch)
- [Variables](#variables)

## Prerequisites

- `go` to be installed (when using binary mode)

## Tasks

### Config

| Task                                      | Description                  |
| ----------------------------------------- | ---------------------------- |
| [config/build](./tasks/config/build.yaml) | Generates crypto-config.yaml |

#### config/build

Generates the `crypto-config.yaml` configuration file used to produce crypto material.

```yaml
- name: Generate crypto-config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: config/build
```

### Lifecycle

| Task                        | Description               |
| --------------------------- | ------------------------- |
| [start](./tasks/start.yaml) | Generates crypto material |
| [fetch](./tasks/fetch.yaml) | Fetches MSP folders       |

#### start

Runs `cryptogen` to generate crypto material for the Fabric-X network.

```yaml
- name: Generate the crypto material for Fabric-X with cryptogen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: start
```

#### fetch

Fetches the MSP folder for each organization. Emulates the fetch operation performed by [`hyperledger.fabricx.fabric_ca`](../fabric_ca/README.md) when using Fabric-CA.

```yaml
- name: Copy the MSP folder of each Fabric-X organization
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: fetch
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
