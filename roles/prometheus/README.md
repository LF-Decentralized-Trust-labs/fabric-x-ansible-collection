# hyperledger.fabricx.prometheus

> Deploys and manages Prometheus metrics collectors in container or Kubernetes mode.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
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
  - [crypto/openssl/generate\_cert](#cryptoopensslgenerate_cert)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [k8s/crypto/rm](#k8scryptorm)
  - [config/transfer](#configtransfer)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [config/rm](#configrm)
  - [k8s/config/rm](#k8sconfigrm)
  - [fetch\_logs](#fetch_logs)
  - [container/fetch\_logs](#containerfetch_logs)
  - [k8s/fetch\_logs](#k8sfetch_logs)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.prometheus
```

## Tasks

### ping

> Check that the Prometheus listener is reachable

Validates network reachability to the active Prometheus listener on the target host, or to the Kubernetes NodePort when that exposure path is enabled.

```yaml
- name: Check that the Prometheus listener is reachable
  vars:
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services.
    prometheus_port: 9090
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: ping
```

### start

> Start Prometheus in the selected deployment mode

Starts Prometheus as either a container or Kubernetes workload based on the deployment mode flags. Renders configuration, prepares storage, and applies Kubernetes resources needed for the selected mode. When Kubernetes mode is enabled, it can also expose Prometheus through the optional NodePort Service.

```yaml
- name: Start Prometheus in the selected deployment mode
  vars:
    # Enables the container deployment path when set to `true`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: start
```

### container/start

> Start the Prometheus container

Renders the remote configuration, creates the data directory, and starts Prometheus through the shared container role.

```yaml
- name: Start the Prometheus container
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote data directory consumed by `prometheus_remote_data_dir`. Example: `/var/lib/prometheus/data`.
    remote_data_dir: "/var/lib/prometheus/data"
    # Container registry endpoint for Prometheus images.
    prometheus_registry_endpoint: "{{ lookup('env', 'PROMETHEUS_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Image name used when composing `prometheus_image`.
    prometheus_image_name: prometheus
    # Image tag used when composing `prometheus_image`.
    prometheus_image_tag: latest
    # Fully qualified Prometheus container image.
    prometheus_image: "{{ prometheus_registry_endpoint }}/{{ prometheus_image_name }}:{{ prometheus_image_tag }}"
    # Container name used for the Prometheus workload.
    prometheus_container_name: "{{ inventory_hostname }}"
    # Remote directory where Prometheus configuration files are written.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Remote directory where Prometheus TSDB data is stored.
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
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services.
    prometheus_port: 9090
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/start
```

### k8s/start

> Start Prometheus on Kubernetes

Ensures the namespace exists, renders and transfers Prometheus configuration, and creates the headless Service, optional NodePort and LoadBalancer Services, and StatefulSet resources.

```yaml
- name: Start Prometheus on Kubernetes
  vars:
    # Container registry endpoint for Prometheus images.
    prometheus_registry_endpoint: "{{ lookup('env', 'PROMETHEUS_REGISTRY_ENDPOINT') or 'docker.io/prom' }}"
    # Image name used when composing `prometheus_image`.
    prometheus_image_name: prometheus
    # Image tag used when composing `prometheus_image`.
    prometheus_image_tag: latest
    # Fully qualified Prometheus container image.
    prometheus_image: "{{ prometheus_registry_endpoint }}/{{ prometheus_image_name }}:{{ prometheus_image_tag }}"
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services.
    prometheus_port: 9090
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes NodePort value used by the external HTTP Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30990`.
    prometheus_k8s_node_port: 30990
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
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Persistent volume size requested for Prometheus data. Example: `20Gi`.
    k8s_storage_size: "20Gi"
    # Optional image pull secret name for private registries. Example: `prometheus-registry-creds`.
    k8s_image_pull_secret: "prometheus-registry-creds"
    # Optional Kubernetes storage class name for the Prometheus PVC. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Initial delay before the readiness probe starts. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Interval between readiness probe attempts. Example: `5`.
    k8s_readiness_probe_period_seconds: 5
    # Timeout for each readiness probe request. Example: `3`.
    k8s_readiness_probe_timeout_seconds: 3
    # Number of failed readiness probes before the pod is marked unready. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Initial delay before the liveness probe starts. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Interval between liveness probe attempts. Example: `10`.
    k8s_liveness_probe_period_seconds: 10
    # Timeout for each liveness probe request. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Number of failed liveness probes before Kubernetes restarts the pod. Example: `5`.
    k8s_liveness_probe_failure_threshold: 5
    # Set to `true` to create a LoadBalancer Service entry that exposes the HTTP port externally. When undefined or `false`, the HTTP port is not included in the LoadBalancer Service.
    prometheus_k8s_loadbalancer_expose_http_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/start
```

### k8s/ping

> Check that the Prometheus NodePort is reachable

Probes configured Kubernetes NodePort values and LoadBalancer-exposed service ports for external reachability.

```yaml
- name: Check that the Prometheus NodePort is reachable
  vars:
    # TCP port exposed by Prometheus and used by the container listener and Kubernetes Services.
    prometheus_port: 9090
    # Kubernetes NodePort value used by the external HTTP Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30990`.
    prometheus_k8s_node_port: 30990
    # Set to `true` to create a LoadBalancer Service entry that exposes the HTTP port externally. When undefined or `false`, the HTTP port is not included in the LoadBalancer Service.
    prometheus_k8s_loadbalancer_expose_http_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/ping
```

### stop

> Stop the Prometheus container deployment

Stops Prometheus when the container deployment path is enabled.

```yaml
- name: Stop the Prometheus container deployment
  vars:
    # Enables the container deployment path when set to `true`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: stop
```

### container/stop

> Stop the Prometheus container

Stops the running Prometheus container through the shared container role.

```yaml
- name: Stop the Prometheus container
  vars:
    # Container name used for the Prometheus workload.
    prometheus_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/stop
```

### teardown

> Remove the Prometheus deployment

Removes the active Prometheus container or Kubernetes workload and then deletes its data.

```yaml
- name: Remove the Prometheus deployment
  vars:
    # Enables the container deployment path when set to `true`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: teardown
```

### container/rm

> Remove the Prometheus container

Removes the Prometheus container through the shared container role.

```yaml
- name: Remove the Prometheus container
  vars:
    # Container name used for the Prometheus workload.
    prometheus_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/rm
```

### k8s/rm

> Remove Prometheus Kubernetes resources

Deletes the Prometheus StatefulSet and both Services from Kubernetes.

```yaml
- name: Remove Prometheus Kubernetes resources
  vars:
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes NodePort value used by the external HTTP Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30990`.
    prometheus_k8s_node_port: 30990
    # Set to `true` to create a LoadBalancer Service entry that exposes the HTTP port externally. When undefined or `false`, the HTTP port is not included in the LoadBalancer Service.
    prometheus_k8s_loadbalancer_expose_http_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/rm
```

### data/rm

> Remove Prometheus data

Deletes Prometheus data from the active deployment mode.

```yaml
- name: Remove Prometheus data
  vars:
    # Remote data directory consumed by `prometheus_remote_data_dir`. Example: `/var/lib/prometheus/data`.
    remote_data_dir: "/var/lib/prometheus/data"
    # Remote directory where Prometheus TSDB data is stored.
    prometheus_remote_data_dir: "{{ remote_data_dir }}"
    # Enables the container deployment path when set to `true`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: data/rm
```

### k8s/data/rm

> Remove the Prometheus data PVC

Deletes the PersistentVolumeClaim created for the Prometheus StatefulSet.

```yaml
- name: Remove the Prometheus data PVC
  vars:
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/data/rm
```

### wipe

> Remove all Prometheus data and configuration

Tears down Prometheus and removes its data, TLS material, and generated configuration files.

```yaml
- name: Remove all Prometheus data and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: wipe
```

### crypto/setup

> Generate Prometheus TLS materials

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

> Generate a self-signed TLS certificate for Prometheus

Delegates certificate creation to the shared OpenSSL role using Prometheus-specific output paths.

```yaml
- name: Generate a self-signed TLS certificate for Prometheus
  vars:
    # Optional certificate organization data forwarded to OpenSSL. Example: `{'common_name': 'prometheus.observability.svc.cluster.local', 'organization_name': 'Hyperledger Fabric-X'}`.
    organization:
      common_name: "prometheus.observability.svc.cluster.local"
      organization_name: "Hyperledger Fabric-X"
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote directory where Prometheus configuration files are written.
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

> Apply the Prometheus TLS Secret on Kubernetes

Creates or updates the Kubernetes Secret that stores the Prometheus TLS server keypair.

```yaml
- name: Apply the Prometheus TLS Secret on Kubernetes
  vars:
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote directory where Prometheus configuration files are written.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Filename used for the Prometheus TLS private key.
    prometheus_tls_private_key_file: server.key
    # Filename used for the Prometheus TLS certificate.
    prometheus_tls_cert_file: server.crt
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/crypto/transfer
```

### crypto/fetch

> Fetch Prometheus TLS certificates

Fetches the generated Prometheus TLS certificate material to the control node.

```yaml
- name: Fetch Prometheus TLS certificates
  vars:
    # Control-node directory where fetched Prometheus artifacts are written. Example: `/tmp/prometheus-artifacts`.
    fetched_artifacts_dir: "/tmp/prometheus-artifacts"
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote directory where Prometheus configuration files are written.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove Prometheus TLS materials

Deletes the Prometheus TLS directory and removes the Kubernetes Secret when Kubernetes mode is enabled.

```yaml
- name: Remove Prometheus TLS materials
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote directory where Prometheus configuration files are written.
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

> Remove the Prometheus TLS Secret

Deletes the Kubernetes Secret that stores the Prometheus TLS server keypair.

```yaml
- name: Remove the Prometheus TLS Secret
  vars:
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/crypto/rm
```

### config/transfer

> Transfer Prometheus configuration files

Renders the main scrape configuration and supporting files on the remote host, including scrape target lists and TLS client settings. Applies the Kubernetes ConfigMap when Kubernetes mode is enabled.

```yaml
- name: Transfer Prometheus configuration files
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote directory where Prometheus configuration files are written.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Filename of the main Prometheus scrape configuration.
    prometheus_config_file: prometheus.yaml
    # Filename of the Prometheus web TLS configuration file.
    prometheus_web_config_file: web-config.yaml
    # Filename of the promtool HTTP client configuration used for TLS health checks.
    prometheus_http_config_file: http-config.yaml
    # Global Prometheus scrape interval.
    prometheus_scrape_interval: 2s
    # In-container or in-pod mount point for Prometheus configuration files.
    prometheus_container_config_dir: /etc/prometheus/config
    # Filename used for the Prometheus TLS private key.
    prometheus_tls_private_key_file: server.key
    # Filename used for the Prometheus TLS certificate.
    prometheus_tls_cert_file: server.crt
    # Optional scrape job definitions rendered into `prometheus.yaml` and the Kubernetes ConfigMap. Example: `[{ job_name: fabric-orderer, static_configs: [{ targets: [orderer1.example.com:9443, orderer2.example.com:9443] }] }, { job_name: node_exporter, static_configs: [{ targets: [worker1.example.com:9100] }] }]`.
    prometheus_scrape_services:[{ job_name: fabric-orderer, static_configs: [{ targets: [orderer1.example.com:9443, orderer2.example.com:9443] }] }, { job_name: node_exporter, static_configs: [{ targets: [worker1.example.com:9100] }] }]
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: config/transfer
```

### k8s/config/transfer

> Apply the Prometheus ConfigMap on Kubernetes

Creates or updates the ConfigMap that carries the rendered Prometheus configuration and optional TLS CA files.

```yaml
- name: Apply the Prometheus ConfigMap on Kubernetes
  vars:
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote directory where Prometheus configuration files are written.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Filename of the main Prometheus scrape configuration.
    prometheus_config_file: prometheus.yaml
    # Filename of the Prometheus web TLS configuration file.
    prometheus_web_config_file: web-config.yaml
    # Filename of the promtool HTTP client configuration used for TLS health checks.
    prometheus_http_config_file: http-config.yaml
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
    # Optional scrape job definitions rendered into `prometheus.yaml` and the Kubernetes ConfigMap. Example: `[{ job_name: fabric-orderer, static_configs: [{ targets: [orderer1.example.com:9443, orderer2.example.com:9443] }] }, { job_name: node_exporter, static_configs: [{ targets: [worker1.example.com:9100] }] }]`.
    prometheus_scrape_services:[{ job_name: fabric-orderer, static_configs: [{ targets: [orderer1.example.com:9443, orderer2.example.com:9443] }] }, { job_name: node_exporter, static_configs: [{ targets: [worker1.example.com:9100] }] }]
    # Enables HTTPS and TLS-aware health checks when set to `true`.
    prometheus_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/config/transfer
```

### config/rm

> Remove Prometheus configuration files

Deletes the remote Prometheus configuration directory and optionally removes the Kubernetes ConfigMap.

```yaml
- name: Remove Prometheus configuration files
  vars:
    # Remote configuration directory consumed by `prometheus_remote_config_dir`. Example: `/var/lib/prometheus/config`.
    remote_config_dir: "/var/lib/prometheus/config"
    # Remote directory where Prometheus configuration files are written.
    prometheus_remote_config_dir: "{{ remote_config_dir }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: config/rm
```

### k8s/config/rm

> Remove the Prometheus ConfigMap

Deletes the Kubernetes ConfigMap that stores Prometheus configuration.

```yaml
- name: Remove the Prometheus ConfigMap
  vars:
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/config/rm
```

### fetch_logs

> Fetch Prometheus logs from the active deployment mode

Collects Prometheus logs from either the container deployment or the Kubernetes pod.

```yaml
- name: Fetch Prometheus logs from the active deployment mode
  vars:
    # Enables the container deployment path when set to `true`.
    prometheus_use_container: "{{ not prometheus_use_k8s }}"
    # Enables the Kubernetes deployment path when set to `true`.
    prometheus_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: fetch_logs
```

### container/fetch_logs

> Fetch Prometheus container logs

Collects logs for the Prometheus container through the shared container role.

```yaml
- name: Fetch Prometheus container logs
  vars:
    # Container name used for the Prometheus workload.
    prometheus_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: container/fetch_logs
```

### k8s/fetch_logs

> Fetch Prometheus pod logs

Collects logs for the Prometheus pod through the shared Kubernetes role.

```yaml
- name: Fetch Prometheus pod logs
  vars:
    # Kubernetes namespace used for Prometheus resources. Example: `observability`.
    k8s_namespace: "observability"
    # Base Kubernetes resource name used for the Prometheus StatefulSet and Services.
    prometheus_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: k8s/fetch_logs
```
