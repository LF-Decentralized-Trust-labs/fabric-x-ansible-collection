# hyperledger.fabricx.loadgen

> Runs a Load Generator to test Fabric-X network throughput.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)
  - [get_metrics](#get_metrics)
  - [limit_rate](#limit_rate)
  - [prometheus/get_scrapers](#prometheusget_scrapers)
  - [config/transfer](#configtransfer)
  - [config/mtls/monitoring/transfer](#configmtlsmonitoringtransfer)
  - [config/rm](#configrm)
  - [crypto/setup](#cryptosetup)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric_ca/enroll](#cryptofabric_caenroll)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [bin/build](#binbuild)
  - [bin/install](#bininstall)
  - [bin/rm](#binrm)
  - [bin/start](#binstart)
  - [bin/stop](#binstop)
  - [bin/transfer](#bintransfer)
  - [bin/fetch_logs](#binfetch_logs)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch_logs](#containerfetch_logs)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch_logs](#k8sfetch_logs)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### start

Start the load generator

Start the Loadgen runtime selected by the runtime mode flags.

```yaml
- name: Start the load generator
  vars:
    # Run the container runtime. The default derives from `loadgen_use_bin` and `loadgen_use_k8s`.
    loadgen_use_container: "{{ (not loadgen_use_bin) and (not loadgen_use_k8s) }}"
    # Run the binary runtime.
    loadgen_use_bin: false
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: start
```

### stop

Stop the load generator

Stop the active Loadgen runtime selected by the runtime mode flags.

```yaml
- name: Stop the load generator
  vars:
    # Run the container runtime. The default derives from `loadgen_use_bin` and `loadgen_use_k8s`.
    loadgen_use_container: "{{ (not loadgen_use_bin) and (not loadgen_use_k8s) }}"
    # Run the binary runtime.
    loadgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: stop
```

### teardown

Remove runtime artifacts

Remove runtime resources for the active Loadgen deployment mode.

```yaml
- name: Remove runtime artifacts
  vars:
    # Run the container runtime. The default derives from `loadgen_use_bin` and `loadgen_use_k8s`.
    loadgen_use_container: "{{ (not loadgen_use_bin) and (not loadgen_use_k8s) }}"
    # Run the binary runtime.
    loadgen_use_bin: false
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: teardown
```

### wipe

Remove all load generator data

Remove runtime resources, binary artifacts, crypto material, and generated configuration.

```yaml
- name: Remove all load generator data
  vars:
    # Run the binary runtime.
    loadgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: wipe
```

### fetch_logs

Collect runtime logs

Collect Loadgen logs for the active runtime mode.

```yaml
- name: Collect runtime logs
  vars:
    # Run the container runtime. The default derives from `loadgen_use_bin` and `loadgen_use_k8s`.
    loadgen_use_container: "{{ (not loadgen_use_bin) and (not loadgen_use_k8s) }}"
    # Run the binary runtime.
    loadgen_use_bin: false
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: fetch_logs
```

### ping

Check the HTTP endpoint

Verify that the Loadgen HTTP control port is reachable.

```yaml
- name: Check the HTTP endpoint
  vars:
    # HTTP control port exposed by Loadgen.
    loadgen_web_port: 1000
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: ping
```

### get_metrics

Fetch exported metrics

Query the Loadgen metrics endpoint.

```yaml
- name: Fetch exported metrics
  vars:
    # Canonical host name used for metrics and Fabric CA enrollment.
    actual_host: "string"
    # Prometheus metrics port exposed by Loadgen.
    loadgen_metrics_port: 1000
    # NodePort used for the metrics port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_metrics_port`.
    loadgen_k8s_metrics_node_port: "{{ loadgen_metrics_port }}"
    # Protocol used to reach the monitoring endpoint.
    loadgen_monitoring_http_protocol: "{{ 'https' if loadgen_monitoring_use_tls else 'http' }}"
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Assert the latency metric when fetching metrics.
    loadgen_assert_metrics: false
    # Use Kubernetes resources.
    loadgen_use_k8s: false
    # Expose the Kubernetes Service via NodePort when `loadgen_use_k8s` is enabled. This drives the HTTP, metrics, and gRPC NodePort access paths.
    loadgen_k8s_use_node_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: get_metrics
```

### limit_rate

Update the runtime rate limit

Send an HTTP request that updates the generated transaction rate.

```yaml
- name: Update the runtime rate limit
  vars:
    # Canonical host name used for metrics and Fabric CA enrollment.
    actual_host: "string"
    # HTTP control port exposed by Loadgen.
    loadgen_web_port: 1000
    # NodePort used for the HTTP control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_web_port`.
    loadgen_k8s_web_node_port: "{{ loadgen_web_port }}"
    # Maximum generated transaction rate.
    loadgen_limit_rate: 10
    # Use Kubernetes resources.
    loadgen_use_k8s: false
    # Expose the Kubernetes Service via NodePort when `loadgen_use_k8s` is enabled. This drives the HTTP, metrics, and gRPC NodePort access paths.
    loadgen_k8s_use_node_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: limit_rate
```

### prometheus/get_scrapers

Build Prometheus scrape targets

Build the Prometheus scrape service definition for all Loadgen hosts.

```yaml
- name: Build Prometheus scrape targets
  vars:
    # Inventory hosts running Loadgen instances.
    loadgen_hosts: ["entry1", "entry2"]
    # Local artifacts directory used for fetched TLS and MSP files.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: prometheus/get_scrapers
```

### config/transfer

Dispatch configuration rendering

Render and transfer Loadgen configuration.

```yaml
- name: Dispatch configuration rendering
  vars:
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Config mount path inside a container or pod.
    loadgen_container_config_dir: /config
    # Effective config directory used inside rendered Loadgen configuration. The default derives from `loadgen_remote_config_dir`, `loadgen_use_bin`, and `loadgen_container_config_dir`.
    loadgen_config_dir: "{{ loadgen_remote_config_dir if loadgen_use_bin else loadgen_container_config_dir }}"
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # Run the binary runtime.
    loadgen_use_bin: false
    # Use Kubernetes resources.
    loadgen_use_k8s: false
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
    # Enable mTLS for the main endpoint.
    loadgen_use_mtls: false
    # Committer inventory hosts used by the dispatcher to derive client targets.
    committer_hosts: ["entry1", "entry2"]
    # Orderer inventory hosts used by the dispatcher to derive client targets.
    orderer_hosts: ["entry1", "entry2"]
    # Additional mTLS client identities trusted by the main endpoint.
    loadgen_mtls_clients: ["entry1", "entry2"]
    # Additional mTLS organizations trusted by the main endpoint.
    loadgen_mtls_orgs: [{}]
    # Additional mTLS client identities trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_clients: ["entry1", "entry2"]
    # Additional mTLS organizations trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_orgs: [{}]
    # HTTP control port exposed by Loadgen.
    loadgen_web_port: 1000
    # Prometheus metrics port exposed by Loadgen.
    loadgen_metrics_port: 1000
    # gRPC control port exposed by Loadgen.
    loadgen_rpc_port: 1000
    # Render the config transaction block section.
    loadgen_generate_config_block: false
    # Render the namespace creation section.
    loadgen_generate_namespace: false
    # Render the transaction load section.
    loadgen_generate_load: false
    # Generated key size in bytes.
    loadgen_key_size: 1000
    # Random seed used to build repeatable transaction streams.
    loadgen_tx_seed: 1000
    # Worker goroutine count used by the load profile.
    loadgen_workers: 1000
    # Maximum generated block size.
    loadgen_block_max_size: 1000
    # Minimum generated block size.
    loadgen_block_min_size: 1000
    # Preferred block flush interval.
    loadgen_block_preferred_rate: "string"
    # Enable read-only transactions in the load profile.
    loadgen_generate_read_only_tx: false
    # Read-only key count per transaction.
    loadgen_read_only_tx_keys: 1000
    # Enable write-only transactions in the load profile.
    loadgen_generate_write_only_tx: false
    # Write-only key count per transaction.
    loadgen_write_only_tx_keys: 1000
    # Write-only value size in bytes.
    loadgen_write_only_tx_val_size: 1000
    # Enable read-write transactions in the load profile.
    loadgen_generate_read_write_tx: false
    # Read-write key count per transaction.
    loadgen_read_write_tx_keys: 1000
    # Read-write value size in bytes.
    loadgen_read_write_tx_val_size: 1000
    # Signature scheme used for generated identities.
    loadgen_key_scheme: "string"
    # Monitoring endpoint rate limit in requests per second.
    loadgen_monitoring_rate_limit_requests_per_second: 1000
    # Monitoring endpoint rate limit burst size.
    loadgen_monitoring_rate_limit_burst: 1000
    # Prefix used by the latency sampler.
    loadgen_latency_sampler_prefix: "string"
    # Portion of transactions sampled for latency tracking.
    loadgen_latency_sampler_portion: 1000
    # Histogram distribution used for latency buckets.
    loadgen_latency_distribution: "string"
    # Upper latency bound tracked by the histogram.
    loadgen_max_latency: "string"
    # Number of latency histogram buckets.
    loadgen_latency_buckets: 1000
    # Maximum generated transaction rate.
    loadgen_limit_rate: 10
    # Batch size used by the stream pipeline.
    loadgen_stream_batches: 1000
    # Channel buffer size used by the stream pipeline.
    loadgen_stream_buffers_size: 1000
    # Log level specification.
    loadgen_log_level: info
    # Log message format template.
    loadgen_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Local artifacts directory used for fetched TLS and MSP files.
    fetched_artifacts_dir: "string"
    # Channel identifier rendered into generated transactions.
    channel_id: "string"
    # Organization definition consumed by crypto, config, and Kubernetes templates.
    organization: {}
    # Orderer router hosts targeted by the orderer client.
    orderer_router_hosts: ["entry1", "entry2"]
    # Orderer assembler hosts targeted by the orderer client.
    orderer_assembler_hosts: ["entry1", "entry2"]
    # Sidecar host targeted by the orderer and sidecar clients.
    committer_sidecar_host: "string"
    # Broadcast goroutine count used by the orderer client.
    loadgen_broadcast_parallelism: 1000
    # Optional stopping limit for generated blocks.
    loadgen_limit_blocks: 1000
    # Optional stopping limit for generated transactions.
    loadgen_limit_transactions: 1000
    # Enable mTLS for the monitoring endpoint. The default mirrors `loadgen_use_mtls`.
    loadgen_monitoring_use_mtls: "{{ loadgen_use_mtls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/transfer
```

### config/mtls/monitoring/transfer

Transfer monitoring mTLS CA bundles

Transfer CA bundles trusted by the monitoring endpoint.

```yaml
- name: Transfer monitoring mTLS CA bundles
  vars:
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Local artifacts directory used for fetched TLS and MSP files.
    fetched_artifacts_dir: "string"
    # Additional mTLS client identities trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_clients: ["entry1", "entry2"]
    # Additional mTLS organizations trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_orgs: [{}]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/mtls/monitoring/transfer
```

### config/rm

Remove rendered configuration

Remove host-side configuration files and optionally the Kubernetes ConfigMap.

```yaml
- name: Remove rendered configuration
  vars:
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/rm
```

### crypto/setup

Prepare crypto material

Prepare the Loadgen MSP and TLS artifacts using cryptogen or Fabric CA.

```yaml
- name: Prepare crypto material
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates.
    organization: {}
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/setup
```

### crypto/cryptogen/transfer

Transfer cryptogen artifacts

Transfer MSP and TLS artifacts generated by cryptogen to the Loadgen host.

```yaml
- name: Transfer cryptogen artifacts
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates.
    organization: {}
    # Local cryptogen output directory.
    cryptogen_artifacts_dir: "string"
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

Enroll identities with Fabric CA

Enroll the Loadgen peer and user identities against Fabric CA.

```yaml
- name: Enroll identities with Fabric CA
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates.
    organization: {}
    # Local artifacts directory used for fetched TLS and MSP files.
    fetched_artifacts_dir: "string"
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Canonical host name used for metrics and Fabric CA enrollment.
    actual_host: "string"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/fabric_ca/enroll
```

### crypto/fetch

Fetch generated certificates

Fetch Loadgen MSP signcerts and TLS certificates back to the control node.

```yaml
- name: Fetch generated certificates
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates.
    organization: {}
    # Local artifacts directory used for fetched TLS and MSP files.
    fetched_artifacts_dir: "string"
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/fetch
```

### crypto/rm

Remove crypto material

Remove Loadgen MSP and TLS artifacts from the host and optionally from Kubernetes.

```yaml
- name: Remove crypto material
  vars:
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/rm
```

### bin/build

Build the load generator binary

Build the Loadgen binary from source through the shared bin role.

```yaml
- name: Build the load generator binary
  vars:
    # Binary name used by the shared bin role.
    loadgen_bin_name: loadgen
    # Git host used for binary builds.
    loadgen_git_hub_url: github.com
    # Git repository that provides the Loadgen source.
    loadgen_git_repo: hyperledger/fabric-x-committer
    # Git revision used for binary builds and installs.
    loadgen_git_commit: v0.1.9
    # Go package path for the Loadgen binary.
    loadgen_source_code_package: cmd/loadgen
    # Go package used for binary installation. The default derives from `loadgen_git_hub_url`, `loadgen_git_repo`, and `loadgen_source_code_package`.
    loadgen_bin_package: "{{ loadgen_git_hub_url }}/{{ loadgen_git_repo }}/{{ loadgen_source_code_package }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/build
```

### bin/install

Install the load generator binary

Install the Loadgen binary through the shared bin role.

```yaml
- name: Install the load generator binary
  vars:
    # Binary name used by the shared bin role.
    loadgen_bin_name: loadgen
    # Go package used for binary installation. The default derives from `loadgen_git_hub_url`, `loadgen_git_repo`, and `loadgen_source_code_package`.
    loadgen_bin_package: "{{ loadgen_git_hub_url }}/{{ loadgen_git_repo }}/{{ loadgen_source_code_package }}"
    # Git host used for binary builds.
    loadgen_git_hub_url: github.com
    # Git repository that provides the Loadgen source.
    loadgen_git_repo: hyperledger/fabric-x-committer
    # Git revision used for binary builds and installs.
    loadgen_git_commit: v0.1.9
    # Go package path for the Loadgen binary.
    loadgen_source_code_package: cmd/loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/install
```

### bin/rm

Remove the load generator binary

Remove the installed Loadgen binary.

```yaml
- name: Remove the load generator binary
  vars:
    # Binary name used by the shared bin role.
    loadgen_bin_name: loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/rm
```

### bin/start

Start the binary runtime

Start the Loadgen as a local binary process.

```yaml
- name: Start the binary runtime
  vars:
    # Binary name used by the shared bin role.
    loadgen_bin_name: loadgen
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # HTTP control port exposed by Loadgen.
    loadgen_web_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/start
```

### bin/stop

Stop the binary runtime

Stop the Loadgen binary process.

```yaml
- name: Stop the binary runtime
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/stop
```

### bin/transfer

Transfer the load generator binary

Transfer the Loadgen binary through the shared bin role.

```yaml
- name: Transfer the load generator binary
  vars:
    # Binary name used by the shared bin role.
    loadgen_bin_name: loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/transfer
```

### bin/fetch_logs

Fetch binary logs

Collect logs from a binary-based Loadgen runtime.

```yaml
- name: Fetch binary logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/fetch_logs
```

### container/start

Start the container runtime

Start the Loadgen as a local container.

```yaml
- name: Start the container runtime
  vars:
    # Container name used by the runtime.
    loadgen_container_name: "{{ inventory_hostname }}"
    # Loadgen container image. The default derives from `loadgen_registry_endpoint`, `loadgen_image_name`, and `loadgen_image_tag`.
    loadgen_image: "{{ loadgen_registry_endpoint }}/{{ loadgen_image_name }}:{{ loadgen_image_tag }}"
    # Image registry endpoint.
    loadgen_registry_endpoint: "{{ lookup('env', 'LOADGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image name used by the Loadgen container.
    loadgen_image_name: fabric-x-loadgen
    # Image tag used by the Loadgen container.
    loadgen_image_tag: 0.1.9
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Config mount path inside a container or pod.
    loadgen_container_config_dir: /config
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # HTTP control port exposed by Loadgen.
    loadgen_web_port: 1000
    # Prometheus metrics port exposed by Loadgen.
    loadgen_metrics_port: 1000
    # gRPC control port exposed by Loadgen.
    loadgen_rpc_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: container/start
```

### container/stop

Stop the container runtime

Stop the Loadgen container.

```yaml
- name: Stop the container runtime
  vars:
    # Container name used by the runtime.
    loadgen_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: container/stop
```

### container/rm

Remove the container runtime

Remove the Loadgen container and image reference.

```yaml
- name: Remove the container runtime
  vars:
    # Container name used by the runtime.
    loadgen_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: container/rm
```

### container/fetch_logs

Fetch container logs

Collect logs from a containerized Loadgen runtime.

```yaml
- name: Fetch container logs
  vars:
    # Container name used by the runtime.
    loadgen_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: container/fetch_logs
```

### k8s/start

Start the Kubernetes deployment

Create the Kubernetes Service, NodePort Service, and Deployment for the Loadgen.

```yaml
- name: Start the Kubernetes deployment
  vars:
    # Committer inventory hosts used by the dispatcher to derive client targets.
    committer_hosts: ["entry1", "entry2"]
    # Orderer inventory hosts used by the dispatcher to derive client targets.
    orderer_hosts: ["entry1", "entry2"]
    # Organization definition consumed by crypto, config, and Kubernetes templates.
    organization: {}
    # Loadgen container image. The default derives from `loadgen_registry_endpoint`, `loadgen_image_name`, and `loadgen_image_tag`.
    loadgen_image: "{{ loadgen_registry_endpoint }}/{{ loadgen_image_name }}:{{ loadgen_image_tag }}"
    # Image registry endpoint.
    loadgen_registry_endpoint: "{{ lookup('env', 'LOADGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image name used by the Loadgen container.
    loadgen_image_name: fabric-x-loadgen
    # Image tag used by the Loadgen container.
    loadgen_image_tag: 0.1.9
    # Config mount path inside a container or pod.
    loadgen_container_config_dir: /config
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # Deployment rollout wait timeout in seconds.
    loadgen_k8s_wait_timeout: 120
    # Pod FSGroup used for mounted config and secrets.
    loadgen_k8s_fs_group: 10001
    # Kubernetes namespace used for loadgen resources.
    k8s_namespace: "string"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
    # Enable mTLS for the main endpoint.
    loadgen_use_mtls: false
    # Enable mTLS for the monitoring endpoint. The default mirrors `loadgen_use_mtls`.
    loadgen_monitoring_use_mtls: "{{ loadgen_use_mtls }}"
    # Additional mTLS client identities trusted by the main endpoint.
    loadgen_mtls_clients: ["entry1", "entry2"]
    # Additional mTLS organizations trusted by the main endpoint.
    loadgen_mtls_orgs: [{}]
    # Additional mTLS client identities trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_clients: ["entry1", "entry2"]
    # Additional mTLS organizations trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_orgs: [{}]
    # Optional image pull secret used by Kubernetes workloads.
    k8s_image_pull_secret: "string"
    # Use Kubernetes resources.
    loadgen_use_k8s: false
    # Expose the Kubernetes Service via NodePort when `loadgen_use_k8s` is enabled. This drives the HTTP, metrics, and gRPC NodePort access paths.
    loadgen_k8s_use_node_port: false
    # HTTP control port exposed by Loadgen.
    loadgen_web_port: 1000
    # Prometheus metrics port exposed by Loadgen.
    loadgen_metrics_port: 1000
    # gRPC control port exposed by Loadgen.
    loadgen_rpc_port: 1000
    # NodePort used for the HTTP control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_web_port`.
    loadgen_k8s_web_node_port: "{{ loadgen_web_port }}"
    # NodePort used for the metrics port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_metrics_port`.
    loadgen_k8s_metrics_node_port: "{{ loadgen_metrics_port }}"
    # NodePort used for the gRPC control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_rpc_port`.
    loadgen_k8s_rpc_node_port: "{{ loadgen_rpc_port }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/start
```

### k8s/ping

Check the Kubernetes node ports

Verify that the Loadgen NodePort endpoints are reachable.

```yaml
- name: Check the Kubernetes node ports
  vars:
    # Expose the Kubernetes Service via NodePort when `loadgen_use_k8s` is enabled. This drives the HTTP, metrics, and gRPC NodePort access paths.
    loadgen_k8s_use_node_port: false
    # HTTP control port exposed by Loadgen.
    loadgen_web_port: 1000
    # Prometheus metrics port exposed by Loadgen.
    loadgen_metrics_port: 1000
    # gRPC control port exposed by Loadgen.
    loadgen_rpc_port: 1000
    # NodePort used for the HTTP control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_web_port`.
    loadgen_k8s_web_node_port: "{{ loadgen_web_port }}"
    # NodePort used for the metrics port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_metrics_port`.
    loadgen_k8s_metrics_node_port: "{{ loadgen_metrics_port }}"
    # NodePort used for the gRPC control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. The default mirrors `loadgen_rpc_port`.
    loadgen_k8s_rpc_node_port: "{{ loadgen_rpc_port }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/ping
```

### k8s/rm

Remove Kubernetes resources

Remove the Kubernetes Deployment and Services created for the Loadgen.

```yaml
- name: Remove Kubernetes resources
  vars:
    # Kubernetes namespace used for loadgen resources.
    k8s_namespace: "string"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/rm
```

### k8s/fetch_logs

Fetch pod logs

Collect logs from the Kubernetes pod running Loadgen.

```yaml
- name: Fetch pod logs
  vars:
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

Publish the Kubernetes ConfigMap

Publish the rendered Loadgen configuration and CA bundles as a ConfigMap.

```yaml
- name: Publish the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for loadgen resources.
    k8s_namespace: "string"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # Orderer router hosts targeted by the orderer client.
    orderer_router_hosts: ["entry1", "entry2"]
    # Orderer assembler hosts targeted by the orderer client.
    orderer_assembler_hosts: ["entry1", "entry2"]
    # Sidecar host targeted by the orderer and sidecar clients.
    committer_sidecar_host: "string"
    # Enable mTLS for the main endpoint.
    loadgen_use_mtls: false
    # Enable mTLS for the monitoring endpoint. The default mirrors `loadgen_use_mtls`.
    loadgen_monitoring_use_mtls: "{{ loadgen_use_mtls }}"
    # Additional mTLS client identities trusted by the main endpoint.
    loadgen_mtls_clients: ["entry1", "entry2"]
    # Additional mTLS organizations trusted by the main endpoint.
    loadgen_mtls_orgs: [{}]
    # Additional mTLS client identities trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_clients: ["entry1", "entry2"]
    # Additional mTLS organizations trusted by the monitoring endpoint.
    loadgen_monitoring_mtls_orgs: [{}]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

Remove the Kubernetes ConfigMap

Remove the ConfigMap created for the Loadgen configuration.

```yaml
- name: Remove the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for loadgen resources.
    k8s_namespace: "string"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

Publish the Kubernetes Secret

Publish the Loadgen MSP and TLS material as a Kubernetes Secret.

```yaml
- name: Publish the Kubernetes Secret
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates.
    organization: {}
    # Base remote config directory that feeds `loadgen_remote_config_dir`.
    remote_config_dir: "string"
    # Remote config directory used by Loadgen. The default derives from `remote_config_dir`.
    loadgen_remote_config_dir: "string"
    # Local artifacts directory used for fetched TLS and MSP files.
    fetched_artifacts_dir: "string"
    # Canonical host name used for metrics and Fabric CA enrollment.
    actual_host: "string"
    # Crypto identity name used for MSP and TLS file names. The default derives from `organization.peer.name` with `inventory_hostname` fallback.
    loadgen_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Kubernetes namespace used for loadgen resources.
    k8s_namespace: "string"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint. The default mirrors `loadgen_use_tls`.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

Remove the Kubernetes Secret

Remove the Secret created for Loadgen MSP and TLS material.

```yaml
- name: Remove the Kubernetes Secret
  vars:
    # Kubernetes namespace used for loadgen resources.
    k8s_namespace: "string"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/crypto/rm
```
