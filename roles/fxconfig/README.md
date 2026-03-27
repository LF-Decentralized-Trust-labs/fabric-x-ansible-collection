# hyperledger.fabricx.fxconfig

The role `hyperledger.fabricx.fxconfig` can be used to run the `fxconfig` CLI utility needed to handle the namespaces lifecycle on Hyperledger Fabric-X.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [namespace\_create](#namespace_create)
  - [namespaces\_create](#namespaces_create)
  - [namespace\_list](#namespace_list)
  - [config/transfer](#configtransfer)
  - [wipe](#wipe)

## Prerequisites

The role requires:

- `go` to be installed if you plan to use it as binary through the `fxconfig_use_bin` variable.

## Variables

| Variable                         | Default                                                  | Description                                                   |
| -------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| `fxconfig_registry_endpoint`     | `$FXCONFIG_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                   |
| `fxconfig_image_name`            | `fabric-x-tools`                                         | Container image name                                          |
| `fxconfig_image_tag`             | `0.0.8`                                                  | Container image tag                                           |
| `fxconfig_image`                 | `{{ registry }}/{{ name }}:{{ tag }}`                    | Full container image reference                                |
| `fxconfig_container_name`        | `fxconfig`                                               | Name given to the ephemeral container                         |
| `fxconfig_git_uri`               | `https://github.com/hyperledger/fabric-x.git`            | Git repository used to build the binary                       |
| `fxconfig_git_commit`            | `v0.0.8`                                                 | Git ref (tag or commit) to check out                          |
| `fxconfig_source_code_package`   | `tools/fxconfig`                                         | Go source package path within the repository                  |
| `fxconfig_bin_name`              | `fxconfig`                                               | Name of the produced binary                                   |
| `fxconfig_bin_package`           | `github.com/hyperledger/fabric-x/tools/fxconfig`         | Fully-qualified Go package used for `go install`              |
| `fxconfig_use_bin`               | `false`                                                  | Set to `true` to use the native binary instead of a container |
| `fxconfig_remote_config_dir`     | `{{ remote_config_dir }}/fxconfig`                       | Configuration directory on the remote node                    |
| `fxconfig_container_config_dir`  | `/tmp`                                                   | Configuration directory inside the container                  |
| `fxconfig_use_tls`               | `false`                                                  | Enable TLS when communicating with the Orderer/Committer      |
| `fxconfig_mtls_client_cert_path` | `{{ remote_config_dir }}/tls/server.crt`                 | mTLS client certificate path                                  |
| `fxconfig_mtls_client_key_path`  | `{{ remote_config_dir }}/tls/server.key`                 | mTLS client private key path                                  |
| `fxconfig_msp_id`                | `{{ organization.name }}MSP`                             | MSP ID used to authenticate requests                          |

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
    tasks_from: namespace_list
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
