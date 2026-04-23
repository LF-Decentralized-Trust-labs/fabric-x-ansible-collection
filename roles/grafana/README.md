# hyperledger.fabricx.grafana

> Manages Grafana for Fabric-X metrics visualization in container and Kubernetes deployments, including provisioning, dashboards, data sources, and TLS artifacts.

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
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch_logs](#containerfetch_logs)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/copy_dashboard](#configcopy_dashboard)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate_cert](#cryptoopensslgenerate_cert)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch_logs](#k8sfetch_logs)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/config/copy_dashboard](#k8sconfigcopy_dashboard)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.grafana
```

## Tasks

### start

> Start Grafana in the selected deployment mode

Starts Grafana by dispatching to the container or Kubernetes entry point after provisioning data sources, dashboards, and optional TLS artifacts have been prepared. Set exactly one deployment mode flag for the target host.

```yaml
- name: Start Grafana in the selected deployment mode
  vars:
    # Enables container mode.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: start
```

### stop

> Stop Grafana in container mode

Stops the Grafana container without removing the generated provisioning or TLS artifacts.

```yaml
- name: Stop Grafana in container mode
  vars:
    # Enables container mode.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: stop
```

### teardown

> Remove Grafana in the selected deployment mode

Removes the Grafana container or Kubernetes workload by dispatching to the matching entry point. Leaves generated provisioning files and TLS material in place for reuse or later cleanup.

```yaml
- name: Remove Grafana in the selected deployment mode
  vars:
    # Enables container mode.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: teardown
```

### wipe

> Remove all Grafana data

Removes the Grafana workload, generated configuration, and TLS material.

```yaml
- name: Remove all Grafana data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: wipe
```

### fetch_logs

> Collect Grafana logs for the selected deployment mode

Collects Grafana logs from the container deployment or from the Kubernetes pod for troubleshooting.

```yaml
- name: Collect Grafana logs for the selected deployment mode
  vars:
    # Enables container mode.
    grafana_use_container: "{{ not grafana_use_k8s }}"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: fetch_logs
```

### ping

> Check that the Grafana web port is reachable

Verifies that the Grafana web interface port is reachable on the target host. In Kubernetes mode, also validates the optional NodePort configuration when enabled.

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

### container/start

> Start the Grafana container

Starts the containerized Grafana deployment with the generated datasource and dashboard provisioning files mounted into the container. TLS files are mounted when TLS is enabled.

```yaml
- name: Start the Grafana container
  vars:
    # Sets the Grafana container name.
    grafana_container_name: "{{ inventory_hostname }}"
    # Sets the Grafana image reference.
    grafana_image: "{{ grafana_registry_endpoint }}/{{ grafana_image_name }}:{{ grafana_image_tag }}"
    # Sets the Grafana image registry endpoint.
    grafana_registry_endpoint: "{{ lookup('env', 'GRAFANA_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana image name.
    grafana_image_name: grafana-oss
    # Sets the Grafana image tag.
    grafana_image_tag: latest
    # Sets the Grafana admin username. Example: `admin`.
    grafana_username: "admin"
    # Sets the Grafana admin password. Example: `{{ vault_grafana_admin_password }}`. Store this value in Ansible Vault.
    grafana_password: "{{ vault_grafana_admin_password }}"
    # Sets the Grafana web port.
    grafana_web_port: 3000
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
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

### container/stop

> Stop the Grafana container

Stops the running Grafana container by name without deleting the associated artifacts.

```yaml
- name: Stop the Grafana container
  vars:
    # Sets the Grafana container name.
    grafana_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: container/stop
```

### container/rm

> Remove the Grafana container

Removes the Grafana container by name while leaving the staged provisioning files and TLS material untouched.

```yaml
- name: Remove the Grafana container
  vars:
    # Sets the Grafana container name.
    grafana_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch logs from the Grafana container

Collects logs from the named Grafana container for post-startup inspection.

```yaml
- name: Fetch logs from the Grafana container
  vars:
    # Sets the Grafana container name.
    grafana_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: container/fetch_logs
```

### config/transfer

> Transfer Grafana configuration files

Writes the datasource and dashboard provisioning files to the remote Grafana config directory. Applies the Kubernetes ConfigMap when Kubernetes mode is enabled.

```yaml
- name: Transfer Grafana configuration files
  vars:
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Sets the Grafana datasource provisioning filename.
    grafana_datasource_file: datasources.yaml
    # Sets the Grafana dashboard provider filename.
    grafana_dashboards_file: dashboards.yaml
    # Sets the provisioning path inside the Grafana container.
    grafana_container_config_dir: /etc/grafana/provisioning
    # Enables Kubernetes mode.
    grafana_use_k8s: false
    # Sets the inventory host name of the Prometheus instance used by Grafana. Example: `prometheus-1.example.com`. The referenced host must expose the Prometheus inventory vars used by the templates.
    prometheus_host: "prometheus-1.example.com"
    # Sets the shared fetched-artifacts root used by Grafana. Example: `/tmp/fabricx-artifacts`. Required when relying on it to derive paths for fetched TLS artifacts.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/transfer
```

### config/rm

> Remove Grafana configuration files

Removes the remote Grafana provisioning directory. Deletes the Kubernetes ConfigMap when Kubernetes mode is enabled.

```yaml
- name: Remove Grafana configuration files
  vars:
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/rm
```

### config/copy_dashboard

> Copy a Grafana dashboard JSON file

Copies one Grafana dashboard JSON file into the remote dashboards directory. Applies the dashboard ConfigMap when Kubernetes mode is enabled.

```yaml
- name: Copy a Grafana dashboard JSON file
  vars:
    # Sets the local path to the Grafana dashboard JSON file. Example: `/opt/fabricx/grafana/dashboards/main.json`.
    grafana_dashboard_path: "/opt/fabricx/grafana/dashboards/main.json"
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Sets the Grafana dashboard filename.
    grafana_dashboard_file: dashboard.json
    # Enables Kubernetes mode.
    grafana_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/copy_dashboard
```

### crypto/setup

> Prepare Grafana TLS material

Generates Grafana TLS material when TLS is enabled and stages it with the other Grafana artifacts. Applies the Kubernetes Secret when Kubernetes mode is enabled.

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

### crypto/fetch

> Fetch the Grafana TLS CA certificate

Fetches the Grafana TLS CA certificate when TLS is enabled so other roles can trust the Grafana endpoint.

```yaml
- name: Fetch the Grafana TLS CA certificate
  vars:
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Sets the shared fetched-artifacts root used by Grafana. Example: `/tmp/fabricx-artifacts`. Required when relying on it to derive paths for fetched TLS artifacts.
    fetched_artifacts_dir: "/tmp/fabricx-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove Grafana TLS material

Removes the Grafana TLS directory when TLS is enabled. Deletes the Kubernetes Secret when Kubernetes mode is enabled.

```yaml
- name: Remove Grafana TLS material
  vars:
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Enables Kubernetes mode.
    grafana_use_k8s: false
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/rm
```

### crypto/openssl/generate_cert

> Generate a self-signed certificate for Grafana

Generates the Grafana TLS key pair and certificate using OpenSSL for the staged Grafana artifacts directory.

```yaml
- name: Generate a self-signed certificate for Grafana
  vars:
    # Sets the optional organization mapping used for TLS certificate generation. Example: `{'name': 'Grafana', 'domain': 'grafana.fabricx.example'}`. When set, `organization.domain` is used as the OpenSSL organization name.
    organization:
      name: "Grafana"
      domain: "grafana.fabricx.example"
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Sets the Grafana TLS private key filename.
    grafana_tls_private_key_file: server.key
    # Sets the Grafana TLS certificate filename.
    grafana_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/openssl/generate_cert
```

### k8s/start

> Start Grafana on Kubernetes

Applies the Grafana Service, optional NodePort Service, Secret, ConfigMaps, and Deployment on Kubernetes. Generated datasource, dashboard, and TLS artifacts must already exist.

```yaml
- name: Start Grafana on Kubernetes
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Grafana web port.
    grafana_web_port: 3000
    # Enables the optional Grafana NodePort Service.
    grafana_k8s_use_node_port: false
    # Sets the optional explicit Grafana NodePort value used by the NodePort Service and ping checks. Example: `32000`. When omitted, Kubernetes can auto-assign the NodePort.
    grafana_k8s_web_node_port: 32000
    # Sets the Grafana Deployment wait timeout in seconds.
    grafana_k8s_wait_timeout: 120
    # Sets the Grafana pod filesystem group.
    grafana_k8s_fs_group: 472
    # Sets the Grafana image reference.
    grafana_image: "{{ grafana_registry_endpoint }}/{{ grafana_image_name }}:{{ grafana_image_tag }}"
    # Sets the Grafana image registry endpoint.
    grafana_registry_endpoint: "{{ lookup('env', 'GRAFANA_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana image name.
    grafana_image_name: grafana-oss
    # Sets the Grafana image tag.
    grafana_image_tag: latest
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
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
    # Sets the inventory host name of the Prometheus instance used by Grafana. Example: `prometheus-1.example.com`. The referenced host must expose the Prometheus inventory vars used by the templates.
    prometheus_host: "prometheus-1.example.com"
    # Sets the Kubernetes namespace used for Grafana resources. Example: `fabricx-observability`.
    k8s_namespace: "fabricx-observability"
    # Sets the optional image pull secret used by the Grafana Deployment. Example: `grafana-registry-secret`.
    k8s_image_pull_secret: "grafana-registry-secret"
    # Sets the Grafana readiness probe initial delay. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Sets the Grafana readiness probe period. Example: `5`.
    k8s_readiness_probe_period_seconds: 5
    # Sets the Grafana readiness probe timeout. Example: `3`.
    k8s_readiness_probe_timeout_seconds: 3
    # Sets the Grafana readiness probe failure threshold. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Sets the Grafana liveness probe initial delay. Example: `20`.
    k8s_liveness_probe_initial_delay_seconds: 20
    # Sets the Grafana liveness probe period. Example: `10`.
    k8s_liveness_probe_period_seconds: 10
    # Sets the Grafana liveness probe timeout. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Sets the Grafana liveness probe failure threshold. Example: `3`.
    k8s_liveness_probe_failure_threshold: 3
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/start
```

### k8s/ping

> Check that the Grafana NodePort is reachable

Checks that the Grafana NodePort is reachable when NodePort mode is enabled.

```yaml
- name: Check that the Grafana NodePort is reachable
  vars:
    # Sets the Grafana web port.
    grafana_web_port: 3000
    # Enables the optional Grafana NodePort Service.
    grafana_k8s_use_node_port: false
    # Sets the optional explicit Grafana NodePort value used by the NodePort Service and ping checks. Example: `32000`. When omitted, Kubernetes can auto-assign the NodePort.
    grafana_k8s_web_node_port: 32000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/ping
```

### k8s/rm

> Remove Grafana Kubernetes resources

Deletes the Grafana Deployment, Service, and NodePort Service from Kubernetes.

```yaml
- name: Remove Grafana Kubernetes resources
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Grafana resources. Example: `fabricx-observability`.
    k8s_namespace: "fabricx-observability"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch logs from the Grafana pod

Collects logs from the Grafana pod selected by the Grafana application label.

```yaml
- name: Fetch logs from the Grafana pod
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

> Apply the Grafana Kubernetes ConfigMap

Applies the Kubernetes ConfigMap that contains Grafana provisioning files for the datasource and dashboard providers.

```yaml
- name: Apply the Grafana Kubernetes ConfigMap
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Sets the Grafana datasource provisioning filename.
    grafana_datasource_file: datasources.yaml
    # Sets the Grafana dashboard provider filename.
    grafana_dashboards_file: dashboards.yaml
    # Sets the inventory host name of the Prometheus instance used by Grafana. Example: `prometheus-1.example.com`. The referenced host must expose the Prometheus inventory vars used by the templates.
    prometheus_host: "prometheus-1.example.com"
    # Sets the Kubernetes namespace used for Grafana resources. Example: `fabricx-observability`.
    k8s_namespace: "fabricx-observability"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Delete Grafana Kubernetes ConfigMaps

Deletes the Grafana provisioning ConfigMap and dashboard ConfigMaps from the namespace.

```yaml
- name: Delete Grafana Kubernetes ConfigMaps
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Sets the Kubernetes namespace used for Grafana resources. Example: `fabricx-observability`.
    k8s_namespace: "fabricx-observability"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/config/rm
```

### k8s/config/copy_dashboard

> Apply a Grafana dashboard Kubernetes ConfigMap

Applies a dashboard ConfigMap for one Grafana dashboard JSON file.

```yaml
- name: Apply a Grafana dashboard Kubernetes ConfigMap
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Grafana dashboard filename.
    grafana_dashboard_file: dashboard.json
    # Sets the local path to the Grafana dashboard JSON file. Example: `/opt/fabricx/grafana/dashboards/main.json`.
    grafana_dashboard_path: "/opt/fabricx/grafana/dashboards/main.json"
    # Sets the Kubernetes namespace used for Grafana resources. Example: `fabricx-observability`.
    k8s_namespace: "fabricx-observability"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/config/copy_dashboard
```

### k8s/crypto/transfer

> Apply the Grafana Kubernetes Secret

Applies the Grafana Kubernetes Secret that holds admin credentials and optional TLS material for the Grafana Deployment.

```yaml
- name: Apply the Grafana Kubernetes Secret
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Grafana provisioning files and TLS material.
    grafana_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the shared remote config root used by Grafana. Example: `/var/hyperledger/fabricx/grafana`. Required when using it for `grafana_remote_config_dir`.
    remote_config_dir: "/var/hyperledger/fabricx/grafana"
    # Sets the Grafana admin username. Example: `admin`.
    grafana_username: "admin"
    # Sets the Grafana admin password. Example: `{{ vault_grafana_admin_password }}`. Store this value in Ansible Vault.
    grafana_password: "{{ vault_grafana_admin_password }}"
    # Enables Grafana TLS handling.
    grafana_use_tls: false
    # Sets the Grafana TLS private key filename.
    grafana_tls_private_key_file: server.key
    # Sets the Grafana TLS certificate filename.
    grafana_tls_cert_file: server.crt
    # Sets the Kubernetes namespace used for Grafana resources. Example: `fabricx-observability`.
    k8s_namespace: "fabricx-observability"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Delete the Grafana Kubernetes Secret

Deletes the Grafana Kubernetes Secret from the namespace.

```yaml
- name: Delete the Grafana Kubernetes Secret
  vars:
    # Sets the base Kubernetes resource name for Grafana.
    grafana_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Grafana resources. Example: `fabricx-observability`.
    k8s_namespace: "fabricx-observability"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: k8s/crypto/rm
```
