# hyperledger.fabricx.configtxgen

The role `hyperledger.fabricx.configtxgen` can be used to run the `configtxgen` CLI tool.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [start](#start)

## Tasks

### config/build

The task `config/build` allows to generate the `configtx.yaml` configuration file which is later used to build the genesis block.

```yaml
- name: Generate configtx.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: config/build
```

### start

The task `start` allows to start `configtxgen` for the generation of the genesis block needed to bootstrap the Fabric-X network.

```yaml
- name: Generate the genesis block for Fabric-X
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: start
```
