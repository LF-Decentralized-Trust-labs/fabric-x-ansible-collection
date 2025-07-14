# hyperledger.fabricx.cryptogen

The role `hyperledger.fabricx.cryptogen` can be used to run the `cryptogen` CLI tool.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [start](#start)

## Prerequisites

The role requires:

- `go` to be installed.

## Tasks

### config/build

The task `config/build` allows to generate the `crypto-config.yaml` configuration file which is later used to generate the crypto material with `cryptogen`.

```yaml
- name: Generate crypto-config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: config/build
```

### start

The task `start` allows to start `cryptogen` for the generation of the crypto material needed to run the Fabric-X network.

```yaml
- name: Generate the crypto material for Fabric-X with cryptogen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: start
```
