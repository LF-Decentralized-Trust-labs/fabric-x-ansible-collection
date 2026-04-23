# hyperledger.fabricx.node_exporter

> Runs a Prometheus Node Exporter to collect machine state metrics (RAM, disk, CPU, network).

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)
  - [get_host_set](#get_host_set)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/transfer_grafana_dashboard](#configtransfer_grafana_dashboard)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate_cert](#cryptoopensslgenerate_cert)
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
  - [prometheus/get_scrapers](#prometheusget_scrapers)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.node_exporter
```

## Tasks

### start

Start Node Exporter

Starts Node Exporter using the container or Kubernetes backend selected for the host.

```yaml
- name: Start Node Exporter
  vars:
    # Enables the container backend. The default is derived from `node_exporter_use_k8s`.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: start
```

### stop

Stop Node Exporter

Stops a container-based Node Exporter deployment.

```yaml
- name: Stop Node Exporter
  vars:
    # Enables the container backend. The default is derived from `node_exporter_use_k8s`.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: stop
```

### teardown

Remove Node Exporter runtime resources

Removes Node Exporter runtime resources for the enabled backend.

```yaml
- name: Remove Node Exporter runtime resources
  vars:
    # Enables the container backend. The default is derived from `node_exporter_use_k8s`.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: teardown
```

### wipe

Remove Node Exporter data and runtime resources

Removes runtime resources, generated TLS material, and transferred configuration for Node Exporter.

```yaml
- name: Remove Node Exporter data and runtime resources
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: wipe
```

### fetch_logs

Collect Node Exporter logs

Collects logs from the active Node Exporter backend for this host.

```yaml
- name: Collect Node Exporter logs
  vars:
    # Enables the container backend. The default is derived from `node_exporter_use_k8s`.
    node_exporter_use_container: "{{ not node_exporter_use_k8s }}"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: fetch_logs
```

### ping

Check Node Exporter reachability

Verifies that the Node Exporter metrics port is reachable on the current host or, for Kubernetes deployments, that the NodePort exposure is reachable.

```yaml
- name: Check Node Exporter reachability
  vars:
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value.
    node_exporter_port: 1000
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: ping
```

### get_host_set

Build the Node Exporter host group

Adds one inventory host per unique `ansible_host` with a defined `node_exporter_port` to the `node_exporter_hosts` group.

```yaml
- name: Build the Node Exporter host group
  vars:
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value.
    node_exporter_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: get_host_set
```

### config/transfer

Transfer Node Exporter configuration

Creates the Node Exporter configuration directory and renders the web configuration file when TLS is enabled.

Also applies the Kubernetes ConfigMap when the Kubernetes backend is enabled.

```yaml
- name: Transfer Node Exporter configuration
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
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

Remove Node Exporter configuration

Removes transferred Node Exporter configuration files from the remote host.

Also removes the Kubernetes ConfigMap when the Kubernetes backend is enabled.

```yaml
- name: Remove Node Exporter configuration
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Enables the Kubernetes backend or cleanup path when true.
    node_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/rm
```

### config/transfer_grafana_dashboard

Transfer the Grafana dashboard for Node Exporter

Copies the bundled Node Exporter dashboard into Grafana by delegating to the Grafana role.

```yaml
- name: Transfer the Grafana dashboard for Node Exporter
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: config/transfer_grafana_dashboard
```

### crypto/setup

Generate Node Exporter TLS material

Generates TLS material for Node Exporter when TLS is enabled.

Also applies the Kubernetes TLS Secret when the Kubernetes backend is enabled.

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

Fetch Node Exporter TLS certificates

Fetches the generated Node Exporter CA certificate and server certificate from the remote host when TLS is enabled.

```yaml
- name: Fetch Node Exporter TLS certificates
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the local directory used to store fetched TLS artifacts.
    fetched_artifacts_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/fetch
```

### crypto/rm

Remove Node Exporter TLS material

Removes generated TLS material for Node Exporter.

Also removes the Kubernetes TLS Secret when the Kubernetes backend is enabled.

```yaml
- name: Remove Node Exporter TLS material
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
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

Generate a self-signed TLS certificate for Node Exporter

Delegates to the OpenSSL role to generate a self-signed certificate and private key for Node Exporter.

```yaml
- name: Generate a self-signed TLS certificate for Node Exporter
  vars:
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the Node Exporter TLS private key filename.
    node_exporter_tls_private_key_file: server.key
    # Sets the Node Exporter TLS certificate filename.
    node_exporter_tls_cert_file: server.crt
    # Provides organization data used to build the OpenSSL subject. When organization data does not define a domain value, the inventory hostname is used instead.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: crypto/openssl/generate_cert
```

### container/start

Start Node Exporter in a container

Starts the Node Exporter container with the configured image, port, mounts, and optional TLS web configuration.

```yaml
- name: Start Node Exporter in a container
  vars:
    # Sets the container name used for the Node Exporter runtime.
    node_exporter_container_name: node-exporter
    # Sets the registry endpoint used to build the default Node Exporter image reference. The default reads `NODE_EXPORTER_REGISTRY_ENDPOINT` and falls back to `docker.io/prom`.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference. The default derives from `node_exporter_registry_endpoint`, `node_exporter_image_name`, and `node_exporter_image_tag`.
    node_exporter_image: "{{ node_exporter_registry_endpoint }}/{{ node_exporter_image_name }}:{{ node_exporter_image_tag }}"
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value.
    node_exporter_port: 1000
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
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

Stop the Node Exporter container

Stops the Node Exporter container by delegating to the shared container role.

```yaml
- name: Stop the Node Exporter container
  vars:
    # Sets the container name used for the Node Exporter runtime.
    node_exporter_container_name: node-exporter
    # Sets the registry endpoint used to build the default Node Exporter image reference. The default reads `NODE_EXPORTER_REGISTRY_ENDPOINT` and falls back to `docker.io/prom`.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference. The default derives from `node_exporter_registry_endpoint`, `node_exporter_image_name`, and `node_exporter_image_tag`.
    node_exporter_image: "{{ node_exporter_registry_endpoint }}/{{ node_exporter_image_name }}:{{ node_exporter_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: container/stop
```

### container/rm

Remove the Node Exporter container

Removes the Node Exporter container by delegating to the shared container role.

```yaml
- name: Remove the Node Exporter container
  vars:
    # Sets the container name used for the Node Exporter runtime.
    node_exporter_container_name: node-exporter
    # Sets the registry endpoint used to build the default Node Exporter image reference. The default reads `NODE_EXPORTER_REGISTRY_ENDPOINT` and falls back to `docker.io/prom`.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference. The default derives from `node_exporter_registry_endpoint`, `node_exporter_image_name`, and `node_exporter_image_tag`.
    node_exporter_image: "{{ node_exporter_registry_endpoint }}/{{ node_exporter_image_name }}:{{ node_exporter_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: container/rm
```

### container/fetch_logs

Fetch logs from the Node Exporter container

Collects logs from the Node Exporter container by delegating to the shared container role.

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

Start Node Exporter on Kubernetes

Creates the Kubernetes Service, optional NodePort Service, and DaemonSet for Node Exporter.

```yaml
- name: Start Node Exporter on Kubernetes
  vars:
    # Sets how long to wait for the Node Exporter DaemonSet rollout.
    node_exporter_k8s_wait_timeout: 120
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. The default derives from `inventory_hostname`.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value.
    node_exporter_port: 1000
    # Sets the Kubernetes NodePort used for Node Exporter when `node_exporter_k8s_use_node_port` is true. The default derives from `node_exporter_port`.
    node_exporter_k8s_port_node_port: 1000
    # Enables the optional NodePort Service and NodePort reachability check when true.
    node_exporter_k8s_use_node_port: false
    # Sets the registry endpoint used to build the default Node Exporter image reference. The default reads `NODE_EXPORTER_REGISTRY_ENDPOINT` and falls back to `docker.io/prom`.
    node_exporter_registry_endpoint: "{{ lookup('env', 'NODE_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Sets the Node Exporter image name used in the default image reference.
    node_exporter_image_name: node-exporter
    # Sets the Node Exporter image tag used in the default image reference.
    node_exporter_image_tag: latest
    # Sets the full Node Exporter image reference. The default derives from `node_exporter_registry_endpoint`, `node_exporter_image_name`, and `node_exporter_image_tag`.
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
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true.
    k8s_namespace: "string"
    # Sets the optional image pull secret used by the Node Exporter DaemonSet.
    k8s_image_pull_secret: "string"
    # Overrides the DaemonSet readiness probe initial delay. The template defaults to 10 seconds.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Overrides the DaemonSet readiness probe period. The template defaults to 10 seconds.
    k8s_readiness_probe_period_seconds: 1000
    # Overrides the DaemonSet readiness probe timeout. The template defaults to 5 seconds.
    k8s_readiness_probe_timeout_seconds: 1000
    # Overrides the DaemonSet readiness probe failure threshold. The template defaults to 3 failures.
    k8s_readiness_probe_failure_threshold: 1000
    # Overrides the DaemonSet liveness probe initial delay. The template defaults to 30 seconds.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Overrides the DaemonSet liveness probe period. The template defaults to 15 seconds.
    k8s_liveness_probe_period_seconds: 1000
    # Overrides the DaemonSet liveness probe timeout. The template defaults to 5 seconds.
    k8s_liveness_probe_timeout_seconds: 1000
    # Overrides the DaemonSet liveness probe failure threshold. The template defaults to 5 failures.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/start
```

### k8s/ping

Check Node Exporter reachability on Kubernetes

Checks that the Kubernetes NodePort exposed by Node Exporter is reachable when the NodePort Service is enabled.

```yaml
- name: Check Node Exporter reachability on Kubernetes
  vars:
    # Sets the TCP port exposed by Node Exporter and seeds the default Kubernetes NodePort value.
    node_exporter_port: 1000
    # Enables the optional NodePort Service and NodePort reachability check when true.
    node_exporter_k8s_use_node_port: false
    # Sets the Kubernetes NodePort used for Node Exporter when `node_exporter_k8s_use_node_port` is true. The default derives from `node_exporter_port`.
    node_exporter_k8s_port_node_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/ping
```

### k8s/rm

Remove Node Exporter Kubernetes resources

Removes the Kubernetes DaemonSet and Services created for Node Exporter.

```yaml
- name: Remove Node Exporter Kubernetes resources
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. The default derives from `inventory_hostname`.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/rm
```

### k8s/fetch_logs

Fetch logs from Node Exporter pods

Collects logs from Node Exporter pods by delegating to the shared Kubernetes role.

```yaml
- name: Fetch logs from Node Exporter pods
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. The default derives from `inventory_hostname`.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

Apply the Node Exporter Kubernetes ConfigMap

Ensures the target namespace exists and applies the ConfigMap used by the Node Exporter DaemonSet.

```yaml
- name: Apply the Node Exporter Kubernetes ConfigMap
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. The default derives from `inventory_hostname`.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Sets the rendered Node Exporter web configuration filename.
    node_exporter_web_config_file: web-config.yaml
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

Remove the Node Exporter Kubernetes ConfigMap

Deletes the ConfigMap used by the Node Exporter Kubernetes deployment.

```yaml
- name: Remove the Node Exporter Kubernetes ConfigMap
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. The default derives from `inventory_hostname`.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

Apply the Node Exporter Kubernetes TLS Secret

Ensures the target namespace exists and applies the Secret that stores Node Exporter TLS material.

```yaml
- name: Apply the Node Exporter Kubernetes TLS Secret
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. The default derives from `inventory_hostname`.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables the TLS web configuration and certificate paths when true.
    node_exporter_use_tls: false
    # Sets the base remote deployment directory used by `node_exporter_remote_config_dir`.
    remote_deploy_dir: "string"
    # Sets the remote Node Exporter configuration directory. The default derives from `remote_deploy_dir`.
    node_exporter_remote_config_dir: "{{ remote_deploy_dir }}/node-exporter/config"
    # Sets the Node Exporter TLS private key filename.
    node_exporter_tls_private_key_file: server.key
    # Sets the Node Exporter TLS certificate filename.
    node_exporter_tls_cert_file: server.crt
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

Remove the Node Exporter Kubernetes TLS Secret

Deletes the Secret that stores Node Exporter TLS material for Kubernetes deployments.

```yaml
- name: Remove the Node Exporter Kubernetes TLS Secret
  vars:
    # Sets the Kubernetes object name used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. The default derives from `inventory_hostname`.
    node_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Node Exporter resources, including the Service, optional NodePort Service, and DaemonSet. Required when `node_exporter_use_k8s` is true.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: k8s/crypto/rm
```

### prometheus/get_scrapers

Build Prometheus scrape targets for Node Exporter

Builds the scrape service definitions Prometheus uses to collect metrics from the selected Node Exporter hosts.

```yaml
- name: Build Prometheus scrape targets for Node Exporter
  vars:
    # Lists the inventory hosts exposed as Prometheus scrape targets.
    node_exporter_hosts: ["entry1", "entry2"]
    # Sets the local directory used to store fetched TLS artifacts.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.node_exporter
    tasks_from: prometheus/get_scrapers
```
