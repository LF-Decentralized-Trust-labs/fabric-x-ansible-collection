# hyperledger.fabricx.node_exporter

> Runs Prometheus Node Exporter in container or Kubernetes mode to collect machine state metrics such as RAM, disk, CPU, and network usage.

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
  - [get\_host\_set](#get_host_set)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/transfer\_grafana\_dashboard](#configtransfer_grafana_dashboard)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate\_cert](#cryptoopensslgenerate_cert)
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
  - [prometheus/get\_scrapers](#prometheusget_scrapers)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.node_exporter
```

## Tasks

### start

> Start Node Exporter

Starts Node Exporter using the backend selected for the host. In container mode, launches the local `node_exporter_container_name` container and publishes `node_exporter_port`. In Kubernetes mode, creates the Service and DaemonSet in `k8s_namespace` and waits for rollout completion.

```yaml
- name: Start Node Exporter
  vars:
    # Enables the container backend.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: start
```

### stop

> Stop Node Exporter

Stops the container-backed Node Exporter workload for the host. Kubernetes deployments use `teardown` instead of this entry point.

```yaml
- name: Stop Node Exporter
  vars:
    # Enables the container backend.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: stop
```

### teardown

> Remove Node Exporter runtime resources

Removes Node Exporter runtime resources for the enabled backend. Container mode removes the local runtime container. Kubernetes mode removes the Service, optional NodePort Service, and DaemonSet.

```yaml
- name: Remove Node Exporter runtime resources
  vars:
    # Enables the container backend.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: teardown
```

### wipe

> Remove Node Exporter data and runtime resources

Removes runtime resources, generated TLS material, and transferred configuration for Node Exporter. Use this to fully reset either deployment mode on the current host.

```yaml
- name: Remove Node Exporter data and runtime resources
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: wipe
```

### fetch_logs

> Collect Node Exporter logs

Collects logs from the active Node Exporter backend for this host. Container mode reads the container log stream. Kubernetes mode reads the matching pod logs from the DaemonSet.

```yaml
- name: Collect Node Exporter logs
  vars:
    # Enables the container backend.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: fetch_logs
```

### ping

> Check Node Exporter reachability

Verifies that the Node Exporter metrics port is reachable on the current host. Kubernetes deployments verify the optional NodePort exposure when it is enabled.

```yaml
- name: Check Node Exporter reachability
  vars:
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value. Example: `9100`.
    node_exporter_port: 9100
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: ping
```

### get_host_set

> Build the Node Exporter host group

Adds one inventory host per unique `ansible_host` with a defined `node_exporter_port` to the `node_exporter_hosts` group. Example hosts include `worker-1`, `worker-2`, and `worker-3`.

```yaml
- name: Build the Node Exporter host group
  vars:
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value. Example: `9100`.
    node_exporter_port: 9100
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: get_host_set
```

### config/transfer

> Transfer Node Exporter configuration

Creates the Node Exporter configuration directory and renders the web configuration file when TLS is enabled. Container mode writes the config under `node_exporter_remote_config_dir` for bind-mounting into the runtime container. Kubernetes mode also applies the ConfigMap that supplies the same config to the DaemonSet.

```yaml
- name: Transfer Node Exporter configuration
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the configuration mount point inside the Node Exporter container.
    node_exporter_container_config_dir: /var/config
    # Sets the rendered Node Exporter web configuration filename.
    node_exporter_web_config_file: web-config.yaml
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Sets the Node Exporter TLS private key filename.
    node_exporter_tls_private_key_file: server.key
    # Sets the Node Exporter TLS certificate filename.
    node_exporter_tls_cert_file: server.crt
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/transfer
```

### config/rm

> Remove Node Exporter configuration

Removes transferred Node Exporter configuration files from the remote host. Kubernetes mode also removes the ConfigMap used by the DaemonSet.

```yaml
- name: Remove Node Exporter configuration
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/rm
```

### config/transfer_grafana_dashboard

> Transfer the Grafana dashboard for Node Exporter

Copies the bundled Node Exporter dashboard into Grafana by delegating to the Grafana role.

```yaml
- name: Transfer the Grafana dashboard for Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/transfer_grafana_dashboard
```

### crypto/setup

> Generate Node Exporter TLS material

Generates TLS material for Node Exporter when TLS is enabled. Container mode writes certs and keys under `node_exporter_remote_config_dir`/tls. Kubernetes mode also applies the Secret that mounts the same artifacts into the DaemonSet.

```yaml
- name: Generate Node Exporter TLS material
  vars:
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/setup
```

### crypto/fetch

> Fetch Node Exporter TLS certificates

Fetches the generated Node Exporter CA certificate and server certificate from the remote host when TLS is enabled. Writes the artifacts into `fetched_artifacts_dir` for later reuse.

```yaml
- name: Fetch Node Exporter TLS certificates
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the local directory used to store fetched TLS artifacts. Example: `/tmp/fabricx-artifacts/node-exporter`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove Node Exporter TLS material

Removes generated TLS material for Node Exporter. Kubernetes mode also removes the TLS Secret used by the DaemonSet.

```yaml
- name: Remove Node Exporter TLS material
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/rm
```

### crypto/openssl/generate_cert

> Generate a self-signed TLS certificate for Node Exporter

Delegates to the OpenSSL role to generate a self-signed certificate and private key for Node Exporter. Uses the organization data and TLS filenames to place the artifacts under the Node Exporter config path.

```yaml
- name: Generate a self-signed TLS certificate for Node Exporter
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the Node Exporter TLS private key filename.
    node_exporter_tls_private_key_file: server.key
    # Sets the Node Exporter TLS certificate filename.
    node_exporter_tls_cert_file: server.crt
    # Provides organization data used to build the OpenSSL subject. When organization data does not define a domain value, the inventory hostname is used instead. Example: `domain=node-exporter.example.org, common_name=node-exporter, organization=Example Org`.
    organization:domain=node-exporter.example.org, common_name=node-exporter, organization=Example Org
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/openssl/generate_cert
```

### container/start

> Start Node Exporter in a container

Starts the Node Exporter container with the configured image, port, mounts, and optional TLS web configuration. The container name comes from `node_exporter_container_name` and the image from `node_exporter_image`. The runtime binds the host root filesystem plus `node_exporter_remote_config_dir` for config and TLS material.

```yaml
- name: Start Node Exporter in a container
  vars:
    # Sets the container name used for the Node Exporter runtime.
    node_exporter_container_name: node-exporter
    # Sets the registry endpoint used to build the default Node Exporter image reference.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference.
    node_exporter_image: "{{ node_exporter_registry_endpoint }}/{{ node_exporter_image_name }}:{{ node_exporter_image_tag }}"
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value. Example: `9100`.
    node_exporter_port: 9100
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the configuration mount point inside the Node Exporter container.
    node_exporter_container_config_dir: /var/config
    # Sets the rendered Node Exporter web configuration filename.
    node_exporter_web_config_file: web-config.yaml
    # Sets the host root filesystem mount flags used by the container runtime path.
    node_exporter_root_fs_flags: ro,rslave
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: container/start
```

### container/stop

> Stop the Node Exporter container

Stops the Node Exporter container by delegating to the shared container role. Uses the configured container name and image reference to identify the runtime.

```yaml
- name: Stop the Node Exporter container
  vars:
    # Sets the container name used for the Node Exporter runtime.
    node_exporter_container_name: node-exporter
    # Sets the registry endpoint used to build the default Node Exporter image reference.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference.
    node_exporter_image: "{{ node_exporter_registry_endpoint }}/{{ node_exporter_image_name }}:{{ node_exporter_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: container/stop
```

### container/rm

> Remove the Node Exporter container

Removes the Node Exporter container by delegating to the shared container role. Leaves the config and TLS paths untouched so a later start can reuse them if desired.

```yaml
- name: Remove the Node Exporter container
  vars:
    # Sets the container name used for the Node Exporter runtime.
    node_exporter_container_name: node-exporter
    # Sets the registry endpoint used to build the default Node Exporter image reference.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference.
    node_exporter_image: "{{ node_exporter_registry_endpoint }}/{{ node_exporter_image_name }}:{{ node_exporter_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch logs from the Node Exporter container

Collects logs from the Node Exporter container by delegating to the shared container role. This is the container-mode log path used by the top-level fetch_logs entry point.

```yaml
- name: Fetch logs from the Node Exporter container
  vars:
    # Sets the container name used for the Node Exporter runtime.
    node_exporter_container_name: node-exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: container/fetch_logs
```

### k8s/start

> Start Node Exporter on Kubernetes

Creates the Kubernetes Service, optional NodePort Service, and DaemonSet for Node Exporter. Uses `k8s_namespace`, `node_exporter_k8s_resource_name`, and `node_exporter_port` to shape the workload identity and service exposure. Waits for the DaemonSet rollout before returning.

```yaml
- name: Start Node Exporter on Kubernetes
  vars:
    # Sets how long to wait for the Node Exporter DaemonSet rollout.
    node_exporter_k8s_wait_timeout: 120
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value. Example: `9100`.
    node_exporter_port: 9100
    # Sets the Kubernetes NodePort used for Node Exporter when `node_exporter_k8s_use_node_port` is true. Example: `31000`.
    node_exporter_k8s_node_port: 31000
    # Enables the optional NodePort Service and NodePort reachability check when true.
    node_exporter_k8s_use_node_port: false
    # Sets the registry endpoint used to build the default Node Exporter image reference.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference.
    node_exporter_image: "{{ node_exporter_registry_endpoint }}/{{ node_exporter_image_name }}:{{ node_exporter_image_tag }}"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Sets the configuration mount point inside the Node Exporter container.
    node_exporter_container_config_dir: /var/config
    # Sets the rendered Node Exporter web configuration filename.
    node_exporter_web_config_file: web-config.yaml
    # Sets the Node Exporter TLS certificate filename.
    node_exporter_tls_cert_file: server.crt
    # Sets the Node Exporter TLS private key filename.
    node_exporter_tls_private_key_file: server.key
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true. Example: `monitoring`.
    k8s_namespace: "monitoring"
    # Sets the optional image pull secret used by the Node Exporter DaemonSet. Example: `regcred`.
    k8s_image_pull_secret: "regcred"
    # Overrides the DaemonSet readiness probe initial delay. The template defaults to 10 seconds. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Overrides the DaemonSet readiness probe period. The template defaults to 10 seconds. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Overrides the DaemonSet readiness probe timeout. The template defaults to 5 seconds. Example: `5`.
    k8s_readiness_probe_timeout_seconds: 5
    # Overrides the DaemonSet readiness probe failure threshold. The template defaults to 3 failures. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Overrides the DaemonSet liveness probe initial delay. The template defaults to 30 seconds. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Overrides the DaemonSet liveness probe period. The template defaults to 15 seconds. Example: `15`.
    k8s_liveness_probe_period_seconds: 15
    # Overrides the DaemonSet liveness probe timeout. The template defaults to 5 seconds. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Overrides the DaemonSet liveness probe failure threshold. The template defaults to 5 failures. Example: `5`.
    k8s_liveness_probe_failure_threshold: 5
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/start
```

### k8s/ping

> Check Node Exporter reachability on Kubernetes

Checks that the Kubernetes NodePort exposed by Node Exporter is reachable when the NodePort Service is enabled. Skips the NodePort check when `node_exporter_k8s_use_node_port` is false.

```yaml
- name: Check Node Exporter reachability on Kubernetes
  vars:
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value. Example: `9100`.
    node_exporter_port: 9100
    # Enables the optional NodePort Service and NodePort reachability check when true.
    node_exporter_k8s_use_node_port: false
    # Sets the Kubernetes NodePort used for Node Exporter when `node_exporter_k8s_use_node_port` is true. Example: `31000`.
    node_exporter_k8s_node_port: 31000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/ping
```

### k8s/rm

> Remove Node Exporter Kubernetes resources

Removes the Kubernetes DaemonSet and Services created for Node Exporter. Targets the workload by `k8s_namespace` and `node_exporter_k8s_resource_name`.

```yaml
- name: Remove Node Exporter Kubernetes resources
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true. Example: `monitoring`.
    k8s_namespace: "monitoring"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch logs from Node Exporter pods

Collects logs from Node Exporter pods by delegating to the shared Kubernetes role. This is the Kubernetes-mode log path used by the top-level fetch_logs entry point.

```yaml
- name: Fetch logs from Node Exporter pods
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

> Apply the Node Exporter Kubernetes ConfigMap

Ensures the target namespace exists and applies the ConfigMap used by the Node Exporter DaemonSet. The ConfigMap points at `node_exporter_remote_config_dir` content and the rendered web config when TLS is enabled.

```yaml
- name: Apply the Node Exporter Kubernetes ConfigMap
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Sets the rendered Node Exporter web configuration filename.
    node_exporter_web_config_file: web-config.yaml
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true. Example: `monitoring`.
    k8s_namespace: "monitoring"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the Node Exporter Kubernetes ConfigMap

Deletes the ConfigMap used by the Node Exporter Kubernetes deployment. Keeps the namespace and runtime pods untouched so teardown can be handled separately.

```yaml
- name: Remove the Node Exporter Kubernetes ConfigMap
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true. Example: `monitoring`.
    k8s_namespace: "monitoring"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

> Apply the Node Exporter Kubernetes TLS Secret

Ensures the target namespace exists and applies the Secret that stores Node Exporter TLS material. The Secret name matches `node_exporter_k8s_resource_name`.

```yaml
- name: Apply the Node Exporter Kubernetes TLS Secret
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`. Example: `/opt/fabricx/node-exporter`.
    remote_deploy_dir: "/opt/fabricx/node-exporter"
    # Sets the remote Node Exporter configuration directory.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the Node Exporter TLS private key filename.
    node_exporter_tls_private_key_file: server.key
    # Sets the Node Exporter TLS certificate filename.
    node_exporter_tls_cert_file: server.crt
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true. Example: `monitoring`.
    k8s_namespace: "monitoring"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Remove the Node Exporter Kubernetes TLS Secret

Deletes the Secret that stores Node Exporter TLS material for Kubernetes deployments. Targets the Secret named after `node_exporter_k8s_resource_name`.

```yaml
- name: Remove the Node Exporter Kubernetes TLS Secret
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true. Example: `monitoring`.
    k8s_namespace: "monitoring"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/crypto/rm
```

### prometheus/get_scrapers

> Build Prometheus scrape targets for Node Exporter

Builds the scrape service definitions Prometheus uses to collect metrics from the selected Node Exporter hosts. Uses the host list from `node_exporter_hosts` together with `node_exporter_port` to create scrape targets.

```yaml
- name: Build Prometheus scrape targets for Node Exporter
  vars:
    # Lists the inventory hosts exposed as Prometheus scrape targets. Example: `['worker-1', 'worker-2', 'worker-3']`.
    node_exporter_hosts:
      - "worker-1"
      - "worker-2"
      - "worker-3"
    # Sets the local directory used to store fetched TLS artifacts. Example: `/tmp/fabricx-artifacts/node-exporter`.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts/node-exporter"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: prometheus/get_scrapers
```
