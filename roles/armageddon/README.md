# hyperledger.fabricx.armageddon

The role `hyperledger.fabricx.armageddon` can be used to run the `armageddon` CLI tool. The role allows to run it both as binary and as container.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [create_shared_config](#create_shared_config)

## Tasks

### config/build

The task `config/build` allows to generate the `shared_config.yaml` configuration file which is later used to build the `shared_config.binpb` protobuf.

```yaml
- name: Generate shared_config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: config/build
```

### create_shared_config

The task `create_shared_config` allows to generate the `shared_config.binpb` serialized protobuf which contains all the necessary configuration to bootstrap the Fabric-X Orderer. This block can be embedded in the genesis block to provide such configuration to the orderers.

```yaml
- name: Generate shared_config.binpb
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: create_shared_config
```
