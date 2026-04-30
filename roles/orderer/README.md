# hyperledger.fabricx.orderer

> Manages Fabric-X Orderer consenter, batcher, assembler, and router components across binary, container, and Kubernetes deployments.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)
  - [get\_metrics](#get_metrics)
  - [bin/build](#binbuild)
  - [bin/install](#bininstall)
  - [bin/transfer](#bintransfer)
  - [bin/rm](#binrm)
  - [bin/start](#binstart)
  - [bin/stop](#binstop)
  - [bin/fetch\_logs](#binfetch_logs)
  - [bin/teardown](#binteardown)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [container/teardown](#containerteardown)
  - [data/rm](#datarm)
  - [config/transfer](#configtransfer)
  - [config/mtls/transfer](#configmtlstransfer)
  - [config/rm](#configrm)
  - [config/transfer\_grafana\_dashboard](#configtransfer_grafana_dashboard)
  - [crypto/setup](#cryptosetup)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric\_ca/enroll](#cryptofabric_caenroll)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/teardown](#k8steardown)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)
  - [prometheus/get\_scrapers](#prometheusget_scrapers)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.orderer
```

## Tasks

### start

> Dispatch orderer startup by component and deployment mode

Dispatches `consensus`, `batcher`, `assembler`, or `router` startup to the selected `bin`, `container`, or `k8s` implementation. Consumes configuration, crypto, genesis, and TLS material prepared by the config and crypto entrypoints.

```yaml
- name: Dispatch orderer startup by component and deployment mode
  vars:
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Deployment backend selected by the top-level dispatcher.
    orderer_deployment_mode: "{%- if orderer_use_bin -%}bin{%- elif orderer_use_k8s -%}k8s{%- else -%}container{%- endif -%}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: start
```

### stop

> Dispatch orderer shutdown by component and deployment mode

Dispatches component shutdown to the active binary, container, or Kubernetes lifecycle implementation. Stops the running orderer process or workload without removing generated config, crypto, genesis, or data artifacts.

```yaml
- name: Dispatch orderer shutdown by component and deployment mode
  vars:
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Deployment backend selected by the top-level dispatcher.
    orderer_deployment_mode: "{%- if orderer_use_bin -%}bin{%- elif orderer_use_k8s -%}k8s{%- else -%}container{%- endif -%}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: stop
```

### teardown

> Dispatch orderer teardown by component and deployment mode

Dispatches component teardown to the selected deployment backend. Removes runtime resources for the consenter, batcher, assembler, or router while leaving reusable generated config and crypto cleanup to dedicated entrypoints.

```yaml
- name: Dispatch orderer teardown by component and deployment mode
  vars:
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Deployment backend selected by the top-level dispatcher.
    orderer_deployment_mode: "{%- if orderer_use_bin -%}bin{%- elif orderer_use_k8s -%}k8s{%- else -%}container{%- endif -%}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: teardown
```

### wipe

> Remove orderer runtime state, config, and optional binary

Runs lifecycle teardown, removes generated orderer configuration and MSP/TLS material, and removes the installed binary when binary mode is selected. Use for a full role-local reset after generated artifacts have been fetched or are no longer needed.

```yaml
- name: Remove orderer runtime state, config, and optional binary
  vars:
    # Selects the binary deployment branch.
    orderer_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: wipe
```

### fetch_logs

> Fetch orderer logs from the active deployment backend

Delegates log collection to the Kubernetes pod selector, container name, or binary process implementation according to the enabled deployment mode. Collects runtime logs for any orderer component without modifying config, crypto, or data artifacts.

```yaml
- name: Fetch orderer logs from the active deployment backend
  vars:
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
    # Selects the container deployment branch.
    orderer_use_container: "{{ (not orderer_use_bin) and (not orderer_use_k8s) }}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: fetch_logs
```

### ping

> Check the orderer gRPC port

Checks the configured orderer gRPC listener for binary and container deployments. When Kubernetes mode is active, delegates to the NodePort ping branch so exposed Service ports can be checked from the control node.

```yaml
- name: Check the orderer gRPC port
  vars:
    # gRPC port exposed by the orderer. Example: `7050`.
    orderer_rpc_port: 7050
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: ping
```

### get_metrics

> Retrieve orderer Prometheus metrics

Fetches Prometheus metrics from the configured orderer monitoring endpoint using the selected HTTP protocol. Consumes the metrics listener written into the generated orderer config.

```yaml
- name: Retrieve orderer Prometheus metrics
  vars:
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Protocol used by the metrics fetch branch.
    orderer_http_protocol: http
    # Metrics port queried by the metrics fetch branch. Example: `9445`.
    orderer_metrics_port: 9445
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: get_metrics
```

### bin/build

> Build the orderer binary from source

Builds the orderer binary through the shared bin role using the configured Git repository, ref, and Go package path. Produces a binary that can be transferred and started for consenter, batcher, assembler, or router component modes.

```yaml
- name: Build the orderer binary from source
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
    # Git host used to resolve the orderer source repository.
    orderer_git_hub_url: github.com
    # Repository path for the orderer source code.
    orderer_git_repo: hyperledger/fabric-x-orderer
    # Git ref or release tag used by the bin build and install branches.
    orderer_git_commit: v0.0.23
    # Go package path that builds the orderer binary.
    orderer_source_code_package: cmd/arma
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/build
```

### bin/install

> Install the published orderer binary

Installs the configured released orderer binary through the shared bin role. Uses the Git host, repository, package path, and ref metadata to resolve the published binary package.

```yaml
- name: Install the published orderer binary
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
    # Go package path used by the install branch.
    orderer_bin_package: "{{ orderer_git_hub_url }}/{{ orderer_git_repo }}/{{ orderer_source_code_package }}"
    # Git host used to resolve the orderer source repository.
    orderer_git_hub_url: github.com
    # Repository path for the orderer source code.
    orderer_git_repo: hyperledger/fabric-x-orderer
    # Go package path that builds the orderer binary.
    orderer_source_code_package: cmd/arma
    # Git ref or release tag used by the bin build and install branches.
    orderer_git_commit: v0.0.23
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/install
```

### bin/transfer

> Transfer the orderer binary to the target host

Copies the built or downloaded orderer binary through the shared bin role. Prepares target hosts for binary-mode lifecycle tasks without rendering config or crypto.

```yaml
- name: Transfer the orderer binary to the target host
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/transfer
```

### bin/rm

> Remove the installed orderer binary

Deletes the installed orderer binary through the shared bin role. Does not remove generated config, crypto material, or persisted orderer data.

```yaml
- name: Remove the installed orderer binary
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/rm
```

### bin/start

> Start the orderer binary process

Ensures the binary-mode data directory exists and starts `orderer_bin_name` with the selected component subcommand and generated config file. Consumes remote config, genesis, MSP, and TLS material already transferred into the orderer config directory.

```yaml
- name: Start the orderer binary process
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Shared base directory for persisted runtime data. Example: `/var/hyperledger/fabric-x/data/orderer/router-1`.
    remote_data_dir: "/var/hyperledger/fabric-x/data/orderer/router-1"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where orderer data is stored.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # gRPC port exposed by the orderer. Example: `7050`.
    orderer_rpc_port: 7050
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/start
```

### bin/stop

> Stop the orderer binary process

Stops the orderer binary process through the shared bin role. Leaves the binary, generated config, crypto, logs, and persisted data in place for restart or inspection.

```yaml
- name: Stop the orderer binary process
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/stop
```

### bin/fetch_logs

> Fetch logs for the orderer binary process

Collects logs for the binary-mode orderer process through the shared bin role. Useful after running consenter, batcher, assembler, or router components directly on the host.

```yaml
- name: Fetch logs for the orderer binary process
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/fetch_logs
```

### bin/teardown

> Remove the orderer binary runtime state

Stops the binary-mode orderer process and removes its persisted data directory. Keeps generated configuration and crypto artifacts under the config directory for explicit cleanup or later reuse.

```yaml
- name: Remove the orderer binary runtime state
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/teardown
```

### container/start

> Start the orderer container

Ensures the host data directory exists and starts the orderer container with the selected component command. Mounts generated config and TLS/MSP material read-only, mounts the data directory read-write, and exposes gRPC and metrics ports.

```yaml
- name: Start the orderer container
  vars:
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Container name used by the container lifecycle branch.
    orderer_container_name: "{{ inventory_hostname }}"
    # Full image reference used by the container and Kubernetes branches.
    orderer_image: "{{ orderer_registry_endpoint }}/{{ orderer_image_name }}:{{ orderer_image_tag }}"
    # Registry prefix used to build the orderer image reference.
    orderer_registry_endpoint: "{{ lookup('env', 'ORDERER_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image name used for the orderer container.
    orderer_image_name: fabric-x-orderer
    # Image tag used for the orderer container.
    orderer_image_tag: 0.0.23
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Shared base directory for persisted runtime data. Example: `/var/hyperledger/fabric-x/data/orderer/router-1`.
    remote_data_dir: "/var/hyperledger/fabric-x/data/orderer/router-1"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where orderer data is stored.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Container path where orderer configuration is mounted.
    orderer_container_config_dir: /config
    # Container path where orderer data is mounted.
    orderer_container_data_dir: /data
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # gRPC port exposed by the orderer. Example: `7050`.
    orderer_rpc_port: 7050
    # Metrics port exposed by the orderer. Example: `7060`.
    orderer_metrics_port: 7060
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/start
```

### container/stop

> Stop the orderer container

Stops the named orderer container through the shared container role. Leaves the container definition, mounted config, crypto material, and persisted data for restart or inspection.

```yaml
- name: Stop the orderer container
  vars:
    # Container name used by the container lifecycle branch.
    orderer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/stop
```

### container/rm

> Remove the orderer container

Deletes the named orderer container through the shared container role. Does not remove host-side generated config, crypto material, or persisted data directories.

```yaml
- name: Remove the orderer container
  vars:
    # Container name used by the container lifecycle branch.
    orderer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch logs from the orderer container

Collects logs for the configured orderer container. Covers consenter, batcher, assembler, and router containers by using the role's container name.

```yaml
- name: Fetch logs from the orderer container
  vars:
    # Container name used by the container lifecycle branch.
    orderer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/fetch_logs
```

### container/teardown

> Remove the orderer container runtime state

Deletes the orderer container and removes its persisted data directory. Keeps generated config and crypto artifacts on the host unless the config or crypto cleanup entrypoints are run.

```yaml
- name: Remove the orderer container runtime state
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/teardown
```

### data/rm

> Remove orderer persisted data

Deletes the orderer data directory for binary and container deployments. In Kubernetes mode, removes the orderer PVC so StatefulSet-managed component data can be recreated.

```yaml
- name: Remove orderer persisted data
  vars:
    # Remote directory where orderer data is stored.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Shared base directory for persisted runtime data. Example: `/var/hyperledger/fabric-x/data/orderer/router-1`.
    remote_data_dir: "/var/hyperledger/fabric-x/data/orderer/router-1"
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
    # Kubernetes namespace used for orderer resources. Example: `fabricx-orderer`.
    k8s_namespace: "fabricx-orderer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: data/rm
```

### config/transfer

> Render and transfer orderer configuration

Renders the component-specific orderer config for `consensus`, `batcher`, `assembler`, or `router`. Copies the genesis block from configtxgen artifacts, writes data and config paths for the selected deployment mode, and prepares optional TLS, mTLS, metrics, and Kubernetes ConfigMap artifacts.

```yaml
- name: Render and transfer orderer configuration
  vars:
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Shared base directory for persisted runtime data. Example: `/var/hyperledger/fabric-x/data/orderer/router-1`.
    remote_data_dir: "/var/hyperledger/fabric-x/data/orderer/router-1"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where orderer data is stored.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Container path where orderer configuration is mounted.
    orderer_container_config_dir: /config
    # Container path where orderer data is mounted.
    orderer_container_data_dir: /data
    # Configuration path embedded into rendered orderer files.
    orderer_config_dir: "{{ orderer_remote_config_dir if orderer_use_bin else orderer_container_config_dir }}"
    # Data path embedded into rendered orderer files.
    orderer_data_dir: "{{ orderer_remote_data_dir if orderer_use_bin else orderer_container_data_dir }}"
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # Control-node directory containing configtxgen artifacts. Example: `/tmp/fabric-x/artifacts/configtxgen`.
    configtxgen_artifacts_dir: "/tmp/fabric-x/artifacts/configtxgen"
    # Channel identifier used to derive the genesis block filename. Example: `fabricx-channel`.
    channel_id: "fabricx-channel"
    # Genesis block filename copied into the config directory.
    orderer_genesis_block_file: "{{ channel_id }}_block.pb"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Enables server-side TLS in the rendered config.
    orderer_use_tls: false
    # Enables client mutual TLS in the rendered config.
    orderer_use_mtls: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
    # gRPC port exposed by the orderer. Example: `7050`.
    orderer_rpc_port: 7050
    # Metrics port written into the rendered config when enabled. Example: `9444`.
    orderer_metrics_port: 9444
    # Optional metrics logging interval written into the rendered config. Example: `10s`.
    orderer_metrics_log_interval: "10s"
    # Client identifiers whose mTLS CA certificates are mounted or transferred. Trusts fetched `tls/ca.crt` files under those artifact directories. Example: `['loadgen-1', 'gateway-1']`.
    orderer_mtls_clients:
      - "loadgen-1"
      - "gateway-1"
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred. Example: `[{'domain': 'org1.example.com'}, {'domain': 'org2.example.com'}]`.
    orderer_mtls_orgs:
      - domain: "org1.example.com"
      - domain: "org2.example.com"
    # Organization metadata shared by the orderer crypto and config branches. Example: `{'domain': 'orderer.example.com', 'orderer': {'name': 'orderer-consenter-1'}, 'fabric_ca_host': 'ca-orderer'}`.
    organization:
      domain: "orderer.example.com"
      orderer:
        name: "orderer-consenter-1"
      fabric_ca_host: "ca-orderer"
    # Party identifier written into the orderer configuration. Example: `consenter-1`, `batcher-1`, `assembler-1`, or `router-1`.
    orderer_group: "router-1"
    # Batcher shard identifier written only by the batcher template. Example: `0`.
    orderer_shard_id: 0
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer
```

### config/mtls/transfer

> Transfer mTLS CA certificates for orderer clients and orgs

Copies trusted client and organization TLS CA certificates into the orderer mTLS directory structure. Consumes fetched client `tls/ca.crt` files and peer organization tlsca certificates so generated configs can enable client mutual TLS.

```yaml
- name: Transfer mTLS CA certificates for orderer clients and orgs
  vars:
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Control-node directory containing fetched crypto artifacts. Example: `/tmp/fabric-x/artifacts/fetched`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/fetched"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Client identifiers whose mTLS CA certificates are mounted or transferred. Trusts fetched `tls/ca.crt` files under those artifact directories. Example: `['loadgen-1', 'gateway-1']`.
    orderer_mtls_clients:
      - "loadgen-1"
      - "gateway-1"
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred. Example: `[{'domain': 'org1.example.com'}, {'domain': 'org2.example.com'}]`.
    orderer_mtls_orgs:
      - domain: "org1.example.com"
      - domain: "org2.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/mtls/transfer
```

### config/rm

> Remove orderer configuration

Deletes the orderer configuration directory, including rendered config, genesis block, mTLS trust bundles, and deployment-local config artifacts. In Kubernetes mode, also delegates removal of the orderer ConfigMap.

```yaml
- name: Remove orderer configuration
  vars:
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/rm
```

### config/transfer_grafana_dashboard

> Copy the orderer Grafana dashboard

Publishes the bundled Fabric-X Orderer Grafana dashboard through the grafana role. The dashboard consumes Prometheus scrape targets produced for consenter, batcher, assembler, and router metrics endpoints.

```yaml
- name: Copy the orderer Grafana dashboard
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer_grafana_dashboard
```

### crypto/setup

> Prepare orderer crypto material

Validates TLS and mTLS prerequisites, provisions orderer MSP and TLS material through cryptogen or Fabric CA, and optionally creates the Kubernetes Secret. Produces the crypto artifacts consumed by config rendering, binary/container mounts, and Kubernetes workloads.

```yaml
- name: Prepare orderer crypto material
  vars:
    # Enables server-side TLS in the rendered config.
    orderer_use_tls: false
    # Enables client mutual TLS in the rendered config.
    orderer_use_mtls: false
    # Organization metadata shared by the orderer crypto and config branches. Example: `{'domain': 'orderer.example.com', 'orderer': {'name': 'orderer-consenter-1'}, 'fabric_ca_host': 'ca-orderer'}`.
    organization:
      domain: "orderer.example.com"
      orderer:
        name: "orderer-consenter-1"
      fabric_ca_host: "ca-orderer"
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/setup
```

### crypto/cryptogen/transfer

> Transfer cryptogen-generated orderer crypto material

Copies cryptogen-generated MSP and TLS artifacts for the orderer identity into the remote configuration directory. Consumes the cryptogen artifact tree for the orderer organization and prepares material for local mounts or Kubernetes Secret creation.

```yaml
- name: Transfer cryptogen-generated orderer crypto material
  vars:
    # Control-node directory containing cryptogen-generated crypto artifacts. Example: `/tmp/fabric-x/artifacts/cryptogen`.
    cryptogen_artifacts_dir: "/tmp/fabric-x/artifacts/cryptogen"
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Organization metadata shared by the orderer crypto and config branches. Example: `{'domain': 'orderer.example.com', 'orderer': {'name': 'orderer-consenter-1'}, 'fabric_ca_host': 'ca-orderer'}`.
    organization:
      domain: "orderer.example.com"
      orderer:
        name: "orderer-consenter-1"
      fabric_ca_host: "ca-orderer"
    # Orderer identity name used to derive crypto artifact paths.
    orderer_crypto_name: "{{ organization.orderer.name | default(inventory_hostname) }}"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

> Enroll the orderer with Fabric CA

Copies the Fabric CA TLS certificate when needed and enrolls both MSP and TLS identities for the orderer host. Writes generated MSP and server TLS material into the orderer config directory for later config, runtime, and fetch tasks.

```yaml
- name: Enroll the orderer with Fabric CA
  vars:
    # Control-node directory containing fetched crypto artifacts. Example: `/tmp/fabric-x/artifacts/fetched`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/fetched"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Organization metadata shared by the orderer crypto and config branches. Example: `{'domain': 'orderer.example.com', 'orderer': {'name': 'orderer-consenter-1'}, 'fabric_ca_host': 'ca-orderer'}`.
    organization:
      domain: "orderer.example.com"
      orderer:
        name: "orderer-consenter-1"
      fabric_ca_host: "ca-orderer"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/fabric_ca/enroll
```

### crypto/fetch

> Fetch orderer certificates to the control node

Fetches the orderer sign certificate, TLS server certificate, and TLS CA certificate to the control node. Publishes artifacts consumed by downstream config generation, client mTLS trust bundles, and other roles.

```yaml
- name: Fetch orderer certificates to the control node
  vars:
    # Control-node directory containing fetched crypto artifacts. Example: `/tmp/fabric-x/artifacts/fetched`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/fetched"
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Organization metadata shared by the orderer crypto and config branches. Example: `{'domain': 'orderer.example.com', 'orderer': {'name': 'orderer-consenter-1'}, 'fabric_ca_host': 'ca-orderer'}`.
    organization:
      domain: "orderer.example.com"
      orderer:
        name: "orderer-consenter-1"
      fabric_ca_host: "ca-orderer"
    # Orderer identity name used to derive crypto artifact paths.
    orderer_crypto_name: "{{ organization.orderer.name | default(inventory_hostname) }}"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove orderer crypto material

Deletes the orderer MSP and TLS directories from the config path. In Kubernetes mode, also delegates deletion of the Secret that mounted MSP and TLS material into the workload.

```yaml
- name: Remove orderer crypto material
  vars:
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/rm
```

### k8s/start

> Create the orderer Kubernetes workload

Creates the orderer Kubernetes Service, StatefulSet, and optional NodePort and LoadBalancer Services after ensuring the namespace exists. Consumes ConfigMap and Secret artifacts generated by the Kubernetes config and crypto transfer entrypoints, then starts the selected component container.

```yaml
- name: Create the orderer Kubernetes workload
  vars:
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Seconds to wait for the orderer StatefulSet rollout.
    orderer_k8s_wait_timeout: 120
    # gRPC port exposed by the orderer. Example: `7050`.
    orderer_rpc_port: 7050
    # Metrics port exposed by the orderer. Example: `7060`.
    orderer_metrics_port: 7060
    # Kubernetes NodePort value used by the external RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31050`.
    orderer_k8s_rpc_node_port: 31050
    # Kubernetes NodePort value used by the external metrics Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31051`.
    orderer_k8s_metrics_node_port: 31051
    # Filesystem group applied to mounted ConfigMap and Secret volumes.
    orderer_k8s_fs_group: 10001
    # Full image reference used by the container and Kubernetes branches.
    orderer_image: "{{ orderer_registry_endpoint }}/{{ orderer_image_name }}:{{ orderer_image_tag }}"
    # Registry prefix used to build the orderer image reference.
    orderer_registry_endpoint: "{{ lookup('env', 'ORDERER_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image name used for the orderer container.
    orderer_image_name: fabric-x-orderer
    # Image tag used for the orderer container.
    orderer_image_tag: 0.0.23
    # Container path where orderer configuration is mounted.
    orderer_container_config_dir: /config
    # Container path where orderer data is mounted.
    orderer_container_data_dir: /data
    # Enables client mutual TLS in the rendered config.
    orderer_use_mtls: false
    # Client identifiers whose mTLS CA certificates are mounted or transferred. Trusts fetched `tls/ca.crt` files under those artifact directories. Example: `['loadgen-1', 'gateway-1']`.
    orderer_mtls_clients:
      - "loadgen-1"
      - "gateway-1"
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred. Example: `[{'domain': 'org1.example.com'}, {'domain': 'org2.example.com'}]`.
    orderer_mtls_orgs:
      - domain: "org1.example.com"
      - domain: "org2.example.com"
    # Organization metadata shared by the orderer crypto and config branches. Example: `{'domain': 'orderer.example.com', 'orderer': {'name': 'orderer-consenter-1'}, 'fabric_ca_host': 'ca-orderer'}`.
    organization:
      domain: "orderer.example.com"
      orderer:
        name: "orderer-consenter-1"
      fabric_ca_host: "ca-orderer"
    # Kubernetes namespace used for orderer resources. Example: `fabricx-orderer`.
    k8s_namespace: "fabricx-orderer"
    # PVC storage request used by the orderer StatefulSet. Example: `20Gi`.
    k8s_storage_size: "20Gi"
    # Optional storage class used by the StatefulSet PVC. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Optional image pull secret used by the StatefulSet. Example: `regcred-orderer`.
    k8s_image_pull_secret: "regcred-orderer"
    # Optional readiness probe initial delay override. Example: `15`.
    k8s_readiness_probe_initial_delay_seconds: 15
    # Optional readiness probe period override. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Optional readiness probe timeout override. Example: `3`.
    k8s_readiness_probe_timeout_seconds: 3
    # Optional readiness probe failure threshold override. Example: `6`.
    k8s_readiness_probe_failure_threshold: 6
    # Optional liveness probe initial delay override. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Optional liveness probe period override. Example: `20`.
    k8s_liveness_probe_period_seconds: 20
    # Optional liveness probe timeout override. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Optional liveness probe failure threshold override. Example: `3`.
    k8s_liveness_probe_failure_threshold: 3
    # Set to `true` to create a LoadBalancer Service entry that exposes the RPC port externally. When undefined or `false`, the RPC port is not included in the LoadBalancer Service.
    orderer_k8s_loadbalancer_expose_rpc_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the metrics port externally. When undefined or `false`, the metrics port is not included in the LoadBalancer Service.
    orderer_k8s_loadbalancer_expose_metrics_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/start
```

### k8s/ping

> Check the orderer Kubernetes Service ports

Probes configured Kubernetes NodePort values and LoadBalancer-exposed service ports for external reachability.

```yaml
- name: Check the orderer Kubernetes Service ports
  vars:
    # Kubernetes NodePort value used by the external RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31050`.
    orderer_k8s_rpc_node_port: 31050
    # Kubernetes NodePort value used by the external metrics Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31051`.
    orderer_k8s_metrics_node_port: 31051
    # Set to `true` to create a LoadBalancer Service entry that exposes the RPC port externally. When undefined or `false`, the RPC port is not included in the LoadBalancer Service.
    orderer_k8s_loadbalancer_expose_rpc_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the metrics port externally. When undefined or `false`, the metrics port is not included in the LoadBalancer Service.
    orderer_k8s_loadbalancer_expose_metrics_port: false
    # gRPC port exposed by the orderer. Example: `7050`.
    orderer_rpc_port: 7050
    # Metrics port exposed by the orderer. Example: `7060`.
    orderer_metrics_port: 7060
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/ping
```

### k8s/rm

> Remove the orderer Kubernetes workload

Deletes the orderer StatefulSet and Services from the configured namespace. Leaves ConfigMap, Secret, and PVC artifacts for explicit config, crypto, or data cleanup entrypoints.

```yaml
- name: Remove the orderer Kubernetes workload
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for orderer resources. Example: `fabricx-orderer`.
    k8s_namespace: "fabricx-orderer"
    # Kubernetes NodePort value used by the external RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31050`.
    orderer_k8s_rpc_node_port: 31050
    # Set to `true` to create a LoadBalancer Service entry that exposes the RPC port externally. When undefined or `false`, the RPC port is not included in the LoadBalancer Service.
    orderer_k8s_loadbalancer_expose_rpc_port: false
    # Kubernetes NodePort value used by the external metrics Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31051`.
    orderer_k8s_metrics_node_port: 31051
    # Set to `true` to create a LoadBalancer Service entry that exposes the metrics port externally. When undefined or `false`, the metrics port is not included in the LoadBalancer Service.
    orderer_k8s_loadbalancer_expose_metrics_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/rm
```

### k8s/teardown

> Remove the orderer Kubernetes workload and data

Deletes the Kubernetes workload and removes persisted orderer data. Keeps generated ConfigMap and Secret artifacts unless their dedicated removal entrypoints are invoked.

```yaml
- name: Remove the orderer Kubernetes workload and data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/teardown
```

### k8s/fetch_logs

> Fetch logs from the orderer Kubernetes pod

Collects logs from pods selected by the orderer Kubernetes app label. Works for consenter, batcher, assembler, and router workloads by using the generated resource name labels.

```yaml
- name: Fetch logs from the orderer Kubernetes pod
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

> Create the orderer Kubernetes ConfigMap

Slurps the generated genesis block and renders the orderer ConfigMap. Includes the component config file and optional mTLS CA bundles consumed by the Kubernetes StatefulSet.

```yaml
- name: Create the orderer Kubernetes ConfigMap
  vars:
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # Enables client mutual TLS in the rendered config.
    orderer_use_mtls: false
    # Client identifiers whose mTLS CA certificates are mounted or transferred. Trusts fetched `tls/ca.crt` files under those artifact directories. Example: `['loadgen-1', 'gateway-1']`.
    orderer_mtls_clients:
      - "loadgen-1"
      - "gateway-1"
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred. Example: `[{'domain': 'org1.example.com'}, {'domain': 'org2.example.com'}]`.
    orderer_mtls_orgs:
      - domain: "org1.example.com"
      - domain: "org2.example.com"
    # Kubernetes namespace used for orderer resources. Example: `fabricx-orderer`.
    k8s_namespace: "fabricx-orderer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the orderer Kubernetes ConfigMap

Deletes the ConfigMap that holds orderer configuration, genesis material, and optional mTLS CA bundles. Does not remove the local generated config directory.

```yaml
- name: Remove the orderer Kubernetes ConfigMap
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for orderer resources. Example: `fabricx-orderer`.
    k8s_namespace: "fabricx-orderer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

> Create the orderer Kubernetes Secret

Resolves orderer MSP and TLS file locations and renders the Kubernetes Secret. The Secret is consumed by the StatefulSet to mount MSP private key, signcert, CA certs, TLS server key, TLS server certificate, and TLS CA material.

```yaml
- name: Create the orderer Kubernetes Secret
  vars:
    # Shared base directory for generated configuration. Example: `/var/hyperledger/fabric-x/config/orderer/assembler-1`.
    remote_config_dir: "/var/hyperledger/fabric-x/config/orderer/assembler-1"
    # Remote directory where orderer configuration is written.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Organization metadata shared by the orderer crypto and config branches. Example: `{'domain': 'orderer.example.com', 'orderer': {'name': 'orderer-consenter-1'}, 'fabric_ca_host': 'ca-orderer'}`.
    organization:
      domain: "orderer.example.com"
      orderer:
        name: "orderer-consenter-1"
      fabric_ca_host: "ca-orderer"
    # Orderer identity name used to derive crypto artifact paths.
    orderer_crypto_name: "{{ organization.orderer.name | default(inventory_hostname) }}"
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Orderer component to manage; use `consensus` for the consenter process. Example: `consensus`, `batcher`, `assembler`, or `router`.
    orderer_component_type: "router"
    # Kubernetes namespace used for orderer resources. Example: `fabricx-orderer`.
    k8s_namespace: "fabricx-orderer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Remove the orderer Kubernetes Secret

Deletes the Secret that stores orderer MSP and TLS material. Does not remove the local MSP and TLS directories under the orderer config path.

```yaml
- name: Remove the orderer Kubernetes Secret
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for orderer resources. Example: `fabricx-orderer`.
    k8s_namespace: "fabricx-orderer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/crypto/rm
```

### prometheus/get_scrapers

> Build Prometheus scrape targets for orderer hosts

Groups orderer hosts by component type and exposes Prometheus scrape service definitions for downstream monitoring configuration. Produces scrape targets for consenter, batcher, assembler, and router metrics endpoints using each host's configured metrics port.

```yaml
- name: Build Prometheus scrape targets for orderer hosts
  vars:
    # Inventory hosts dedicated to orderer nodes. Example: `['orderer-consenter-1', 'orderer-batcher-1', 'orderer-assembler-1', 'orderer-router-1']`.
    orderer_hosts:
      - "orderer-consenter-1"
      - "orderer-batcher-1"
      - "orderer-assembler-1"
      - "orderer-router-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: prometheus/get_scrapers
```
