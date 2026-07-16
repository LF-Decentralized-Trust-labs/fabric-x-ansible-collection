# hyperledger.fabricx.block_explorer

> Deploys and manages the Fabric-X Block Explorer server across container and Kubernetes modes, including committer sidecar streaming, PostgreSQL connectivity, TLS/mTLS, and log collection workflows.

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
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [crypto/setup](#cryptosetup)
  - [crypto/openssl/generate\_cert](#cryptoopensslgenerate_cert)
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
ansible-doc -t role hyperledger.fabricx.block_explorer
```

## Tasks

### start

> Start the Block Explorer server

Start the Block Explorer server runtime selected by the deployment mode flags. Container mode is the default, and Kubernetes mode applies Services and a Deployment. The runtime consumes the rendered Block Explorer configuration and TLS material prepared by the config and crypto entry points.

```yaml
- name: Start the Block Explorer server
  vars:
    # Run the container runtime.
    block_explorer_use_container: "{{ (not block_explorer_use_k8s) and (not block_explorer_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: start
```

### stop

> Stop the Block Explorer server

Stop the active Block Explorer container without removing configuration, crypto material, logs, or Kubernetes resources.

```yaml
- name: Stop the Block Explorer server
  vars:
    # Run the container runtime.
    block_explorer_use_container: "{{ (not block_explorer_use_k8s) and (not block_explorer_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: stop
```

### teardown

> Remove runtime artifacts

Remove runtime resources for the selected Block Explorer deployment mode. Deletes the local container or Kubernetes workload resources while leaving generated config, crypto material, and fetched artifacts intact.

```yaml
- name: Remove runtime artifacts
  vars:
    # Run the container runtime.
    block_explorer_use_container: "{{ (not block_explorer_use_k8s) and (not block_explorer_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: teardown
```

### wipe

> Remove all Block Explorer server data

Remove Block Explorer runtime resources, generated configuration, and crypto material from the host.

```yaml
- name: Remove all Block Explorer server data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: wipe
```

### fetch_logs

> Collect runtime logs

Collect Block Explorer server logs for the selected deployment mode.

```yaml
- name: Collect runtime logs
  vars:
    # Run the container runtime.
    block_explorer_use_container: "{{ (not block_explorer_use_k8s) and (not block_explorer_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: fetch_logs
```

### ping

> Check the REST endpoint

Verify that the Block Explorer REST endpoint is reachable. Uses direct host access for container deployments and delegates to the Kubernetes ping task when `block_explorer_use_k8s` is enabled.

```yaml
- name: Check the REST endpoint
  vars:
    # REST API port exposed by the Block Explorer server. Example: `18080`.
    block_explorer_port: 18080
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: ping
```

### container/start

> Start the container runtime

Start the Block Explorer server as a local container with the rendered config directory mounted read-only. Exposes the REST port and waits for it to become reachable.

```yaml
- name: Start the container runtime
  vars:
    # Container name used by the runtime.
    block_explorer_container_name: "{{ inventory_hostname }}"
    # Block Explorer container image.
    block_explorer_image: "{{ block_explorer_registry_endpoint }}/{{ block_explorer_image_name }}:{{ block_explorer_image_tag }}"
    # Image registry endpoint.
    block_explorer_registry_endpoint: "{{ lookup('env', 'BLOCK_EXPLORER_REGISTRY_ENDPOINT') or 'ghcr.io/lf-decentralized-trust-labs' }}"
    # Image name used by the Block Explorer container.
    block_explorer_image_name: fabric-x-block-explorer
    # Image tag used by the Block Explorer container.
    block_explorer_image_tag: 0.1.0-dryrun.2
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Config mount path inside a container or pod.
    block_explorer_container_config_dir: /app/config
    # Rendered Block Explorer config filename.
    block_explorer_config_file: config.yaml
    # REST API port exposed by the Block Explorer server. Example: `18080`.
    block_explorer_port: 18080
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: container/start
```

### container/stop

> Stop the container runtime

Stop the local Block Explorer container. Preserves the container definition, mounted configuration, crypto material, and logs for later cleanup or collection.

```yaml
- name: Stop the container runtime
  vars:
    # Container name used by the runtime.
    block_explorer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: container/stop
```

### container/rm

> Remove the container runtime

Remove the local Block Explorer container runtime resources. Leaves host-side generated configuration and crypto material under the remote config directory.

```yaml
- name: Remove the container runtime
  vars:
    # Container name used by the runtime.
    block_explorer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch container logs

Collect logs from a containerized Block Explorer runtime.

```yaml
- name: Fetch container logs
  vars:
    # Container name used by the runtime.
    block_explorer_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: container/fetch_logs
```

### config/transfer

> Render and transfer the Block Explorer configuration

Render the Block Explorer configuration file with the resolved PostgreSQL and committer sidecar connection details. Transfers the committer sidecar and PostgreSQL TLS CA certificates when their respective TLS modes are enabled. For Kubernetes deployments, also publishes the rendered config and trusted CA bundles as a ConfigMap.

```yaml
- name: Render and transfer the Block Explorer configuration
  vars:
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Config mount path inside a container or pod.
    block_explorer_container_config_dir: /app/config
    # Rendered Block Explorer config filename.
    block_explorer_config_file: config.yaml
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
    # REST API port exposed by the Block Explorer server. Example: `18080`.
    block_explorer_port: 18080
    # First block number streamed from the committer sidecar.
    block_explorer_start_block: 0
    # Number of block processor workers.
    block_explorer_processor_count: 4
    # Number of database writer workers.
    block_explorer_writer_count: 4
    # Maximum PostgreSQL connection pool size.
    block_explorer_max_conns: 20
    # Buffer size of the raw block channel.
    block_explorer_raw_channel_size: 500
    # Buffer size of the processed block channel.
    block_explorer_proc_channel_size: 500
    # Default page size for transaction list REST queries.
    block_explorer_default_tx_limit: 50
    # Filename of the self-signed client TLS private key used for mTLS to the committer sidecar.
    block_explorer_tls_private_key_file: client.key
    # Filename of the self-signed client TLS certificate used for mTLS to the committer sidecar.
    block_explorer_tls_cert_file: client.crt
    # Names the inventory host that provides the committer sidecar Block Explorer streams from. Example: `committer-sidecar`.
    sidecar_host: "committer-sidecar"
    # Names the inventory host that provides the PostgreSQL database used by Block Explorer. Example: `block-explorer-db`.
    postgres_db_host: "block-explorer-db"
    # Local artifacts directory used for fetched TLS material. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: config/transfer
```

### config/rm

> Remove rendered configuration

Remove host-side rendered Block Explorer configuration. Also removes the Kubernetes ConfigMap when Kubernetes deployment mode is enabled.

```yaml
- name: Remove rendered configuration
  vars:
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: config/rm
```

### crypto/setup

> Prepare crypto material

Generates a self-signed client certificate for the committer sidecar mTLS connection when the sidecar requires mTLS. Then publishes Kubernetes Secret material when Kubernetes mode is enabled.

```yaml
- name: Prepare crypto material
  vars:
    # Names the inventory host that provides the committer sidecar Block Explorer streams from. Example: `committer-sidecar`.
    sidecar_host: "committer-sidecar"
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: crypto/setup
```

### crypto/openssl/generate_cert

> Generate a self-signed client certificate for Block Explorer

Generates the Block Explorer client TLS key pair and certificate using OpenSSL for the staged Block Explorer artifacts directory.

```yaml
- name: Generate a self-signed client certificate for Block Explorer
  vars:
    # Sets the optional organization mapping used for TLS certificate generation. Example: `{'domain': 'block-explorer.fabricx.example'}`.
    organization:
      domain: "block-explorer.fabricx.example"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Filename of the self-signed client TLS private key used for mTLS to the committer sidecar.
    block_explorer_tls_private_key_file: client.key
    # Filename of the self-signed client TLS certificate used for mTLS to the committer sidecar.
    block_explorer_tls_cert_file: client.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: crypto/openssl/generate_cert
```

### crypto/fetch

> Fetch the Block Explorer client CA certificate

Fetches the Block Explorer self-signed client CA certificate so the committer sidecar can trust it as an mTLS client.

```yaml
- name: Fetch the Block Explorer client CA certificate
  vars:
    # Names the inventory host that provides the committer sidecar Block Explorer streams from. Example: `committer-sidecar`.
    sidecar_host: "committer-sidecar"
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Local artifacts directory used for fetched TLS material. Example: `/tmp/fabricx-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove crypto material

Remove Block Explorer TLS artifacts from the host config directory. Also removes the Kubernetes Secret when Kubernetes deployment mode is enabled.

```yaml
- name: Remove crypto material
  vars:
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Use Kubernetes resources.
    block_explorer_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: crypto/rm
```

### k8s/start

> Start the Kubernetes deployment

Create or update Kubernetes resources for the Block Explorer server. Ensures the namespace exists, applies the Service, optional NodePort and LoadBalancer Services, and Deployment, and mounts generated ConfigMap and optional Secret artifacts into the pod.

```yaml
- name: Start the Kubernetes deployment
  vars:
    # Block Explorer container image.
    block_explorer_image: "{{ block_explorer_registry_endpoint }}/{{ block_explorer_image_name }}:{{ block_explorer_image_tag }}"
    # Image registry endpoint.
    block_explorer_registry_endpoint: "{{ lookup('env', 'BLOCK_EXPLORER_REGISTRY_ENDPOINT') or 'ghcr.io/lf-decentralized-trust-labs' }}"
    # Image name used by the Block Explorer container.
    block_explorer_image_name: fabric-x-block-explorer
    # Image tag used by the Block Explorer container.
    block_explorer_image_tag: 0.1.0-dryrun.2
    # Config mount path inside a container or pod.
    block_explorer_container_config_dir: /app/config
    # Rendered Block Explorer config filename.
    block_explorer_config_file: config.yaml
    # Deployment rollout wait timeout in seconds.
    block_explorer_k8s_wait_timeout: 120
    # Pod FSGroup used for mounted config and secrets.
    block_explorer_k8s_fs_group: 10001
    # Kubernetes namespace used for Block Explorer resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Block Explorer resources.
    block_explorer_k8s_part_of: block-explorer
    # Optional image pull secret used by the Block Explorer Deployment. Example: `fabricx-registry-pull`.
    k8s_image_pull_secret: "fabricx-registry-pull"
    # REST API port exposed by the Block Explorer server. Example: `18080`.
    block_explorer_port: 18080
    # Kubernetes NodePort value used by the external Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30680`.
    block_explorer_k8s_node_port: 30680
    # Set to `true` to create a LoadBalancer Service entry that exposes the REST port externally. When undefined or `false`, the REST port is not included in the LoadBalancer Service.
    block_explorer_k8s_loadbalancer_expose_port: false
    # Filename of the self-signed client TLS private key used for mTLS to the committer sidecar.
    block_explorer_tls_private_key_file: client.key
    # Filename of the self-signed client TLS certificate used for mTLS to the committer sidecar.
    block_explorer_tls_cert_file: client.crt
    # Names the inventory host that provides the committer sidecar Block Explorer streams from. Example: `committer-sidecar`.
    sidecar_host: "committer-sidecar"
    # Names the inventory host that provides the PostgreSQL database used by Block Explorer. Example: `block-explorer-db`.
    postgres_db_host: "block-explorer-db"
    # Optional Kubernetes container resource requests and limits. Example: `{'requests': {'memory': '512Mi', 'cpu': '250m'}, 'limits': {'memory': '1Gi', 'cpu': '1000m'}}`.
    k8s_resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "1000m"
    # Sets the Block Explorer readiness probe initial delay. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Sets the Block Explorer readiness probe period. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Sets the Block Explorer readiness probe timeout. Example: `5`.
    k8s_readiness_probe_timeout_seconds: 5
    # Sets the Block Explorer readiness probe failure threshold. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Sets the Block Explorer liveness probe initial delay. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Sets the Block Explorer liveness probe period. Example: `15`.
    k8s_liveness_probe_period_seconds: 15
    # Sets the Block Explorer liveness probe timeout. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Sets the Block Explorer liveness probe failure threshold. Example: `5`.
    k8s_liveness_probe_failure_threshold: 5
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/start
```

### k8s/ping

> Check that the Block Explorer Kubernetes service is reachable

Probes configured Kubernetes NodePort values and LoadBalancer-exposed service ports for external reachability.

```yaml
- name: Check that the Block Explorer Kubernetes service is reachable
  vars:
    # REST API port exposed by the Block Explorer server. Example: `18080`.
    block_explorer_port: 18080
    # Kubernetes NodePort value used by the external Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30680`.
    block_explorer_k8s_node_port: 30680
    # Set to `true` to create a LoadBalancer Service entry that exposes the REST port externally. When undefined or `false`, the REST port is not included in the LoadBalancer Service.
    block_explorer_k8s_loadbalancer_expose_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/ping
```

### k8s/rm

> Remove Kubernetes resources

Remove the Kubernetes Deployment and Services created for the Block Explorer server. Does not remove the ConfigMap or Secret; use the Kubernetes config and crypto remove entry points for those generated artifacts.

```yaml
- name: Remove Kubernetes resources
  vars:
    # Kubernetes namespace used for Block Explorer resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes NodePort value used by the external Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30680`.
    block_explorer_k8s_node_port: 30680
    # Set to `true` to create a LoadBalancer Service entry that exposes the REST port externally. When undefined or `false`, the REST port is not included in the LoadBalancer Service.
    block_explorer_k8s_loadbalancer_expose_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch pod logs

Collect logs from the Kubernetes pod running the Block Explorer server.

```yaml
- name: Fetch pod logs
  vars:
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

> Publish the Kubernetes ConfigMap

Publish the rendered Block Explorer configuration and trusted CA bundles as a Kubernetes ConfigMap.

```yaml
- name: Publish the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for Block Explorer resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Block Explorer resources.
    block_explorer_k8s_part_of: block-explorer
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Rendered Block Explorer config filename.
    block_explorer_config_file: config.yaml
    # Names the inventory host that provides the committer sidecar Block Explorer streams from. Example: `committer-sidecar`.
    sidecar_host: "committer-sidecar"
    # Names the inventory host that provides the PostgreSQL database used by Block Explorer. Example: `block-explorer-db`.
    postgres_db_host: "block-explorer-db"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the Kubernetes ConfigMap

Remove the Kubernetes ConfigMap created for the Block Explorer configuration.

```yaml
- name: Remove the Kubernetes ConfigMap
  vars:
    # Kubernetes namespace used for Block Explorer resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

> Publish the Kubernetes Secret

Publish the Block Explorer self-signed client TLS material as a Kubernetes Secret when the committer sidecar requires mTLS.

```yaml
- name: Publish the Kubernetes Secret
  vars:
    # Names the inventory host that provides the committer sidecar Block Explorer streams from. Example: `committer-sidecar`.
    sidecar_host: "committer-sidecar"
    # Remote config directory used by Block Explorer.
    block_explorer_remote_config_dir: "{{ remote_config_dir }}"
    # Base remote config directory that feeds `block_explorer_remote_config_dir`. Example: `/var/hyperledger/fabricx/block-explorer/config`.
    remote_config_dir: "/var/hyperledger/fabricx/block-explorer/config"
    # Filename of the self-signed client TLS private key used for mTLS to the committer sidecar.
    block_explorer_tls_private_key_file: client.key
    # Filename of the self-signed client TLS certificate used for mTLS to the committer sidecar.
    block_explorer_tls_cert_file: client.crt
    # Kubernetes namespace used for Block Explorer resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Block Explorer resources.
    block_explorer_k8s_part_of: block-explorer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Remove the Kubernetes Secret

Remove the Kubernetes Secret created for the Block Explorer client TLS material.

```yaml
- name: Remove the Kubernetes Secret
  vars:
    # Kubernetes namespace used for Block Explorer resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: k8s/crypto/rm
```

### openshift/start

> Start the OpenShift deployment

Reuses the Kubernetes workload flow and manages an OpenShift Route for the REST port.

```yaml
- name: Start the OpenShift deployment
  vars:
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Block Explorer resources.
    block_explorer_k8s_part_of: block-explorer
    # Specifies the OpenShift Route host. Example: `block-explorer.apps.example.com`.
    block_explorer_openshift_route: "block-explorer.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: openshift/start
```

### openshift/ping

> Check the OpenShift deployment

Checks the configured OpenShift Route and reuses the Kubernetes service ping flow.

```yaml
- name: Check the OpenShift deployment
  vars:
    # Specifies the OpenShift Route host. Example: `block-explorer.apps.example.com`.
    block_explorer_openshift_route: "block-explorer.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: openshift/ping
```

### openshift/rm

> Remove the OpenShift deployment

Reuses the Kubernetes workload flow and removes the OpenShift Route for the REST port.

```yaml
- name: Remove the OpenShift deployment
  vars:
    # Kubernetes resource name used for the Deployment, Service, ConfigMap, optional Secret, and optional NodePort Service.
    block_explorer_k8s_resource_name: "{{ inventory_hostname }}"
    # Specifies the OpenShift Route host. Example: `block-explorer.apps.example.com`.
    block_explorer_openshift_route: "block-explorer.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer
    tasks_from: openshift/rm
```
