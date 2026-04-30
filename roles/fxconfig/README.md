# hyperledger.fabricx.fxconfig

> Generates and transfers fxconfig configuration material, manages namespace transaction artifacts, and submits Fabric-X namespace lifecycle changes.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
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
  - [get\_endorser](#get_endorser)
  - [merge](#merge)
  - [namespace/create](#namespacecreate)
  - [namespace/group](#namespacegroup)
  - [namespace/list](#namespacelist)
  - [submit](#submit)
  - [wipe](#wipe)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.fxconfig
```

## Tasks

### bin/build

> Build the fxconfig binary

Builds the fxconfig Go binary from the configured Fabric-X source package by delegating compilation to the shared bin role.

```yaml
- name: Build the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Selects the Git ref used by build and install workflows.
    fxconfig_git_commit: v0.0.12
    # Defines the Git host used to resolve the Fabric-X source repository.
    fxconfig_git_hub_url: github.com
    # Defines the Fabric-X source repository path.
    fxconfig_git_repo: hyperledger/fabric-x
    # Defines the Go package path containing the fxconfig source code.
    fxconfig_source_code_package: tools/fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/build
```

### bin/endorse

> Endorse a namespace transaction with the fxconfig binary

Copies a namespace transaction JSON file to the managed host, endorses it with the local fxconfig binary and rendered configuration, then fetches the endorsed JSON artifact into the source artifact tree.

```yaml
- name: Endorse a namespace transaction with the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the local namespace transaction JSON file to endorse. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/payments/ns.json`.
    fxconfig_tx_to_endorse: "/tmp/fabricx/config-build/fxconfig-artifacts/payments/ns.json"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/endorse
```

### bin/install

> Install the fxconfig binary

Installs the fxconfig Go package from the configured Fabric-X source package by delegating to the shared bin role.

```yaml
- name: Install the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the Go package path used to install fxconfig.
    fxconfig_bin_package: "{{ fxconfig_git_hub_url }}/{{ fxconfig_git_repo }}/{{ fxconfig_source_code_package }}"
    # Selects the Git ref used by build and install workflows.
    fxconfig_git_commit: v0.0.12
    # Defines the Git host used to resolve the Fabric-X source repository.
    fxconfig_git_hub_url: github.com
    # Defines the Fabric-X source repository path.
    fxconfig_git_repo: hyperledger/fabric-x
    # Defines the Go package path containing the fxconfig source code.
    fxconfig_source_code_package: tools/fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/install
```

### bin/merge

> Merge endorsed transactions with the fxconfig binary

Collects endorsed namespace transaction JSON files from the artifact directory and writes a merged transaction using the local fxconfig binary.

```yaml
- name: Merge endorsed transactions with the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the local directory containing endorsed namespace transaction JSON files to merge. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/mychannel/endorsed`.
    fxconfig_endorsed_txs_dir: "/tmp/fabricx/config-build/fxconfig-artifacts/mychannel/endorsed"
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/merge
```

### bin/namespace/create

> Create a namespace transaction with the fxconfig binary

Creates a namespace transaction JSON artifact for the configured namespace and endorsement policy with the local fxconfig binary.

```yaml
- name: Create a namespace transaction with the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the namespace identifier used when creating namespace transaction artifacts. Accepts either a string or an integer value. Example: `payments`.
    fxconfig_namespace_id: payments
    # Defines the namespace endorsement policy. Example: `threshold:/tmp/fabricx/config-build/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem`.
    fxconfig_namespace_policy: "threshold:/tmp/fabricx/config-build/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem"
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/namespace/create
```

### bin/namespace/list

> List namespaces with the fxconfig binary

Lists namespaces from the configured Fabric-X network by invoking the local fxconfig binary with the rendered fxconfig file.

```yaml
- name: List namespaces with the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/namespace/list
```

### bin/rm

> Remove the fxconfig binary

Removes the fxconfig binary from the managed host by delegating cleanup to the shared bin role.

```yaml
- name: Remove the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/rm
```

### bin/submit

> Submit a namespace transaction with the fxconfig binary

Transfers a merged namespace transaction JSON artifact to the managed host and submits it with the local fxconfig binary and rendered configuration.

```yaml
- name: Submit a namespace transaction with the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the local merged namespace transaction JSON file to submit. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/payments/merged.json`.
    fxconfig_tx_to_submit_path: "/tmp/fabricx/config-build/fxconfig-artifacts/payments/merged.json"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/submit
```

### bin/transfer

> Transfer the fxconfig binary

Transfers the previously built fxconfig binary to the managed host by delegating to the shared bin role.

```yaml
- name: Transfer the fxconfig binary
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: bin/transfer
```

### config/mtls/transfer

> Transfer fxconfig mTLS client material

Copies the client certificate and key consumed by fxconfig for mTLS connections into `fxconfig_remote_config_dir`/mtls.

```yaml
- name: Transfer fxconfig mTLS client material
  vars:
    # Defines the source certificate path used for fxconfig mTLS.
    fxconfig_mtls_client_cert_path: "{{ remote_config_dir }}/tls/server.crt"
    # Defines the source private key path used for fxconfig mTLS.
    fxconfig_mtls_client_key_path: "{{ remote_config_dir }}/tls/server.key"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: config/mtls/transfer
```

### config/tls/transfer

> Transfer fxconfig TLS trust material

Copies fetched Orderer Router and Committer Query-Service CA certificates into the fxconfig TLS trust directories consumed by the rendered configuration. Inventory hosts named by the endpoint variables must expose connection metadata, RPC ports, and TLS flags.

```yaml
- name: Transfer fxconfig TLS trust material
  vars:
    # Identifies the inventory host for the Committer Query-Service endpoint consumed by fxconfig. Example: `committer-query-service`.
    committer_query_service_host: "committer-query-service"
    # Defines the local directory that stores fetched crypto and TLS artifacts consumed by fxconfig. Example: `/tmp/fabricx/config-build`.
    fetched_artifacts_dir: "/tmp/fabricx/config-build"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Identifies the inventory host for the Orderer Router endpoint consumed by fxconfig. Example: `orderer-router-1`.
    orderer_router_host: "orderer-router-1"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: config/tls/transfer
```

### config/transfer

> Transfer fxconfig configuration material

Creates the remote fxconfig configuration directory, renders the fxconfig file, copies MSP material, and stages TLS or mTLS assets when the inventory enables them. For k8s deployments that expose NodePorts, writes NodePort addresses from the Orderer Router, Committer Sidecar, and Committer Query-Service hostvars; otherwise writes the component RPC addresses. Consumes fetched TLS artifacts, MSP directories, channel identifiers, endpoint hosts, RPC ports, and optional timeout values.

```yaml
- name: Transfer fxconfig configuration material
  vars:
    # Defines the Fabric-X channel written into the rendered fxconfig file. Example: `mychannel`.
    channel_id: "mychannel"
    # Defines the Committer Query-Service connection timeout written into the rendered fxconfig file. Example: `45s`.
    fxconfig_committer_query_service_connection_timeout: "45s"
    # Identifies the inventory host for the Committer Query-Service endpoint consumed by fxconfig. Example: `committer-query-service`.
    committer_query_service_host: "committer-query-service"
    # Defines the Committer Sidecar notification connection timeout written into the rendered fxconfig file. Example: `45s`.
    fxconfig_committer_sidecar_connection_timeout: "45s"
    # Identifies the inventory host for the Committer Sidecar notification endpoint consumed by fxconfig. Example: `committer-sidecar`.
    committer_sidecar_host: "committer-sidecar"
    # Defines the Committer Sidecar notification waiting timeout written into the rendered fxconfig file. Example: `2m`.
    fxconfig_committer_sidecar_waiting_timeout: "2m"
    # Defines the local directory that stores fetched crypto and TLS artifacts consumed by fxconfig. Example: `/tmp/fabricx/config-build`.
    fetched_artifacts_dir: "/tmp/fabricx/config-build"
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the source MSP directory copied into the fxconfig configuration directory. Example: `/opt/hyperledger/fabricx/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp`.
    fxconfig_msp_config_path: "/opt/hyperledger/fabricx/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp"
    # Defines the MSP identifier written into the rendered configuration.
    fxconfig_msp_id: "{{ organization.name }}MSP"
    # Defines the source certificate path used for fxconfig mTLS.
    fxconfig_mtls_client_cert_path: "{{ remote_config_dir }}/tls/server.crt"
    # Defines the source private key path used for fxconfig mTLS.
    fxconfig_mtls_client_key_path: "{{ remote_config_dir }}/tls/server.key"
    # Defines the Orderer Router connection timeout written into the rendered fxconfig file. Example: `45s`.
    fxconfig_orderer_connection_timeout: "45s"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Identifies the inventory host for the Orderer Router endpoint consumed by fxconfig. Example: `orderer-router-1`.
    orderer_router_host: "orderer-router-1"
    # Provides organization metadata when `fxconfig_msp_id` is not supplied directly. Example: `{'name': 'Org1', 'domain': 'org1.example.com'}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: config/transfer
```

### container/endorse

> Endorse a namespace transaction with the fxconfig container

Copies a namespace transaction JSON file to the managed host, mounts the rendered configuration into a transient fxconfig container, and fetches the endorsed JSON artifact into the source artifact tree.

```yaml
- name: Endorse a namespace transaction with the fxconfig container
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the local namespace transaction JSON file to endorse. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/payments/ns.json`.
    fxconfig_tx_to_endorse: "/tmp/fabricx/config-build/fxconfig-artifacts/payments/ns.json"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/endorse
```

### container/merge

> Merge endorsed transactions with the fxconfig container

Collects endorsed namespace transaction JSON files from the artifact directory, mounts them into a transient fxconfig container, and writes a merged transaction artifact.

```yaml
- name: Merge endorsed transactions with the fxconfig container
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the local directory containing endorsed namespace transaction JSON files to merge. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/mychannel/endorsed`.
    fxconfig_endorsed_txs_dir: "/tmp/fabricx/config-build/fxconfig-artifacts/mychannel/endorsed"
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/merge
```

### container/namespace/create

> Create a namespace transaction with the fxconfig container

Creates a namespace transaction JSON artifact for the configured namespace and endorsement policy by running fxconfig in a transient container. For threshold policies, mounts the referenced signing certificate into the container and rewrites the policy path for container execution.

```yaml
- name: Create a namespace transaction with the fxconfig container
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the namespace identifier used when creating namespace transaction artifacts. Accepts either a string or an integer value. Example: `payments`.
    fxconfig_namespace_id: payments
    # Defines the namespace endorsement policy. Example: `threshold:/tmp/fabricx/config-build/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem`.
    fxconfig_namespace_policy: "threshold:/tmp/fabricx/config-build/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem"
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/namespace/create
```

### container/namespace/list

> List namespaces with the fxconfig container

Lists namespaces from the configured Fabric-X network by mounting the rendered configuration into a transient fxconfig container.

```yaml
- name: List namespaces with the fxconfig container
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/namespace/list
```

### container/submit

> Submit a namespace transaction with the fxconfig container

Transfers a merged namespace transaction JSON artifact to the managed host, mounts the fxconfig configuration directory, and submits it from a transient container.

```yaml
- name: Submit a namespace transaction with the fxconfig container
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the local merged namespace transaction JSON file to submit. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/payments/merged.json`.
    fxconfig_tx_to_submit_path: "/tmp/fabricx/config-build/fxconfig-artifacts/payments/merged.json"
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: container/submit
```

### endorse

> Endorse a namespace transaction

Dispatches namespace transaction endorsement to either the host binary or a transient container based on `fxconfig_use_bin`. Consumes a namespace transaction JSON artifact and the rendered fxconfig configuration, then fetches the endorsed artifact.

```yaml
- name: Endorse a namespace transaction
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the local namespace transaction JSON file to endorse. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/payments/ns.json`.
    fxconfig_tx_to_endorse: "/tmp/fabricx/config-build/fxconfig-artifacts/payments/ns.json"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: endorse
```

### get_endorser

> Resolve the namespace endorser user

Selects the preferred endorser from `organization.users` for namespace transaction endorsement and stores it in `fxconfig_endorser_user`.

```yaml
- name: Resolve the namespace endorser user
  vars:
    # Provides organization metadata required by tasks that read `organization.*`, including names, users, domains, and namespace declarations. Example: `{'name': 'Org1', 'domain': 'org1.example.com'}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: get_endorser
```

### merge

> Merge endorsed namespace transactions

Dispatches endorsed namespace transaction merging to either the host binary or a transient container based on `fxconfig_use_bin`. Consumes endorsed JSON artifacts and writes the merged transaction artifact used by submission.

```yaml
- name: Merge endorsed namespace transactions
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the local directory containing endorsed namespace transaction JSON files to merge. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/mychannel/endorsed`.
    fxconfig_endorsed_txs_dir: "/tmp/fabricx/config-build/fxconfig-artifacts/mychannel/endorsed"
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: merge
```

### namespace/create

> Create a namespace transaction

Dispatches namespace transaction creation to either the host binary or a transient container based on `fxconfig_use_bin`. Writes a namespace transaction JSON artifact for the configured namespace identifier and endorsement policy.

```yaml
- name: Create a namespace transaction
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the namespace identifier used when creating namespace transaction artifacts. Accepts either a string or an integer value. Example: `payments`.
    fxconfig_namespace_id: payments
    # Defines the namespace endorsement policy. Example: `threshold:/tmp/fabricx/config-build/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem`.
    fxconfig_namespace_policy: "threshold:/tmp/fabricx/config-build/crypto/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem"
    # Defines the transaction artifact path on the managed host.
    fxconfig_output: "{{ fxconfig_remote_config_dir }}/tx.json"
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/create
```

### namespace/group

> Group hosts by declared namespaces

Builds a namespace-to-host mapping from inventory organization data before creating, endorsing, merging, and submitting namespace transactions. For threshold policies, resolves the signing certificate path under the fetched crypto artifact directory. Inventory hosts selected via `fxconfig_hosts` must define organization namespace data.

```yaml
- name: Group hosts by declared namespaces
  vars:
    # Defines the local directory that stores fetched crypto and TLS artifacts consumed by fxconfig. Example: `/tmp/fabricx/config-build`.
    fetched_artifacts_dir: "/tmp/fabricx/config-build"
    # Limits namespace grouping to a subset of inventory hosts. If omitted, the task considers all hosts. Example: `['committer-sidecar', 'committer-query-service']`. Selected hosts must expose the organization metadata expected by the namespace grouping helper.
    fxconfig_hosts:
      - "committer-sidecar"
      - "committer-query-service"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/group
```

### namespace/list

> List namespaces

Dispatches namespace listing to either the host binary or a transient container based on `fxconfig_use_bin`. Consumes the rendered fxconfig configuration that points at the Orderer Router and Committer services.

```yaml
- name: List namespaces
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the fxconfig log format.
    fxconfig_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s} %{id:03x}%{color:reset} %{message}"
    # Defines the fxconfig log level.
    fxconfig_log_level: info
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: namespace/list
```

### submit

> Submit a namespace transaction

Dispatches merged namespace transaction submission to either the host binary or a transient container based on `fxconfig_use_bin`. Consumes the merged JSON artifact and rendered fxconfig configuration, then waits for submission completion.

```yaml
- name: Submit a namespace transaction
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Defines the fxconfig configuration filename.
    fxconfig_config_file: fxconfig.yaml
    # Defines the configuration directory mounted inside the fxconfig container.
    fxconfig_container_config_dir: /config
    # Defines the base container name used by fxconfig workflows.
    fxconfig_container_name: fxconfig
    # Defines the fxconfig container image.
    fxconfig_image: "{{ fxconfig_registry_endpoint }}/{{ fxconfig_image_name }}:{{ fxconfig_image_tag }}"
    # Defines the image name used by the fxconfig container image.
    fxconfig_image_name: fabric-x-tools
    # Defines the image tag used by the fxconfig container image.
    fxconfig_image_tag: 0.0.12
    # Defines the registry endpoint used by the fxconfig container image.
    fxconfig_registry_endpoint: "{{ lookup('env', 'FXCONFIG_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxconfig remote configuration directory.
    fxconfig_remote_config_dir: "{{ remote_config_dir }}/fxconfig"
    # Supplies the local merged namespace transaction JSON file to submit. Example: `/tmp/fabricx/config-build/fxconfig-artifacts/payments/merged.json`.
    fxconfig_tx_to_submit_path: "/tmp/fabricx/config-build/fxconfig-artifacts/payments/merged.json"
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
    # Provides the base remote configuration directory used by the role. Example: `/opt/hyperledger/fabricx/config`.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: submit
```

### wipe

> Remove fxconfig binaries when enabled

Removes the fxconfig binary from the managed host when the binary workflow is enabled; container workflows have no role-local binary to remove.

```yaml
- name: Remove fxconfig binaries when enabled
  vars:
    # Defines the fxconfig binary name.
    fxconfig_bin_name: fxconfig
    # Selects the host-binary workflow instead of the container workflow.
    fxconfig_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxconfig
    tasks_from: wipe
```
