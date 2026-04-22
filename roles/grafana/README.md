
# hyperledger.fabricx.grafana

> Runs a Grafana instance to visualize Fabric-X component metrics in container or Kubernetes mode.


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [start](#task-start)
  - [stop](#task-stop)
  - [teardown](#task-teardown)
  - [wipe](#task-wipe)
  - [fetch_logs](#task-fetch_logs)
  - [ping](#task-ping)
  - [container/start](#task-container-start)
  - [container/stop](#task-container-stop)
  - [container/rm](#task-container-rm)
  - [container/fetch_logs](#task-container-fetch_logs)
  - [config/transfer](#task-config-transfer)
  - [config/rm](#task-config-rm)
  - [config/copy_dashboard](#task-config-copy_dashboard)
  - [crypto/setup](#task-crypto-setup)
  - [crypto/fetch](#task-crypto-fetch)
  - [crypto/rm](#task-crypto-rm)
  - [crypto/openssl/generate_cert](#task-crypto-openssl-generate_cert)
  - [k8s/start](#task-k8s-start)
  - [k8s/ping](#task-k8s-ping)
  - [k8s/rm](#task-k8s-rm)
  - [k8s/fetch_logs](#task-k8s-fetch_logs)
  - [k8s/config/transfer](#task-k8s-config-transfer)
  - [k8s/config/rm](#task-k8s-config-rm)
  - [k8s/config/copy_dashboard](#task-k8s-config-copy_dashboard)
  - [k8s/crypto/transfer](#task-k8s-crypto-transfer)
  - [k8s/crypto/rm](#task-k8s-crypto-rm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-start"></a>

### start

Start Grafana in the selected deployment mode


Starts Grafana by dispatching to the container or Kubernetes entry point.

Set exactly one deployment mode flag for the target host.


```yaml
- name: Start Grafana in the selected deployment mode
  vars:
    # Enables container mode. The default derives from `grafana_use_k8s`.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: start
```

<a id="task-stop"></a>

### stop

Stop Grafana in container mode


Stops the Grafana container when container mode is enabled.


```yaml
- name: Stop Grafana in container mode
  vars:
    # Enables container mode. The default derives from `grafana_use_k8s`.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: stop
```

<a id="task-teardown"></a>

### teardown

Remove Grafana in the selected deployment mode


Removes the Grafana container or Kubernetes workload by dispatching to the matching entry point.


```yaml
- name: Remove Grafana in the selected deployment mode
  vars:
    # Enables container mode. The default derives from `grafana_use_k8s`.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: teardown
```

<a id="task-wipe"></a>

### wipe

Remove all Grafana data


Removes the Grafana workload, TLS material, and generated configuration.


```yaml
- name: Remove all Grafana data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: wipe
```

<a id="task-fetch_logs"></a>

### fetch_logs

Collect Grafana logs for the selected deployment mode


Collects Grafana logs from the container deployment or from the Kubernetes pod.


```yaml
- name: Collect Grafana logs for the selected deployment mode
  vars:
    # Enables container mode. The default derives from `grafana_use_k8s`.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: fetch_logs
```

<a id="task-ping"></a>

### ping

Check that the Grafana web port is reachable


Verifies that the Grafana web interface port is reachable on the target host.

In Kubernetes mode, also validates the optional NodePort configuration when enabled.


```yaml
- name: Check that the Grafana web port is reachable
  vars:
    # Enables Kubernetes mode.
    grafana_use_k8s: false
    # Sets the Grafana web port.
    grafana_web_port: 3000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: ping
```

<a id="task-container-start"></a>

### container/start

Start the Grafana container


Starts the containerized Grafana deployment.

TLS files are mounted when TLS is enabled.


```yaml
- name: Start the Grafana container
  vars:
    # Sets the Grafana container name. The default derives from `inventory_hostname`.
    grafana_container_name: "{{ inventory_hostname }}"
    # Sets the Grafana image reference. The default derives from `grafana_registry_endpoint`, `grafana_image_name`, and `grafana_image_tag`.
    grafana_image: "{{ grafana_registry_endpoint }}/{{ grafana_image_name }}:{{ grafana_image_tag }}"
    # Sets the Grafana image registry endpoint. The default derives from the `GRAFANA_REGISTRY_ENDPOINT` environment variable.
    grafana_registry_endpoint: "{{ lookup('env', 'GRAFANA_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana image name.
    grafana_image_name: grafana-oss
    # Sets the Grafana image tag.
    grafana_image_tag: latest
    # Sets the Grafana admin username.
    grafana_username: "string"
    # Sets the Grafana admin password. Store this value in Ansible Vault.
    grafana_password: "string"
    # Sets the Grafana web port.
    grafana_web_port: 3000
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the provisioning path inside the Grafana container.
    grafana_container_config_dir: /etc/grafana/provisioning
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Sets the Grafana TLS private key filename.
    grafana_tls_private_key_file: server.key
    # Sets the Grafana TLS certificate filename.
    grafana_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: container/start
```

<a id="task-container-stop"></a>

### container/stop

Stop the Grafana container


Stops the running Grafana container by name.


```yaml
- name: Stop the Grafana container
  vars:
    # Sets the Grafana container name. The default derives from `inventory_hostname`.
    grafana_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: container/stop
```

<a id="task-container-rm"></a>

### container/rm

Remove the Grafana container


Removes the Grafana container by name.


```yaml
- name: Remove the Grafana container
  vars:
    # Sets the Grafana container name. The default derives from `inventory_hostname`.
    grafana_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: container/rm
```

<a id="task-container-fetch_logs"></a>

### container/fetch_logs

Fetch logs from the Grafana container


Collects logs from the named Grafana container.


```yaml
- name: Fetch logs from the Grafana container
  vars:
    # Sets the Grafana container name. The default derives from `inventory_hostname`.
    grafana_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: container/fetch_logs
```

<a id="task-config-transfer"></a>

### config/transfer

Transfer Grafana configuration files


Writes Grafana provisioning files to the remote host.

Applies the Kubernetes ConfigMap when Kubernetes mode is enabled.


```yaml
- name: Transfer Grafana configuration files
  vars:
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the Grafana datasource provisioning filename.
    grafana_datasource_file: datasources.yaml
    # Sets the Grafana dashboard provider filename.
    grafana_dashboards_file: dashboards.yaml
    # Sets the provisioning path inside the Grafana container.
    grafana_container_config_dir: /etc/grafana/provisioning
    # Enables Kubernetes mode.
    grafana_use_k8s: false
    # Sets the inventory host name of the Prometheus instance used by Grafana. The referenced host must expose the Prometheus inventory vars used by the templates.
    prometheus_host: "string"
    # Sets the shared fetched-artifacts root used by Grafana. Required when relying on it to derive paths for fetched TLS artifacts.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/transfer
```

<a id="task-config-rm"></a>

### config/rm

Remove Grafana configuration files


Removes the remote Grafana provisioning directory.

Deletes the Kubernetes ConfigMap when Kubernetes mode is enabled.


```yaml
- name: Remove Grafana configuration files
  vars:
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/rm
```

<a id="task-config-copy_dashboard"></a>

### config/copy_dashboard

Copy a Grafana dashboard JSON file


Copies one Grafana dashboard JSON file into the remote dashboards directory.

Applies the dashboard ConfigMap when Kubernetes mode is enabled.


```yaml
- name: Copy a Grafana dashboard JSON file
  vars:
    # Sets the local path to the Grafana dashboard JSON file.
    grafana_dashboard_path: "string"
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the Grafana dashboard filename.
    grafana_dashboard_file: dashboard.json
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/copy_dashboard
```

<a id="task-crypto-setup"></a>

### crypto/setup

Prepare Grafana TLS material


Generates Grafana TLS material when TLS is enabled.

Applies the Kubernetes Secret when Kubernetes mode is enabled.


```yaml
- name: Prepare Grafana TLS material
  vars:
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/setup
```

<a id="task-crypto-fetch"></a>

### crypto/fetch

Fetch the Grafana TLS CA certificate


Fetches the Grafana TLS CA certificate when TLS is enabled.


```yaml
- name: Fetch the Grafana TLS CA certificate
  vars:
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the shared fetched-artifacts root used by Grafana. Required when relying on it to derive paths for fetched TLS artifacts.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/fetch
```

<a id="task-crypto-rm"></a>

### crypto/rm

Remove Grafana TLS material


Removes the Grafana TLS directory when TLS is enabled.

Deletes the Kubernetes Secret when Kubernetes mode is enabled.


```yaml
- name: Remove Grafana TLS material
  vars:
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Enables Kubernetes mode.
    grafana_use_k8s: false
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/rm
```

<a id="task-crypto-openssl-generate_cert"></a>

### crypto/openssl/generate_cert

Generate a self-signed certificate for Grafana


Generates the Grafana TLS key pair and certificate using OpenSSL.


```yaml
- name: Generate a self-signed certificate for Grafana
  vars:
    # Sets the optional organization mapping used for TLS certificate generation. When set, `organization.domain` is used as the OpenSSL organization name and otherwise defaults to `inventory_hostname`.
    organization: {}
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the Grafana TLS private key filename.
    grafana_tls_private_key_file: server.key
    # Sets the Grafana TLS certificate filename.
    grafana_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/openssl/generate_cert
```

<a id="task-k8s-start"></a>

### k8s/start

Start Grafana on Kubernetes


Applies the Grafana Service, optional NodePort Service, and Deployment on Kubernetes.

Generated provisioning files and optional dashboard ConfigMaps must already exist.


```yaml
- name: Start Grafana on Kubernetes
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Grafana web port.
    grafana_web_port: 3000
    # Enables the optional Grafana NodePort Service.
    grafana_k8s_use_node_port: false
    # Sets the optional explicit Grafana NodePort value used by the NodePort Service and ping checks. When omitted, Kubernetes can auto-assign the NodePort.
    grafana_k8s_web_node_port: 1000
    # Sets the Grafana Deployment wait timeout in seconds.
    grafana_k8s_wait_timeout: 120
    # Sets the Grafana pod filesystem group.
    grafana_k8s_fs_group: 472
    # Sets the Grafana image reference. The default derives from `grafana_registry_endpoint`, `grafana_image_name`, and `grafana_image_tag`.
    grafana_image: "{{ grafana_registry_endpoint }}/{{ grafana_image_name }}:{{ grafana_image_tag }}"
    # Sets the Grafana image registry endpoint. The default derives from the `GRAFANA_REGISTRY_ENDPOINT` environment variable.
    grafana_registry_endpoint: "{{ lookup('env', 'GRAFANA_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana image name.
    grafana_image_name: grafana-oss
    # Sets the Grafana image tag.
    grafana_image_tag: latest
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the provisioning path inside the Grafana container.
    grafana_container_config_dir: /etc/grafana/provisioning
    # Sets the Grafana datasource provisioning filename.
    grafana_datasource_file: datasources.yaml
    # Sets the Grafana dashboard provider filename.
    grafana_dashboards_file: dashboards.yaml
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Sets the Grafana TLS private key filename.
    grafana_tls_private_key_file: server.key
    # Sets the Grafana TLS certificate filename.
    grafana_tls_cert_file: server.crt
    # Sets the inventory host name of the Prometheus instance used by Grafana. The referenced host must expose the Prometheus inventory vars used by the templates.
    prometheus_host: "string"
    # Sets the Kubernetes namespace used for Grafana resources.
    k8s_namespace: "string"
    # Sets the optional image pull secret used by the Grafana Deployment.
    k8s_image_pull_secret: "string"
    # Sets the Grafana readiness probe initial delay.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Sets the Grafana readiness probe period.
    k8s_readiness_probe_period_seconds: 1000
    # Sets the Grafana readiness probe timeout.
    k8s_readiness_probe_timeout_seconds: 1000
    # Sets the Grafana readiness probe failure threshold.
    k8s_readiness_probe_failure_threshold: 1000
    # Sets the Grafana liveness probe initial delay.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Sets the Grafana liveness probe period.
    k8s_liveness_probe_period_seconds: 1000
    # Sets the Grafana liveness probe timeout.
    k8s_liveness_probe_timeout_seconds: 1000
    # Sets the Grafana liveness probe failure threshold.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/start
```

<a id="task-k8s-ping"></a>

### k8s/ping

Check that the Grafana NodePort is reachable


Checks that the Grafana NodePort is reachable when NodePort mode is enabled.


```yaml
- name: Check that the Grafana NodePort is reachable
  vars:
    # Sets the Grafana web port.
    grafana_web_port: 3000
    # Enables the optional Grafana NodePort Service.
    grafana_k8s_use_node_port: false
    # Sets the optional explicit Grafana NodePort value used by the NodePort Service and ping checks. When omitted, Kubernetes can auto-assign the NodePort.
    grafana_k8s_web_node_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/ping
```

<a id="task-k8s-rm"></a>

### k8s/rm

Remove Grafana Kubernetes resources


Deletes the Grafana Deployment, Service, and NodePort Service from Kubernetes.


```yaml
- name: Remove Grafana Kubernetes resources
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Grafana resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/rm
```

<a id="task-k8s-fetch_logs"></a>

### k8s/fetch_logs

Fetch logs from the Grafana pod


Collects logs from the Grafana pod selected by the Grafana application label.


```yaml
- name: Fetch logs from the Grafana pod
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/fetch_logs
```

<a id="task-k8s-config-transfer"></a>

### k8s/config/transfer

Apply the Grafana Kubernetes ConfigMap


Applies the Kubernetes ConfigMap that contains Grafana provisioning files.


```yaml
- name: Apply the Grafana Kubernetes ConfigMap
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the Grafana datasource provisioning filename.
    grafana_datasource_file: datasources.yaml
    # Sets the Grafana dashboard provider filename.
    grafana_dashboards_file: dashboards.yaml
    # Sets the inventory host name of the Prometheus instance used by Grafana. The referenced host must expose the Prometheus inventory vars used by the templates.
    prometheus_host: "string"
    # Sets the Kubernetes namespace used for Grafana resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/config/transfer
```

<a id="task-k8s-config-rm"></a>

### k8s/config/rm

Delete Grafana Kubernetes ConfigMaps


Deletes the Grafana provisioning ConfigMap and dashboard ConfigMaps.


```yaml
- name: Delete Grafana Kubernetes ConfigMaps
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the Kubernetes namespace used for Grafana resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/config/rm
```

<a id="task-k8s-config-copy_dashboard"></a>

### k8s/config/copy_dashboard

Apply a Grafana dashboard Kubernetes ConfigMap


Applies a dashboard ConfigMap for one Grafana dashboard JSON file.


```yaml
- name: Apply a Grafana dashboard Kubernetes ConfigMap
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Grafana dashboard filename.
    grafana_dashboard_file: dashboard.json
    # Sets the local path to the Grafana dashboard JSON file.
    grafana_dashboard_path: "string"
    # Sets the Kubernetes namespace used for Grafana resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/config/copy_dashboard
```

<a id="task-k8s-crypto-transfer"></a>

### k8s/crypto/transfer

Apply the Grafana Kubernetes Secret


Applies the Grafana Kubernetes Secret that holds admin credentials and optional TLS material.


```yaml
- name: Apply the Grafana Kubernetes Secret
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Grafana provisioning files and TLS material. The default derives from `remote_config_dir`.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Required when relying on it to derive the default for `grafana_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the Grafana admin username.
    grafana_username: "string"
    # Sets the Grafana admin password. Store this value in Ansible Vault.
    grafana_password: "string"
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Sets the Grafana TLS private key filename.
    grafana_tls_private_key_file: server.key
    # Sets the Grafana TLS certificate filename.
    grafana_tls_cert_file: server.crt
    # Sets the Kubernetes namespace used for Grafana resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/crypto/transfer
```

<a id="task-k8s-crypto-rm"></a>

### k8s/crypto/rm

Delete the Grafana Kubernetes Secret


Deletes the Grafana Kubernetes Secret.


```yaml
- name: Delete the Grafana Kubernetes Secret
  vars:
    # Sets the base Kubernetes resource name for Grafana. The default derives from `inventory_hostname`.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Grafana resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/crypto/rm
```


