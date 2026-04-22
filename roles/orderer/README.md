
# hyperledger.fabricx.orderer

> Runs Fabric-X Orderer components (`consensus`, `batcher`, `assembler`, `router`).


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [start](#task-start)
  - [stop](#task-stop)
  - [teardown](#task-teardown)
  - [wipe](#task-wipe)
  - [fetch_logs](#task-fetch_logs)
  - [ping](#task-ping)
  - [get_metrics](#task-get_metrics)
  - [bin/build](#task-bin-build)
  - [bin/install](#task-bin-install)
  - [bin/transfer](#task-bin-transfer)
  - [bin/rm](#task-bin-rm)
  - [bin/start](#task-bin-start)
  - [bin/stop](#task-bin-stop)
  - [bin/fetch_logs](#task-bin-fetch_logs)
  - [bin/teardown](#task-bin-teardown)
  - [container/start](#task-container-start)
  - [container/stop](#task-container-stop)
  - [container/rm](#task-container-rm)
  - [container/fetch_logs](#task-container-fetch_logs)
  - [container/teardown](#task-container-teardown)
  - [data/rm](#task-data-rm)
  - [config/transfer](#task-config-transfer)
  - [config/mtls/transfer](#task-config-mtls-transfer)
  - [config/rm](#task-config-rm)
  - [config/transfer_grafana_dashboard](#task-config-transfer_grafana_dashboard)
  - [crypto/setup](#task-crypto-setup)
  - [crypto/cryptogen/transfer](#task-crypto-cryptogen-transfer)
  - [crypto/fabric_ca/enroll](#task-crypto-fabric_ca-enroll)
  - [crypto/fetch](#task-crypto-fetch)
  - [crypto/rm](#task-crypto-rm)
  - [k8s/start](#task-k8s-start)
  - [k8s/ping](#task-k8s-ping)
  - [k8s/rm](#task-k8s-rm)
  - [k8s/teardown](#task-k8s-teardown)
  - [k8s/fetch_logs](#task-k8s-fetch_logs)
  - [k8s/config/transfer](#task-k8s-config-transfer)
  - [k8s/config/rm](#task-k8s-config-rm)
  - [k8s/crypto/transfer](#task-k8s-crypto-transfer)
  - [k8s/crypto/rm](#task-k8s-crypto-rm)
  - [prometheus/get_scrapers](#task-prometheus-get_scrapers)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-start"></a>

### start

Dispatch orderer startup by component and deployment mode


Selects the orderer component implementation and delegates to the matching deployment-mode start task.


```yaml
- name: Dispatch orderer startup by component and deployment mode
  vars:
    # Orderer component to start.
    orderer_component_type: "string"
    # Deployment backend selected by the top-level dispatcher. The default derives from `orderer_use_bin` and `orderer_use_k8s`.
    orderer_deployment_mode: "{%- if orderer_use_bin -%}bin{%- elif orderer_use_k8s -%}k8s{%- else -%}container{%- endif -%}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: start
```

<a id="task-stop"></a>

### stop

Dispatch orderer shutdown by component and deployment mode


Selects the orderer component implementation and delegates to the matching deployment-mode stop task.


```yaml
- name: Dispatch orderer shutdown by component and deployment mode
  vars:
    # Orderer component to start.
    orderer_component_type: "string"
    # Deployment backend selected by the top-level dispatcher. The default derives from `orderer_use_bin` and `orderer_use_k8s`.
    orderer_deployment_mode: "{%- if orderer_use_bin -%}bin{%- elif orderer_use_k8s -%}k8s{%- else -%}container{%- endif -%}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: stop
```

<a id="task-teardown"></a>

### teardown

Dispatch orderer teardown by component and deployment mode


Selects the orderer component implementation and delegates to the matching deployment-mode teardown task.


```yaml
- name: Dispatch orderer teardown by component and deployment mode
  vars:
    # Orderer component to start.
    orderer_component_type: "string"
    # Deployment backend selected by the top-level dispatcher. The default derives from `orderer_use_bin` and `orderer_use_k8s`.
    orderer_deployment_mode: "{%- if orderer_use_bin -%}bin{%- elif orderer_use_k8s -%}k8s{%- else -%}container{%- endif -%}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: teardown
```

<a id="task-wipe"></a>

### wipe

Remove orderer runtime state, config, and optional binary


Runs teardown and removes generated configuration, crypto material, and optionally the installed binary.


```yaml
- name: Remove orderer runtime state, config, and optional binary
  vars:
    # Selects the binary deployment branch.
    orderer_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: wipe
```

<a id="task-fetch_logs"></a>

### fetch_logs

Fetch orderer logs from the active deployment backend


Delegates log collection to the Kubernetes, container, or binary implementation according to the enabled deployment mode.


```yaml
- name: Fetch orderer logs from the active deployment backend
  vars:
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
    # Selects the container deployment branch. The default derives from `orderer_use_bin` and `orderer_use_k8s`.
    orderer_use_container: "{{ (not orderer_use_bin) and (not orderer_use_k8s) }}"
    # Selects the binary deployment branch.
    orderer_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: fetch_logs
```

<a id="task-ping"></a>

### ping

Check the orderer gRPC port


Pings the configured orderer gRPC endpoint through the shared utils role, or the Kubernetes NodePort endpoints when enabled.


```yaml
- name: Check the orderer gRPC port
  vars:
    # gRPC port exposed by the orderer.
    orderer_rpc_port: 1000
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: ping
```

<a id="task-get_metrics"></a>

### get_metrics

Retrieve orderer Prometheus metrics


Fetches metrics from the orderer monitoring endpoint when metrics are enabled.


```yaml
- name: Retrieve orderer Prometheus metrics
  vars:
    # Host name or IP used by control-node HTTP requests.
    actual_host: "string"
    # Protocol used by the metrics fetch branch.
    orderer_http_protocol: http
    # Metrics port queried by the metrics fetch branch.
    orderer_metrics_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: get_metrics
```

<a id="task-bin-build"></a>

### bin/build

Build the orderer binary from source


Builds the orderer binary through the shared bin role using the configured Git repository and Go package.


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

<a id="task-bin-install"></a>

### bin/install

Install the published orderer binary


Installs the configured released orderer binary through the shared bin role.


```yaml
- name: Install the published orderer binary
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
    # Go package path used by the install branch. The default derives from `orderer_git_hub_url`, `orderer_git_repo`, and `orderer_source_code_package`.
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

<a id="task-bin-transfer"></a>

### bin/transfer

Transfer the orderer binary to the target host


Copies the built or downloaded orderer binary through the shared bin role.


```yaml
- name: Transfer the orderer binary to the target host
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/transfer
```

<a id="task-bin-rm"></a>

### bin/rm

Remove the installed orderer binary


Deletes the orderer binary through the shared bin role.


```yaml
- name: Remove the installed orderer binary
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/rm
```

<a id="task-bin-start"></a>

### bin/start

Start the orderer binary process


Ensures the data directory exists and starts the orderer binary with the selected component configuration.


```yaml
- name: Start the orderer binary process
  vars:
    # Binary name used by the bin branches.
    orderer_bin_name: arma
    # Orderer component to start.
    orderer_component_type: "string"
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Shared base directory for persisted runtime data.
    remote_data_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where orderer data is stored. The default derives from `remote_data_dir`.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # gRPC port exposed by the orderer.
    orderer_rpc_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/start
```

<a id="task-bin-stop"></a>

### bin/stop

Stop the orderer binary process


Stops the orderer binary through the shared bin role.


```yaml
- name: Stop the orderer binary process
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/stop
```

<a id="task-bin-fetch_logs"></a>

### bin/fetch_logs

Fetch logs for the orderer binary process


Collects binary-process logs through the shared bin role.


```yaml
- name: Fetch logs for the orderer binary process
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/fetch_logs
```

<a id="task-bin-teardown"></a>

### bin/teardown

Remove the orderer binary runtime state


Stops the orderer binary and removes its persisted data.


```yaml
- name: Remove the orderer binary runtime state
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: bin/teardown
```

<a id="task-container-start"></a>

### container/start

Start the orderer container


Ensures the data directory exists and starts the orderer container with the configured ports and volume mounts.


```yaml
- name: Start the orderer container
  vars:
    # Orderer component to start.
    orderer_component_type: "string"
    # Container name used by the container lifecycle branch. The default derives from `inventory_hostname`.
    orderer_container_name: "{{ inventory_hostname }}"
    # Full image reference used by the container and Kubernetes branches. The default derives from `orderer_registry_endpoint`, `orderer_image_name`, and `orderer_image_tag`.
    orderer_image: "{{ orderer_registry_endpoint }}/{{ orderer_image_name }}:{{ orderer_image_tag }}"
    # Registry prefix used to build the orderer image reference. The default derives from `ORDERER_REGISTRY_ENDPOINT`.
    orderer_registry_endpoint: "{{ lookup('env', 'ORDERER_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image name used for the orderer container.
    orderer_image_name: fabric-x-orderer
    # Image tag used for the orderer container.
    orderer_image_tag: 0.0.23
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Shared base directory for persisted runtime data.
    remote_data_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where orderer data is stored. The default derives from `remote_data_dir`.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Container path where orderer configuration is mounted.
    orderer_container_config_dir: /config
    # Container path where orderer data is mounted.
    orderer_container_data_dir: /data
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # gRPC port exposed by the orderer.
    orderer_rpc_port: 1000
    # Metrics port exposed by the orderer.
    orderer_metrics_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/start
```

<a id="task-container-stop"></a>

### container/stop

Stop the orderer container


Stops the orderer container through the shared container role.


```yaml
- name: Stop the orderer container
  vars:
    # Container name used by the container lifecycle branch. The default derives from `inventory_hostname`.
    orderer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/stop
```

<a id="task-container-rm"></a>

### container/rm

Remove the orderer container


Deletes the orderer container through the shared container role.


```yaml
- name: Remove the orderer container
  vars:
    # Container name used by the container lifecycle branch. The default derives from `inventory_hostname`.
    orderer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/rm
```

<a id="task-container-fetch_logs"></a>

### container/fetch_logs

Fetch logs from the orderer container


Collects logs for the configured orderer container.


```yaml
- name: Fetch logs from the orderer container
  vars:
    # Container name used by the container lifecycle branch. The default derives from `inventory_hostname`.
    orderer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/fetch_logs
```

<a id="task-container-teardown"></a>

### container/teardown

Remove the orderer container runtime state


Deletes the orderer container and removes its persisted data.


```yaml
- name: Remove the orderer container runtime state
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: container/teardown
```

<a id="task-data-rm"></a>

### data/rm

Remove orderer persisted data


Deletes the orderer data directory locally or removes the Kubernetes PVC when running in Kubernetes mode.


```yaml
- name: Remove orderer persisted data
  vars:
    # Remote directory where orderer data is stored. The default derives from `remote_data_dir`.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Shared base directory for persisted runtime data.
    remote_data_dir: "string"
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
    # Kubernetes namespace used for orderer resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: data/rm
```

<a id="task-config-transfer"></a>

### config/transfer

Render and transfer orderer configuration


Creates the main orderer configuration file, copies the genesis block, and optionally prepares mTLS and Kubernetes-specific configuration.


```yaml
- name: Render and transfer orderer configuration
  vars:
    # Orderer component to start.
    orderer_component_type: "string"
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Shared base directory for persisted runtime data.
    remote_data_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where orderer data is stored. The default derives from `remote_data_dir`.
    orderer_remote_data_dir: "{{ remote_data_dir }}"
    # Container path where orderer configuration is mounted.
    orderer_container_config_dir: /config
    # Container path where orderer data is mounted.
    orderer_container_data_dir: /data
    # Configuration path embedded into rendered orderer files. The default derives from `orderer_remote_config_dir`, `orderer_use_bin`, and `orderer_container_config_dir`.
    orderer_config_dir: "{{ orderer_remote_config_dir if orderer_use_bin else orderer_container_config_dir }}"
    # Data path embedded into rendered orderer files. The default derives from `orderer_remote_data_dir`, `orderer_use_bin`, and `orderer_container_data_dir`.
    orderer_data_dir: "{{ orderer_remote_data_dir if orderer_use_bin else orderer_container_data_dir }}"
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # Control-node directory containing configtxgen artifacts.
    configtxgen_artifacts_dir: "string"
    # Channel identifier used to derive the genesis block filename.
    channel_id: "string"
    # Genesis block filename copied into the config directory. The default derives from `channel_id`.
    orderer_genesis_block_file: "{{ channel_id }}_block.pb"
    # Selects the binary deployment branch.
    orderer_use_bin: false
    # Enables server-side TLS in the rendered config.
    orderer_use_tls: false
    # Enables client mutual TLS in the rendered config.
    orderer_use_mtls: false
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
    # gRPC port exposed by the orderer.
    orderer_rpc_port: 1000
    # Metrics port written into the rendered config when enabled.
    orderer_metrics_port: 1000
    # Optional metrics logging interval written into the rendered config. The template falls back to 10s when unset.
    orderer_metrics_log_interval: "string"
    # Client identifiers whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_clients: ["entry1", "entry2"]
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_orgs: [{}]
    # Organization metadata shared by the orderer crypto and config branches.
    organization: {}
    # Party identifier written into the orderer configuration.
    orderer_group: "string"
    # Batcher shard identifier written only by the batcher template.
    orderer_shard_id: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer
```

<a id="task-config-mtls-transfer"></a>

### config/mtls/transfer

Transfer mTLS CA certificates for orderer clients and orgs


Copies trusted client and organization TLS CA certificates into the orderer mTLS directory structure.


```yaml
- name: Transfer mTLS CA certificates for orderer clients and orgs
  vars:
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Control-node directory containing fetched crypto artifacts.
    fetched_artifacts_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Client identifiers whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_clients: ["entry1", "entry2"]
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_orgs: [{}]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/mtls/transfer
```

<a id="task-config-rm"></a>

### config/rm

Remove orderer configuration


Deletes the orderer configuration directory and optionally removes Kubernetes ConfigMap resources.


```yaml
- name: Remove orderer configuration
  vars:
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/rm
```

<a id="task-config-transfer_grafana_dashboard"></a>

### config/transfer_grafana_dashboard

Copy the orderer Grafana dashboard


Publishes the bundled Fabric-X Orderer Grafana dashboard through the grafana role.


```yaml
- name: Copy the orderer Grafana dashboard
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer_grafana_dashboard
```

<a id="task-crypto-setup"></a>

### crypto/setup

Prepare orderer crypto material


Validates TLS prerequisites, provisions crypto material through cryptogen or Fabric CA, and optionally creates the Kubernetes Secret.


```yaml
- name: Prepare orderer crypto material
  vars:
    # Enables server-side TLS in the rendered config.
    orderer_use_tls: false
    # Enables client mutual TLS in the rendered config.
    orderer_use_mtls: false
    # Organization metadata shared by the orderer crypto and config branches.
    organization: {}
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/setup
```

<a id="task-crypto-cryptogen-transfer"></a>

### crypto/cryptogen/transfer

Transfer cryptogen-generated orderer crypto material


Copies cryptogen-generated MSP and TLS artifacts into the remote orderer configuration directory.


```yaml
- name: Transfer cryptogen-generated orderer crypto material
  vars:
    # Control-node directory containing cryptogen-generated crypto artifacts.
    cryptogen_artifacts_dir: "string"
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Organization metadata shared by the orderer crypto and config branches.
    organization: {}
    # Orderer identity name used to derive crypto artifact paths. The default derives from `organization.orderer.name` and falls back to `inventory_hostname`.
    orderer_crypto_name: "{{ organization.orderer.name | default(inventory_hostname) }}"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/cryptogen/transfer
```

<a id="task-crypto-fabric_ca-enroll"></a>

### crypto/fabric_ca/enroll

Enroll the orderer with Fabric CA


Copies the Fabric CA TLS certificate when needed and enrolls both MSP and TLS identities for the orderer.


```yaml
- name: Enroll the orderer with Fabric CA
  vars:
    # Control-node directory containing fetched crypto artifacts.
    fetched_artifacts_dir: "string"
    # Host name or IP used by control-node HTTP requests.
    actual_host: "string"
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Organization metadata shared by the orderer crypto and config branches.
    organization: {}
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/fabric_ca/enroll
```

<a id="task-crypto-fetch"></a>

### crypto/fetch

Fetch orderer certificates to the control node


Fetches the orderer sign certificate, TLS certificate, and TLS CA certificate for downstream artifact generation.


```yaml
- name: Fetch orderer certificates to the control node
  vars:
    # Control-node directory containing fetched crypto artifacts.
    fetched_artifacts_dir: "string"
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Organization metadata shared by the orderer crypto and config branches.
    organization: {}
    # Orderer identity name used to derive crypto artifact paths. The default derives from `organization.orderer.name` and falls back to `inventory_hostname`.
    orderer_crypto_name: "{{ organization.orderer.name | default(inventory_hostname) }}"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/fetch
```

<a id="task-crypto-rm"></a>

### crypto/rm

Remove orderer crypto material


Deletes the orderer MSP and TLS directories and optionally removes the Kubernetes Secret.


```yaml
- name: Remove orderer crypto material
  vars:
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Selects the Kubernetes deployment branch.
    orderer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/rm
```

<a id="task-k8s-start"></a>

### k8s/start

Create the orderer Kubernetes workload


Creates the orderer Services and StatefulSet in Kubernetes after ensuring the namespace exists, and optionally creates the NodePort Service.


```yaml
- name: Create the orderer Kubernetes workload
  vars:
    # Orderer component to start.
    orderer_component_type: "string"
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service. The default derives from `inventory_hostname`.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Seconds to wait for the orderer StatefulSet rollout.
    orderer_k8s_wait_timeout: 120
    # Enables the optional NodePort Service for the orderer Kubernetes deployment. The NodePort Service and Kubernetes ping branch use this toggle.
    orderer_k8s_use_node_port: false
    # gRPC port exposed by the orderer.
    orderer_rpc_port: 1000
    # Metrics port exposed by the orderer.
    orderer_metrics_port: 1000
    # NodePort used to expose the orderer gRPC service when NodePort exposure is enabled. The default derives from `orderer_rpc_port`.
    orderer_k8s_rpc_node_port: "{{ orderer_rpc_port }}"
    # NodePort used to expose the orderer metrics endpoint when NodePort exposure is enabled. The default derives from `orderer_metrics_port`.
    orderer_k8s_metrics_node_port: "{{ orderer_metrics_port }}"
    # Filesystem group applied to mounted ConfigMap and Secret volumes.
    orderer_k8s_fs_group: 10001
    # Full image reference used by the container and Kubernetes branches. The default derives from `orderer_registry_endpoint`, `orderer_image_name`, and `orderer_image_tag`.
    orderer_image: "{{ orderer_registry_endpoint }}/{{ orderer_image_name }}:{{ orderer_image_tag }}"
    # Registry prefix used to build the orderer image reference. The default derives from `ORDERER_REGISTRY_ENDPOINT`.
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
    # Client identifiers whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_clients: ["entry1", "entry2"]
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_orgs: [{}]
    # Organization metadata shared by the orderer crypto and config branches.
    organization: {}
    # Kubernetes namespace used for orderer resources.
    k8s_namespace: "string"
    # PVC storage request used by the orderer StatefulSet.
    k8s_storage_size: "string"
    # Optional storage class used by the StatefulSet PVC.
    k8s_storage_class: "string"
    # Optional image pull secret used by the StatefulSet.
    k8s_image_pull_secret: "string"
    # Optional readiness probe initial delay override.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Optional readiness probe period override.
    k8s_readiness_probe_period_seconds: 1000
    # Optional readiness probe timeout override.
    k8s_readiness_probe_timeout_seconds: 1000
    # Optional readiness probe failure threshold override.
    k8s_readiness_probe_failure_threshold: 1000
    # Optional liveness probe initial delay override.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Optional liveness probe period override.
    k8s_liveness_probe_period_seconds: 1000
    # Optional liveness probe timeout override.
    k8s_liveness_probe_timeout_seconds: 1000
    # Optional liveness probe failure threshold override.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/start
```

<a id="task-k8s-ping"></a>

### k8s/ping

Check the orderer Kubernetes Service ports


Checks the Kubernetes NodePort endpoints when NodePort exposure is enabled.


```yaml
- name: Check the orderer Kubernetes Service ports
  vars:
    # Enables the optional NodePort Service for the orderer Kubernetes deployment. The NodePort Service and Kubernetes ping branch use this toggle.
    orderer_k8s_use_node_port: false
    # NodePort used to expose the orderer gRPC service when NodePort exposure is enabled. The default derives from `orderer_rpc_port`.
    orderer_k8s_rpc_node_port: "{{ orderer_rpc_port }}"
    # NodePort used to expose the orderer metrics endpoint when NodePort exposure is enabled. The default derives from `orderer_metrics_port`.
    orderer_k8s_metrics_node_port: "{{ orderer_metrics_port }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/ping
```

<a id="task-k8s-rm"></a>

### k8s/rm

Remove the orderer Kubernetes workload


Deletes the orderer StatefulSet and Services from Kubernetes.


```yaml
- name: Remove the orderer Kubernetes workload
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service. The default derives from `inventory_hostname`.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for orderer resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/rm
```

<a id="task-k8s-teardown"></a>

### k8s/teardown

Remove the orderer Kubernetes workload and data


Deletes the Kubernetes workload and removes persisted orderer data.


```yaml
- name: Remove the orderer Kubernetes workload and data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/teardown
```

<a id="task-k8s-fetch_logs"></a>

### k8s/fetch_logs

Fetch logs from the orderer Kubernetes pod


Collects logs from pods selected by the orderer Kubernetes app label.


```yaml
- name: Fetch logs from the orderer Kubernetes pod
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service. The default derives from `inventory_hostname`.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/fetch_logs
```

<a id="task-k8s-config-transfer"></a>

### k8s/config/transfer

Create the orderer Kubernetes ConfigMap


Slurps the genesis block and renders the orderer ConfigMap, including optional mTLS CA bundles.


```yaml
- name: Create the orderer Kubernetes ConfigMap
  vars:
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service. The default derives from `inventory_hostname`.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Orderer component to start.
    orderer_component_type: "string"
    # Rendered orderer configuration filename.
    orderer_config_file: node_config.yaml
    # Enables client mutual TLS in the rendered config.
    orderer_use_mtls: false
    # Client identifiers whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_clients: ["entry1", "entry2"]
    # Organization dictionaries whose mTLS CA certificates are mounted or transferred.
    orderer_mtls_orgs: [{}]
    # Kubernetes namespace used for orderer resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/config/transfer
```

<a id="task-k8s-config-rm"></a>

### k8s/config/rm

Remove the orderer Kubernetes ConfigMap


Deletes the ConfigMap that holds orderer configuration and genesis material.


```yaml
- name: Remove the orderer Kubernetes ConfigMap
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service. The default derives from `inventory_hostname`.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for orderer resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/config/rm
```

<a id="task-k8s-crypto-transfer"></a>

### k8s/crypto/transfer

Create the orderer Kubernetes Secret


Resolves the orderer crypto file locations and renders the Kubernetes Secret containing MSP and TLS material.


```yaml
- name: Create the orderer Kubernetes Secret
  vars:
    # Shared base directory for generated configuration.
    remote_config_dir: "string"
    # Remote directory where orderer configuration is written. The default derives from `remote_config_dir`.
    orderer_remote_config_dir: "{{ remote_config_dir }}"
    # Organization metadata shared by the orderer crypto and config branches.
    organization: {}
    # Orderer identity name used to derive crypto artifact paths. The default derives from `organization.orderer.name` and falls back to `inventory_hostname`.
    orderer_crypto_name: "{{ organization.orderer.name | default(inventory_hostname) }}"
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service. The default derives from `inventory_hostname`.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Orderer component to start.
    orderer_component_type: "string"
    # Kubernetes namespace used for orderer resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/crypto/transfer
```

<a id="task-k8s-crypto-rm"></a>

### k8s/crypto/rm

Remove the orderer Kubernetes Secret


Deletes the Secret that stores orderer MSP and TLS material.


```yaml
- name: Remove the orderer Kubernetes Secret
  vars:
    # Base name used for the orderer Kubernetes objects, including the optional NodePort Service. The default derives from `inventory_hostname`.
    orderer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for orderer resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: k8s/crypto/rm
```

<a id="task-prometheus-get_scrapers"></a>

### prometheus/get_scrapers

Build Prometheus scrape targets for orderer hosts


Groups orderer hosts by component type and exposes Prometheus scrape service definitions for downstream monitoring configuration.


```yaml
- name: Build Prometheus scrape targets for orderer hosts
  vars:
    # Inventory hosts dedicated to orderer nodes.
    orderer_hosts: ["entry1", "entry2"]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: prometheus/get_scrapers
```


