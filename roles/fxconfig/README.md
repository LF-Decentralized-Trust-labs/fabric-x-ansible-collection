# hyperledger.fabricx.fxconfig

> Runs the `fxconfig` CLI utility for namespace lifecycle management on Fabric-X.

<!-- @depends_on: hyperledger.fabricx.cryptogen, hyperledger.fabricx.fabric_ca, hyperledger.fabricx.k8s -->

## Table of Contents <!-- omit in toc -->

- [Depends On](#depends-on)
- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Config](#config)
    - [config/transfer](#configtransfer)
  - [Lifecycle](#lifecycle)
    - [namespace_create](#namespace_create)
    - [namespaces_create](#namespaces_create)
    - [namespace_list](#namespace_list)
    - [wipe](#wipe)
- [Variables](#variables)

## Depends On

| Role                                                      | Reason                             |
| --------------------------------------------------------- | ---------------------------------- |
| [`hyperledger.fabricx.cryptogen`](../cryptogen/README.md) | Crypto material for authentication |
| [`hyperledger.fabricx.fabric_ca`](../fabric_ca/README.md) | Crypto material for authentication |
| [`hyperledger.fabricx.k8s`](../k8s/README.md)             | Namespace creation (k8s mode)      |

## Prerequisites

- `go` to be installed (when using binary mode)

## Tasks

### Config

| Task                                            | Description                                         |
| ----------------------------------------------- | --------------------------------------------------- |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers MSP signing material and TLS certificates |

#### config/transfer

Transfers MSP signing material, namespace endorsement public keys, and TLS certificates to the remote node so that `fxconfig` can authenticate its requests to the Fabric-X Orderer and Committer:

```yaml
- name: Transfer the fxconfig configuration material
  vars:
    fxconfig_msp_config_path: /tmp/meta-ns-admin/msp
    fxconfig_namespaces:
      - name: workload
        user:
          name: User1
          organization: "{{ hostvars[inventory_hostname].organization }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: config/transfer
```

### Lifecycle

| Task                                                | Description                 |
| --------------------------------------------------- | --------------------------- |
| [namespace_create](./tasks/namespace_create.yaml)   | Creates a new namespace     |
| [namespaces_create](./tasks/namespaces_create.yaml) | Creates multiple namespaces |
| [namespace_list](./tasks/namespace_list.yaml)       | Lists all namespaces        |
| [wipe](./tasks/wipe.yaml)                           | Removes fxconfig binary     |

#### namespace_create

Creates a new namespace and assigns it the given public key used by the Fabric-X committer to verify endorsement signatures:

```yaml
- name: Create the namespace "workload"
  vars:
    fxconfig_namespace: workload
    channel_id: arma
    orderer_router_host: orderer-router-1
    fxconfig_msp_id: Org1MSP
    fxconfig_msp_dir: ./meta_namespace_admin_msp
    fxconfig_pubkey_path: ./namespace_endorser_msp/signcerts/cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace_create
```

#### namespaces_create

Creates multiple namespaces at once:

```yaml
- name: Create multiple namespaces
  vars:
    channel_id: arma
    orderer_router_host: orderer-router-1
    fxconfig_msp_id: Org1MSP
    fxconfig_msp_dir: ./meta_namespace_admin_msp
    fxconfig_namespaces:
      - namespace: workload
        pubkeys:
          - ./namespace_endorser_msp/signcerts/cert.pem
      - namespace: workload2
        pubkeys:
          - ./namespace_endorser2_msp/signcerts/cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespaces_create
```

#### namespace_list

Lists all namespaces currently created on a Fabric-X committer:

```yaml
- name: List the namespaces
  vars:
    committer_query_service_host: committer-query-service
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace_list
```

#### wipe

Removes the `fxconfig` binary from the remote node (when `fxconfig_use_bin` is set):

```yaml
- name: Wipe fxconfig
  vars:
    fxconfig_use_bin: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: wipe
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
