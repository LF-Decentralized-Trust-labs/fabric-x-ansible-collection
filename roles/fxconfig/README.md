# hyperledger.fabricx.fxconfig

The role `hyperledger.fabricx.fxconfig` can be used to run the `fxconfig` CLI utility needed to handle the namespaces lifecycle on Hyperledger Fabric-X.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [namespace_create](#namespace_create)
  - [namespaces_create](#namespaces_create)
  - [namespace_list](#namespace_list)

## Prerequisites

The role requires:

- `go` to be installed if you plan to use it as binary through the `fxconfig_use_bin` variable.

## Tasks

### namespace_create

The task `namespace_create` creates a new namespace and assigns it the given public key used by the Fabric-X committer to verify the endorsement signatures:

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

### namespaces_create

The task `namespaces_create` creates multiple namespaces at once:

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

### namespace_list

The task `namespace_list` lists all the namespaces currently created on a Fabric-X committer:

```yaml
- name: List the namespaces
  vars:
    committer_query_service_host: committer-query-service
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace_create
```
