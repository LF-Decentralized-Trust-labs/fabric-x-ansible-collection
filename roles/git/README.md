# hyperledger.fabricx.git

The role `hyperledger.fabricx.git` can be used to perform `git` operations on a node.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [install](#install)
  - [clone](#clone)

## Prerequisites

The role requires `git` to be installed on the targeted node.

## Tasks

### install

The task `install` installs `git` on the targeted node:

```yaml
- name: Install git
  ansible.builtin.include_role:
    name: hyperledger.fabricx.git
    tasks_from: install
```

### clone

The task `clone` allows to clone a Git Repository at a given commit in a given location on the file system.

For example:

```yaml
- name: Clone the Fabric-X Orderer repository
  vars:
    git_hub_url: github.com
    git_repo: LF-Decentralized-Trust-labs/fabric-x-ansible-collection
    git_dir: .ansible/collections/ansible_collections/hyperledger/fabricx
    git_commit: latest
  ansible.builtin.include_role:
    name: hyperledger.fabricx.git
    tasks_from: clone
```

**Note**: The `git_hub_url` and `git_repo` are separated to allow the git role to internally handle URL construction with either HTTPS or SSH protocols. The `git_repo` should not include the domain or protocol (e.g., `LF-Decentralized-Trust-labs/fabric-x-ansible-collection` instead of `https://github.com/LF-Decentralized-Trust-labs/fabric-x-ansible-collection.git`).
