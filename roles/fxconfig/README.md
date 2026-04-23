# hyperledger.fabricx.fxconfig

> Runs the `fxconfig` CLI utility for namespace lifecycle management on Fabric-X.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [bin/build](#binbuild)
  - [bin/endorse](#binendorse)
  - [bin/install](#bininstall)
  - [bin/merge](#binmerge)
  - [bin/namespace/create](#binnamespacecreate)
  - [bin/namespace/list](#binnamespacelist)
  - [bin/rm](#binrm)
  - [bin/submit](#binsubmit)
  - [bin/transfer](#bintransfer)
  - [config/mtls/transfer](#configmtlstransfer)
  - [config/tls/transfer](#configtlstransfer)
  - [config/transfer](#configtransfer)
  - [container/endorse](#containerendorse)
  - [container/merge](#containermerge)
  - [container/namespace/create](#containernamespacecreate)
  - [container/namespace/list](#containernamespacelist)
  - [container/submit](#containersubmit)
  - [endorse](#endorse)
  - [get_endorser](#get_endorser)
  - [merge](#merge)
  - [namespace/create](#namespacecreate)
  - [namespace/group](#namespacegroup)
  - [namespace/list](#namespacelist)
  - [submit](#submit)
  - [wipe](#wipe)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### bin/build

Build the fxconfig binary

Builds the fxconfig Go binary by delegating compilation to the shared bin role.

```yaml
- name: Build the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Selects the Git ref used by build and install workflows. Example: `v0.0.12`.
    fxconfig_git_commit: v0.0.12
    # Defines the Git host used to resolve the Fabric-X source repository. Example: `github.com`.
    fxconfig_git_hub_url: github.com
    # Defines the Fabric-X source repository path. Example: `hyperledger/fabric-x`.
    fxconfig_git_repo: hyperledger/fabric-x
    # Defines the Go package path containing the fxconfig source code. Example: `tools/fxconfig`.
    fxconfig_source_code_package: tools/fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/build
```

### bin/endorse

Endorse a namespace transaction with the fxconfig binary

Copies a transaction to the target host, endorses it with the local fxconfig binary, and fetches the endorsed JSON artifact.

```yaml
- name: Endorse a namespace transaction with the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the JSON transaction file to endorse. Example: `/tmp/fxconfig-artifacts/workload/ns.json`.
    fxconfig_tx_to_endorse: "string"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/endorse
```

### bin/install

Install the fxconfig binary

Installs the fxconfig Go package by delegating to the shared bin role.

```yaml
- name: Install the fxconfig binary
  vars:
    # Defines the Go package path used to install fxconfig. The default derives from `fxconfig_git_hub_url`, `fxconfig_git_repo`, and `fxconfig_source_code_package`.
    fxconfig_bin_package: "{{ fxconfig_git_hub_url }}/{{ fxconfig_git_repo }}/{{ fxconfig_source_code_package }}"
    # Selects the Git ref used by build and install workflows. Example: `v0.0.12`.
    fxconfig_git_commit: v0.0.12
    # Defines the Git host used to resolve the Fabric-X source repository. Example: `github.com`.
    fxconfig_git_hub_url: github.com
    # Defines the Fabric-X source repository path. Example: `hyperledger/fabric-x`.
    fxconfig_git_repo: hyperledger/fabric-x
    # Defines the Go package path containing the fxconfig source code. Example: `tools/fxconfig`.
    fxconfig_source_code_package: tools/fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/install
```

### bin/merge

Merge endorsed transactions with the fxconfig binary

Collects endorsed transaction files and merges them into a single transaction using the local fxconfig binary.

```yaml
- name: Merge endorsed transactions with the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the directory containing endorsed JSON transactions. Example: `/tmp/fxconfig-artifacts/workload/endorsed`.
    fxconfig_endorsed_txs_dir: "string"
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/merge
```

### bin/namespace/create

Create a namespace transaction with the fxconfig binary

Creates a namespace transaction JSON file with the local fxconfig binary.

```yaml
- name: Create a namespace transaction with the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the namespace identifier. Accepts either a string or an integer value. Examples: `workload`, `0`.
    fxconfig_namespace_id: "string"
    # Defines the namespace endorsement policy. Example: `threshold:/tmp/pubkey.pem`.
    fxconfig_namespace_policy: "string"
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/namespace/create
```

### bin/namespace/list

List namespaces with the fxconfig binary

Lists namespaces from the configured Fabric-X network by invoking the local fxconfig binary.

```yaml
- name: List namespaces with the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/namespace/list
```

### bin/rm

Remove the fxconfig binary

Removes the fxconfig binary from the managed host by delegating to the shared bin role.

```yaml
- name: Remove the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/rm
```

### bin/submit

Submit a namespace transaction with the fxconfig binary

Transfers a merged transaction to the managed host and submits it with the local fxconfig binary.

```yaml
- name: Submit a namespace transaction with the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the merged JSON transaction file to submit. Example: `/tmp/fxconfig-artifacts/workload/merged.json`.
    fxconfig_tx_to_submit_path: "string"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/submit
```

### bin/transfer

Transfer the fxconfig binary

Transfers the fxconfig binary to the managed host by delegating to the shared bin role.

```yaml
- name: Transfer the fxconfig binary
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/transfer
```

### config/mtls/transfer

Transfer fxconfig mTLS client material

Copies the client certificate and key used by fxconfig for mTLS connections into the role-specific configuration directory.

```yaml
- name: Transfer fxconfig mTLS client material
  vars:
    # Defines the source certificate path used for fxconfig mTLS. The default derives from `remote_config_dir`.
    fxconfig_mtls_client_cert_path: "{{ remote_config_dir }}/tls/server.crt"
    # Defines the source private key path used for fxconfig mTLS. The default derives from `remote_config_dir`.
    fxconfig_mtls_client_key_path: "{{ remote_config_dir }}/tls/server.key"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: config/mtls/transfer
```

### config/tls/transfer

Transfer fxconfig TLS trust material

Copies the Orderer Router and Committer Query-Service CA certificates required by the rendered fxconfig configuration.

Inventory hosts named by the gating variables must expose connection metadata, RPC ports, and TLS flags.

```yaml
- name: Transfer fxconfig TLS trust material
  vars:
    # Identifies the inventory host for the Committer Query-Service component. Example: `committer-query-service-1`.
    committer_query_service_host: "string"
    # Defines the local directory that stores fetched artifacts. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "string"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Identifies the inventory host for the Orderer Router component. Example: `orderer-router-1`.
    orderer_router_host: "string"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: config/tls/transfer
```

### config/transfer

Transfer fxconfig configuration material

Renders the fxconfig configuration file, copies MSP material, and stages TLS and mTLS assets when the inventory enables them.

Inventory hosts named by the routing variables must expose connection metadata, RPC ports, and TLS or mTLS flags.

```yaml
- name: Transfer fxconfig configuration material
  vars:
    # Defines the Fabric-X channel used by the task. Example: `arma`.
    channel_id: "string"
    # Defines the query-service connection timeout. Example: `30s`.
    fxconfig_committer_query_service_connection_timeout: 30s
    # Identifies the inventory host for the Committer Query-Service component. Example: `committer-query-service-1`.
    committer_query_service_host: "string"
    # Defines the sidecar connection timeout. Example: `30s`.
    fxconfig_committer_sidecar_connection_timeout: 30s
    # Identifies the inventory host for the Committer Sidecar component. Example: `committer-sidecar-1`.
    committer_sidecar_host: "string"
    # Defines the sidecar waiting timeout. Example: `30s`.
    fxconfig_committer_sidecar_waiting_timeout: 30s
    # Defines the local directory that stores fetched artifacts. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "string"
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the source MSP directory copied into the fxconfig configuration directory. Example: `/opt/hlf/config/users/User1@example.com/msp`.
    fxconfig_msp_config_path: "string"
    # Defines the MSP identifier written into the rendered configuration. The default derives from `organization.name`.
    fxconfig_msp_id: "{{ organization.name }}MSP"
    # Defines the source certificate path used for fxconfig mTLS. The default derives from `remote_config_dir`.
    fxconfig_mtls_client_cert_path: "{{ remote_config_dir }}/tls/server.crt"
    # Defines the source private key path used for fxconfig mTLS. The default derives from `remote_config_dir`.
    fxconfig_mtls_client_key_path: "{{ remote_config_dir }}/tls/server.key"
    # Defines the orderer connection timeout written into the rendered configuration. Example: `30s`.
    fxconfig_orderer_connection_timeout: 30s
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Identifies the inventory host for the Orderer Router component. Example: `orderer-router-1`.
    orderer_router_host: "string"
    # Provides organization metadata required by tasks that read `organization.*`.
    organization: {}
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: config/transfer
```

### container/endorse

Endorse a namespace transaction with the fxconfig container

Copies a transaction to the target host, endorses it with a transient fxconfig container, and fetches the endorsed JSON artifact.

```yaml
- name: Endorse a namespace transaction with the fxconfig container
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the JSON transaction file to endorse. Example: `/tmp/fxconfig-artifacts/workload/ns.json`.
    fxconfig_tx_to_endorse: "string"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/endorse
```

### container/merge

Merge endorsed transactions with the fxconfig container

Collects endorsed transactions and merges them into a single artifact by running fxconfig in a transient container.

```yaml
- name: Merge endorsed transactions with the fxconfig container
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the directory containing endorsed JSON transactions. Example: `/tmp/fxconfig-artifacts/workload/endorsed`.
    fxconfig_endorsed_txs_dir: "string"
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/merge
```

### container/namespace/create

Create a namespace transaction with the fxconfig container

Creates a namespace transaction JSON file by running fxconfig in a transient container.

```yaml
- name: Create a namespace transaction with the fxconfig container
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the namespace identifier. Accepts either a string or an integer value. Examples: `workload`, `0`.
    fxconfig_namespace_id: "string"
    # Defines the namespace endorsement policy. Example: `threshold:/tmp/pubkey.pem`.
    fxconfig_namespace_policy: "string"
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/namespace/create
```

### container/namespace/list

List namespaces with the fxconfig container

Lists namespaces from the configured Fabric-X network by running fxconfig in a transient container.

```yaml
- name: List namespaces with the fxconfig container
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/namespace/list
```

### container/submit

Submit a namespace transaction with the fxconfig container

Transfers a merged transaction to the managed host and submits it by running fxconfig in a transient container.

```yaml
- name: Submit a namespace transaction with the fxconfig container
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the merged JSON transaction file to submit. Example: `/tmp/fxconfig-artifacts/workload/merged.json`.
    fxconfig_tx_to_submit_path: "string"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/submit
```

### endorse

Endorse a namespace transaction

Dispatches transaction endorsement to either the host binary or a transient container based on `fxconfig_use_bin`.

```yaml
- name: Endorse a namespace transaction
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the JSON transaction file to endorse. Example: `/tmp/fxconfig-artifacts/workload/ns.json`.
    fxconfig_tx_to_endorse: "string"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: endorse
```

### get_endorser

Resolve the namespace endorser user

Selects the preferred endorser from `organization.users` and stores it in `fxconfig_endorser_user`.

```yaml
- name: Resolve the namespace endorser user
  vars:
    # Provides organization metadata required by tasks that read `organization.*`.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: get_endorser
```

### merge

Merge endorsed namespace transactions

Dispatches merge operations to either the host binary or a transient container based on `fxconfig_use_bin`.

```yaml
- name: Merge endorsed namespace transactions
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the directory containing endorsed JSON transactions. Example: `/tmp/fxconfig-artifacts/workload/endorsed`.
    fxconfig_endorsed_txs_dir: "string"
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: merge
```

### namespace/create

Create a namespace transaction

Dispatches namespace transaction creation to either the host binary or a transient container based on `fxconfig_use_bin`.

```yaml
- name: Create a namespace transaction
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the namespace identifier. Accepts either a string or an integer value. Examples: `workload`, `0`.
    fxconfig_namespace_id: "string"
    # Defines the namespace endorsement policy. Example: `threshold:/tmp/pubkey.pem`.
    fxconfig_namespace_policy: "string"
    # Defines the transaction artifact path on the managed host. The default derives from `fxconfig_remote_config_dir`.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/create
```

### namespace/group

Group hosts by declared namespaces

Builds a namespace-to-host mapping from inventory organization data.

Inventory hosts selected via `fxconfig_hosts` must define the organization data expected by the helper.

```yaml
- name: Group hosts by declared namespaces
  vars:
    # Defines the local directory that stores fetched artifacts. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "string"
    # Limits namespace grouping to a subset of inventory hosts. If omitted, the task considers all hosts. Selected hosts must expose the organization metadata expected by the namespace grouping helper.
    fxconfig_hosts: ["entry1", "entry2"]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/group
```

### namespace/list

List namespaces

Dispatches namespace listing to either the host binary or a transient container based on `fxconfig_use_bin`.

```yaml
- name: List namespaces
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level. Example: `info`.
    fxconfig_log_level: info
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/list
```

### submit

Submit a namespace transaction

Dispatches merged transaction submission to either the host binary or a transient container based on `fxconfig_use_bin`.

```yaml
- name: Submit a namespace transaction
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename. Example: `fxconfig.yaml`.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container. Example: `/config`.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows. Example: `fxconfig`.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image. The default derives from `fxconfig_registry_endpoint`, `fxconfig_image_name`, and `fxconfig_image_tag`.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the default fxconfig container image. Example: `fabric-x-tools`.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the default fxconfig container image. Example: `0.0.12`.
    fxconfig_image_tag: 0.0.12
    # Defines the registry endpoint used by the default fxconfig container image. Example: `docker.io/hyperledger`.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory. The default derives from `remote_config_dir`.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the merged JSON transaction file to submit. Example: `/tmp/fxconfig-artifacts/workload/merged.json`.
    fxconfig_tx_to_submit_path: "string"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hlf/config`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: submit
```

### wipe

Remove fxconfig binaries when enabled

Removes the fxconfig binary from the managed host when the binary workflow is enabled.

```yaml
- name: Remove fxconfig binaries when enabled
  vars:
    # Defines the fxconfig binary name. Example: `fxconfig`.
    fxconfig_bin_name: fxconfig
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: wipe
```
