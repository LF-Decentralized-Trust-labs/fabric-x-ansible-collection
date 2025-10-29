# Hyperledger Fabric-X Ansible Collection Playbooks

This folder contains playbooks that show how to use the `hyperledger.fabricx` Ansible collection roles.

## Table of Contents <!-- omit in toc -->

- [How to use](#how-to-use)
- [Group naming](#group-naming)

## How to use

These playbooks can be also used directly in your Ansible project by importing them. For example:

```yaml
- name: Generate crypto material
  ansible.builtin.import_playbook: hyperledger.fabricx.artifacts.build_crypto_material
```

More examples are available in the [examples/playbooks](../examples/playbooks) folder.

## Group naming

These playbooks come with some predefined host groups which are required within your inventory of reference to work. Specifically:

```yaml
fabric-x-orderers: # Group of all the Fabric-X Orderer hosts
fabric-x-committer: # Group of all the Fabric-X Committer hosts
load_generators: # Group of all the Fabric-X Load generator hosts
monitoring: # Group of all the monitoring hosts
```

Examples of usage of such groups are available in the [examples/inventory](../examples/inventory) folder.

**IMPORTANT**: if you import the playbooks within such collection but you don't follow the naming here indicated, the playbooks are not going to work. If grouping the hosts is not possible, consider to create your own playbooks where you use the Hyperledger Fabric-X Ansible [roles](../roles) directly.
