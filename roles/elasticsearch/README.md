
# hyperledger.fabricx.elasticsearch

> Runs an ElasticSearch container for log storage.


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
  - [config/rm](#task-config-rm)
  - [data/rm](#task-data-rm)
  - [crypto/setup](#task-crypto-setup)
  - [crypto/fetch](#task-crypto-fetch)
  - [crypto/rm](#task-crypto-rm)
  - [crypto/openssl/generate_cert](#task-crypto-openssl-generate_cert)
  - [k8s/start](#task-k8s-start)
  - [k8s/ping](#task-k8s-ping)
  - [k8s/rm](#task-k8s-rm)
  - [k8s/fetch_logs](#task-k8s-fetch_logs)
  - [k8s/crypto/rm](#task-k8s-crypto-rm)
  - [k8s/crypto/transfer](#task-k8s-crypto-transfer)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-start"></a>

### start

Start ElasticSearch


Starts ElasticSearch using the selected deployment mode.

Container mode is the default unless `elasticsearch_use_k8s` is enabled.


```yaml
- name: Start ElasticSearch
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`. The default derives from `elasticsearch_use_k8s`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: start
```

<a id="task-stop"></a>

### stop

Stop the ElasticSearch container


Stops the ElasticSearch container instance.

Uses the container helper role internally.


```yaml
- name: Stop the ElasticSearch container
  vars:
    # Container name for the ElasticSearch instance. The default derives from `inventory_hostname`.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: stop
```

<a id="task-teardown"></a>

### teardown

Remove ElasticSearch runtime resources and data


Removes ElasticSearch runtime resources for the selected deployment mode.

Also removes the container data directory or Kubernetes PVC through the `data/rm` entry point.


```yaml
- name: Remove ElasticSearch runtime resources and data
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`. The default derives from `elasticsearch_use_k8s`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: teardown
```

<a id="task-wipe"></a>

### wipe

Wipe ElasticSearch data and configuration


Removes ElasticSearch runtime resources, TLS materials, and configuration files.

This entry point sequences the teardown, crypto cleanup, and config cleanup flows.


```yaml
- name: Wipe ElasticSearch data and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: wipe
```

<a id="task-fetch_logs"></a>

### fetch_logs

Fetch ElasticSearch logs


Collects ElasticSearch logs from the selected deployment mode.

Delegates to the container or Kubernetes log collection entry point.


```yaml
- name: Fetch ElasticSearch logs
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`. The default derives from `elasticsearch_use_k8s`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: fetch_logs
```

<a id="task-ping"></a>

### ping

Check ElasticSearch reachability


Probes the ElasticSearch ports in container mode.

Delegates to `k8s/ping` when ElasticSearch runs on Kubernetes.


```yaml
- name: Check ElasticSearch reachability
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # ElasticSearch HTTP port used by the container, Kubernetes Service, and readiness checks. Example: `9200`.
    elasticsearch_http_port: 1000
    # ElasticSearch transport port used by the container and Kubernetes Service. Example: `9300`.
    elasticsearch_transport_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: ping
```

<a id="task-container-start"></a>

### container/start

Start ElasticSearch in a container


Creates the required data volume and starts the ElasticSearch container.

Configures TLS volume mounts and environment variables when TLS is enabled.


```yaml
- name: Start ElasticSearch in a container
  vars:
    # Container name for the ElasticSearch instance. The default derives from `inventory_hostname`.
    elasticsearch_container_name: "{{ inventory_hostname }}"
    # Container registry endpoint used to build `elasticsearch_image`. The default derives from `ELASTICSEARCH_REGISTRY_ENDPOINT` and falls back to `docker.io/library`.
    elasticsearch_registry_endpoint: "{{ lookup('env', 'ELASTICSEARCH_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # ElasticSearch image repository name.
    elasticsearch_image_name: elasticsearch
    # ElasticSearch image tag.
    elasticsearch_image_tag: 8.19.6
    # Full container image reference for ElasticSearch. The default derives from `elasticsearch_registry_endpoint`, `elasticsearch_image_name`, and `elasticsearch_image_tag`.
    elasticsearch_image: "{{ elasticsearch_registry_endpoint }}/{{ elasticsearch_image_name }}:{{ elasticsearch_image_tag }}"
    # Remote directory used for ElasticSearch configuration and TLS files. The default derives from `remote_config_dir`.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Required when relying on the default of that option.
    remote_config_dir: "string"
    # Remote directory used for ElasticSearch persistent data. The default derives from `remote_data_dir`.
    elasticsearch_remote_data_dir: "{{ remote_data_dir }}"
    # Shared remote data directory consumed by `elasticsearch_remote_data_dir`. Required when relying on the default of that option.
    remote_data_dir: "string"
    # Base configuration directory path inside the ElasticSearch container.
    elasticsearch_container_config_dir: /usr/share/elasticsearch
    # Data directory path inside the ElasticSearch container.
    elasticsearch_container_data_dir: /usr/share/elasticsearch/data
    # ElasticSearch HTTP port used by the container, Kubernetes Service, and readiness checks. Example: `9200`.
    elasticsearch_http_port: 1000
    # ElasticSearch transport port used by the container and Kubernetes Service. Example: `9300`.
    elasticsearch_transport_port: 1000
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

<a id="task-container-stop"></a>

### container/stop

Stop the ElasticSearch container


Stops the ElasticSearch container instance.

Uses the container helper role internally.


```yaml
- name: Stop the ElasticSearch container
  vars:
    # Container name for the ElasticSearch instance. The default derives from `inventory_hostname`.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: container/stop
```

<a id="task-container-rm"></a>

### container/rm

Remove the ElasticSearch container


Removes the ElasticSearch container instance.

Container volumes are handled separately by the `data/rm` entry point.


```yaml
- name: Remove the ElasticSearch container
  vars:
    # Container name for the ElasticSearch instance. The default derives from `inventory_hostname`.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: container/rm
```

<a id="task-container-fetch_logs"></a>

### container/fetch_logs

Fetch ElasticSearch container logs


Collects logs from the ElasticSearch container instance.

Uses the container helper role internally.


```yaml
- name: Fetch ElasticSearch container logs
  vars:
    # Container name for the ElasticSearch instance. The default derives from `inventory_hostname`.
    elasticsearch_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: container/fetch_logs
```

<a id="task-config-rm"></a>

### config/rm

Remove the ElasticSearch configuration directory


Deletes the remote ElasticSearch configuration directory from the target host.

This also removes TLS materials stored under that directory.


```yaml
- name: Remove the ElasticSearch configuration directory
  vars:
    # Remote directory used for ElasticSearch configuration and TLS files. The default derives from `remote_config_dir`.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Required when relying on the default of that option.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: config/rm
```

<a id="task-data-rm"></a>

### data/rm

Remove ElasticSearch data storage


Removes the ElasticSearch persistent data directory in container deployments.

Deletes the ElasticSearch PVC in Kubernetes deployments.


```yaml
- name: Remove ElasticSearch data storage
  vars:
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
    # Runs ElasticSearch as a container when set to `true`. The default derives from `elasticsearch_use_k8s`.
    elasticsearch_use_container: "{{ not elasticsearch_use_k8s }}"
    # Remote directory used for ElasticSearch persistent data. The default derives from `remote_data_dir`.
    elasticsearch_remote_data_dir: "{{ remote_data_dir }}"
    # Shared remote data directory consumed by `elasticsearch_remote_data_dir`. Required when relying on the default of that option.
    remote_data_dir: "string"
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret. The default derives from `inventory_hostname`.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: data/rm
```

<a id="task-crypto-setup"></a>

### crypto/setup

Prepare ElasticSearch TLS materials


Generates TLS materials when TLS is enabled.

Uploads the generated materials to Kubernetes when Kubernetes mode is enabled.


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

<a id="task-crypto-fetch"></a>

### crypto/fetch

Fetch ElasticSearch TLS certificates


Fetches the ElasticSearch CA certificate and server certificate from the remote host.

This entry point only performs work when TLS is enabled.


```yaml
- name: Fetch ElasticSearch TLS certificates
  vars:
    # Enables TLS material handling and HTTPS configuration for ElasticSearch.
    elasticsearch_use_tls: false
    # Remote directory used for ElasticSearch configuration and TLS files. The default derives from `remote_config_dir`.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Required when relying on the default of that option.
    remote_config_dir: "string"
    # Control-node directory where fetched ElasticSearch artifacts are written. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/fetch
```

<a id="task-crypto-rm"></a>

### crypto/rm

Remove ElasticSearch TLS materials


Deletes local ElasticSearch TLS files from the remote host.

Removes the Kubernetes Secret when Kubernetes mode is enabled.


```yaml
- name: Remove ElasticSearch TLS materials
  vars:
    # Remote directory used for ElasticSearch configuration and TLS files. The default derives from `remote_config_dir`.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Required when relying on the default of that option.
    remote_config_dir: "string"
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Runs ElasticSearch on Kubernetes when set to `true`.
    elasticsearch_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/rm
```

<a id="task-crypto-openssl-generate_cert"></a>

### crypto/openssl/generate_cert

Generate ElasticSearch TLS materials with OpenSSL


Generates a self-signed TLS certificate and private key for ElasticSearch on the target host.

Writes the generated files under the ElasticSearch remote configuration directory.


```yaml
- name: Generate ElasticSearch TLS materials with OpenSSL
  vars:
    # Remote directory used for ElasticSearch configuration and TLS files. The default derives from `remote_config_dir`.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Required when relying on the default of that option.
    remote_config_dir: "string"
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Filename of the ElasticSearch TLS certificate under the TLS directory.
    elasticsearch_tls_cert_file: server.crt
    # Optionally provides organization metadata used to derive the TLS certificate organization name.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: crypto/openssl/generate_cert
```

<a id="task-k8s-start"></a>

### k8s/start

Start ElasticSearch on Kubernetes


Ensures the Kubernetes namespace exists and applies the ElasticSearch Services and StatefulSet.

Uses the role templates to configure storage, TLS mounts, and the optional NodePort Service.


```yaml
- name: Start ElasticSearch on Kubernetes
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret. The default derives from `inventory_hostname`.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "string"
    # Timeout in seconds while waiting for the ElasticSearch StatefulSet rollout to complete.
    elasticsearch_k8s_wait_timeout: 120
    # Kubernetes pod `fsGroup` applied so mounted TLS files are readable by the ElasticSearch process.
    elasticsearch_k8s_fs_group: 1000
    # Enables the optional Kubernetes NodePort Service for ElasticSearch when set to `true`. When `false`, no NodePort Service is created and the `k8s/ping` check is skipped.
    elasticsearch_k8s_use_node_port: false
    # Optional NodePort value used by the external ElasticSearch HTTP Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically.
    elasticsearch_k8s_http_node_port: 1000
    # Optional NodePort value used by the external ElasticSearch transport Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically.
    elasticsearch_k8s_transport_node_port: 1000
    # ElasticSearch HTTP port used by the container, Kubernetes Service, and readiness checks. Example: `9200`.
    elasticsearch_http_port: 1000
    # ElasticSearch transport port used by the container and Kubernetes Service. Example: `9300`.
    elasticsearch_transport_port: 1000
    # Container registry endpoint used to build `elasticsearch_image`. The default derives from `ELASTICSEARCH_REGISTRY_ENDPOINT` and falls back to `docker.io/library`.
    elasticsearch_registry_endpoint: "{{ lookup('env', 'ELASTICSEARCH_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # ElasticSearch image repository name.
    elasticsearch_image_name: elasticsearch
    # ElasticSearch image tag.
    elasticsearch_image_tag: 8.19.6
    # Full container image reference for ElasticSearch. The default derives from `elasticsearch_registry_endpoint`, `elasticsearch_image_name`, and `elasticsearch_image_tag`.
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
    k8s_storage_size: "string"
    # Kubernetes storage class name for the ElasticSearch PVC when a non-default class is required.
    k8s_storage_class: "string"
    # Existing Kubernetes `imagePullSecret` name used for private registries.
    k8s_image_pull_secret: "string"
    # Optionally overrides the readiness probe initial delay in seconds.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Optionally overrides the readiness probe interval in seconds.
    k8s_readiness_probe_period_seconds: 1000
    # Optionally overrides the readiness probe timeout in seconds.
    k8s_readiness_probe_timeout_seconds: 1000
    # Optionally overrides the readiness probe failure threshold.
    k8s_readiness_probe_failure_threshold: 1000
    # Optionally overrides the liveness probe initial delay in seconds.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Optionally overrides the liveness probe interval in seconds.
    k8s_liveness_probe_period_seconds: 1000
    # Optionally overrides the liveness probe timeout in seconds.
    k8s_liveness_probe_timeout_seconds: 1000
    # Optionally overrides the liveness probe failure threshold.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/start
```

<a id="task-k8s-ping"></a>

### k8s/ping

Check ElasticSearch NodePort reachability on Kubernetes


Probes the ElasticSearch HTTP and transport NodePorts when `elasticsearch_k8s_use_node_port` is `true`.

Each port is only checked when its matching NodePort value is defined.


```yaml
- name: Check ElasticSearch NodePort reachability on Kubernetes
  vars:
    # Enables the optional Kubernetes NodePort Service for ElasticSearch when set to `true`. When `false`, no NodePort Service is created and the `k8s/ping` check is skipped.
    elasticsearch_k8s_use_node_port: false
    # Optional NodePort value used by the external ElasticSearch HTTP Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically.
    elasticsearch_k8s_http_node_port: 1000
    # Optional NodePort value used by the external ElasticSearch transport Service. Only relevant when `elasticsearch_k8s_use_node_port` is `true`. When undefined, Kubernetes allocates the NodePort automatically.
    elasticsearch_k8s_transport_node_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/ping
```

<a id="task-k8s-rm"></a>

### k8s/rm

Remove ElasticSearch Kubernetes resources


Deletes the ElasticSearch StatefulSet and Services from Kubernetes.

The persistent volume claim is removed separately by the `data/rm` entry point.


```yaml
- name: Remove ElasticSearch Kubernetes resources
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret. The default derives from `inventory_hostname`.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/rm
```

<a id="task-k8s-fetch_logs"></a>

### k8s/fetch_logs

Fetch ElasticSearch pod logs


Collects logs from the ElasticSearch pod in Kubernetes.

Selects pods using the ElasticSearch application label.


```yaml
- name: Fetch ElasticSearch pod logs
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret. The default derives from `inventory_hostname`.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/fetch_logs
```

<a id="task-k8s-crypto-rm"></a>

### k8s/crypto/rm

Remove the ElasticSearch Kubernetes TLS Secret


Deletes the Kubernetes Secret that stores ElasticSearch TLS materials.

This entry point is typically invoked from the ElasticSearch crypto cleanup workflow.


```yaml
- name: Remove the ElasticSearch Kubernetes TLS Secret
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret. The default derives from `inventory_hostname`.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/crypto/rm
```

<a id="task-k8s-crypto-transfer"></a>

### k8s/crypto/transfer

Apply the ElasticSearch Kubernetes TLS Secret


Applies the Kubernetes Secret that stores ElasticSearch TLS materials.

Ensures the Kubernetes namespace exists before applying the Secret.


```yaml
- name: Apply the ElasticSearch Kubernetes TLS Secret
  vars:
    # Base Kubernetes resource name used for ElasticSearch objects, including the StatefulSet, Services, and Secret. The default derives from `inventory_hostname`.
    elasticsearch_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for ElasticSearch resources. Set `required` explicitly at each entry point depending on whether Kubernetes mode is optional or mandatory there.
    k8s_namespace: "string"
    # Enables TLS material handling and HTTPS configuration for ElasticSearch.
    elasticsearch_use_tls: false
    # Remote directory used for ElasticSearch configuration and TLS files. The default derives from `remote_config_dir`.
    elasticsearch_remote_config_dir: "{{ remote_config_dir }}"
    # Shared remote configuration directory consumed by `elasticsearch_remote_config_dir`. Required when relying on the default of that option.
    remote_config_dir: "string"
    # Filename of the ElasticSearch TLS private key under the TLS directory.
    elasticsearch_tls_private_key_file: server.key
    # Filename of the ElasticSearch TLS certificate under the TLS directory.
    elasticsearch_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: k8s/crypto/transfer
```


