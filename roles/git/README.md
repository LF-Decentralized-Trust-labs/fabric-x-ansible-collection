# hyperledger.fabricx.git

> Performs `git` operations on a node.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Lifecycle](#lifecycle)
    - [install](#install)
    - [clone](#clone)
- [Variables](#variables)

## Prerequisites

- `git` installed on the targeted node

## Tasks

### Lifecycle

| Task                            | Description             |
| ------------------------------- | ----------------------- |
| [install](./tasks/install.yaml) | Installs git            |
| [clone](./tasks/clone.yaml)     | Clones a Git repository |

#### install

Installs `git` on the targeted node:

```yaml
- name: Install git
  ansible.builtin.include_role:
    name: hyperledger.fabricx.git
    tasks_from: install
```

#### clone

Clones a Git repository at a given commit into a specified location:

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

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
