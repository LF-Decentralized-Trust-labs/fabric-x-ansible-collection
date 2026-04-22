
# hyperledger.fabricx.jaeger

> Runs a Jaeger instance for distributed tracing.


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
  - [k8s/start](#task-k8s-start)
  - [k8s/rm](#task-k8s-rm)
  - [k8s/fetch_logs](#task-k8s-fetch_logs)
  - [k8s/ping](#task-k8s-ping)
  - [config/transfer](#task-config-transfer)
  - [config/rm](#task-config-rm)
  - [k8s/config/transfer](#task-k8s-config-transfer)
  - [k8s/config/rm](#task-k8s-config-rm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-start"></a>

### start

Select the Jaeger deployment mode to start


Dispatches Jaeger startup to the container or Kubernetes implementation.


```yaml
- name: Select the Jaeger deployment mode to start
  vars:
    # Runs the container-based Jaeger path when set to `true`. The default derives from `jaeger_use_k8s`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: start
```

<a id="task-stop"></a>

### stop

Select the Jaeger deployment mode to stop


Dispatches Jaeger shutdown to the container implementation.


```yaml
- name: Select the Jaeger deployment mode to stop
  vars:
    # Runs the container-based Jaeger path when set to `true`. The default derives from `jaeger_use_k8s`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: stop
```

<a id="task-teardown"></a>

### teardown

Select the Jaeger deployment mode to remove


Dispatches Jaeger removal to the container or Kubernetes implementation.


```yaml
- name: Select the Jaeger deployment mode to remove
  vars:
    # Runs the container-based Jaeger path when set to `true`. The default derives from `jaeger_use_k8s`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: teardown
```

<a id="task-wipe"></a>

### wipe

Remove the Jaeger deployment and configuration


Runs the teardown and configuration cleanup entry points for Jaeger.


```yaml
- name: Remove the Jaeger deployment and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: wipe
```

<a id="task-fetch_logs"></a>

### fetch_logs

Select the Jaeger deployment mode to collect logs from


Dispatches Jaeger log collection to the container or Kubernetes implementation.


```yaml
- name: Select the Jaeger deployment mode to collect logs from
  vars:
    # Runs the container-based Jaeger path when set to `true`. The default derives from `jaeger_use_k8s`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: fetch_logs
```

<a id="task-ping"></a>

### ping

Check that Jaeger service ports are reachable


Builds the Jaeger port list and delegates the connectivity check to the utils role.


```yaml
- name: Check that Jaeger service ports are reachable
  vars:
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
    # Sets the Jaeger query UI port.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port.
    jaeger_collector_port: 4317
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: ping
```

<a id="task-container-start"></a>

### container/start

Start Jaeger in a container runtime


Builds Jaeger runtime settings and delegates container startup to the container role.

This entry point requires the ElasticSearch host inventory to be available.


```yaml
- name: Start Jaeger in a container runtime
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage.
    elasticsearch_host: "string"
    # Sets the Jaeger container name. The default derives from `inventory_hostname`.
    jaeger_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint for the Jaeger image.
    jaeger_registry_endpoint: "{{ lookup('env', 'JAEGER_REGISTRY_ENDPOINT') or 'docker.io/jaegertracing' }}"
    # Sets the Jaeger image name.
    jaeger_image_name: all-in-one
    # Sets the Jaeger image tag.
    jaeger_image_tag: latest
    # Sets the Jaeger container image. The default derives from `jaeger_registry_endpoint`, `jaeger_image_name`, and `jaeger_image_tag`.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
    # Sets the shared remote configuration base directory. This backs the default of `jaeger_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. The default derives from `remote_config_dir`.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the in-container directory where Jaeger reads configuration and certificates.
    jaeger_container_config_dir: /var/config
    # Sets the Jaeger query UI port.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port.
    jaeger_collector_port: 4317
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/start
```

<a id="task-container-stop"></a>

### container/stop

Stop the Jaeger container


Delegates Jaeger container shutdown to the container role.


```yaml
- name: Stop the Jaeger container
  vars:
    # Sets the Jaeger container name. The default derives from `inventory_hostname`.
    jaeger_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint for the Jaeger image.
    jaeger_registry_endpoint: "{{ lookup('env', 'JAEGER_REGISTRY_ENDPOINT') or 'docker.io/jaegertracing' }}"
    # Sets the Jaeger image name.
    jaeger_image_name: all-in-one
    # Sets the Jaeger image tag.
    jaeger_image_tag: latest
    # Sets the Jaeger container image. The default derives from `jaeger_registry_endpoint`, `jaeger_image_name`, and `jaeger_image_tag`.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/stop
```

<a id="task-container-rm"></a>

### container/rm

Remove the Jaeger container


Delegates Jaeger container removal to the container role.


```yaml
- name: Remove the Jaeger container
  vars:
    # Sets the Jaeger container name. The default derives from `inventory_hostname`.
    jaeger_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint for the Jaeger image.
    jaeger_registry_endpoint: "{{ lookup('env', 'JAEGER_REGISTRY_ENDPOINT') or 'docker.io/jaegertracing' }}"
    # Sets the Jaeger image name.
    jaeger_image_name: all-in-one
    # Sets the Jaeger image tag.
    jaeger_image_tag: latest
    # Sets the Jaeger container image. The default derives from `jaeger_registry_endpoint`, `jaeger_image_name`, and `jaeger_image_tag`.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/rm
```

<a id="task-container-fetch_logs"></a>

### container/fetch_logs

Fetch logs from the Jaeger container


Delegates Jaeger container log collection to the container role.


```yaml
- name: Fetch logs from the Jaeger container
  vars:
    # Sets the Jaeger container name. The default derives from `inventory_hostname`.
    jaeger_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/fetch_logs
```

<a id="task-k8s-start"></a>

### k8s/start

Start Jaeger on Kubernetes


Applies the Jaeger Kubernetes service, node port service, and deployment resources.

The NodePort service is created only when `jaeger_k8s_use_node_port` is set to `true`.

This entry point requires the ElasticSearch host inventory to be available.


```yaml
- name: Start Jaeger on Kubernetes
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage.
    elasticsearch_host: "string"
    # Sets the Kubernetes resource name used for Jaeger objects. The default derives from `inventory_hostname`.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the rollout wait timeout for the Jaeger Kubernetes deployment.
    jaeger_k8s_wait_timeout: 120
    # Sets the pod filesystem group for the Jaeger Kubernetes workload.
    jaeger_k8s_fs_group: 0
    # Exposes the Jaeger Kubernetes service through a NodePort service when set to `true`. The NodePort service uses the per-port node port values below.
    jaeger_k8s_use_node_port: false
    # Sets the registry endpoint for the Jaeger image.
    jaeger_registry_endpoint: "{{ lookup('env', 'JAEGER_REGISTRY_ENDPOINT') or 'docker.io/jaegertracing' }}"
    # Sets the Jaeger image name.
    jaeger_image_name: all-in-one
    # Sets the Jaeger image tag.
    jaeger_image_tag: latest
    # Sets the Jaeger container image. The default derives from `jaeger_registry_endpoint`, `jaeger_image_name`, and `jaeger_image_tag`.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
    # Sets the in-container directory where Jaeger reads configuration and certificates.
    jaeger_container_config_dir: /var/config
    # Sets the Jaeger query UI port.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port.
    jaeger_collector_port: 4317
    # Sets the Kubernetes NodePort for the Jaeger UI service. The default derives from `jaeger_ui_port`.
    jaeger_k8s_ui_node_port: "{{ jaeger_ui_port }}"
    # Sets the Kubernetes NodePort for the Jaeger admin service. The default derives from `jaeger_admin_port`.
    jaeger_k8s_admin_node_port: "{{ jaeger_admin_port }}"
    # Sets the Kubernetes NodePort for the Jaeger collector HTTP server. The default derives from `jaeger_http_server_port`.
    jaeger_k8s_http_server_node_port: "{{ jaeger_http_server_port }}"
    # Sets the Kubernetes NodePort for the Jaeger OTLP HTTP collector. The default derives from `jaeger_http_collector_port`.
    jaeger_k8s_http_collector_node_port: "{{ jaeger_http_collector_port }}"
    # Sets the Kubernetes NodePort for the Jaeger gRPC server. The default derives from `jaeger_grpc_server_port`.
    jaeger_k8s_grpc_server_node_port: "{{ jaeger_grpc_server_port }}"
    # Sets the Kubernetes NodePort for the Jaeger OTLP gRPC collector. The default derives from `jaeger_collector_port`.
    jaeger_k8s_collector_node_port: "{{ jaeger_collector_port }}"
    # Sets the Kubernetes namespace used for Jaeger resources.
    k8s_namespace: "string"
    # Sets the Kubernetes imagePullSecret name when the deployment needs one.
    k8s_image_pull_secret: "string"
    # Sets the readiness probe initial delay used by the Jaeger deployment template.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Sets the readiness probe period used by the Jaeger deployment template.
    k8s_readiness_probe_period_seconds: 1000
    # Sets the readiness probe timeout used by the Jaeger deployment template.
    k8s_readiness_probe_timeout_seconds: 1000
    # Sets the readiness probe failure threshold used by the Jaeger deployment template.
    k8s_readiness_probe_failure_threshold: 1000
    # Sets the liveness probe initial delay used by the Jaeger deployment template.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Sets the liveness probe period used by the Jaeger deployment template.
    k8s_liveness_probe_period_seconds: 1000
    # Sets the liveness probe timeout used by the Jaeger deployment template.
    k8s_liveness_probe_timeout_seconds: 1000
    # Sets the liveness probe failure threshold used by the Jaeger deployment template.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/start
```

<a id="task-k8s-rm"></a>

### k8s/rm

Remove Jaeger Kubernetes resources


Deletes the Jaeger deployment and service resources from Kubernetes.


```yaml
- name: Remove Jaeger Kubernetes resources
  vars:
    # Sets the Kubernetes resource name used for Jaeger objects. The default derives from `inventory_hostname`.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Jaeger resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/rm
```

<a id="task-k8s-fetch_logs"></a>

### k8s/fetch_logs

Fetch logs from Jaeger pods


Delegates Jaeger pod log collection to the k8s role using the Jaeger pod label selector.


```yaml
- name: Fetch logs from Jaeger pods
  vars:
    # Sets the Kubernetes resource name used for Jaeger objects. The default derives from `inventory_hostname`.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/fetch_logs
```

<a id="task-k8s-ping"></a>

### k8s/ping

Check that Jaeger Kubernetes node ports are reachable


Builds the Jaeger Kubernetes node port list and delegates the connectivity check to the utils role.

The node port values default to the corresponding Jaeger service ports.


```yaml
- name: Check that Jaeger Kubernetes node ports are reachable
  vars:
    # Exposes the Jaeger Kubernetes service through a NodePort service when set to `true`. The NodePort service uses the per-port node port values below.
    jaeger_k8s_use_node_port: false
    # Sets the Jaeger query UI port.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port.
    jaeger_collector_port: 4317
    # Sets the Kubernetes NodePort for the Jaeger UI service. The default derives from `jaeger_ui_port`.
    jaeger_k8s_ui_node_port: "{{ jaeger_ui_port }}"
    # Sets the Kubernetes NodePort for the Jaeger admin service. The default derives from `jaeger_admin_port`.
    jaeger_k8s_admin_node_port: "{{ jaeger_admin_port }}"
    # Sets the Kubernetes NodePort for the Jaeger collector HTTP server. The default derives from `jaeger_http_server_port`.
    jaeger_k8s_http_server_node_port: "{{ jaeger_http_server_port }}"
    # Sets the Kubernetes NodePort for the Jaeger OTLP HTTP collector. The default derives from `jaeger_http_collector_port`.
    jaeger_k8s_http_collector_node_port: "{{ jaeger_http_collector_port }}"
    # Sets the Kubernetes NodePort for the Jaeger gRPC server. The default derives from `jaeger_grpc_server_port`.
    jaeger_k8s_grpc_server_node_port: "{{ jaeger_grpc_server_port }}"
    # Sets the Kubernetes NodePort for the Jaeger OTLP gRPC collector. The default derives from `jaeger_collector_port`.
    jaeger_k8s_collector_node_port: "{{ jaeger_collector_port }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/ping
```

<a id="task-config-transfer"></a>

### config/transfer

Transfer Jaeger configuration assets


Creates the Jaeger configuration directory and copies the ElasticSearch CA certificate when TLS is enabled.

Delegates Kubernetes ConfigMap creation to the Jaeger Kubernetes config entry point when requested.


```yaml
- name: Transfer Jaeger configuration assets
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage.
    elasticsearch_host: "string"
    # Sets the local directory containing fetched artifacts used by Jaeger.
    fetched_artifacts_dir: "string"
    # Sets the shared remote configuration base directory. This backs the default of `jaeger_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. The default derives from `remote_config_dir`.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/transfer
```

<a id="task-config-rm"></a>

### config/rm

Remove Jaeger configuration assets


Deletes the remote Jaeger configuration directory.

Nested Jaeger Kubernetes config cleanup validates its own required arguments.


```yaml
- name: Remove Jaeger configuration assets
  vars:
    # Sets the shared remote configuration base directory. This backs the default of `jaeger_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. The default derives from `remote_config_dir`.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/rm
```

<a id="task-k8s-config-transfer"></a>

### k8s/config/transfer

Create the Jaeger Kubernetes ConfigMap


Applies the Jaeger ConfigMap that carries the ElasticSearch CA certificate when TLS is enabled.


```yaml
- name: Create the Jaeger Kubernetes ConfigMap
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage.
    elasticsearch_host: "string"
    # Sets the Kubernetes resource name used for Jaeger objects. The default derives from `inventory_hostname`.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the shared remote configuration base directory. This backs the default of `jaeger_remote_config_dir`.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. The default derives from `remote_config_dir`.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the Kubernetes namespace used for Jaeger resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/config/transfer
```

<a id="task-k8s-config-rm"></a>

### k8s/config/rm

Remove the Jaeger Kubernetes ConfigMap


Deletes the Jaeger ConfigMap from Kubernetes when the Kubernetes deployment mode is enabled.


```yaml
- name: Remove the Jaeger Kubernetes ConfigMap
  vars:
    # Sets the Kubernetes resource name used for Jaeger objects. The default derives from `inventory_hostname`.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Jaeger resources.
    k8s_namespace: "string"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/config/rm
```


