# hyperledger.fabricx.evm

> Deploys and manages the Fabric-X EVM gateway and embedded endorser across container and Kubernetes modes, including orderer and committer sidecar connectivity, TLS/mTLS, persistent state, and log collection workflows.

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
  - [rpc\_check](#rpc_check)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [crypto/setup](#cryptosetup)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric\_ca/enroll](#cryptofabric_caenroll)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)
  - [openshift/start](#openshiftstart)
  - [openshift/ping](#openshiftping)
  - [openshift/rm](#openshiftrm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.evm
```

## Tasks

### start

> Start the Fabric-X EVM gateway

Start the EVM gateway and embedded endorser runtime selected by the deployment mode flags. Container mode is the default, and Kubernetes mode applies Services, a PersistentVolumeClaim, and a StatefulSet. The runtime consumes the rendered configuration and crypto material prepared by the config and crypto entry points.

```yaml
- name: Start the Fabric-X EVM gateway
  vars:
    # Run the container runtime.
    evm_use_container: "{{ (not evm_use_k8s) and (not evm_use_openshift) }}"
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: start
```

### stop

> Stop the Fabric-X EVM gateway

Stop the active EVM container without removing configuration, crypto material, logs, or Kubernetes resources.

```yaml
- name: Stop the Fabric-X EVM gateway
  vars:
    # Run the container runtime.
    evm_use_container: "{{ (not evm_use_k8s) and (not evm_use_openshift) }}"
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: stop
```

### teardown

> Remove runtime artifacts

Remove runtime resources for the selected EVM deployment mode. Deletes the local container or Kubernetes workload resources while leaving generated config, crypto material, and fetched artifacts intact.

```yaml
- name: Remove runtime artifacts
  vars:
    # Run the container runtime.
    evm_use_container: "{{ (not evm_use_k8s) and (not evm_use_openshift) }}"
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: teardown
```

### wipe

> Remove all EVM data

Remove EVM runtime resources, generated configuration, crypto material, and persisted state from the host.

```yaml
- name: Remove all EVM data
  vars:
    # Remote data directory used by EVM for the gateway and embedded endorser SQLite state.
    evm_remote_data_dir: "{{ remote_data_dir }}"
    # Base remote data directory that feeds `evm_remote_data_dir`.
    remote_data_dir: "/var/hyperledger/fabricx/evm/data"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: wipe
```

### fetch_logs

> Collect runtime logs

Collect EVM gateway logs for the selected deployment mode.

```yaml
- name: Collect runtime logs
  vars:
    # Run the container runtime.
    evm_use_container: "{{ (not evm_use_k8s) and (not evm_use_openshift) }}"
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: fetch_logs
```

### ping

> Check the JSON-RPC endpoint

Verify that the EVM gateway's JSON-RPC endpoint is reachable and answering for the configured chain. Checks the TCP port, then asserts `eth_chainId` matches `evm_chain_id` and that `eth_blockNumber` succeeds. Because the gateway only opens its listener once its embedded endorser has synchronized with the committer sidecar, a successful `eth_chainId` reply also proves Fabric-X connectivity. Uses direct host access for container deployments and delegates to the Kubernetes ping task when `evm_use_k8s` is enabled.

```yaml
- name: Check the JSON-RPC endpoint
  vars:
    # Ethereum JSON-RPC (HTTP and WebSocket) port exposed by the gateway.
    evm_port: 8545
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: ping
```

### rpc_check

> Assert the EVM JSON-RPC endpoint answers for the configured chain

Internal helper included with `evm_ping_base_url` set by the caller. Asserts `eth_chainId` matches `evm_chain_id` and that `eth_blockNumber` succeeds.

```yaml
- name: Assert the EVM JSON-RPC endpoint answers for the configured chain
  vars:
    # Ethereum-style chain ID served by the gateway.
    evm_chain_id: 4011
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: rpc_check
```

### container/start

> Start the container runtime

Start the EVM gateway as a local container with the rendered config directory mounted read-only and a read-write data directory for its persisted state. Exposes the JSON-RPC port and waits for it to become reachable.

```yaml
- name: Start the container runtime
  vars:
    # Container name used by the runtime.
    evm_container_name: "{{ inventory_hostname }}"
    # EVM container image.
    evm_image: "{{ evm_registry_endpoint }}/{{ evm_image_name }}:{{ evm_image_tag }}"
    # Image registry endpoint.
    evm_registry_endpoint: "{{ lookup('env', 'EVM_REGISTRY_ENDPOINT') or 'ghcr.io/hyperledger' }}"
    # Image name used by the EVM container.
    evm_image_name: fabric-x-evm
    # Image tag used by the EVM container.
    evm_image_tag: 0.1.3
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Config mount path inside a container or pod.
    evm_container_config_dir: /config
    # Rendered EVM gateway configuration filename.
    evm_config_file: gateway.yaml
    # Base remote data directory that feeds `evm_remote_data_dir`.
    remote_data_dir: "/var/hyperledger/fabricx/evm/data"
    # Remote data directory used by EVM for the gateway and embedded endorser SQLite state.
    evm_remote_data_dir: "{{ remote_data_dir }}"
    # Data mount path inside a container or pod for the gateway and embedded endorser SQLite state.
    evm_container_data_dir: /data
    # Ethereum JSON-RPC (HTTP and WebSocket) port exposed by the gateway.
    evm_port: 8545
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: container/start
```

### container/stop

> Stop the container runtime

Stop the local EVM container. Preserves the container definition, mounted configuration, crypto material, and logs for later cleanup or collection.

```yaml
- name: Stop the container runtime
  vars:
    # Container name used by the runtime.
    evm_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: container/stop
```

### container/rm

> Remove the container runtime

Remove the local EVM container runtime resources. Leaves host-side generated configuration, crypto material, and persisted state under the remote config and data directories.

```yaml
- name: Remove the container runtime
  vars:
    # Container name used by the runtime.
    evm_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch container logs

Collect logs from a containerized EVM runtime.

```yaml
- name: Fetch container logs
  vars:
    # Container name used by the runtime.
    evm_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: container/fetch_logs
```

### config/transfer

> Render and transfer the EVM gateway configuration

Render the EVM gateway configuration with the resolved orderer and committer sidecar connection details. Transfers the committer sidecar and each orderer router's TLS CA certificates when their respective TLS modes are enabled. For Kubernetes deployments, also publishes the rendered config and trusted CA bundles as a ConfigMap. Fails when `organization.namespaces` does not declare exactly one namespace, since the gateway can only serve a single Fabric-X application namespace.

```yaml
- name: Render and transfer the EVM gateway configuration
  vars:
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Config mount path inside a container or pod.
    evm_container_config_dir: /config
    # Data mount path inside a container or pod for the gateway and embedded endorser SQLite state.
    evm_container_data_dir: /data
    # Rendered EVM gateway configuration filename.
    evm_config_file: gateway.yaml
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
    # Ethereum JSON-RPC (HTTP and WebSocket) port exposed by the gateway.
    evm_port: 8545
    # Ethereum-style chain ID served by the gateway.
    evm_chain_id: 4011
    # Version of the Fabric-X application namespace.
    evm_ns_version: 1.0
    # Network protocol the gateway speaks to the committer and orderers, `fabric-x` or `fabric`.
    evm_protocol: fabric-x
    # Log level specification passed to `logging.spec`.
    evm_log_level: info
    # Log record format specifier passed to `logging.format`.
    evm_log_format: "%{color}%{time:2006-01-02 15:04:05.000 MST} [%{module}] %{shortfunc} -> %{level:.4s}%{color:reset} %{message}"
    # Number of gateway worker goroutines.
    evm_worker_count: 16
    # Number of parallel orderer submitter instances.
    evm_submitter_count: 16
    # Buffer size of the endorsement channel.
    evm_endorsement_chan_size: 1000
    # Label for the embedded endorser.
    evm_endorser_name: "{{ organization.name | lower }}"
    # Sets the organization mapping used for the embedded endorser's peer identity, the gateway's signing identity, and client TLS. `organization.role` must be `peer`. When `organization.fabric_ca_host` is undefined, crypto material generated by `cryptogen` is transferred; otherwise the identities are enrolled with Fabric CA. `organization.users` must declare at least one user; the first entry becomes the gateway's transaction-signing identity. `organization.namespaces` must declare exactly one entry; the gateway can only serve a single Fabric-X application namespace, and `config/transfer` fails otherwise.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      role: "peer"
      fabric_ca_host: "fca-org1"
      peer:
        name: "fabric-x-evm"
        secret: "fabric-x-evmPWD"
      users:
        - name: "fabric-x-evm"
          secret: "fabric-x-evmPWD"
      namespaces:
        - id: "basic"
          policy: "threshold"
    # Fabric channel rendered into the gateway configuration.
    channel_id: "arma"
    # Committer inventory hosts used to derive the committer sidecar the gateway and embedded endorser synchronize with. The sidecar is selected as the entry whose `committer_component_type` is `sidecar`; when the caller scopes this list to hosts sharing `organization.domain` with the EVM host, that selection also confirms the sidecar belongs to the same organization.
    committer_hosts:
      - "committer-sidecar"
      - "committer-validator"
    # Names the inventory hosts that provide the Fabric-X Orderer routers the gateway submits transactions to. One orderer endpoint is rendered per entry, across every organization.
    orderer_router_hosts:
      - "orderer-router-1"
      - "orderer-router-2"
      - "orderer-router-3"
      - "orderer-router-4"
    # Local artifacts directory used for fetched crypto material.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: config/transfer
```

### config/rm

> Remove rendered configuration

Remove host-side rendered EVM configuration. Also removes the Kubernetes ConfigMap when Kubernetes deployment mode is enabled.

```yaml
- name: Remove rendered configuration
  vars:
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: config/rm
```

### crypto/setup

> Prepare crypto material

Enrolls the peer identity backing the embedded endorser, each declared user identity, and (when any connected orderer or the committer sidecar requires mTLS) a shared client TLS key pair. Selects `cryptogen` or Fabric CA based on `organization.fabric_ca_host`. Then publishes Kubernetes Secret material when Kubernetes mode is enabled.

```yaml
- name: Prepare crypto material
  vars:
    # Sets the organization mapping used for the embedded endorser's peer identity, the gateway's signing identity, and client TLS. `organization.role` must be `peer`. When `organization.fabric_ca_host` is undefined, crypto material generated by `cryptogen` is transferred; otherwise the identities are enrolled with Fabric CA. `organization.users` must declare at least one user; the first entry becomes the gateway's transaction-signing identity. `organization.namespaces` must declare exactly one entry; the gateway can only serve a single Fabric-X application namespace, and `config/transfer` fails otherwise.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      role: "peer"
      fabric_ca_host: "fca-org1"
      peer:
        name: "fabric-x-evm"
        secret: "fabric-x-evmPWD"
      users:
        - name: "fabric-x-evm"
          secret: "fabric-x-evmPWD"
      namespaces:
        - id: "basic"
          policy: "threshold"
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: crypto/setup
```

### crypto/cryptogen/transfer

> Transfer cryptogen-generated crypto material for EVM

Transfers the peer MSP, each user MSP, and (when `evm_use_tls` is `true`) TLS key material generated by `cryptogen` for the EVM identities named by `organization.peer.name` and `organization.users`.

```yaml
- name: Transfer cryptogen-generated crypto material for EVM
  vars:
    # Sets the organization mapping used for the embedded endorser's peer identity, the gateway's signing identity, and client TLS. `organization.role` must be `peer`. When `organization.fabric_ca_host` is undefined, crypto material generated by `cryptogen` is transferred; otherwise the identities are enrolled with Fabric CA. `organization.users` must declare at least one user; the first entry becomes the gateway's transaction-signing identity. `organization.namespaces` must declare exactly one entry; the gateway can only serve a single Fabric-X application namespace, and `config/transfer` fails otherwise.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      role: "peer"
      fabric_ca_host: "fca-org1"
      peer:
        name: "fabric-x-evm"
        secret: "fabric-x-evmPWD"
      users:
        - name: "fabric-x-evm"
          secret: "fabric-x-evmPWD"
      namespaces:
        - id: "basic"
          policy: "threshold"
    # Local cryptogen output directory. Required when `organization.fabric_ca_host` is undefined.
    cryptogen_artifacts_dir: "/tmp/fabricx-crypto"
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Name of the enrolled peer identity backing the embedded endorser.
    evm_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Enroll a shared client TLS key pair for EVM, used when any connected orderer or the committer sidecar requires mTLS. Set this to `true` whenever any orderer router (from `orderer_hosts`) or the committer sidecar (derived from `committer_hosts`) has `orderer_use_mtls` or `committer_use_mtls` enabled; the TLS mode used on each individual connection is still derived from that host's own flags.
    evm_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

> Enroll EVM identities with Fabric CA

Enrolls the peer identity, each user identity, and (when `evm_use_tls` is `true`) the client TLS identity through Fabric CA. Uses `actual_host` in the CSR SAN list.

```yaml
- name: Enroll EVM identities with Fabric CA
  vars:
    # Sets the organization mapping used for the embedded endorser's peer identity, the gateway's signing identity, and client TLS. `organization.role` must be `peer`. When `organization.fabric_ca_host` is undefined, crypto material generated by `cryptogen` is transferred; otherwise the identities are enrolled with Fabric CA. `organization.users` must declare at least one user; the first entry becomes the gateway's transaction-signing identity. `organization.namespaces` must declare exactly one entry; the gateway can only serve a single Fabric-X application namespace, and `config/transfer` fails otherwise.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      role: "peer"
      fabric_ca_host: "fca-org1"
      peer:
        name: "fabric-x-evm"
        secret: "fabric-x-evmPWD"
      users:
        - name: "fabric-x-evm"
          secret: "fabric-x-evmPWD"
      namespaces:
        - id: "basic"
          policy: "threshold"
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Name of the enrolled peer identity backing the embedded endorser.
    evm_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Enroll a shared client TLS key pair for EVM, used when any connected orderer or the committer sidecar requires mTLS. Set this to `true` whenever any orderer router (from `orderer_hosts`) or the committer sidecar (derived from `committer_hosts`) has `orderer_use_mtls` or `committer_use_mtls` enabled; the TLS mode used on each individual connection is still derived from that host's own flags.
    evm_use_tls: false
    # Real machine host.
    actual_host: "myvpc.cloud.ibm.com"
    # Local artifacts directory used for fetched crypto material.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: crypto/fabric_ca/enroll
```

### crypto/fetch

> Fetch EVM identity certificates

Fetches the EVM peer and user sign certificates so `fxconfig` can build namespace endorsement policies that reference them. Also fetches the client TLS CA certificate when `evm_use_tls` is `true`, so other Fabric-X components can be configured to trust EVM as an mTLS client.

```yaml
- name: Fetch EVM identity certificates
  vars:
    # Sets the organization mapping used for the embedded endorser's peer identity, the gateway's signing identity, and client TLS. `organization.role` must be `peer`. When `organization.fabric_ca_host` is undefined, crypto material generated by `cryptogen` is transferred; otherwise the identities are enrolled with Fabric CA. `organization.users` must declare at least one user; the first entry becomes the gateway's transaction-signing identity. `organization.namespaces` must declare exactly one entry; the gateway can only serve a single Fabric-X application namespace, and `config/transfer` fails otherwise.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      role: "peer"
      fabric_ca_host: "fca-org1"
      peer:
        name: "fabric-x-evm"
        secret: "fabric-x-evmPWD"
      users:
        - name: "fabric-x-evm"
          secret: "fabric-x-evmPWD"
      namespaces:
        - id: "basic"
          policy: "threshold"
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Local artifacts directory used for fetched crypto material.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
    # Name of the enrolled peer identity backing the embedded endorser.
    evm_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Enroll a shared client TLS key pair for EVM, used when any connected orderer or the committer sidecar requires mTLS. Set this to `true` whenever any orderer router (from `orderer_hosts`) or the committer sidecar (derived from `committer_hosts`) has `orderer_use_mtls` or `committer_use_mtls` enabled; the TLS mode used on each individual connection is still derived from that host's own flags.
    evm_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove crypto material

Remove EVM MSP and TLS artifacts from the host config directory. Also removes the Kubernetes Secret when Kubernetes deployment mode is enabled.

```yaml
- name: Remove crypto material
  vars:
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Use Kubernetes resources.
    evm_use_k8s: false
    # Selects the OpenShift deployment branch.
    evm_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: crypto/rm
```

### k8s/start

> Start the Kubernetes deployment

Create or update Kubernetes resources for the EVM gateway. Ensures the namespace exists, applies the Service, optional NodePort and LoadBalancer Services, a PersistentVolumeClaim template, and the StatefulSet, mounting the generated ConfigMap and Secret artifacts into the pod.

```yaml
- name: Start the Kubernetes deployment
  vars:
    # EVM container image.
    evm_image: "{{ evm_registry_endpoint }}/{{ evm_image_name }}:{{ evm_image_tag }}"
    # Image registry endpoint.
    evm_registry_endpoint: "{{ lookup('env', 'EVM_REGISTRY_ENDPOINT') or 'ghcr.io/hyperledger' }}"
    # Image name used by the EVM container.
    evm_image_name: fabric-x-evm
    # Image tag used by the EVM container.
    evm_image_tag: 0.1.3
    # Config mount path inside a container or pod.
    evm_container_config_dir: /config
    # Rendered EVM gateway configuration filename.
    evm_config_file: gateway.yaml
    # Data mount path inside a container or pod for the gateway and embedded endorser SQLite state.
    evm_container_data_dir: /data
    # StatefulSet rollout wait timeout in seconds.
    evm_k8s_wait_timeout: 120
    # Pod FSGroup used for mounted config, secrets, and data.
    evm_k8s_fs_group: 10001
    # Kubernetes namespace used for EVM resources.
    k8s_namespace: "fabricx-evm"
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to EVM resources.
    evm_k8s_part_of: evm
    # Optional image pull secret used by the EVM StatefulSet.
    k8s_image_pull_secret: "fabricx-registry-pull"
    # Ethereum JSON-RPC (HTTP and WebSocket) port exposed by the gateway.
    evm_port: 8545
    # Kubernetes NodePort value used by the external Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec.
    evm_k8s_node_port: 30545
    # Set to `true` to create a LoadBalancer Service entry that exposes the JSON-RPC port externally. When undefined or `false`, the JSON-RPC port is not included in the LoadBalancer Service.
    evm_k8s_loadbalancer_expose_port: false
    # Sets the organization mapping used for the embedded endorser's peer identity, the gateway's signing identity, and client TLS. `organization.role` must be `peer`. When `organization.fabric_ca_host` is undefined, crypto material generated by `cryptogen` is transferred; otherwise the identities are enrolled with Fabric CA. `organization.users` must declare at least one user; the first entry becomes the gateway's transaction-signing identity. `organization.namespaces` must declare exactly one entry; the gateway can only serve a single Fabric-X application namespace, and `config/transfer` fails otherwise.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      role: "peer"
      fabric_ca_host: "fca-org1"
      peer:
        name: "fabric-x-evm"
        secret: "fabric-x-evmPWD"
      users:
        - name: "fabric-x-evm"
          secret: "fabric-x-evmPWD"
      namespaces:
        - id: "basic"
          policy: "threshold"
    # Name of the enrolled peer identity backing the embedded endorser.
    evm_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Enroll a shared client TLS key pair for EVM, used when any connected orderer or the committer sidecar requires mTLS. Set this to `true` whenever any orderer router (from `orderer_hosts`) or the committer sidecar (derived from `committer_hosts`) has `orderer_use_mtls` or `committer_use_mtls` enabled; the TLS mode used on each individual connection is still derived from that host's own flags.
    evm_use_tls: false
    # Committer inventory hosts used to derive the committer sidecar the gateway and embedded endorser synchronize with. The sidecar is selected as the entry whose `committer_component_type` is `sidecar`; when the caller scopes this list to hosts sharing `organization.domain` with the EVM host, that selection also confirms the sidecar belongs to the same organization.
    committer_hosts:
      - "committer-sidecar"
      - "committer-validator"
    # Names the inventory hosts that provide the Fabric-X Orderer routers the gateway submits transactions to. One orderer endpoint is rendered per entry, across every organization.
    orderer_router_hosts:
      - "orderer-router-1"
      - "orderer-router-2"
      - "orderer-router-3"
      - "orderer-router-4"
    # Optional Kubernetes container resource requests and limits.
    k8s_resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "1000m"
    # StorageClass used for the EVM data PersistentVolumeClaim.
    k8s_storage_class: "standard"
    # Requested storage size for the EVM data PersistentVolumeClaim.
    k8s_storage_size: "500Mi"
    # Sets the EVM readiness probe initial delay.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Sets the EVM readiness probe period.
    k8s_readiness_probe_period_seconds: 10
    # Sets the EVM readiness probe timeout.
    k8s_readiness_probe_timeout_seconds: 5
    # Sets the EVM readiness probe failure threshold.
    k8s_readiness_probe_failure_threshold: 3
    # Sets the EVM liveness probe initial delay.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Sets the EVM liveness probe period.
    k8s_liveness_probe_period_seconds: 15
    # Sets the EVM liveness probe timeout.
    k8s_liveness_probe_timeout_seconds: 5
    # Sets the EVM liveness probe failure threshold.
    k8s_liveness_probe_failure_threshold: 5
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/start
```

### k8s/ping

> Check that the EVM Kubernetes services are reachable

Probes the configured NodePort value and LoadBalancer-exposed service port for external reachability, then asserts `eth_chainId` and `eth_blockNumber` succeed over that address.

```yaml
- name: Check that the EVM Kubernetes services are reachable
  vars:
    # Ethereum JSON-RPC (HTTP and WebSocket) port exposed by the gateway.
    evm_port: 8545
    # Kubernetes NodePort value used by the external Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec.
    evm_k8s_node_port: 30545
    # Set to `true` to create a LoadBalancer Service entry that exposes the JSON-RPC port externally. When undefined or `false`, the JSON-RPC port is not included in the LoadBalancer Service.
    evm_k8s_loadbalancer_expose_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/ping
```

### k8s/rm

> Remove Kubernetes resources

Remove the Kubernetes StatefulSet and Services created for the EVM gateway. Does not remove the ConfigMap, Secret, or PersistentVolumeClaim; use the Kubernetes config and crypto remove entry points, or `wipe`, for those generated artifacts.

```yaml
- name: Remove Kubernetes resources
  vars:
    # Kubernetes namespace used for EVM resources.
    k8s_namespace: "fabricx-evm"
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes NodePort value used by the external Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec.
    evm_k8s_node_port: 30545
    # Set to `true` to create a LoadBalancer Service entry that exposes the JSON-RPC port externally. When undefined or `false`, the JSON-RPC port is not included in the LoadBalancer Service.
    evm_k8s_loadbalancer_expose_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch pod logs

Collect logs from the Kubernetes pod running the EVM gateway.

```yaml
- name: Fetch pod logs
  vars:
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

> Publish the Kubernetes ConfigMap

Publish the rendered EVM configuration and trusted CA bundles as a Kubernetes ConfigMap.

```yaml
- name: Publish the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for EVM resources.
    k8s_namespace: "fabricx-evm"
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to EVM resources.
    evm_k8s_part_of: evm
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Rendered EVM gateway configuration filename.
    evm_config_file: gateway.yaml
    # Committer sidecar host derived from `committer_hosts` by `config/transfer` or `k8s/start`; consumed directly by `k8s/config/transfer`, which is always included from within their scope.
    sidecar_host: "committer-sidecar"
    # Names the inventory hosts that provide the Fabric-X Orderer routers the gateway submits transactions to. One orderer endpoint is rendered per entry, across every organization.
    orderer_router_hosts:
      - "orderer-router-1"
      - "orderer-router-2"
      - "orderer-router-3"
      - "orderer-router-4"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the Kubernetes ConfigMap

Remove the Kubernetes ConfigMap created for the EVM configuration.

```yaml
- name: Remove the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for EVM resources.
    k8s_namespace: "fabricx-evm"
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

> Publish the Kubernetes Secret

Publish the EVM peer MSP, user MSPs, and (when `evm_use_tls` is `true`) client TLS material as a Kubernetes Secret.

```yaml
- name: Publish the Kubernetes Secret
  vars:
    # Sets the organization mapping used for the embedded endorser's peer identity, the gateway's signing identity, and client TLS. `organization.role` must be `peer`. When `organization.fabric_ca_host` is undefined, crypto material generated by `cryptogen` is transferred; otherwise the identities are enrolled with Fabric CA. `organization.users` must declare at least one user; the first entry becomes the gateway's transaction-signing identity. `organization.namespaces` must declare exactly one entry; the gateway can only serve a single Fabric-X application namespace, and `config/transfer` fails otherwise.
    organization:
      name: "Org1"
      domain: "org1.example.com"
      role: "peer"
      fabric_ca_host: "fca-org1"
      peer:
        name: "fabric-x-evm"
        secret: "fabric-x-evmPWD"
      users:
        - name: "fabric-x-evm"
          secret: "fabric-x-evmPWD"
      namespaces:
        - id: "basic"
          policy: "threshold"
    # Remote config directory used by EVM.
    evm_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `evm_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/evm/config"
    # Name of the enrolled peer identity backing the embedded endorser.
    evm_crypto_name: "{{ organization.peer.name | default(inventory_hostname) }}"
    # Enroll a shared client TLS key pair for EVM, used when any connected orderer or the committer sidecar requires mTLS. Set this to `true` whenever any orderer router (from `orderer_hosts`) or the committer sidecar (derived from `committer_hosts`) has `orderer_use_mtls` or `committer_use_mtls` enabled; the TLS mode used on each individual connection is still derived from that host's own flags.
    evm_use_tls: false
    # Kubernetes namespace used for EVM resources.
    k8s_namespace: "fabricx-evm"
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to EVM resources.
    evm_k8s_part_of: evm
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Remove the Kubernetes Secret

Remove the Kubernetes Secret created for the EVM identities.

```yaml
- name: Remove the Kubernetes Secret
  vars:
    # Kubernetes namespace used for EVM resources.
    k8s_namespace: "fabricx-evm"
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: k8s/crypto/rm
```

### openshift/start

> Start the OpenShift deployment

Reuses the Kubernetes workload flow and manages an OpenShift Route for the JSON-RPC port.

```yaml
- name: Start the OpenShift deployment
  vars:
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to EVM resources.
    evm_k8s_part_of: evm
    # Specifies the OpenShift Route host for the JSON-RPC port.
    evm_openshift_route: "fabric-x-evm.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: openshift/start
```

### openshift/ping

> Check the OpenShift deployment

Checks the configured OpenShift Route and reuses the Kubernetes service ping flow.

```yaml
- name: Check the OpenShift deployment
  vars:
    # Specifies the OpenShift Route host for the JSON-RPC port.
    evm_openshift_route: "fabric-x-evm.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: openshift/ping
```

### openshift/rm

> Remove the OpenShift deployment

Reuses the Kubernetes workload flow and removes the OpenShift Route for the JSON-RPC port.

```yaml
- name: Remove the OpenShift deployment
  vars:
    # Kubernetes resource name used for the StatefulSet, Service, ConfigMap, Secret, optional NodePort Service, and PersistentVolumeClaim.
    evm_k8s_resource_name: "{{ inventory_hostname }}"
    # Specifies the OpenShift Route host for the JSON-RPC port.
    evm_openshift_route: "fabric-x-evm.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.evm
    tasks_from: openshift/rm
```
