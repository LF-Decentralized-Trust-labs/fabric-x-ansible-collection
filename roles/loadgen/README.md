# hyperledger.fabricx.loadgen

> Deploys and manages the Fabric-X Load Generator across binary, container, and Kubernetes modes for workload, metrics, TLS, and log collection workflows.

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
  - [limit\_rate](#limit_rate)
  - [prometheus/get\_scrapers](#prometheusget_scrapers)
  - [config/transfer](#configtransfer)
  - [config/mtls/monitoring/transfer](#configmtlsmonitoringtransfer)
  - [config/rm](#configrm)
  - [crypto/setup](#cryptosetup)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric\_ca/enroll](#cryptofabric_caenroll)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [bin/build](#binbuild)
  - [bin/install](#bininstall)
  - [bin/rm](#binrm)
  - [bin/start](#binstart)
  - [bin/stop](#binstop)
  - [bin/transfer](#bintransfer)
  - [bin/fetch\_logs](#binfetch_logs)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.loadgen
```

## Tasks

### start

> Start the load generator

Start the Loadgen runtime selected by the deployment mode flags. Container mode is the default, binary mode starts the installed `loadgen` process, and Kubernetes mode applies Services and a Deployment. The runtime consumes the rendered Loadgen configuration and crypto material prepared by the config and crypto entry points.

```yaml
- name: Start the load generator
  vars:
    # Run the container runtime.
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

> Stop the load generator

Stop the active Loadgen runtime selected by the deployment mode flags. Stops the local binary process or container without removing configuration, crypto material, logs, or Kubernetes resources.

```yaml
- name: Stop the load generator
  vars:
    # Run the container runtime.
    loadgen_use_container: "{{ (not loadgen_use_bin) and (not loadgen_use_k8s) }}"
    # Run the binary runtime.
    loadgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: stop
```

### teardown

> Remove runtime artifacts

Remove runtime resources for the selected Loadgen deployment mode. Deletes the local container or Kubernetes workload resources while leaving generated config, crypto material, and fetched artifacts intact.

```yaml
- name: Remove runtime artifacts
  vars:
    # Run the container runtime.
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

> Remove all load generator data

Remove Loadgen runtime resources, binary artifacts, generated configuration, and crypto material from the host. Use this lifecycle entry point for a full role-local cleanup before rebuilding config or credentials.

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

> Collect runtime logs

Collect Loadgen logs for the selected deployment mode. Binary, container, and Kubernetes modes delegate to their mode-specific log collection tasks and store the fetched runtime output as role artifacts.

```yaml
- name: Collect runtime logs
  vars:
    # Run the container runtime.
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

> Check the HTTP endpoint

Verify that the Loadgen HTTP control endpoint is reachable. Uses direct host access for binary and container deployments and delegates to the Kubernetes ping task when `loadgen_use_k8s` is enabled.

```yaml
- name: Check the HTTP endpoint
  vars:
    # HTTP control port exposed by Loadgen. Example: `8080`.
    loadgen_web_port: 8080
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: ping
```

### get_metrics

> Fetch exported metrics

Query the Loadgen Prometheus metrics endpoint over HTTP or HTTPS. In Kubernetes NodePort mode, targets the configured metrics NodePort; otherwise, it uses the host metrics port and selected monitoring protocol.

```yaml
- name: Fetch exported metrics
  vars:
    # Canonical host name used for metrics and Fabric CA enrollment. Example: `loadgen1.example.com`.
    actual_host: "loadgen1.example.com"
    # Prometheus metrics port exposed by Loadgen. Example: `9443`.
    loadgen_metrics_port: 9443
    # NodePort used for the metrics port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30090`.
    loadgen_k8s_metrics_node_port: 30090
    # Protocol used to reach the monitoring endpoint.
    loadgen_monitoring_http_protocol: "{{ 'https' if loadgen_monitoring_use_tls else 'http' }}"
    # Enable TLS for the monitoring endpoint.
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

> Update the runtime rate limit

Send a control-plane HTTP request that changes the active generated transaction rate. Supports host ports for binary and container deployments and the configured HTTP NodePort for Kubernetes access.

```yaml
- name: Update the runtime rate limit
  vars:
    # Canonical host name used for metrics and Fabric CA enrollment. Example: `loadgen1.example.com`.
    actual_host: "loadgen1.example.com"
    # HTTP control port exposed by Loadgen. Example: `8080`.
    loadgen_web_port: 8080
    # NodePort used for the HTTP control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30080`.
    loadgen_k8s_web_node_port: 30080
    # Maximum generated transaction rate. Example: `2500`.
    loadgen_limit_rate: 2500
    # Use Kubernetes resources.
    loadgen_use_k8s: false
    # Expose the Kubernetes Service via NodePort when `loadgen_use_k8s` is enabled. This drives the HTTP, metrics, and gRPC NodePort access paths.
    loadgen_k8s_use_node_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: limit_rate
```

### prometheus/get_scrapers

> Build Prometheus scrape targets

Build Prometheus scrape target definitions for all Loadgen hosts. Includes monitoring endpoint and TLS artifact paths consumed by the Prometheus role when scraping Loadgen metrics.

```yaml
- name: Build Prometheus scrape targets
  vars:
    # Inventory hosts running Loadgen instances. Example: `['loadgen1', 'loadgen2']`.
    loadgen_hosts:
      - "loadgen1"
      - "loadgen2"
    # Local artifacts directory used for fetched TLS and MSP files. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: prometheus/get_scrapers
```

### config/transfer

> Dispatch configuration rendering

Render the Loadgen configuration file and transfer config-side support artifacts. The generated config contains orderer router and assembler targets, optional committer sidecar access, TLS and mTLS paths, workload profile settings, stream limits, and logging behavior. For Kubernetes deployments, also publishes the rendered config and trusted CA bundles as a ConfigMap.

```yaml
- name: Dispatch configuration rendering
  vars:
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Config mount path inside a container or pod.
    loadgen_container_config_dir: /config
    # Effective config directory used inside rendered Loadgen configuration.
    loadgen_config_dir: "{{ loadgen_remote_config_dir if loadgen_use_bin else loadgen_container_config_dir }}"
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # Run the binary runtime.
    loadgen_use_bin: false
    # Use Kubernetes resources.
    loadgen_use_k8s: false
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
    # Enable mTLS for the main endpoint.
    loadgen_use_mtls: false
    # Committer inventory hosts used by the dispatcher to derive client targets. Example: `['committer-sidecar1', 'committer-validator1']`.
    committer_hosts:
      - "committer-sidecar1"
      - "committer-validator1"
    # Orderer inventory hosts used by the dispatcher to derive client targets. Example: `['orderer-router1', 'orderer-assembler1']`.
    orderer_hosts:
      - "orderer-router1"
      - "orderer-assembler1"
    # Additional mTLS client identities trusted by the main endpoint. Example: `['orderer-router1', 'committer-sidecar1']`.
    loadgen_mtls_clients:
      - "orderer-router1"
      - "committer-sidecar1"
    # Additional mTLS organizations trusted by the main endpoint. Example: `[{'domain': 'org1.example.com'}, {'domain': 'org2.example.com'}]`.
    loadgen_mtls_orgs:
      - domain: "org1.example.com"
      - domain: "org2.example.com"
    # Additional mTLS client identities trusted by the monitoring endpoint. Example: `['prometheus1', 'node-exporter1']`.
    loadgen_monitoring_mtls_clients:
      - "prometheus1"
      - "node-exporter1"
    # Additional mTLS organizations trusted by the monitoring endpoint. Example: `[{'domain': 'monitoring.example.com'}]`.
    loadgen_monitoring_mtls_orgs:
      - domain: "monitoring.example.com"
    # HTTP control port exposed by Loadgen. Example: `8080`.
    loadgen_web_port: 8080
    # Prometheus metrics port exposed by Loadgen. Example: `9443`.
    loadgen_metrics_port: 9443
    # gRPC control port exposed by Loadgen. Example: `7051`.
    loadgen_rpc_port: 7051
    # Render the config transaction block section.
    loadgen_generate_config_block: false
    # Render the namespace creation section. Example: `true` when the workload should create namespace records before sending load.
    loadgen_generate_namespace: false
    # Render the transaction load section. Example: `true` for a normal benchmark workload.
    loadgen_generate_load: false
    # Generated key size in bytes. Example: `32`.
    loadgen_key_size: 32
    # Random seed used to build repeatable transaction streams. Example: `12345`.
    loadgen_tx_seed: 12345
    # Worker goroutine count used by the load profile. Example: `16`.
    loadgen_workers: 16
    # Maximum generated block size. Example: `500`.
    loadgen_block_max_size: 500
    # Minimum generated block size. Example: `1`.
    loadgen_block_min_size: 1
    # Preferred block flush interval. Example: `1s`.
    loadgen_block_preferred_rate: "1s"
    # Enable read-only transactions in the load profile. Example: `true` to include read-only query traffic.
    loadgen_generate_read_only_tx: false
    # Read-only key count per transaction. Example: `2`.
    loadgen_read_only_tx_keys: 2
    # Enable write-only transactions in the load profile. Example: `true` to include blind-write traffic.
    loadgen_generate_write_only_tx: false
    # Write-only key count per transaction. Example: `4`.
    loadgen_write_only_tx_keys: 4
    # Write-only value size in bytes. Example: `256`.
    loadgen_write_only_tx_val_size: 256
    # Enable read-write transactions in the load profile. Example: `true` to include endorsement-style read-write traffic.
    loadgen_generate_read_write_tx: false
    # Read-write key count per transaction. Example: `2`.
    loadgen_read_write_tx_keys: 2
    # Read-write value size in bytes. Example: `128`.
    loadgen_read_write_tx_val_size: 128
    # Signature scheme used for generated identities. Example: `ECDSA`.
    loadgen_key_scheme: "ECDSA"
    # Monitoring endpoint rate limit in requests per second. Example: `50`.
    loadgen_monitoring_rate_limit_requests_per_second: 50
    # Monitoring endpoint rate limit burst size. Example: `100`.
    loadgen_monitoring_rate_limit_burst: 100
    # Prefix used by the latency sampler. Example: `loadgen_lg_1`.
    loadgen_latency_sampler_prefix: "loadgen_lg_1"
    # Portion of transactions sampled for latency tracking. Example: `0.01`.
    loadgen_latency_sampler_portion: 0.01
    # Histogram distribution used for latency buckets. Example: `uniform`.
    loadgen_latency_distribution: "uniform"
    # Upper latency bound tracked by the histogram. Example: `5s`.
    loadgen_max_latency: "5s"
    # Number of latency histogram buckets. Example: `1000`.
    loadgen_latency_buckets: 1000
    # Maximum generated transaction rate. Example: `2500`.
    loadgen_limit_rate: 2500
    # Batch size used by the stream pipeline. Example: `10`.
    loadgen_stream_batches: 10
    # Channel buffer size used by the stream pipeline. Example: `64`.
    loadgen_stream_buffers_size: 64
    # Log level specification.
    loadgen_log_level: info
    # Log message format template.
    loadgen_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Local artifacts directory used for fetched TLS and MSP files. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
    # Channel identifier rendered into generated transactions. Example: `fabricx-channel`.
    channel_id: "fabricx-channel"
    # Organization definition consumed by crypto, config, and Kubernetes templates. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'loadgen1', 'secret': 'loadgen1pw'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "loadgen1"
        secret: "loadgen1pw"
    # Orderer router hosts targeted by the orderer client. Example: `['orderer-router1', 'orderer-router2']`.
    orderer_router_hosts:
      - "orderer-router1"
      - "orderer-router2"
    # Orderer assembler hosts targeted by the orderer client. Example: `['orderer-assembler1', 'orderer-assembler2']`.
    orderer_assembler_hosts:
      - "orderer-assembler1"
      - "orderer-assembler2"
    # Sidecar host targeted by the orderer and sidecar clients. Example: `committer-sidecar1`.
    committer_sidecar_host: "committer-sidecar1"
    # Broadcast goroutine count used by the orderer client. Example: `8`.
    loadgen_broadcast_parallelism: 8
    # Optional stopping limit for generated blocks. Example: `100`.
    loadgen_limit_blocks: 100
    # Optional stopping limit for generated transactions. Example: `100000`.
    loadgen_limit_transactions: 100000
    # Enable mTLS for the monitoring endpoint.
    loadgen_monitoring_use_mtls: "{{ loadgen_use_mtls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/transfer
```

### config/mtls/monitoring/transfer

> Transfer monitoring mTLS CA bundles

Transfer CA bundles trusted by the Loadgen monitoring endpoint. Copies client and organization CA files into the config tree so the metrics listener can verify Prometheus or other monitoring clients when mTLS is enabled.

```yaml
- name: Transfer monitoring mTLS CA bundles
  vars:
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Local artifacts directory used for fetched TLS and MSP files. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
    # Additional mTLS client identities trusted by the monitoring endpoint. Example: `['prometheus1', 'node-exporter1']`.
    loadgen_monitoring_mtls_clients:
      - "prometheus1"
      - "node-exporter1"
    # Additional mTLS organizations trusted by the monitoring endpoint. Example: `[{'domain': 'monitoring.example.com'}]`.
    loadgen_monitoring_mtls_orgs:
      - domain: "monitoring.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/mtls/monitoring/transfer
```

### config/rm

> Remove rendered configuration

Remove host-side rendered Loadgen configuration. Also removes the Kubernetes ConfigMap when Kubernetes deployment mode is enabled.

```yaml
- name: Remove rendered configuration
  vars:
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/rm
```

### crypto/setup

> Prepare crypto material

Prepare Loadgen MSP, user, and TLS material through the configured crypto source. Delegates to cryptogen transfer or Fabric CA enrollment, then publishes Kubernetes Secret material when Kubernetes mode is enabled.

```yaml
- name: Prepare crypto material
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'loadgen1', 'secret': 'loadgen1pw'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "loadgen1"
        secret: "loadgen1pw"
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/setup
```

### crypto/cryptogen/transfer

> Transfer cryptogen artifacts

Transfer MSP, user, and TLS artifacts generated by cryptogen to the Loadgen host config directory. The copied paths are consumed by the rendered orderer client, sidecar client, server, and monitoring TLS sections.

```yaml
- name: Transfer cryptogen artifacts
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'loadgen1', 'secret': 'loadgen1pw'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "loadgen1"
        secret: "loadgen1pw"
    # Local cryptogen output directory. Example: `/tmp/fabricx-crypto`.
    cryptogen_artifacts_dir: "/tmp/fabricx-crypto"
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

> Enroll identities with Fabric CA

Enroll Loadgen peer, user, and optional TLS identities against Fabric CA. Writes MSP and TLS artifacts under the remote config directory for use by the generated Loadgen config and later fetch or Kubernetes transfer tasks.

```yaml
- name: Enroll identities with Fabric CA
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'loadgen1', 'secret': 'loadgen1pw'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "loadgen1"
        secret: "loadgen1pw"
    # Local artifacts directory used for fetched TLS and MSP files. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Canonical host name used for metrics and Fabric CA enrollment. Example: `loadgen1.example.com`.
    actual_host: "loadgen1.example.com"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/fabric_ca/enroll
```

### crypto/fetch

> Fetch generated certificates

Fetch generated Loadgen MSP signcerts and TLS certificates back to the control node. Stores artifacts under the fetched artifacts directory so other roles can trust Loadgen endpoints or reuse generated crypto outputs.

```yaml
- name: Fetch generated certificates
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'loadgen1', 'secret': 'loadgen1pw'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "loadgen1"
        secret: "loadgen1pw"
    # Local artifacts directory used for fetched TLS and MSP files. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove crypto material

Remove Loadgen MSP, user, and TLS artifacts from the host config directory. Also removes the Kubernetes Secret when Kubernetes deployment mode is enabled.

```yaml
- name: Remove crypto material
  vars:
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
    # Use Kubernetes resources.
    loadgen_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/rm
```

### bin/build

> Build the load generator binary

Build the `loadgen` binary from the configured Fabric-X source repository. Uses the shared binary helper role and the configured Git host, repository, revision, and Go package path.

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
    # Go package used for binary installation.
    loadgen_bin_package: "{{ loadgen_git_hub_url }}/{{ loadgen_git_repo }}/{{ loadgen_source_code_package }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/build
```

### bin/install

> Install the load generator binary

Install the `loadgen` binary through the shared binary helper role. Consumes the configured Go package and source revision so binary deployments can start the local process.

```yaml
- name: Install the load generator binary
  vars:
    # Binary name used by the shared bin role.
    loadgen_bin_name: loadgen
    # Go package used for binary installation.
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

> Remove the load generator binary

Remove the installed `loadgen` binary managed by the shared binary helper role. Does not remove generated configuration, crypto material, or runtime logs.

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

> Start the binary runtime

Start Loadgen as a local binary process using the rendered config file. Waits on the HTTP control port after invoking `loadgen start --config=...`.

```yaml
- name: Start the binary runtime
  vars:
    # Binary name used by the shared bin role.
    loadgen_bin_name: loadgen
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # HTTP control port exposed by Loadgen. Example: `8080`.
    loadgen_web_port: 8080
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/start
```

### bin/stop

> Stop the binary runtime

Stop the local Loadgen binary process managed by the shared binary helper role. Leaves the remote config directory and logs available for inspection or collection.

```yaml
- name: Stop the binary runtime
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/stop
```

### bin/transfer

> Transfer the load generator binary

Transfer a prebuilt `loadgen` binary through the shared binary helper role. Used by binary deployments when the executable is built elsewhere and then staged onto the target host.

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

> Fetch binary logs

Collect logs emitted by a binary-based Loadgen runtime. Fetches process logs without changing the running state or removing generated artifacts.

```yaml
- name: Fetch binary logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: bin/fetch_logs
```

### container/start

> Start the container runtime

Start Loadgen as a local container with the rendered config directory mounted read-only. Exposes the HTTP, Prometheus metrics, and gRPC ports and waits for the HTTP control port to become reachable.

```yaml
- name: Start the container runtime
  vars:
    # Container name used by the runtime.
    loadgen_container_name: "{{ inventory_hostname }}"
    # Loadgen container image.
    loadgen_image: "{{ loadgen_registry_endpoint }}/{{ loadgen_image_name }}:{{ loadgen_image_tag }}"
    # Image registry endpoint.
    loadgen_registry_endpoint: "{{ lookup('env', 'LOADGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image name used by the Loadgen container.
    loadgen_image_name: fabric-x-loadgen
    # Image tag used by the Loadgen container.
    loadgen_image_tag: 0.1.9
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Config mount path inside a container or pod.
    loadgen_container_config_dir: /config
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # HTTP control port exposed by Loadgen. Example: `8080`.
    loadgen_web_port: 8080
    # Prometheus metrics port exposed by Loadgen. Example: `9443`.
    loadgen_metrics_port: 9443
    # gRPC control port exposed by Loadgen. Example: `7051`.
    loadgen_rpc_port: 7051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: container/start
```

### container/stop

> Stop the container runtime

Stop the local Loadgen container. Preserves the container definition, image reference, mounted configuration, crypto material, and logs for later cleanup or collection.

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

> Remove the container runtime

Remove the local Loadgen container runtime resources. Leaves host-side generated configuration and crypto material under the remote config directory.

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

> Fetch container logs

Collect logs from a containerized Loadgen runtime. Reads container logs for the configured container name without modifying runtime or config state.

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

> Start the Kubernetes deployment

Create or update Kubernetes resources for Loadgen. Ensures the namespace exists, applies the Service, optional NodePort Service, and Deployment, and mounts generated ConfigMap and Secret artifacts into the pod.

```yaml
- name: Start the Kubernetes deployment
  vars:
    # Committer inventory hosts used by the dispatcher to derive client targets. Example: `['committer-sidecar1', 'committer-validator1']`.
    committer_hosts:
      - "committer-sidecar1"
      - "committer-validator1"
    # Orderer inventory hosts used by the dispatcher to derive client targets. Example: `['orderer-router1', 'orderer-assembler1']`.
    orderer_hosts:
      - "orderer-router1"
      - "orderer-assembler1"
    # Organization definition consumed by crypto, config, and Kubernetes templates. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'loadgen1', 'secret': 'loadgen1pw'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "loadgen1"
        secret: "loadgen1pw"
    # Loadgen container image.
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
    # Kubernetes namespace used for loadgen resources. Example: `fabricx-loadgen`.
    k8s_namespace: "fabricx-loadgen"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
    # Enable mTLS for the main endpoint.
    loadgen_use_mtls: false
    # Enable mTLS for the monitoring endpoint.
    loadgen_monitoring_use_mtls: "{{ loadgen_use_mtls }}"
    # Additional mTLS client identities trusted by the main endpoint. Example: `['orderer-router1', 'committer-sidecar1']`.
    loadgen_mtls_clients:
      - "orderer-router1"
      - "committer-sidecar1"
    # Additional mTLS organizations trusted by the main endpoint. Example: `[{'domain': 'org1.example.com'}, {'domain': 'org2.example.com'}]`.
    loadgen_mtls_orgs:
      - domain: "org1.example.com"
      - domain: "org2.example.com"
    # Additional mTLS client identities trusted by the monitoring endpoint. Example: `['prometheus1', 'node-exporter1']`.
    loadgen_monitoring_mtls_clients:
      - "prometheus1"
      - "node-exporter1"
    # Additional mTLS organizations trusted by the monitoring endpoint. Example: `[{'domain': 'monitoring.example.com'}]`.
    loadgen_monitoring_mtls_orgs:
      - domain: "monitoring.example.com"
    # Optional image pull secret used by Kubernetes workloads. Example: `fabricx-registry-pull`.
    k8s_image_pull_secret: "fabricx-registry-pull"
    # Use Kubernetes resources.
    loadgen_use_k8s: false
    # Expose the Kubernetes Service via NodePort when `loadgen_use_k8s` is enabled. This drives the HTTP, metrics, and gRPC NodePort access paths.
    loadgen_k8s_use_node_port: false
    # HTTP control port exposed by Loadgen. Example: `8080`.
    loadgen_web_port: 8080
    # Prometheus metrics port exposed by Loadgen. Example: `9443`.
    loadgen_metrics_port: 9443
    # gRPC control port exposed by Loadgen. Example: `7051`.
    loadgen_rpc_port: 7051
    # NodePort used for the HTTP control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30080`.
    loadgen_k8s_web_node_port: 30080
    # NodePort used for the metrics port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30090`.
    loadgen_k8s_metrics_node_port: 30090
    # NodePort used for the gRPC control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30051`.
    loadgen_k8s_rpc_node_port: 30051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/start
```

### k8s/ping

> Check the Kubernetes node ports

Verify that Kubernetes-exposed Loadgen endpoints are reachable. Checks configured HTTP, metrics, and gRPC NodePorts when NodePort access is enabled, otherwise uses the service ports.

```yaml
- name: Check the Kubernetes node ports
  vars:
    # Expose the Kubernetes Service via NodePort when `loadgen_use_k8s` is enabled. This drives the HTTP, metrics, and gRPC NodePort access paths.
    loadgen_k8s_use_node_port: false
    # HTTP control port exposed by Loadgen. Example: `8080`.
    loadgen_web_port: 8080
    # Prometheus metrics port exposed by Loadgen. Example: `9443`.
    loadgen_metrics_port: 9443
    # gRPC control port exposed by Loadgen. Example: `7051`.
    loadgen_rpc_port: 7051
    # NodePort used for the HTTP control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30080`.
    loadgen_k8s_web_node_port: 30080
    # NodePort used for the metrics port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30090`.
    loadgen_k8s_metrics_node_port: 30090
    # NodePort used for the gRPC control port when `loadgen_use_k8s` and `loadgen_k8s_use_node_port` are true. Example: `30051`.
    loadgen_k8s_rpc_node_port: 30051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/ping
```

### k8s/rm

> Remove Kubernetes resources

Remove the Kubernetes Deployment and Services created for Loadgen. Does not remove the ConfigMap or Secret; use the Kubernetes config and crypto remove entry points for those generated artifacts.

```yaml
- name: Remove Kubernetes resources
  vars:
    # Kubernetes namespace used for loadgen resources. Example: `fabricx-loadgen`.
    k8s_namespace: "fabricx-loadgen"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch pod logs

Collect logs from the Kubernetes pod running Loadgen. Uses the configured Kubernetes resource name to fetch pod output without changing workload state.

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

> Publish the Kubernetes ConfigMap

Publish the rendered Loadgen configuration and trusted CA bundles as a Kubernetes ConfigMap. The ConfigMap is consumed by the Loadgen Deployment and includes orderer, sidecar, TLS, mTLS, workload, stream, and logging config content.

```yaml
- name: Publish the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for loadgen resources. Example: `fabricx-loadgen`.
    k8s_namespace: "fabricx-loadgen"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Rendered Loadgen config filename.
    loadgen_config_file: config-loadgen.yaml
    # Orderer router hosts targeted by the orderer client. Example: `['orderer-router1', 'orderer-router2']`.
    orderer_router_hosts:
      - "orderer-router1"
      - "orderer-router2"
    # Orderer assembler hosts targeted by the orderer client. Example: `['orderer-assembler1', 'orderer-assembler2']`.
    orderer_assembler_hosts:
      - "orderer-assembler1"
      - "orderer-assembler2"
    # Sidecar host targeted by the orderer and sidecar clients. Example: `committer-sidecar1`.
    committer_sidecar_host: "committer-sidecar1"
    # Enable mTLS for the main endpoint.
    loadgen_use_mtls: false
    # Enable mTLS for the monitoring endpoint.
    loadgen_monitoring_use_mtls: "{{ loadgen_use_mtls }}"
    # Additional mTLS client identities trusted by the main endpoint. Example: `['orderer-router1', 'committer-sidecar1']`.
    loadgen_mtls_clients:
      - "orderer-router1"
      - "committer-sidecar1"
    # Additional mTLS organizations trusted by the main endpoint. Example: `[{'domain': 'org1.example.com'}, {'domain': 'org2.example.com'}]`.
    loadgen_mtls_orgs:
      - domain: "org1.example.com"
      - domain: "org2.example.com"
    # Additional mTLS client identities trusted by the monitoring endpoint. Example: `['prometheus1', 'node-exporter1']`.
    loadgen_monitoring_mtls_clients:
      - "prometheus1"
      - "node-exporter1"
    # Additional mTLS organizations trusted by the monitoring endpoint. Example: `[{'domain': 'monitoring.example.com'}]`.
    loadgen_monitoring_mtls_orgs:
      - domain: "monitoring.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the Kubernetes ConfigMap

Remove the Kubernetes ConfigMap created for Loadgen configuration. Leaves host-side rendered config files intact for inspection, regeneration, or non-Kubernetes deployments.

```yaml
- name: Remove the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for loadgen resources. Example: `fabricx-loadgen`.
    k8s_namespace: "fabricx-loadgen"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

> Publish the Kubernetes Secret

Publish Loadgen MSP and TLS material as a Kubernetes Secret. The Secret is consumed by the Loadgen Deployment and is built from fetched or remote crypto artifacts for the selected identity.

```yaml
- name: Publish the Kubernetes Secret
  vars:
    # Organization definition consumed by crypto, config, and Kubernetes templates. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'loadgen1', 'secret': 'loadgen1pw'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "loadgen1"
        secret: "loadgen1pw"
    # Base remote config directory that feeds `loadgen_remote_config_dir`. Example: `/var/hyperledger/fabricx/loadgen/lg-1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/loadgen/lg-1/config"
    # Remote config directory used by Loadgen.
    loadgen_remote_config_dir: "{{ remote_config_dir }}"
    # Local artifacts directory used for fetched TLS and MSP files. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
    # Canonical host name used for metrics and Fabric CA enrollment. Example: `loadgen1.example.com`.
    actual_host: "loadgen1.example.com"
    # Crypto identity name used for MSP and TLS file names.
    loadgen_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Kubernetes namespace used for loadgen resources. Example: `fabricx-loadgen`.
    k8s_namespace: "fabricx-loadgen"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
    # Enable TLS for the monitoring endpoint.
    loadgen_monitoring_use_tls: "{{ loadgen_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Remove the Kubernetes Secret

Remove the Kubernetes Secret created for Loadgen MSP and TLS material. Leaves host-side crypto artifacts and fetched local artifacts untouched.

```yaml
- name: Remove the Kubernetes Secret
  vars:
    # Kubernetes namespace used for loadgen resources. Example: `fabricx-loadgen`.
    k8s_namespace: "fabricx-loadgen"
    # Kubernetes resource name used for the Deployment, Service, Secret, and optional NodePort Service.
    loadgen_k8s_resource_name: "{{ inventory_hostname }}"
    # Enable TLS for the main endpoint.
    loadgen_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: k8s/crypto/rm
```
