# hyperledger.fabricx.committer

> Runs Fabric-X Committer components across host-binary, container, and Kubernetes deployments. The role renders component configuration, manages TLS/mTLS artifacts, and starts or removes validators, verifiers, coordinators, sidecars, and query-services.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [ping](#ping)
  - [k8s/ping](#k8sping)
  - [validator/start](#validatorstart)
  - [verifier/start](#verifierstart)
  - [coordinator/start](#coordinatorstart)
  - [sidecar/start](#sidecarstart)
  - [query\_service/start](#query_servicestart)
  - [stop](#stop)
  - [teardown](#teardown)
  - [query\_service/teardown](#query_serviceteardown)
  - [sidecar/teardown](#sidecarteardown)
  - [coordinator/teardown](#coordinatorteardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [get\_metrics](#get_metrics)
  - [start](#start)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [bin/install](#bininstall)
  - [bin/build](#binbuild)
  - [bin/stop](#binstop)
  - [bin/rm](#binrm)
  - [bin/fetch\_logs](#binfetch_logs)
  - [bin/transfer](#bintransfer)
  - [validator/container/start](#validatorcontainerstart)
  - [verifier/container/start](#verifiercontainerstart)
  - [coordinator/container/start](#coordinatorcontainerstart)
  - [sidecar/container/start](#sidecarcontainerstart)
  - [query\_service/container/start](#query_servicecontainerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/transfer\_grafana\_dashboard](#configtransfer_grafana_dashboard)
  - [config/db/transfer](#configdbtransfer)
  - [config/db/postgres/transfer](#configdbpostgrestransfer)
  - [config/db/yugabyte/transfer](#configdbyugabytetransfer)
  - [config/mtls/transfer](#configmtlstransfer)
  - [config/mtls/monitoring/transfer](#configmtlsmonitoringtransfer)
  - [crypto/rm](#cryptorm)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric\_ca/enroll](#cryptofabric_caenroll)
  - [data/rm](#datarm)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/crypto/rm](#k8scryptorm)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [prometheus/get\_scrapers](#prometheusget_scrapers)
  - [validator/bin/start](#validatorbinstart)
  - [verifier/bin/start](#verifierbinstart)
  - [coordinator/bin/start](#coordinatorbinstart)
  - [sidecar/bin/start](#sidecarbinstart)
  - [query\_service/bin/start](#query_servicebinstart)
  - [validator/config/transfer](#validatorconfigtransfer)
  - [verifier/config/transfer](#verifierconfigtransfer)
  - [coordinator/config/transfer](#coordinatorconfigtransfer)
  - [sidecar/config/transfer](#sidecarconfigtransfer)
  - [query\_service/config/transfer](#query_serviceconfigtransfer)
  - [validator/k8s/start](#validatork8sstart)
  - [verifier/k8s/start](#verifierk8sstart)
  - [coordinator/k8s/start](#coordinatork8sstart)
  - [sidecar/k8s/start](#sidecark8sstart)
  - [query\_service/k8s/start](#query_servicek8sstart)
  - [validator/k8s/rm](#validatork8srm)
  - [verifier/k8s/rm](#verifierk8srm)
  - [coordinator/k8s/rm](#coordinatork8srm)
  - [sidecar/k8s/rm](#sidecark8srm)
  - [query\_service/k8s/rm](#query_servicek8srm)
  - [validator/k8s/config/transfer](#validatork8sconfigtransfer)
  - [verifier/k8s/config/transfer](#verifierk8sconfigtransfer)
  - [coordinator/k8s/config/transfer](#coordinatork8sconfigtransfer)
  - [sidecar/k8s/config/transfer](#sidecark8sconfigtransfer)
  - [query\_service/k8s/config/transfer](#query_servicek8sconfigtransfer)
  - [validator/teardown](#validatorteardown)
  - [verifier/teardown](#verifierteardown)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.committer
```

## Tasks

### ping

> Check the committer gRPC endpoint

Validate that the Fabric-X Committer RPC port is reachable. Uses `committer_rpc_port` on host deployments and skips the direct host check in Kubernetes mode.

```yaml
- name: Check the committer gRPC endpoint
  vars:
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: ping
```

### k8s/ping

> Check the committer Kubernetes NodePorts

Validate that the optional Kubernetes NodePort Service exposes the RPC and metrics ports. Requires explicit RPC and metrics NodePort values when external Kubernetes access is enabled.

```yaml
- name: Check the committer Kubernetes NodePorts
  vars:
    # Enable the optional Kubernetes NodePort Service for committer RPC and metrics access.
    committer_k8s_use_node_port: false
    # NodePort used for the RPC service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31051`.
    committer_k8s_rpc_node_port: 31051
    # NodePort used for the metrics service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31052`.
    committer_k8s_metrics_node_port: 31052
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: k8s/ping
```

### validator/start

> Start a validator component

Start a validator in bin, container, or Kubernetes mode. The selected runtime path depends on `committer_use_bin` and `committer_use_k8s`. Expects validator configuration and database settings to be generated before the process starts.

```yaml
- name: Start a validator component
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/start
```

### verifier/start

> Start a verifier component

Start a verifier in bin, container, or Kubernetes mode. The selected runtime path depends on `committer_use_bin` and `committer_use_k8s`. Expects verifier configuration and optional TLS/mTLS assets to be available.

```yaml
- name: Start a verifier component
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/start
```

### coordinator/start

> Start a coordinator component

Start a coordinator in bin, container, or Kubernetes mode. Coordinators connect to validator and verifier hosts that must already be configured. Uses `committer_validators` and `committer_verifiers` to locate upstream committers.

```yaml
- name: Start a coordinator component
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/start
```

### sidecar/start

> Start a sidecar component

Start a sidecar in bin, container, or Kubernetes mode. Sidecars require persistent data storage and connect to coordinator and orderer hosts. Uses MSP material plus `committer_coordinator`, `orderer_assemblers`, and `channel_id`.

```yaml
- name: Start a sidecar component
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/start
```

### query_service/start

> Start a query-service component

Start a query-service in bin, container, or Kubernetes mode. The selected runtime path depends on `committer_use_bin` and `committer_use_k8s`. Expects generated database-backed query-service configuration.

```yaml
- name: Start a query-service component
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/start
```

### stop

> Stop a committer process

Stop the selected component in bin or container mode. Kubernetes teardown is handled through the teardown entry points instead. Selects the stop path from `committer_component_type` and `committer_deployment_mode`.

```yaml
- name: Stop a committer process
  vars:
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
    # Deployment mode selected by the role.
    committer_deployment_mode: "{%- if committer_use_bin -%}bin{%- elif committer_use_k8s -%}k8s{%- else -%}container{%- endif -%}"
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: stop
```

### teardown

> Teardown a selected component

Remove the selected component according to its deployment mode. Sidecar teardown also removes sidecar data. Dispatches by `committer_component_type` to the component-specific teardown entry point.

```yaml
- name: Teardown a selected component
  vars:
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: teardown
```

### query_service/teardown

> Teardown the query-service

Remove the query-service according to its deployment mode. Deletes the runtime process, container, or Kubernetes query-service resources.

```yaml
- name: Teardown the query-service
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/teardown
```

### sidecar/teardown

> Teardown the sidecar

Remove the sidecar according to its deployment mode and delete sidecar data. Deletes the runtime process, container, or Kubernetes StatefulSet and storage artifacts.

```yaml
- name: Teardown the sidecar
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/teardown
```

### coordinator/teardown

> Teardown the coordinator

Remove the coordinator according to its deployment mode. Deletes the runtime process, container, or Kubernetes coordinator resources.

```yaml
- name: Teardown the coordinator
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/teardown
```

### wipe

> Remove all committer artifacts

Tear down the selected component and remove binary, config, and crypto assets. Intended for full cleanup of role-managed host artifacts after stopping the component.

```yaml
- name: Remove all committer artifacts
  vars:
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
    # Enable host-binary deployment mode.
    committer_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: wipe
```

### fetch_logs

> Collect committer logs

Fetch logs from the selected deployment mode. Dispatches to binary, container, or Kubernetes log collection based on deployment flags.

```yaml
- name: Collect committer logs
  vars:
    # Enable host-binary deployment mode.
    committer_use_bin: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: fetch_logs
```

### get_metrics

> Retrieve Prometheus metrics

Query the component metrics endpoint and print the response body. Uses `actual_host`, `committer_http_protocol`, and `committer_metrics_port`.

```yaml
- name: Retrieve Prometheus metrics
  vars:
    # Reachable host or IP address used by the metrics client and Fabric-CA CSR generation. Example: `committer-validator-1.example.com`.
    actual_host: "committer-validator-1.example.com"
    # HTTP protocol used by the metrics client.
    committer_http_protocol: "{{ 'https' if committer_use_tls else 'http' }}"
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: get_metrics
```

### start

> Start a committer component by type

Dispatch startup to the selected committer component. `committer_component_type` selects validator, verifier, coordinator, sidecar, or query-service.

```yaml
- name: Start a committer component by type
  vars:
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: start
```

### crypto/setup

> Prepare crypto material

Transfer cryptogen artifacts or enroll with Fabric CA for the selected component. When `committer_use_k8s` is true, also create the Kubernetes secret for the component. Uses `organization` to determine Fabric CA enrollment or cryptogen artifact paths.

```yaml
- name: Prepare crypto material
  vars:
    # Organization definition consumed by crypto and sidecar configuration tasks. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'committer-sidecar-1'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "committer-sidecar-1"
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/setup
```

### crypto/fetch

> Fetch TLS certificates

Fetch the committer TLS CA certificate and server certificate to the control node. This task runs only when `committer_use_tls` is true. Stores fetched files under `fetched_artifacts_dir` for downstream trust bundle generation.

```yaml
- name: Fetch TLS certificates
  vars:
    # Remote config directory used by delegated crypto tasks. Example: `/opt/fabricx/committer/config`.
    remote_config_dir: "/opt/fabricx/committer/config"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
    # Enable TLS material for the selected component.
    committer_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/fetch
```

### bin/install

> Install the committer binary

Install the committer binary through the shared `bin` role Go installer entry point. Uses the configured Git repository, ref, package path, and binary name.

```yaml
- name: Install the committer binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
    # Go package path used by the shared binary installer.
    committer_bin_package: "{{ committer_git_hub_url }}/{{ committer_git_repo }}/{{ committer_source_code_package }}"
    # Git host used for the committer source repository.
    committer_git_hub_url: github.com
    # Git repository that contains the committer sources.
    committer_git_repo: hyperledger/fabric-x-committer
    # Git ref used for building or installing the binary.
    committer_git_commit: v0.1.9
    # Go package path used as the build or install target.
    committer_source_code_package: cmd/committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: bin/install
```

### bin/build

> Build the committer binary

Build the committer binary through the shared `bin` role Go build entry point. Produces the local committer binary artifact later transferred to target hosts.

```yaml
- name: Build the committer binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
    # Git host used for the committer source repository.
    committer_git_hub_url: github.com
    # Git repository that contains the committer sources.
    committer_git_repo: hyperledger/fabric-x-committer
    # Git ref used for building or installing the binary.
    committer_git_commit: v0.1.9
    # Go package path used as the build or install target.
    committer_source_code_package: cmd/committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: bin/build
```

### bin/stop

> Stop a committer binary

Stop the running committer binary process through the shared `bin` role. Applies to validator, verifier, coordinator, sidecar, and query-service host-binary processes.

```yaml
- name: Stop a committer binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: bin/stop
```

### bin/rm

> Remove the committer binary

Remove the installed committer binary from the target host. Uses `committer_bin_name` as the target executable name.

```yaml
- name: Remove the committer binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: bin/rm
```

### bin/fetch_logs

> Fetch committer binary logs

Collect logs generated by the committer binary through the shared `bin` role. Applies to host-binary deployments.

```yaml
- name: Fetch committer binary logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: bin/fetch_logs
```

### bin/transfer

> Transfer the committer binary

Copy the built committer binary to the target host. Uses `committer_bin_name` for the executable transferred by the shared `bin` role.

```yaml
- name: Transfer the committer binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: bin/transfer
```

### validator/container/start

> Start the validator container

Run the validator container with its generated configuration directory mounted read-only. Publishes validator RPC and metrics ports from the container to the host.

```yaml
- name: Start the validator container
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
    # Fully qualified committer image.
    committer_image: "{{ committer_registry_endpoint }}/{{ committer_image_name }}:{{ committer_image_tag }}"
    # Config directory inside the committer container.
    committer_container_config_dir: /config
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/container/start
```

### verifier/container/start

> Start the verifier container

Run the verifier container with its generated configuration directory mounted read-only. Publishes verifier RPC and metrics ports from the container to the host.

```yaml
- name: Start the verifier container
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
    # Fully qualified committer image.
    committer_image: "{{ committer_registry_endpoint }}/{{ committer_image_name }}:{{ committer_image_tag }}"
    # Config directory inside the committer container.
    committer_container_config_dir: /config
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/container/start
```

### coordinator/container/start

> Start the coordinator container

Run the coordinator container with its generated configuration directory mounted read-only. Publishes coordinator RPC and metrics ports from the container to the host.

```yaml
- name: Start the coordinator container
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
    # Fully qualified committer image.
    committer_image: "{{ committer_registry_endpoint }}/{{ committer_image_name }}:{{ committer_image_tag }}"
    # Config directory inside the committer container.
    committer_container_config_dir: /config
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/container/start
```

### sidecar/container/start

> Start the sidecar container

Ensure the sidecar data directory exists and run the sidecar container with config and data volumes mounted. Persists the sidecar ledger under `committer_remote_data_dir`.

```yaml
- name: Start the sidecar container
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
    # Fully qualified committer image.
    committer_image: "{{ committer_registry_endpoint }}/{{ committer_image_name }}:{{ committer_image_tag }}"
    # Config directory inside the committer container.
    committer_container_config_dir: /config
    # Data directory inside the committer container.
    committer_container_data_dir: /data
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote data directory managed by the role.
    committer_remote_data_dir: "{{ remote_data_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/container/start
```

### query_service/container/start

> Start the query-service container

Run the query-service container with its generated configuration directory mounted read-only. Publishes query-service RPC and metrics ports from the container to the host.

```yaml
- name: Start the query-service container
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
    # Fully qualified committer image.
    committer_image: "{{ committer_registry_endpoint }}/{{ committer_image_name }}:{{ committer_image_tag }}"
    # Config directory inside the committer container.
    committer_container_config_dir: /config
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/container/start
```

### container/stop

> Stop a committer container

Stop the committer container through the shared `container` role. Uses `committer_container_name` for the selected component container.

```yaml
- name: Stop a committer container
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: container/stop
```

### container/rm

> Remove a committer container

Remove the committer container through the shared `container` role. Uses `committer_container_name` for the selected component container.

```yaml
- name: Remove a committer container
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch committer container logs

Collect logs from the committer container through the shared `container` role. Uses `committer_container_name` for the selected component container.

```yaml
- name: Fetch committer container logs
  vars:
    # Container name used by the committer container helper.
    committer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: container/fetch_logs
```

### config/transfer

> Generate config by component type

Dispatch configuration generation to the selected committer component. Renders the component YAML config and any required companion artifacts.

```yaml
- name: Generate config by component type
  vars:
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/transfer
```

### config/rm

> Remove committer configuration

Remove the component config directory and the Kubernetes ConfigMap when enabled. Cleans `committer_remote_config_dir` and, for Kubernetes, the component ConfigMap.

```yaml
- name: Remove committer configuration
  vars:
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/rm
```

### config/transfer_grafana_dashboard

> Transfer the committer Grafana dashboard

Publish the committer Grafana dashboard through the shared Grafana helper flow. Installs dashboard configuration used to visualize committer metrics.

```yaml
- name: Transfer the committer Grafana dashboard
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/transfer_grafana_dashboard
```

### config/db/transfer

> Transfer DB config by backend type

Dispatch database configuration generation to the selected backend. Selects PostgreSQL via `postgres_db_host` or YugabyteDB via `yugabyte_cluster_ref_id`.

```yaml
- name: Transfer DB config by backend type
  vars:
    # Inventory host name of the Postgres backend used by validator or query-service configuration. Example: `postgres-committer-1`.
    postgres_db_host: "postgres-committer-1"
    # Yugabyte cluster identifier used by validator or query-service configuration. Example: `yb-committer-ledger`.
    yugabyte_cluster_ref_id: "yb-committer-ledger"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/db/transfer
```

### config/db/postgres/transfer

> Transfer PostgreSQL DB config

Generate the PostgreSQL connection settings consumed by the committer component. Copies the Postgres TLS CA certificate from `fetched_artifacts_dir` when needed.

```yaml
- name: Transfer PostgreSQL DB config
  vars:
    # Inventory host name of the Postgres backend used by validator or query-service configuration. Example: `postgres-committer-1`.
    postgres_db_host: "postgres-committer-1"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/db/postgres/transfer
```

### config/db/yugabyte/transfer

> Transfer Yugabyte DB config

Generate the Yugabyte connection settings consumed by the committer component. Copies the Yugabyte TLS CA certificate from `fetched_artifacts_dir` when needed.

```yaml
- name: Transfer Yugabyte DB config
  vars:
    # Yugabyte cluster identifier used by validator or query-service configuration. Example: `yb-committer-ledger`.
    yugabyte_cluster_ref_id: "yb-committer-ledger"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/db/yugabyte/transfer
```

### config/mtls/transfer

> Transfer committer mTLS certificates

Copy mTLS certificates for the committer service-to-service connections. Builds trust bundles for `committer_mtls_clients` and `committer_mtls_orgs`.

```yaml
- name: Transfer committer mTLS certificates
  vars:
    # mTLS client identifiers trusted by the component. Example: `['committer-sidecar-1', 'loadgen-1']`.
    committer_mtls_clients:
      - "committer-sidecar-1"
      - "loadgen-1"
    # mTLS organizations trusted by the component. Example: `[{'domain': 'org2.example.com'}]`.
    committer_mtls_orgs:
      - domain: "org2.example.com"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/mtls/transfer
```

### config/mtls/monitoring/transfer

> Transfer monitoring mTLS certificates

Copy monitoring mTLS certificates for Prometheus scraping. Builds monitoring trust bundles for Prometheus clients and monitoring organizations.

```yaml
- name: Transfer monitoring mTLS certificates
  vars:
    # Monitoring mTLS client identifiers trusted by the component. Example: `['prometheus-1']`.
    committer_monitoring_mtls_clients:
      - "prometheus-1"
    # Monitoring mTLS organizations trusted by the component. Example: `[{'domain': 'monitoring.example.com'}]`.
    committer_monitoring_mtls_orgs:
      - domain: "monitoring.example.com"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/mtls/monitoring/transfer
```

### crypto/rm

> Remove committer crypto material

Remove local TLS assets and the Kubernetes Secret when enabled. Cleans TLS material under `committer_remote_config_dir` for the selected component.

```yaml
- name: Remove committer crypto material
  vars:
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Enable TLS material for the selected component.
    committer_use_tls: false
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/rm
```

### crypto/cryptogen/transfer

> Transfer committer crypto from cryptogen

Copy cryptogen-generated TLS assets for the selected committer component. Sidecar components also receive MSP material from the organization peer directory.

```yaml
- name: Transfer committer crypto from cryptogen
  vars:
    # Organization definition consumed by crypto and sidecar configuration tasks. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'committer-sidecar-1'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "committer-sidecar-1"
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
    # Control-node directory that stores cryptogen output. Example: `/tmp/fabricx/crypto-material`.
    cryptogen_artifacts_dir: "/tmp/fabricx/crypto-material"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Enable TLS material for the selected component.
    committer_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

> Enroll committer crypto with Fabric CA

Enroll the selected committer component against its Fabric CA and write the resulting TLS assets. Uses `actual_host` as a TLS CSR host and writes certificates under `committer_remote_config_dir`.

```yaml
- name: Enroll committer crypto with Fabric CA
  vars:
    # Organization definition consumed by crypto and sidecar configuration tasks. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'committer-sidecar-1'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "committer-sidecar-1"
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
    # Enable TLS material for the selected component.
    committer_use_tls: false
    # Reachable host or IP address used by the metrics client and Fabric-CA CSR generation. Example: `committer-validator-1.example.com`.
    actual_host: "committer-validator-1.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/fabric_ca/enroll
```

### data/rm

> Remove sidecar data

Remove the sidecar data directory and sidecar PVC when Kubernetes mode is enabled. Applies only to sidecar ledger data stored under `committer_remote_data_dir`.

```yaml
- name: Remove sidecar data
  vars:
    # Remote data directory managed by the role.
    committer_remote_data_dir: "{{ remote_data_dir }}"
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: data/rm
```

### k8s/config/rm

> Remove the committer ConfigMap

Delete the committer Kubernetes ConfigMap. Uses `committer_k8s_resource_name` and `k8s_namespace` to identify the ConfigMap.

```yaml
- name: Remove the committer ConfigMap
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: k8s/config/rm
```

### k8s/crypto/rm

> Remove the committer Secret

Delete the committer Kubernetes Secret. Uses `committer_k8s_resource_name` and `k8s_namespace` to identify the Secret.

```yaml
- name: Remove the committer Secret
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: k8s/crypto/rm
```

### k8s/crypto/transfer

> Create the committer Secret

Create the committer Kubernetes Secret from the generated TLS materials. Includes TLS keys, TLS certificates, and sidecar MSP material when required by the component.

```yaml
- name: Create the committer Secret
  vars:
    # Committer component handled by the entry point. Example: `coordinator`.
    committer_component_type: "coordinator"
    # Crypto material base name for the committer.
    committer_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
    # Organization definition consumed by crypto and sidecar configuration tasks. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'committer-sidecar-1'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "committer-sidecar-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: k8s/crypto/transfer
```

### k8s/fetch_logs

> Fetch committer pod logs

Collect logs from committer pods through the shared Kubernetes helper role. Uses `committer_k8s_resource_name` to select the component workload.

```yaml
- name: Fetch committer pod logs
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: k8s/fetch_logs
```

### prometheus/get_scrapers

> Build Prometheus scrape targets for committer

Construct the Prometheus scrape service definitions for all deployed committer component types. Reads `committer_hosts` and fetched TLS artifacts to build scrape targets.

```yaml
- name: Build Prometheus scrape targets for committer
  vars:
    # Inventory hosts for committer components used by Prometheus scrape generation. Example: `['committer-validator-1', 'committer-verifier-1', 'committer-coordinator-1', 'committer-sidecar-1']`.
    committer_hosts:
      - "committer-validator-1"
      - "committer-verifier-1"
      - "committer-coordinator-1"
      - "committer-sidecar-1"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: prometheus/get_scrapers
```

### validator/bin/start

> Start the validator binary

Run the validator binary with its generated configuration file. Waits for the validator RPC port after starting `start-vc`.

```yaml
- name: Start the validator binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/bin/start
```

### verifier/bin/start

> Start the verifier binary

Run the verifier binary with its generated configuration file. Waits for the verifier RPC port after starting `start-verifier`.

```yaml
- name: Start the verifier binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/bin/start
```

### coordinator/bin/start

> Start the coordinator binary

Run the coordinator binary with its generated configuration file. Waits for the coordinator RPC port after starting `start-coordinator`.

```yaml
- name: Start the coordinator binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/bin/start
```

### sidecar/bin/start

> Start the sidecar binary

Ensure the sidecar data directory exists and run the sidecar binary. Waits for the sidecar RPC port after starting `start-sidecar`.

```yaml
- name: Start the sidecar binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Remote data directory managed by the role.
    committer_remote_data_dir: "{{ remote_data_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/bin/start
```

### query_service/bin/start

> Start the query-service binary

Run the query-service binary with its generated configuration file. Waits for the query-service RPC port after starting `start-query`.

```yaml
- name: Start the query-service binary
  vars:
    # Binary name managed by the committer role.
    committer_bin_name: committer
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/bin/start
```

### validator/config/transfer

> Generate validator config

Render validator configuration, DB settings, mTLS assets, and optional Kubernetes ConfigMap. Requires either `postgres_db_host` or `yugabyte_cluster_ref_id` for the state database.

```yaml
- name: Generate validator config
  vars:
    # Active config directory used by the committer runtime.
    committer_config_dir: "{{ committer_remote_config_dir if committer_use_bin else committer_container_config_dir }}"
    # Maximum size of the committer database connection pool. Example: `32`.
    committer_database_max_connections: 32
    # Minimum size of the committer database connection pool. Example: `8`.
    committer_database_min_connections: 8
    # Initial backoff interval for database retries. Example: `500ms`.
    committer_database_retry_initial_interval: "500ms"
    # Maximum total elapsed time allowed for database retries. Example: `15m`.
    committer_database_retry_max_elapsed_time: "15m"
    # Maximum interval allowed between database retry attempts. Example: `60s`.
    committer_database_retry_max_interval: "60s"
    # Exponential multiplier applied to database retry intervals. Example: `1.5`.
    committer_database_retry_multiplier: 1.5
    # Jitter factor applied to database retry intervals. Example: `0.5`.
    committer_database_retry_randomization_factor: 0.5
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Enable TLS material for the selected component.
    committer_use_tls: false
    # Enable TLS for the monitoring endpoint.
    committer_monitoring_use_tls: "{{ committer_use_tls }}"
    # Enable mTLS for the selected component.
    committer_use_mtls: false
    # Enable mTLS for the monitoring endpoint.
    committer_monitoring_use_mtls: "{{ committer_use_mtls }}"
    # Server rate-limit requests per second. Example: `2000`.
    committer_server_rate_limit_requests_per_second: 2000
    # Server rate-limit burst. Example: `200`.
    committer_server_rate_limit_burst: 200
    # Server keepalive ping interval. Example: `300s`.
    committer_server_keep_alive_time: "300s"
    # Server keepalive acknowledgment timeout. Example: `600s`.
    committer_server_keep_alive_timeout: "600s"
    # Minimum client keepalive interval enforced by the server. Example: `60s`.
    committer_server_keep_alive_min_time: "60s"
    # Allow keepalive pings without active streams. Example: `false`.
    committer_server_keep_alive_permit_without_stream: false
    # Maximum concurrent streaming RPCs allowed per client connection. Example: `128`.
    committer_server_max_concurrent_streams: 128
    # Monitoring rate-limit requests per second. Example: `1000`.
    committer_monitoring_rate_limit_requests_per_second: 1000
    # Monitoring rate-limit burst. Example: `100`.
    committer_monitoring_rate_limit_burst: 100
    # Log level emitted by the committer component.
    committer_log_level: info
    # Log format emitted by the committer component.
    committer_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Worker count for validator transaction preparation. Example: `4`.
    committer_resource_limits_max_workers_for_preparer: 4
    # Worker count for validator MVCC checks. Example: `8`.
    committer_resource_limits_max_workers_for_validator: 8
    # Worker count for validator commit processing. Example: `20`.
    committer_resource_limits_max_workers_for_committer: 20
    # Minimum validator transaction batch size. Example: `100`.
    committer_resource_limits_min_transaction_batch_size: 100
    # Timeout for the minimum validator transaction batch size. Example: `2s`.
    committer_resource_limits_timeout_for_min_transaction_batch_size: "2s"
    # Inventory host name of the Postgres backend used by validator or query-service configuration. Example: `postgres-committer-1`.
    postgres_db_host: "postgres-committer-1"
    # Yugabyte cluster identifier used by validator or query-service configuration. Example: `yb-committer-ledger`.
    yugabyte_cluster_ref_id: "yb-committer-ledger"
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/config/transfer
```

### verifier/config/transfer

> Generate verifier config

Render verifier configuration, mTLS assets, and optional Kubernetes ConfigMap. Includes verifier parallel executor settings and RPC/metrics server settings.

```yaml
- name: Generate verifier config
  vars:
    # Active config directory used by the committer runtime.
    committer_config_dir: "{{ committer_remote_config_dir if committer_use_bin else committer_container_config_dir }}"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Enable TLS material for the selected component.
    committer_use_tls: false
    # Enable TLS for the monitoring endpoint.
    committer_monitoring_use_tls: "{{ committer_use_tls }}"
    # Enable mTLS for the selected component.
    committer_use_mtls: false
    # Enable mTLS for the monitoring endpoint.
    committer_monitoring_use_mtls: "{{ committer_use_mtls }}"
    # Server rate-limit requests per second. Example: `2000`.
    committer_server_rate_limit_requests_per_second: 2000
    # Server rate-limit burst. Example: `200`.
    committer_server_rate_limit_burst: 200
    # Server keepalive ping interval. Example: `300s`.
    committer_server_keep_alive_time: "300s"
    # Server keepalive acknowledgment timeout. Example: `600s`.
    committer_server_keep_alive_timeout: "600s"
    # Minimum client keepalive interval enforced by the server. Example: `60s`.
    committer_server_keep_alive_min_time: "60s"
    # Allow keepalive pings without active streams. Example: `false`.
    committer_server_keep_alive_permit_without_stream: false
    # Maximum concurrent streaming RPCs allowed per client connection. Example: `128`.
    committer_server_max_concurrent_streams: 128
    # Monitoring rate-limit requests per second. Example: `1000`.
    committer_monitoring_rate_limit_requests_per_second: 1000
    # Monitoring rate-limit burst. Example: `100`.
    committer_monitoring_rate_limit_burst: 100
    # Log level emitted by the committer component.
    committer_log_level: info
    # Log format emitted by the committer component.
    committer_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Parallel signature verification workers. Example: `16`.
    committer_verifier_parallelism: 16
    # Signature verification batch size cutoff. Example: `500`.
    committer_verifier_batch_size_cutoff: 500
    # Signature verification batch timeout. Example: `2ms`.
    committer_verifier_batch_time_cutoff: "2ms"
    # Channel buffer size for the verifier pipeline. Example: `1000`.
    committer_verifier_channel_buffer_size: 1000
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/config/transfer
```

### coordinator/config/transfer

> Generate coordinator config

Render coordinator configuration, validator and verifier CA bundles, and optional Kubernetes ConfigMap. Uses `committer_validators` and `committer_verifiers` to build upstream endpoint lists.

```yaml
- name: Generate coordinator config
  vars:
    # Active config directory used by the committer runtime.
    committer_config_dir: "{{ committer_remote_config_dir if committer_use_bin else committer_container_config_dir }}"
    # Maximum size of the committer database connection pool. Example: `32`.
    committer_database_max_connections: 32
    # Minimum size of the committer database connection pool. Example: `8`.
    committer_database_min_connections: 8
    # Initial backoff interval for database retries. Example: `500ms`.
    committer_database_retry_initial_interval: "500ms"
    # Maximum total elapsed time allowed for database retries. Example: `15m`.
    committer_database_retry_max_elapsed_time: "15m"
    # Maximum interval allowed between database retry attempts. Example: `60s`.
    committer_database_retry_max_interval: "60s"
    # Exponential multiplier applied to database retry intervals. Example: `1.5`.
    committer_database_retry_multiplier: 1.5
    # Jitter factor applied to database retry intervals. Example: `0.5`.
    committer_database_retry_randomization_factor: 0.5
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Enable TLS material for the selected component.
    committer_use_tls: false
    # Enable TLS for the monitoring endpoint.
    committer_monitoring_use_tls: "{{ committer_use_tls }}"
    # Enable mTLS for the selected component.
    committer_use_mtls: false
    # Enable mTLS for the monitoring endpoint.
    committer_monitoring_use_mtls: "{{ committer_use_mtls }}"
    # Server rate-limit requests per second. Example: `2000`.
    committer_server_rate_limit_requests_per_second: 2000
    # Server rate-limit burst. Example: `200`.
    committer_server_rate_limit_burst: 200
    # Server keepalive ping interval. Example: `300s`.
    committer_server_keep_alive_time: "300s"
    # Server keepalive acknowledgment timeout. Example: `600s`.
    committer_server_keep_alive_timeout: "600s"
    # Minimum client keepalive interval enforced by the server. Example: `60s`.
    committer_server_keep_alive_min_time: "60s"
    # Allow keepalive pings without active streams. Example: `false`.
    committer_server_keep_alive_permit_without_stream: false
    # Maximum concurrent streaming RPCs allowed per client connection. Example: `128`.
    committer_server_max_concurrent_streams: 128
    # Monitoring rate-limit requests per second. Example: `1000`.
    committer_monitoring_rate_limit_requests_per_second: 1000
    # Monitoring rate-limit burst. Example: `100`.
    committer_monitoring_rate_limit_burst: 100
    # Log level emitted by the committer component.
    committer_log_level: info
    # Log format emitted by the committer component.
    committer_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Dependency-graph constructor count for the coordinator. Example: `4`.
    committer_coordinator_dep_graph_constructors: 4
    # Dependency-graph waiting transaction limit for the coordinator. Example: `20000000`.
    committer_coordinator_dep_graph_wait_tx_limit: 20000000
    # Per-goroutine channel buffer size for the coordinator. Example: `10`.
    committer_coordinator_per_channel_buffer_size_per_goroutine: 10
    # Inventory hosts for validator components. Example: `['committer-validator-1', 'committer-validator-2']`.
    committer_validators:
      - "committer-validator-1"
      - "committer-validator-2"
    # Inventory hosts for verifier components. Example: `['committer-verifier-1', 'committer-verifier-2']`.
    committer_verifiers:
      - "committer-verifier-1"
      - "committer-verifier-2"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/config/transfer
```

### sidecar/config/transfer

> Generate sidecar config

Render sidecar configuration, upstream TLS bundles, and optional Kubernetes ConfigMap. Uses `orderer_assemblers`, `committer_coordinator`, `channel_id`, and MSP material.

```yaml
- name: Generate sidecar config
  vars:
    # Active config directory used by the committer runtime.
    committer_config_dir: "{{ committer_remote_config_dir if committer_use_bin else committer_container_config_dir }}"
    # Active data directory used by the committer runtime.
    committer_data_dir: "{{ committer_remote_data_dir if committer_use_bin else committer_container_data_dir }}"
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Enable TLS material for the selected component.
    committer_use_tls: false
    # Enable TLS for the monitoring endpoint.
    committer_monitoring_use_tls: "{{ committer_use_tls }}"
    # Enable mTLS for the selected component.
    committer_use_mtls: false
    # Enable mTLS for the monitoring endpoint.
    committer_monitoring_use_mtls: "{{ committer_use_mtls }}"
    # Server rate-limit requests per second. Example: `2000`.
    committer_server_rate_limit_requests_per_second: 2000
    # Server rate-limit burst. Example: `200`.
    committer_server_rate_limit_burst: 200
    # Server keepalive ping interval. Example: `300s`.
    committer_server_keep_alive_time: "300s"
    # Server keepalive acknowledgment timeout. Example: `600s`.
    committer_server_keep_alive_timeout: "600s"
    # Minimum client keepalive interval enforced by the server. Example: `60s`.
    committer_server_keep_alive_min_time: "60s"
    # Allow keepalive pings without active streams. Example: `false`.
    committer_server_keep_alive_permit_without_stream: false
    # Maximum concurrent streaming RPCs allowed per client connection. Example: `128`.
    committer_server_max_concurrent_streams: 128
    # Monitoring rate-limit requests per second. Example: `1000`.
    committer_monitoring_rate_limit_requests_per_second: 1000
    # Monitoring rate-limit burst. Example: `100`.
    committer_monitoring_rate_limit_burst: 100
    # Log level emitted by the committer component.
    committer_log_level: info
    # Log format emitted by the committer component.
    committer_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Fabric channel identifier consumed by sidecar configuration. Example: `mychannel`.
    channel_id: "mychannel"
    # Organization definition consumed by crypto and sidecar configuration tasks. Example: `{'name': 'Org1', 'domain': 'org1.example.com', 'peer': {'name': 'committer-sidecar-1'}}`.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      peer:
        name: "committer-sidecar-1"
    # Inventory host name of the coordinator component. Example: `committer-coordinator-1`.
    committer_coordinator: "committer-coordinator-1"
    # Interval between sidecar committed-block updates. Example: `5s`.
    committer_sidecar_last_committed_block_set_interval: "5s"
    # Sidecar waiting transaction limit. Example: `20000000`.
    committer_sidecar_waiting_txs_limit: 20000000
    # Sidecar internal channel buffer size. Example: `100`.
    committer_sidecar_channel_buffer_size: 100
    # Sidecar ledger sync interval. Example: `100`.
    committer_sidecar_ledger_sync_interval: 100
    # Sidecar notification timeout. Example: `10m`.
    committer_sidecar_notification_max_timeout: "10m"
    # Inventory hosts for orderer assembler components. Example: `['orderer-assembler-1', 'orderer-assembler-2']`.
    orderer_assemblers:
      - "orderer-assembler-1"
      - "orderer-assembler-2"
    # Control-node directory that stores fetched artifacts. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/config/transfer
```

### query_service/config/transfer

> Generate query-service config

Render query-service configuration, DB settings, mTLS assets, and optional Kubernetes ConfigMap. Requires either `postgres_db_host` or `yugabyte_cluster_ref_id` for the query database.

```yaml
- name: Generate query-service config
  vars:
    # Active config directory used by the committer runtime.
    committer_config_dir: "{{ committer_remote_config_dir if committer_use_bin else committer_container_config_dir }}"
    # Maximum size of the committer database connection pool. Example: `32`.
    committer_database_max_connections: 32
    # Minimum size of the committer database connection pool. Example: `8`.
    committer_database_min_connections: 8
    # Initial backoff interval for database retries. Example: `500ms`.
    committer_database_retry_initial_interval: "500ms"
    # Maximum total elapsed time allowed for database retries. Example: `15m`.
    committer_database_retry_max_elapsed_time: "15m"
    # Maximum interval allowed between database retry attempts. Example: `60s`.
    committer_database_retry_max_interval: "60s"
    # Exponential multiplier applied to database retry intervals. Example: `1.5`.
    committer_database_retry_multiplier: 1.5
    # Jitter factor applied to database retry intervals. Example: `0.5`.
    committer_database_retry_randomization_factor: 0.5
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Generated config file name used by the selected component.
    committer_config_file: "config-{{ committer_component_type }}.yml"
    # Metrics port exposed by the selected committer component. Example: `9443`.
    committer_metrics_port: 9443
    # RPC port exposed by the selected committer component. Example: `7051`.
    committer_rpc_port: 7051
    # Enable TLS material for the selected component.
    committer_use_tls: false
    # Enable TLS for the monitoring endpoint.
    committer_monitoring_use_tls: "{{ committer_use_tls }}"
    # Enable mTLS for the selected component.
    committer_use_mtls: false
    # Enable mTLS for the monitoring endpoint.
    committer_monitoring_use_mtls: "{{ committer_use_mtls }}"
    # Server rate-limit requests per second. Example: `2000`.
    committer_server_rate_limit_requests_per_second: 2000
    # Server rate-limit burst. Example: `200`.
    committer_server_rate_limit_burst: 200
    # Server keepalive ping interval. Example: `300s`.
    committer_server_keep_alive_time: "300s"
    # Server keepalive acknowledgment timeout. Example: `600s`.
    committer_server_keep_alive_timeout: "600s"
    # Minimum client keepalive interval enforced by the server. Example: `60s`.
    committer_server_keep_alive_min_time: "60s"
    # Allow keepalive pings without active streams. Example: `false`.
    committer_server_keep_alive_permit_without_stream: false
    # Maximum concurrent streaming RPCs allowed per client connection. Example: `128`.
    committer_server_max_concurrent_streams: 128
    # Monitoring rate-limit requests per second. Example: `1000`.
    committer_monitoring_rate_limit_requests_per_second: 1000
    # Monitoring rate-limit burst. Example: `100`.
    committer_monitoring_rate_limit_burst: 100
    # Log level emitted by the committer component.
    committer_log_level: info
    # Log format emitted by the committer component.
    committer_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Query-service minimum batch key count. Example: `1024`.
    committer_query_service_min_batch_keys: 1024
    # Query-service maximum batch wait time. Example: `100ms`.
    committer_query_service_max_batch_wait: "100ms"
    # Query-service view aggregation window. Example: `100ms`.
    committer_query_service_view_aggregation_window: "100ms"
    # Query-service maximum aggregated views. Example: `1024`.
    committer_query_service_max_aggregated_views: 1024
    # Query-service maximum active views. Example: `4096`.
    committer_query_service_max_active_views: 4096
    # Query-service view timeout. Example: `10s`.
    committer_query_service_max_view_timeout: "10s"
    # Query-service maximum request key count. Example: `10000`.
    committer_query_service_max_request_keys: 10000
    # Inventory host name of the Postgres backend used by validator or query-service configuration. Example: `postgres-committer-1`.
    postgres_db_host: "postgres-committer-1"
    # Yugabyte cluster identifier used by validator or query-service configuration. Example: `yb-committer-ledger`.
    yugabyte_cluster_ref_id: "yb-committer-ledger"
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/config/transfer
```

### validator/k8s/start

> Start the validator on Kubernetes

Ensure the namespace exists and apply the validator Service, NodePort Service, and Deployment. Uses generated ConfigMap and Secret artifacts plus RPC and metrics port settings.

```yaml
- name: Start the validator on Kubernetes
  vars:
    # Enable the optional Kubernetes NodePort Service for committer RPC and metrics access.
    committer_k8s_use_node_port: false
    # NodePort used for the RPC service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31051`.
    committer_k8s_rpc_node_port: 31051
    # NodePort used for the metrics service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31052`.
    committer_k8s_metrics_node_port: 31052
    # Wait timeout in seconds for Kubernetes rollouts.
    committer_k8s_wait_timeout: 120
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/k8s/start
```

### verifier/k8s/start

> Start the verifier on Kubernetes

Ensure the namespace exists and apply the verifier Service, NodePort Service, and Deployment. Uses generated ConfigMap and Secret artifacts plus RPC and metrics port settings.

```yaml
- name: Start the verifier on Kubernetes
  vars:
    # Enable the optional Kubernetes NodePort Service for committer RPC and metrics access.
    committer_k8s_use_node_port: false
    # NodePort used for the RPC service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31051`.
    committer_k8s_rpc_node_port: 31051
    # NodePort used for the metrics service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31052`.
    committer_k8s_metrics_node_port: 31052
    # Wait timeout in seconds for Kubernetes rollouts.
    committer_k8s_wait_timeout: 120
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/k8s/start
```

### coordinator/k8s/start

> Start the coordinator on Kubernetes

Ensure the namespace exists and apply the coordinator Service, NodePort Service, and Deployment. Uses validator and verifier host lists to prepare TLS mounts and startup dependencies.

```yaml
- name: Start the coordinator on Kubernetes
  vars:
    # Enable the optional Kubernetes NodePort Service for committer RPC and metrics access.
    committer_k8s_use_node_port: false
    # NodePort used for the RPC service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31051`.
    committer_k8s_rpc_node_port: 31051
    # NodePort used for the metrics service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31052`.
    committer_k8s_metrics_node_port: 31052
    # Wait timeout in seconds for Kubernetes rollouts.
    committer_k8s_wait_timeout: 120
    # Inventory hosts for validator components. Example: `['committer-validator-1', 'committer-validator-2']`.
    committer_validators:
      - "committer-validator-1"
      - "committer-validator-2"
    # Inventory hosts for verifier components. Example: `['committer-verifier-1', 'committer-verifier-2']`.
    committer_verifiers:
      - "committer-verifier-1"
      - "committer-verifier-2"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/k8s/start
```

### sidecar/k8s/start

> Start the sidecar on Kubernetes

Ensure the namespace exists and apply the sidecar Service, NodePort Service, and StatefulSet. Creates the persistent sidecar ledger volume from the configured storage settings.

```yaml
- name: Start the sidecar on Kubernetes
  vars:
    # Enable the optional Kubernetes NodePort Service for committer RPC and metrics access.
    committer_k8s_use_node_port: false
    # NodePort used for the RPC service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31051`.
    committer_k8s_rpc_node_port: 31051
    # NodePort used for the metrics service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31052`.
    committer_k8s_metrics_node_port: 31052
    # Wait timeout in seconds for Kubernetes rollouts.
    committer_k8s_wait_timeout: 120
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/k8s/start
```

### query_service/k8s/start

> Start the query-service on Kubernetes

Ensure the namespace exists and apply the query-service Service, NodePort Service, and Deployment. Uses generated ConfigMap and Secret artifacts plus RPC and metrics port settings.

```yaml
- name: Start the query-service on Kubernetes
  vars:
    # Enable the optional Kubernetes NodePort Service for committer RPC and metrics access.
    committer_k8s_use_node_port: false
    # NodePort used for the RPC service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31051`.
    committer_k8s_rpc_node_port: 31051
    # NodePort used for the metrics service when `committer_k8s_use_node_port` is enabled. Must be explicitly set to a valid Kubernetes NodePort value when needed. Example: `31052`.
    committer_k8s_metrics_node_port: 31052
    # Wait timeout in seconds for Kubernetes rollouts.
    committer_k8s_wait_timeout: 120
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/k8s/start
```

### validator/k8s/rm

> Remove validator Kubernetes resources

Delete the validator Deployment and Services. Uses `committer_k8s_resource_name` in `k8s_namespace` to select resources.

```yaml
- name: Remove validator Kubernetes resources
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/k8s/rm
```

### verifier/k8s/rm

> Remove verifier Kubernetes resources

Delete the verifier Deployment and Services. Uses `committer_k8s_resource_name` in `k8s_namespace` to select resources.

```yaml
- name: Remove verifier Kubernetes resources
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/k8s/rm
```

### coordinator/k8s/rm

> Remove coordinator Kubernetes resources

Delete the coordinator Deployment and Services. Uses `committer_k8s_resource_name` in `k8s_namespace` to select resources.

```yaml
- name: Remove coordinator Kubernetes resources
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/k8s/rm
```

### sidecar/k8s/rm

> Remove sidecar Kubernetes resources

Delete the sidecar StatefulSet and Services. Uses `committer_k8s_resource_name` in `k8s_namespace` to select resources.

```yaml
- name: Remove sidecar Kubernetes resources
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/k8s/rm
```

### query_service/k8s/rm

> Remove query-service Kubernetes resources

Delete the query-service Deployment and Services. Uses `committer_k8s_resource_name` in `k8s_namespace` to select resources.

```yaml
- name: Remove query-service Kubernetes resources
  vars:
    # Base Kubernetes resource name for committer objects. Used by the service, workload, secret, and optional NodePort resources.
    committer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace that contains the committer resources. Example: `fabricx-committer`.
    k8s_namespace: "fabricx-committer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/k8s/rm
```

### validator/k8s/config/transfer

> Create the validator ConfigMap

Ensure the namespace exists and create the validator Kubernetes ConfigMap. Publishes the rendered validator config and mounted CA files for Kubernetes pods.

```yaml
- name: Create the validator ConfigMap
  vars:
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/k8s/config/transfer
```

### verifier/k8s/config/transfer

> Create the verifier ConfigMap

Ensure the namespace exists and create the verifier Kubernetes ConfigMap. Publishes the rendered verifier config and mounted CA files for Kubernetes pods.

```yaml
- name: Create the verifier ConfigMap
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/k8s/config/transfer
```

### coordinator/k8s/config/transfer

> Create the coordinator ConfigMap

Ensure the namespace exists and create the coordinator Kubernetes ConfigMap. Publishes rendered coordinator config plus validator and verifier CA bundle files.

```yaml
- name: Create the coordinator ConfigMap
  vars:
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
    # Inventory hosts for validator components. Example: `['committer-validator-1', 'committer-validator-2']`.
    committer_validators:
      - "committer-validator-1"
      - "committer-validator-2"
    # Inventory hosts for verifier components. Example: `['committer-verifier-1', 'committer-verifier-2']`.
    committer_verifiers:
      - "committer-verifier-1"
      - "committer-verifier-2"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: coordinator/k8s/config/transfer
```

### sidecar/k8s/config/transfer

> Create the sidecar ConfigMap

Ensure the namespace exists and create the sidecar Kubernetes ConfigMap. Publishes rendered sidecar config plus orderer and coordinator CA bundle files.

```yaml
- name: Create the sidecar ConfigMap
  vars:
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: sidecar/k8s/config/transfer
```

### query_service/k8s/config/transfer

> Create the query-service ConfigMap

Ensure the namespace exists and create the query-service Kubernetes ConfigMap. Publishes the rendered query-service config and mounted DB CA file when used.

```yaml
- name: Create the query-service ConfigMap
  vars:
    # Remote config directory managed by the role.
    committer_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: query_service/k8s/config/transfer
```

### validator/teardown

> Teardown the validator

Remove validator runtime resources for the active deployment mode. Dispatches to Kubernetes, container, or host-binary cleanup based on deployment flags.

```yaml
- name: Teardown the validator
  vars:
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
    # Enable host-binary deployment mode.
    committer_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: validator/teardown
```

### verifier/teardown

> Teardown the verifier

Remove verifier runtime resources for the active deployment mode. Dispatches to Kubernetes, container, or host-binary cleanup based on deployment flags.

```yaml
- name: Teardown the verifier
  vars:
    # Enable Kubernetes deployment mode.
    committer_use_k8s: false
    # Enable container deployment mode.
    committer_use_container: "{{ (not committer_use_bin) and (not committer_use_k8s) }}"
    # Enable host-binary deployment mode.
    committer_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: verifier/teardown
```
