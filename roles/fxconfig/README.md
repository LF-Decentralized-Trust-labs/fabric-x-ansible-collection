# hyperledger.fabricx.fxconfig

The role `hyperledger.fabricx.fxconfig` can be used to run the `fxconfig` CLI utility needed to handle the namespaces lifecycle on Hyperledger Fabric-X.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [namespace/create](#namespacecreate)
  - [namespaces_create](#namespaces_create)
  - [namespace/list](#namespacelist)
  - [config/transfer](#configtransfer)
  - [wipe](#wipe)

## Prerequisites

The role requires:

- `go` to be installed if you plan to use it as binary through the `fxconfig_use_bin` variable.

## Tasks

### namespace/create

The task `namespace/create` creates a new namespace and assigns it the given public key used by the Fabric-X committer to verify the endorsement signatures:

```yaml
- name: Create the namespace "workload"
  vars:
    fxconfig_namespace_id: workload
    channel_id: arma
    orderer_router_host: orderer-router-1
    fxconfig_msp_id: Org1MSP
    fxconfig_msp_dir: ./meta_namespace/admin_msp
    fxconfig_pubkey_path: ./namespace/endorser_msp/signcerts/cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/create
```

### namespaces_create

The task `namespaces_create` creates multiple namespaces at once:

```yaml
- name: Create multiple namespaces
  vars:
    channel_id: arma
    orderer_router_host: orderer-router-1
    fxconfig_msp_id: Org1MSP
    fxconfig_msp_dir: ./meta_namespace/admin_msp
    fxconfig_namespaces:
      - namespace: workload
        pubkeys:
          - ./namespace/endorser_msp/signcerts/cert.pem
      - namespace: workload2
        pubkeys:
          - ./namespace/endorser2_msp/signcerts/cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespaces_create
```

### namespace/list

The task `namespace/list` lists all the namespaces currently created on a Fabric-X committer:

```yaml
- name: List the namespaces
  vars:
    committer_query_service_host: committer-query-service
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/list
```

### config/transfer

The task `config/transfer` transfers the MSP signing material, namespace endorsement public keys, and TLS certificates to the remote node so that `fxconfig` can authenticate its requests to the Fabric-X Orderer and Committer:

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

### wipe

The task `wipe` removes the `fxconfig` binary from the remote node (when `fxconfig_use_bin` is set):

```yaml
- name: Wipe fxconfig
  vars:
    fxconfig_use_bin: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: wipe
```
