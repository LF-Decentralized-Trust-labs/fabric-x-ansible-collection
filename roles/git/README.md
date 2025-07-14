# hyperledger.fabricx.git

The role `hyperledger.fabricx.git` can be used to perform `git` operations on a node.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [clone](#clone)

## Prerequisites

The role requires `git` to be installed on the targeted node.

## Tasks

Here the list of the most important tasks.

### clone

The task `clone` allows to clone a Git Repository at a given commit in a given location on the file system.

For example:

```yaml
- name: Clone the Fabric-X Orderer repository
  vars:
    git_uri: https://github.com/LF-Decentralized-Trust-labs/fabric-x-ansible-collection.git
    git_dir: .ansible/collections/ansible_collections/hyperledger/fabricx
    git_commit: latest
  ansible.builtin.include_role:
    name: hyperledger.fabricx.git
    tasks_from: clone
```
