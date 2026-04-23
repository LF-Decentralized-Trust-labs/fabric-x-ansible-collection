# hyperledger.fabricx.prometheus

> Runs a Prometheus metrics collector in container or Kubernetes mode.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [ping](#ping)
  - [start](#start)
  - [container/start](#containerstart)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [stop](#stop)
  - [container/stop](#containerstop)
  - [teardown](#teardown)
  - [container/rm](#containerrm)
  - [k8s/rm](#k8srm)
  - [data/rm](#datarm)
  - [k8s/data/rm](#k8sdatarm)
  - [wipe](#wipe)
  - [crypto/setup](#cryptosetup)
  - [crypto/openssl/generate_cert](#cryptoopensslgenerate_cert)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [k8s/crypto/rm](#k8scryptorm)
  - [config/transfer](#configtransfer)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [config/rm](#configrm)
  - [k8s/config/rm](#k8sconfigrm)
  - [fetch_logs](#fetch_logs)
  - [container/fetch_logs](#containerfetch_logs)
  - [k8s/fetch_logs](#k8sfetch_logs)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### ping

Check that the Prometheus port is reachable

Validates network reachability to the Prometheus listener on the target host or to the Kubernetes NodePort when enabled.

```yaml
- name: Check that the Prometheus port is reachable
  vars:
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services. Example: `9090`.
    prometheus_port: 9090
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: ping
```

### start

Start Prometheus in the selected deployment mode

Starts Prometheus either as a container or as Kubernetes resources based on the deployment mode flags.

When Kubernetes mode is enabled, it can also apply the optional NodePort Service.

```yaml
- name: Start Prometheus in the selected deployment mode
  vars:
    # Enables the container deployment path when set to `true`. The default is the inverse of `prometheus_use_k8s`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: start
```

### container/start

Start the Prometheus container

Creates the remote data directory and starts Prometheus through the shared container role.

```yaml
- name: Start the Prometheus container
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote data directory consumed by `prometheus_remote_data_dir`.
    remote_data_dir: "string"
    # Container registry endpoint for Prometheus images. Defaults to the `PROMETHEUS_REGISTRY_ENDPOINT` environment variable or `docker.io/prom`.
    prometheus_registry_endpoint: "{{ lookup('env', 'PROMETHEUS_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Image name used when composing `prometheus_image`.
    prometheus_image_name: prometheus
    # Image tag used when composing `prometheus_image`.
    prometheus_image_tag: latest
    # Fully qualified Prometheus container image. The default is composed from `prometheus_registry_endpoint`, `prometheus_image_name`, and `prometheus_image_tag`.
    prometheus_image: "{{ prometheus_registry_endpoint }}/{{ prometheus_image_name }}:{{ prometheus_image_tag }}"
    # Container name used for the Prometheus workload. Defaults to `inventory_hostname`.
    prometheus_container_name: "{{ inventory_hostname }}"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where Prometheus TSDB data is stored. Defaults to `remote_data_dir`.
    prometheus_remote_data_dir: "{{ remote_data_dir }}"
    # In-container or in-pod mount point for Prometheus configuration files.
    prometheus_container_config_dir: /etc/prometheus/config
    # In-container or in-pod path for Prometheus TSDB data.
    prometheus_container_data_dir: /data
    # Filename of the main Prometheus scrape configuration.
    prometheus_config_file: prometheus.yaml
    # Filename of the Prometheus web TLS configuration file.
    prometheus_web_config_file: web-config.yaml
    # Filename of the promtool HTTP client configuration used for TLS health checks.
    prometheus_http_config_file: http-config.yaml
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services. Example: `9090`.
    prometheus_port: 9090
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/start
```

### k8s/start

Start Prometheus on Kubernetes

Creates the Kubernetes headless Service, optional NodePort Service, and StatefulSet resources for Prometheus after ensuring the namespace exists.

```yaml
- name: Start Prometheus on Kubernetes
  vars:
    # Container registry endpoint for Prometheus images. Defaults to the `PROMETHEUS_REGISTRY_ENDPOINT` environment variable or `docker.io/prom`.
    prometheus_registry_endpoint: "{{ lookup('env', 'PROMETHEUS_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Image name used when composing `prometheus_image`.
    prometheus_image_name: prometheus
    # Image tag used when composing `prometheus_image`.
    prometheus_image_tag: latest
    # Fully qualified Prometheus container image. The default is composed from `prometheus_registry_endpoint`, `prometheus_image_name`, and `prometheus_image_tag`.
    prometheus_image: "{{ prometheus_registry_endpoint }}/{{ prometheus_image_name }}:{{ prometheus_image_tag }}"
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services. Example: `9090`.
    prometheus_port: 9090
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables the optional Kubernetes NodePort Service when set to `true`.
    prometheus_k8s_use_node_port: false
    # NodePort value used to expose Prometheus outside the cluster when `prometheus_k8s_use_node_port` is enabled. Must be set to a valid Kubernetes NodePort value when `prometheus_k8s_use_node_port` is `true`.
    prometheus_k8s_node_port: 1000
    # File system group assigned to the pod.
    prometheus_k8s_fs_group: 65534
    # In-container or in-pod mount point for Prometheus configuration files.
    prometheus_container_config_dir: /etc/prometheus/config
    # In-container or in-pod path for Prometheus TSDB data.
    prometheus_container_data_dir: /data
    # Filename of the main Prometheus scrape configuration.
    prometheus_config_file: prometheus.yaml
    # Filename of the Prometheus web TLS configuration file.
    prometheus_web_config_file: web-config.yaml
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
    # Maximum number of seconds to wait for the StatefulSet rollout.
    prometheus_k8s_wait_timeout: 120
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Persistent volume size requested for Prometheus data. Example: `20Gi`.
    k8s_storage_size: "string"
    # Optional image pull secret name for private registries.
    k8s_image_pull_secret: "string"
    # Optional Kubernetes storage class name for the Prometheus PVC.
    k8s_storage_class: "string"
    # Initial delay before the readiness probe starts.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Interval between readiness probe attempts.
    k8s_readiness_probe_period_seconds: 1000
    # Timeout for each readiness probe request.
    k8s_readiness_probe_timeout_seconds: 1000
    # Number of failed readiness probes before the pod is marked unready.
    k8s_readiness_probe_failure_threshold: 1000
    # Initial delay before the liveness probe starts.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Interval between liveness probe attempts.
    k8s_liveness_probe_period_seconds: 1000
    # Timeout for each liveness probe request.
    k8s_liveness_probe_timeout_seconds: 1000
    # Number of failed liveness probes before Kubernetes restarts the pod.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/start
```

### k8s/ping

Check that the Prometheus NodePort is reachable

Validates network reachability to the Kubernetes NodePort when the optional NodePort Service is enabled.

```yaml
- name: Check that the Prometheus NodePort is reachable
  vars:
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services. Example: `9090`.
    prometheus_port: 9090
    # Enables the optional Kubernetes NodePort Service when set to `true`.
    prometheus_k8s_use_node_port: false
    # NodePort value used to expose Prometheus outside the cluster when `prometheus_k8s_use_node_port` is enabled. Must be set to a valid Kubernetes NodePort value when `prometheus_k8s_use_node_port` is `true`.
    prometheus_k8s_node_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/ping
```

### stop

Stop the Prometheus container deployment

Stops Prometheus when the container deployment path is enabled.

```yaml
- name: Stop the Prometheus container deployment
  vars:
    # Enables the container deployment path when set to `true`. The default is the inverse of `prometheus_use_k8s`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: stop
```

### container/stop

Stop the Prometheus container

Stops the running Prometheus container through the shared container role.

```yaml
- name: Stop the Prometheus container
  vars:
    # Container name used for the Prometheus workload. Defaults to `inventory_hostname`.
    prometheus_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/stop
```

### teardown

Remove the Prometheus deployment

Removes the Prometheus container or Kubernetes workload and then deletes its data.

```yaml
- name: Remove the Prometheus deployment
  vars:
    # Enables the container deployment path when set to `true`. The default is the inverse of `prometheus_use_k8s`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: teardown
```

### container/rm

Remove the Prometheus container

Removes the Prometheus container through the shared container role.

```yaml
- name: Remove the Prometheus container
  vars:
    # Container name used for the Prometheus workload. Defaults to `inventory_hostname`.
    prometheus_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/rm
```

### k8s/rm

Remove Prometheus Kubernetes resources

Deletes the Prometheus StatefulSet and both Services from Kubernetes.

```yaml
- name: Remove Prometheus Kubernetes resources
  vars:
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/rm
```

### data/rm

Remove Prometheus data

Deletes Prometheus data from the active deployment mode.

```yaml
- name: Remove Prometheus data
  vars:
    # Remote data directory consumed by `prometheus_remote_data_dir`.
    remote_data_dir: "string"
    # Remote directory where Prometheus TSDB data is stored. Defaults to `remote_data_dir`.
    prometheus_remote_data_dir: "{{ remote_data_dir }}"
    # Enables the container deployment path when set to `true`. The default is the inverse of `prometheus_use_k8s`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: data/rm
```

### k8s/data/rm

Remove the Prometheus data PVC

Deletes the PersistentVolumeClaim created for the Prometheus StatefulSet.

```yaml
- name: Remove the Prometheus data PVC
  vars:
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/data/rm
```

### wipe

Remove all Prometheus data and configuration

Tears down Prometheus and removes its data, TLS material, and generated configuration files.

```yaml
- name: Remove all Prometheus data and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: wipe
```

### crypto/setup

Generate Prometheus TLS materials

Generates TLS assets for Prometheus and applies the Kubernetes Secret when Kubernetes mode is enabled.

```yaml
- name: Generate Prometheus TLS materials
  vars:
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/setup
```

### crypto/openssl/generate_cert

Generate a self-signed TLS certificate for Prometheus

Delegates certificate creation to the shared OpenSSL role using Prometheus-specific output paths.

```yaml
- name: Generate a self-signed TLS certificate for Prometheus
  vars:
    # Optional certificate organization data forwarded to OpenSSL.
    organization: {}
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Filename used for the Prometheus TLS private key.
    prometheus_tls_private_key_file: server.key
    # Filename used for the Prometheus TLS certificate.
    prometheus_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/openssl/generate_cert
```

### k8s/crypto/transfer

Apply the Prometheus TLS Secret on Kubernetes

Creates or updates the Kubernetes Secret that stores the Prometheus TLS server keypair.

```yaml
- name: Apply the Prometheus TLS Secret on Kubernetes
  vars:
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Filename used for the Prometheus TLS private key.
    prometheus_tls_private_key_file: server.key
    # Filename used for the Prometheus TLS certificate.
    prometheus_tls_cert_file: server.crt
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/crypto/transfer
```

### crypto/fetch

Fetch Prometheus TLS certificates

Fetches the generated Prometheus TLS CA certificate and server certificate to the control node.

```yaml
- name: Fetch Prometheus TLS certificates
  vars:
    # Control-node directory where fetched Prometheus artifacts are written.
    fetched_artifacts_dir: "string"
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/fetch
```

### crypto/rm

Remove Prometheus TLS materials

Deletes the Prometheus TLS directory and removes the Kubernetes Secret when Kubernetes mode is enabled.

```yaml
- name: Remove Prometheus TLS materials
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/rm
```

### k8s/crypto/rm

Remove the Prometheus TLS Secret

Deletes the Kubernetes Secret that stores the Prometheus TLS server keypair.

```yaml
- name: Remove the Prometheus TLS Secret
  vars:
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/crypto/rm
```

### config/transfer

Transfer Prometheus configuration files

Generates Prometheus configuration files on the remote host and optionally applies the Kubernetes ConfigMap.

```yaml
- name: Transfer Prometheus configuration files
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Filename of the main Prometheus scrape configuration.
    prometheus_config_file: prometheus.yaml
    # Filename of the Prometheus web TLS configuration file.
    prometheus_web_config_file: web-config.yaml
    # Filename of the promtool HTTP client configuration used for TLS health checks.
    prometheus_http_config_file: http-config.yaml
    # Global Prometheus scrape interval. Example: `2s`.
    prometheus_scrape_interval: 2s
    # In-container or in-pod mount point for Prometheus configuration files.
    prometheus_container_config_dir: /etc/prometheus/config
    # Filename used for the Prometheus TLS private key.
    prometheus_tls_private_key_file: server.key
    # Filename used for the Prometheus TLS certificate.
    prometheus_tls_cert_file: server.crt
    # Optional scrape job definitions rendered into `prometheus.yaml` and the Kubernetes ConfigMap.
    prometheus_scrape_services: [{}]
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: config/transfer
```

### k8s/config/transfer

Apply the Prometheus ConfigMap on Kubernetes

Creates or updates the ConfigMap that carries the Prometheus configuration and optional TLS CA files.

```yaml
- name: Apply the Prometheus ConfigMap on Kubernetes
  vars:
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Filename of the main Prometheus scrape configuration.
    prometheus_config_file: prometheus.yaml
    # Filename of the Prometheus web TLS configuration file.
    prometheus_web_config_file: web-config.yaml
    # Filename of the promtool HTTP client configuration used for TLS health checks.
    prometheus_http_config_file: http-config.yaml
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
    # Optional scrape job definitions rendered into `prometheus.yaml` and the Kubernetes ConfigMap.
    prometheus_scrape_services: [{}]
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/config/transfer
```

### config/rm

Remove Prometheus configuration files

Deletes the remote Prometheus configuration directory and optionally removes the Kubernetes ConfigMap.

```yaml
- name: Remove Prometheus configuration files
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`.
    remote_config_dir: "string"
    # Remote directory where Prometheus configuration files are written. Defaults to `remote_config_dir`.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: config/rm
```

### k8s/config/rm

Remove the Prometheus ConfigMap

Deletes the Kubernetes ConfigMap that stores Prometheus configuration.

```yaml
- name: Remove the Prometheus ConfigMap
  vars:
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/config/rm
```

### fetch_logs

Fetch Prometheus logs from the active deployment mode

Collects Prometheus logs from either the container deployment or the Kubernetes pod.

```yaml
- name: Fetch Prometheus logs from the active deployment mode
  vars:
    # Enables the container deployment path when set to `true`. The default is the inverse of `prometheus_use_k8s`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: fetch_logs
```

### container/fetch_logs

Fetch Prometheus container logs

Collects logs for the Prometheus container through the shared container role.

```yaml
- name: Fetch Prometheus container logs
  vars:
    # Container name used for the Prometheus workload. Defaults to `inventory_hostname`.
    prometheus_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/fetch_logs
```

### k8s/fetch_logs

Fetch Prometheus pod logs

Collects logs for the Prometheus pod through the shared Kubernetes role.

```yaml
- name: Fetch Prometheus pod logs
  vars:
    # Kubernetes namespace used for Prometheus resources.
    k8s_namespace: "string"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services. Defaults to `inventory_hostname`.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/fetch_logs
```
