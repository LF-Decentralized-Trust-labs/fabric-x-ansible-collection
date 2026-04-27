# hyperledger.fabricx.elasticsearch

> Deploys and manages ElasticSearch in container or Kubernetes mode for Fabric-X log storage.

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
  - [config/rm](#configrm)
  - [data/rm](#datarm)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate\_cert](#cryptoopensslgenerate_cert)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [k8s/crypto/rm](#k8scryptorm)
  - [k8s/crypto/transfer](#k8scryptotransfer)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.elasticsearch
```

## Tasks

### start

> Start ElasticSearch

Starts ElasticSearch using the selected deployment mode. Container mode is the default unless `elasticsearch_use_k8s` is enabled, in which case the Kubernetes StatefulSet, Services, and optional TLS Secret are managed instead.

```yaml
- name: Start ElasticSearch
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: start
```

### stop

> Stop the ElasticSearch container

Stops the ElasticSearch container instance without removing its data volume or configuration files. Uses the container helper role internally and only applies in container mode.

```yaml
- name: Stop the ElasticSearch container
  vars:
    # Container name for the ElasticSearch instance.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: stop
```

### teardown

> Remove ElasticSearch runtime resources and data

Removes ElasticSearch runtime resources for the selected deployment mode. Also removes the container data directory or Kubernetes PVC through the `data/rm` entry point, leaving TLS and config cleanup to `wipe`.

```yaml
- name: Remove ElasticSearch runtime resources and data
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: teardown
```

### wipe

> Wipe ElasticSearch data and configuration

Removes ElasticSearch runtime resources, TLS materials, and configuration files. This entry point sequences the teardown, crypto cleanup, and config cleanup flows to clear the instance state.

```yaml
- name: Wipe ElasticSearch data and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: wipe
```

### fetch_logs

> Fetch ElasticSearch logs

Collects ElasticSearch logs from the selected deployment mode. Delegates to the container or Kubernetes log collection entry point and writes the results to the control node fetch directory.

```yaml
- name: Fetch ElasticSearch logs
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: fetch_logs
```

### ping

> Check ElasticSearch reachability

Probes the ElasticSearch HTTP and transport ports in container mode. Delegates to `k8s/ping` when ElasticSearch runs on Kubernetes and checks the optional NodePort Service instead.

```yaml
- name: Check ElasticSearch reachability
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # ElasticSearch HTTP port used by the container, Kubernetes Service, and readiness checks. Example: `9200`.
    elasticsearch_http_port: 9200
    # ElasticSearch transport port used by the container and Kubernetes Service. Example: `9300`.
    elasticsearch_transport_port: 9300
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: ping
```

### container/start

> Start ElasticSearch in a container

Creates the required data volume, prepares the configuration path, and starts the ElasticSearch container. Configures TLS volume mounts, environment variables, and the selected HTTP and transport ports when TLS is enabled.

```yaml
- name: Start ElasticSearch in a container
  vars:
    # Container name for the ElasticSearch instance.
    elasticsearch_container_name: "{{ inventory_hostname }}"
    # Container registry endpoint used to build `elasticsearch_image`.
    elasticsearch_registry_endpoint: "{{ lookup('env', 'ELASTICSEARCH_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # ElasticSearch image repository name.
    elasticsearch_image_name: elasticsearch
    # ElasticSearch image tag.
    elasticsearch_image_tag: 8.19.6
    # Full container image reference for ElasticSearch.
    elasticsearch_image: "{{ elasticsearch_registry_endpoint }}/{{ elasticsearch_image_name }}:{{ elasticsearch_image_tag }}"
    # Remote directory used for ElasticSearch configuration and TLS files.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Example: `/opt/fabricx/elasticsearch/config`. Required when relying on the default of that option.
    remote_config_dir: "/opt/fabricx/elasticsearch/config"
    # Remote directory used for ElasticSearch persistent data.
    elasticsearch_remote_data_dir: "{{ remote_data_dir }}"
    # Shared remote data directory consumed by `elasticsearch_remote_data_dir`. Example: `/opt/fabricx/elasticsearch/data`. Required when relying on the default of that option.
    remote_data_dir: "/opt/fabricx/elasticsearch/data"
    # Base configuration directory path inside the ElasticSearch container.
    elasticsearch_container_config_dir: /usr/share/elasticsearch
    # Data directory path inside the ElasticSearch container.
    elasticsearch_container_data_dir: /usr/share/elasticsearch/data
    # ElasticSearch HTTP port used by the container, Kubernetes Service, and readiness checks. Example: `9200`.
    elasticsearch_http_port: 9200
    # ElasticSearch transport port used by the container and Kubernetes Service. Example: `9300`.
    elasticsearch_transport_port: 9300
    # Enables TLS material handling and HTTPS configuration for ElasticSearch.
    elasticsearch_use_tls: false
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Filename of the ElasticSearch TLS certificate under the TLS directory.
    elasticsearch_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: container/start
```

### container/stop

> Stop the ElasticSearch container

Stops the ElasticSearch container instance while preserving the container data directory. Uses the container helper role internally.

```yaml
- name: Stop the ElasticSearch container
  vars:
    # Container name for the ElasticSearch instance.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: container/stop
```

### container/rm

> Remove the ElasticSearch container

Removes the ElasticSearch container instance. Container volumes are handled separately by the `data/rm` entry point, so the persisted data path stays under role control.

```yaml
- name: Remove the ElasticSearch container
  vars:
    # Container name for the ElasticSearch instance.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch ElasticSearch container logs

Collects logs from the ElasticSearch container instance and stores them on the control node. Uses the container helper role internally.

```yaml
- name: Fetch ElasticSearch container logs
  vars:
    # Container name for the ElasticSearch instance.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: container/fetch_logs
```

### config/rm

> Remove the ElasticSearch configuration directory

Deletes the remote ElasticSearch configuration directory from the target host. This also removes TLS materials stored under that directory and clears the container or Kubernetes config path at the source.

```yaml
- name: Remove the ElasticSearch configuration directory
  vars:
    # Remote directory used for ElasticSearch configuration and TLS files.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Example: `/opt/fabricx/elasticsearch/config`. Required when relying on the default of that option.
    remote_config_dir: "/opt/fabricx/elasticsearch/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: config/rm
```

### data/rm

> Remove ElasticSearch data storage

Removes the ElasticSearch persistent data directory in container deployments. Deletes the ElasticSearch PVC in Kubernetes deployments so the data artifact is gone regardless of deployment mode.

```yaml
- name: Remove ElasticSearch data storage
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
    # Remote directory used for ElasticSearch persistent data.
    elasticsearch_remote_data_dir: "{{ remote_data_dir }}"
    # Shared remote data directory consumed by `elasticsearch_remote_data_dir`. Example: `/opt/fabricx/elasticsearch/data`. Required when relying on the default of that option.
    remote_data_dir: "/opt/fabricx/elasticsearch/data"
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Example: `fabricx-elasticsearch`. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "fabricx-elasticsearch"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: data/rm
```

### crypto/setup

> Prepare ElasticSearch TLS materials

Generates TLS materials when TLS is enabled. Uploads the generated materials to Kubernetes when Kubernetes mode is enabled so the Secret and mounted certs stay in sync.

```yaml
- name: Prepare ElasticSearch TLS materials
  vars:
    # Enables TLS material handling and HTTPS configuration for ElasticSearch.
    elasticsearch_use_tls: false
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/setup
```

### crypto/fetch

> Fetch ElasticSearch TLS certificates

Fetches the ElasticSearch CA certificate and server certificate from the remote host into the control-node artifact directory. This entry point only performs work when TLS is enabled.

```yaml
- name: Fetch ElasticSearch TLS certificates
  vars:
    # Enables TLS material handling and HTTPS configuration for ElasticSearch.
    elasticsearch_use_tls: false
    # Remote directory used for ElasticSearch configuration and TLS files.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Example: `/opt/fabricx/elasticsearch/config`. Required when relying on the default of that option.
    remote_config_dir: "/opt/fabricx/elasticsearch/config"
    # Control-node directory where fetched ElasticSearch artifacts such as TLS certificates and log bundles are written. Example: `/tmp/fabricx/elasticsearch-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/elasticsearch-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove ElasticSearch TLS materials

Deletes local ElasticSearch TLS files from the remote host. Removes the Kubernetes Secret when Kubernetes mode is enabled and TLS artifacts are no longer needed.

```yaml
- name: Remove ElasticSearch TLS materials
  vars:
    # Remote directory used for ElasticSearch configuration and TLS files.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Example: `/opt/fabricx/elasticsearch/config`. Required when relying on the default of that option.
    remote_config_dir: "/opt/fabricx/elasticsearch/config"
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/rm
```

### crypto/openssl/generate_cert

> Generate ElasticSearch TLS materials with OpenSSL

Generates a self-signed TLS certificate and private key for ElasticSearch on the target host. Writes the generated files under the ElasticSearch remote configuration directory for later container or Kubernetes use.

```yaml
- name: Generate ElasticSearch TLS materials with OpenSSL
  vars:
    # Remote directory used for ElasticSearch configuration and TLS files.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Example: `/opt/fabricx/elasticsearch/config`. Required when relying on the default of that option.
    remote_config_dir: "/opt/fabricx/elasticsearch/config"
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Filename of the ElasticSearch TLS certificate under the TLS directory.
    elasticsearch_tls_cert_file: server.crt
    # Optionally provides organization metadata used to derive the TLS certificate organization name. Example: `{'common_name': 'elasticsearch.fabricx.example'}`.
    organization:
      common_name: "elasticsearch.fabricx.example"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/openssl/generate_cert
```

### k8s/start

> Start ElasticSearch on Kubernetes

Ensures the Kubernetes namespace exists and applies the ElasticSearch headless Service, optional NodePort Service, StatefulSet, and PVC. Uses the role templates to configure storage, TLS mounts, the configured image, and rollout waiting behavior.

```yaml
- name: Start ElasticSearch on Kubernetes
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Example: `fabricx-elasticsearch`. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "fabricx-elasticsearch"
    # Timeout in seconds while waiting for the ElasticSearch StatefulSet rollout to complete.
    elasticsearch_k8s_wait_timeout: 120
    # Kubernetes pod `fsGroup` applied so mounted TLS files are readable by the ElasticSearch process.
    elasticsearch_k8s_fs_group: 1000
    # Enables the optional Kubernetes NodePort Service for ElasticSearch when set to `true`. When `false`, no NodePort Service is created and the `k8s/ping` check is skipped.
    elasticsearch_k8s_use_node_port: false
    # Optional NodePort value used by the external ElasticSearch HTTP Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically. Example: `30920`.
    elasticsearch_k8s_http_node_port: 30920
    # Optional NodePort value used by the external ElasticSearch transport Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically. Example: `30930`.
    elasticsearch_k8s_transport_node_port: 30930
    # ElasticSearch HTTP port used by the container, Kubernetes Service, and readiness checks. Example: `9200`.
    elasticsearch_http_port: 9200
    # ElasticSearch transport port used by the container and Kubernetes Service. Example: `9300`.
    elasticsearch_transport_port: 9300
    # Container registry endpoint used to build `elasticsearch_image`.
    elasticsearch_registry_endpoint: "{{ lookup('env', 'ELASTICSEARCH_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # ElasticSearch image repository name.
    elasticsearch_image_name: elasticsearch
    # ElasticSearch image tag.
    elasticsearch_image_tag: 8.19.6
    # Full container image reference for ElasticSearch.
    elasticsearch_image: "{{ elasticsearch_registry_endpoint }}/{{ elasticsearch_image_name }}:{{ elasticsearch_image_tag }}"
    # Base configuration directory path inside the ElasticSearch container.
    elasticsearch_container_config_dir: /usr/share/elasticsearch
    # Data directory path inside the ElasticSearch container.
    elasticsearch_container_data_dir: /usr/share/elasticsearch/data
    # Enables TLS material handling and HTTPS configuration for ElasticSearch.
    elasticsearch_use_tls: false
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Filename of the ElasticSearch TLS certificate under the TLS directory.
    elasticsearch_tls_cert_file: server.crt
    # Requested persistent storage size for the ElasticSearch PVC. Example: `20Gi`.
    k8s_storage_size: "20Gi"
    # Kubernetes storage class name for the ElasticSearch PVC when a non-default class is required. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Existing Kubernetes `imagePullSecret` name used for private registries. Example: `elasticsearch-regcred`.
    k8s_image_pull_secret: "elasticsearch-regcred"
    # Optionally overrides the readiness probe initial delay in seconds. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Optionally overrides the readiness probe interval in seconds. Example: `5`.
    k8s_readiness_probe_period_seconds: 5
    # Optionally overrides the readiness probe timeout in seconds. Example: `2`.
    k8s_readiness_probe_timeout_seconds: 2
    # Optionally overrides the readiness probe failure threshold. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Optionally overrides the liveness probe initial delay in seconds. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Optionally overrides the liveness probe interval in seconds. Example: `10`.
    k8s_liveness_probe_period_seconds: 10
    # Optionally overrides the liveness probe timeout in seconds. Example: `2`.
    k8s_liveness_probe_timeout_seconds: 2
    # Optionally overrides the liveness probe failure threshold. Example: `3`.
    k8s_liveness_probe_failure_threshold: 3
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/start
```

### k8s/ping

> Check ElasticSearch NodePort reachability on Kubernetes

Probes the ElasticSearch HTTP and transport NodePorts when `elasticsearch_k8s_use_node_port` is `true`. Each port is only checked when its matching NodePort value is defined, which lets the role verify only the exported service ports.

```yaml
- name: Check ElasticSearch NodePort reachability on Kubernetes
  vars:
    # Enables the optional Kubernetes NodePort Service for ElasticSearch when set to `true`. When `false`, no NodePort Service is created and the `k8s/ping` check is skipped.
    elasticsearch_k8s_use_node_port: false
    # Optional NodePort value used by the external ElasticSearch HTTP Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically. Example: `30920`.
    elasticsearch_k8s_http_node_port: 30920
    # Optional NodePort value used by the external ElasticSearch transport Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically. Example: `30930`.
    elasticsearch_k8s_transport_node_port: 30930
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/ping
```

### k8s/rm

> Remove ElasticSearch Kubernetes resources

Deletes the ElasticSearch StatefulSet and Services from Kubernetes. The persistent volume claim is removed separately by the `data/rm` entry point so data cleanup stays explicit.

```yaml
- name: Remove ElasticSearch Kubernetes resources
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Example: `fabricx-elasticsearch`. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "fabricx-elasticsearch"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch ElasticSearch pod logs

Collects logs from the ElasticSearch pod in Kubernetes and writes them to the control node artifact path. Selects pods using the ElasticSearch application label.

```yaml
- name: Fetch ElasticSearch pod logs
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Example: `fabricx-elasticsearch`. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "fabricx-elasticsearch"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/fetch_logs
```

### k8s/crypto/rm

> Remove the ElasticSearch Kubernetes TLS Secret

Deletes the Kubernetes Secret that stores ElasticSearch TLS materials. This entry point is typically invoked from the ElasticSearch crypto cleanup workflow after the remote certs are removed.

```yaml
- name: Remove the ElasticSearch Kubernetes TLS Secret
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Example: `fabricx-elasticsearch`. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "fabricx-elasticsearch"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/crypto/rm
```

### k8s/crypto/transfer

> Apply the ElasticSearch Kubernetes TLS Secret

Applies the Kubernetes Secret that stores ElasticSearch TLS materials. Ensures the Kubernetes namespace exists before applying the Secret and keeps the pod-mounted certificate paths aligned with the remote files.

```yaml
- name: Apply the ElasticSearch Kubernetes TLS Secret
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Example: `fabricx-elasticsearch`. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "fabricx-elasticsearch"
    # Enables TLS material handling and HTTPS configuration for ElasticSearch.
    elasticsearch_use_tls: false
    # Remote directory used for ElasticSearch configuration and TLS files.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Example: `/opt/fabricx/elasticsearch/config`. Required when relying on the default of that option.
    remote_config_dir: "/opt/fabricx/elasticsearch/config"
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Filename of the ElasticSearch TLS certificate under the TLS directory.
    elasticsearch_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/crypto/transfer
```
