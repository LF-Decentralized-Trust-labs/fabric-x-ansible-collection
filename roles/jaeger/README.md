# hyperledger.fabricx.jaeger

> Deploys and manages Jaeger for Hyperledger Fabric-X tracing in container or Kubernetes mode.

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
  - [k8s/start](#k8sstart)
  - [k8s/rm](#k8srm)
  - [k8s/fetch_logs](#k8sfetch_logs)
  - [k8s/ping](#k8sping)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.jaeger
```

## Tasks

### start

> Select the Jaeger deployment mode to start

Starts Jaeger in container mode or applies the Kubernetes Service and Deployment manifests.

Container mode configures the image, ports, and ElasticSearch connection before the container role starts the workload.

Kubernetes mode creates the namespace, service objects, optional NodePort service, and deployment.

```yaml
- name: Select the Jaeger deployment mode to start
  vars:
    # Runs the container-based Jaeger path when set to `true`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: start
```

### stop

> Select the Jaeger deployment mode to stop

Stops the running Jaeger container without removing configuration assets.

```yaml
- name: Select the Jaeger deployment mode to stop
  vars:
    # Runs the container-based Jaeger path when set to `true`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: stop
```

### teardown

> Select the Jaeger deployment mode to remove

Removes the container workload or Kubernetes resources for the active Jaeger deployment.

Kubernetes teardown deletes the deployment, service, and optional NodePort service.

```yaml
- name: Select the Jaeger deployment mode to remove
  vars:
    # Runs the container-based Jaeger path when set to `true`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: teardown
```

### wipe

> Remove the Jaeger deployment and configuration

Runs the teardown and configuration cleanup entry points for Jaeger.

```yaml
- name: Remove the Jaeger deployment and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: wipe
```

### fetch_logs

> Select the Jaeger deployment mode to collect logs from

Collects logs from the running Jaeger container or from the Jaeger pods in Kubernetes.

```yaml
- name: Select the Jaeger deployment mode to collect logs from
  vars:
    # Runs the container-based Jaeger path when set to `true`.
    jaeger_use_container: "{{ not jaeger_use_k8s }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: fetch_logs
```

### ping

> Check that Jaeger service ports are reachable

Checks the Jaeger query, admin, collector, and OTLP endpoints with the utils ping helper.

Container mode pings the published host ports, while Kubernetes mode checks the service ports and optional NodePort values.

```yaml
- name: Check that Jaeger service ports are reachable
  vars:
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
    # Sets the Jaeger query UI port. Example: `16686` for the Jaeger query web interface endpoint.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port. Example: `14269` for liveness and admin access on the Jaeger service.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port. Example: `14268` for the collector HTTP endpoint exposed by the service.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port. Example: `4318` for OTLP/HTTP ingestion from agents and SDKs.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port. Example: `14250` for the collector gRPC endpoint used by tracing clients.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port. Example: `4317` for OTLP/gRPC ingestion from Jaeger agents.
    jaeger_collector_port: 4317
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: ping
```

### container/start

> Start Jaeger in a container runtime

Builds the Jaeger container environment, publishes the query and collector ports, and mounts the remote config directory.

Starts the all-in-one container and waits for the query UI port to answer before returning.

This entry point requires the ElasticSearch host inventory to be available.

```yaml
- name: Start Jaeger in a container runtime
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage. Example: `elasticsearch-0` when Jaeger should send spans to that inventory host.
    elasticsearch_host: "string"
    # Sets the Jaeger container name.
    jaeger_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint for the Jaeger image.
    jaeger_registry_endpoint: "{{ lookup('env', 'JAEGER_REGISTRY_ENDPOINT') or 'docker.io/jaegertracing' }}"
    # Sets the Jaeger image name.
    jaeger_image_name: all-in-one
    # Sets the Jaeger image tag.
    jaeger_image_tag: latest
    # Sets the Jaeger container image.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
    # Sets the shared remote configuration base directory. Example: `/var/lib/fabricx/jaeger/config` on the control or remote host.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. Example: `/var/lib/fabricx/jaeger/config` so the container and Kubernetes ConfigMap use the same path.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the in-container directory where Jaeger reads configuration and certificates. Example: `/var/config` for the all-in-one image mount point.
    jaeger_container_config_dir: /var/config
    # Sets the Jaeger query UI port. Example: `16686` for the Jaeger query web interface endpoint.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port. Example: `14269` for liveness and admin access on the Jaeger service.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port. Example: `14268` for the collector HTTP endpoint exposed by the service.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port. Example: `4318` for OTLP/HTTP ingestion from agents and SDKs.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port. Example: `14250` for the collector gRPC endpoint used by tracing clients.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port. Example: `4317` for OTLP/gRPC ingestion from Jaeger agents.
    jaeger_collector_port: 4317
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/start
```

### container/stop

> Stop the Jaeger container

Stops the named Jaeger container without changing image or configuration settings.

```yaml
- name: Stop the Jaeger container
  vars:
    # Sets the Jaeger container name.
    jaeger_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint for the Jaeger image.
    jaeger_registry_endpoint: "{{ lookup('env', 'JAEGER_REGISTRY_ENDPOINT') or 'docker.io/jaegertracing' }}"
    # Sets the Jaeger image name.
    jaeger_image_name: all-in-one
    # Sets the Jaeger image tag.
    jaeger_image_tag: latest
    # Sets the Jaeger container image.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/stop
```

### container/rm

> Remove the Jaeger container

Removes the Jaeger container and its runtime state from the container host.

```yaml
- name: Remove the Jaeger container
  vars:
    # Sets the Jaeger container name.
    jaeger_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint for the Jaeger image.
    jaeger_registry_endpoint: "{{ lookup('env', 'JAEGER_REGISTRY_ENDPOINT') or 'docker.io/jaegertracing' }}"
    # Sets the Jaeger image name.
    jaeger_image_name: all-in-one
    # Sets the Jaeger image tag.
    jaeger_image_tag: latest
    # Sets the Jaeger container image.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch logs from the Jaeger container

Collects the container logs for the Jaeger runtime from the named container.

```yaml
- name: Fetch logs from the Jaeger container
  vars:
    # Sets the Jaeger container name.
    jaeger_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: container/fetch_logs
```

### k8s/start

> Start Jaeger on Kubernetes

Applies the Jaeger Service, optional NodePort Service, and Deployment resources to Kubernetes.

The deployment template mounts the configuration path, wires the ElasticSearch CA certificate, and uses the provided probe and port settings.

The NodePort service is created only when `jaeger_k8s_use_node_port` is set to `true`.

This entry point requires the ElasticSearch host inventory to be available.

```yaml
- name: Start Jaeger on Kubernetes
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage. Example: `elasticsearch-0` when Jaeger should send spans to that inventory host.
    elasticsearch_host: "string"
    # Sets the Kubernetes resource name used for Jaeger objects.
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
    # Sets the Jaeger container image.
    jaeger_image: "{{ jaeger_registry_endpoint }}/{{ jaeger_image_name }}:{{ jaeger_image_tag }}"
    # Sets the in-container directory where Jaeger reads configuration and certificates. Example: `/var/config` for the all-in-one image mount point.
    jaeger_container_config_dir: /var/config
    # Sets the Jaeger query UI port. Example: `16686` for the Jaeger query web interface endpoint.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port. Example: `14269` for liveness and admin access on the Jaeger service.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port. Example: `14268` for the collector HTTP endpoint exposed by the service.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port. Example: `4318` for OTLP/HTTP ingestion from agents and SDKs.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port. Example: `14250` for the collector gRPC endpoint used by tracing clients.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port. Example: `4317` for OTLP/gRPC ingestion from Jaeger agents.
    jaeger_collector_port: 4317
    # Sets the Kubernetes NodePort for the Jaeger UI service. Example: `30686` to expose the query UI on a stable node port.
    jaeger_k8s_ui_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger admin service. Example: `30669` for the admin and health-check node port.
    jaeger_k8s_admin_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger collector HTTP server. Example: `30668` for the collector HTTP node port.
    jaeger_k8s_http_server_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger OTLP HTTP collector. Example: `30418` for OTLP/HTTP traffic through Kubernetes.
    jaeger_k8s_http_collector_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger gRPC server. Example: `31450` for the gRPC collector service endpoint.
    jaeger_k8s_grpc_server_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger OTLP gRPC collector. Example: `30417` for OTLP/gRPC traffic through Kubernetes.
    jaeger_k8s_collector_node_port: 1000
    # Sets the Kubernetes namespace used for Jaeger resources. Example: `tracing` when Jaeger shares a namespace with other observability services.
    k8s_namespace: "string"
    # Sets the Kubernetes imagePullSecret name when the deployment needs one. Example: `registry-pull-secret` when the Jaeger image comes from a private registry.
    k8s_image_pull_secret: "string"
    # Sets the readiness probe initial delay used by the Jaeger deployment template. Example: `5` to let the pod initialize before readiness checks begin.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Sets the readiness probe period used by the Jaeger deployment template. Example: `10` to check whether the query and collector endpoints are ready every ten seconds.
    k8s_readiness_probe_period_seconds: 1000
    # Sets the readiness probe timeout used by the Jaeger deployment template. Example: `2` for a fast readiness failure on the Jaeger service endpoint.
    k8s_readiness_probe_timeout_seconds: 1000
    # Sets the readiness probe failure threshold used by the Jaeger deployment template. Example: `3` to fail readiness after three consecutive misses.
    k8s_readiness_probe_failure_threshold: 1000
    # Sets the liveness probe initial delay used by the Jaeger deployment template. Example: `15` to wait for the query and collector services to settle before liveness checks.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Sets the liveness probe period used by the Jaeger deployment template. Example: `20` to run liveness checks at a slower cadence than readiness checks.
    k8s_liveness_probe_period_seconds: 1000
    # Sets the liveness probe timeout used by the Jaeger deployment template. Example: `2` for a quick failure if the admin endpoint stops responding.
    k8s_liveness_probe_timeout_seconds: 1000
    # Sets the liveness probe failure threshold used by the Jaeger deployment template. Example: `3` to restart the pod after three missed liveness checks.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/start
```

### k8s/rm

> Remove Jaeger Kubernetes resources

Deletes the Jaeger Deployment, Service, and NodePort Service from the target namespace.

```yaml
- name: Remove Jaeger Kubernetes resources
  vars:
    # Sets the Kubernetes resource name used for Jaeger objects.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Jaeger resources. Example: `tracing` when Jaeger shares a namespace with other observability services.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch logs from Jaeger pods

Collects logs from Jaeger pods using the resource label selector for the Kubernetes deployment.

```yaml
- name: Fetch logs from Jaeger pods
  vars:
    # Sets the Kubernetes resource name used for Jaeger objects.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/fetch_logs
```

### k8s/ping

> Check that Jaeger Kubernetes node ports are reachable

Checks the Jaeger Kubernetes service ports and, when enabled, the NodePort values for the query, admin, and collector endpoints.

```yaml
- name: Check that Jaeger Kubernetes node ports are reachable
  vars:
    # Exposes the Jaeger Kubernetes service through a NodePort service when set to `true`. The NodePort service uses the per-port node port values below.
    jaeger_k8s_use_node_port: false
    # Sets the Jaeger query UI port. Example: `16686` for the Jaeger query web interface endpoint.
    jaeger_ui_port: 16686
    # Sets the Jaeger admin HTTP port. Example: `14269` for liveness and admin access on the Jaeger service.
    jaeger_admin_port: 14269
    # Sets the Jaeger collector HTTP server port. Example: `14268` for the collector HTTP endpoint exposed by the service.
    jaeger_http_server_port: 14268
    # Sets the Jaeger OTLP HTTP collector port. Example: `4318` for OTLP/HTTP ingestion from agents and SDKs.
    jaeger_http_collector_port: 4318
    # Sets the Jaeger gRPC server port. Example: `14250` for the collector gRPC endpoint used by tracing clients.
    jaeger_grpc_server_port: 14250
    # Sets the Jaeger OTLP gRPC collector port. Example: `4317` for OTLP/gRPC ingestion from Jaeger agents.
    jaeger_collector_port: 4317
    # Sets the Kubernetes NodePort for the Jaeger UI service. Example: `30686` to expose the query UI on a stable node port.
    jaeger_k8s_ui_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger admin service. Example: `30669` for the admin and health-check node port.
    jaeger_k8s_admin_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger collector HTTP server. Example: `30668` for the collector HTTP node port.
    jaeger_k8s_http_server_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger OTLP HTTP collector. Example: `30418` for OTLP/HTTP traffic through Kubernetes.
    jaeger_k8s_http_collector_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger gRPC server. Example: `31450` for the gRPC collector service endpoint.
    jaeger_k8s_grpc_server_node_port: 1000
    # Sets the Kubernetes NodePort for the Jaeger OTLP gRPC collector. Example: `30417` for OTLP/gRPC traffic through Kubernetes.
    jaeger_k8s_collector_node_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/ping
```

### config/transfer

> Transfer Jaeger configuration assets

Creates the remote Jaeger config path, copies the ElasticSearch CA certificate when TLS is enabled, and prepares the runtime config directory.

In Kubernetes mode, also delegates ConfigMap creation to the Kubernetes config entry point.

```yaml
- name: Transfer Jaeger configuration assets
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage. Example: `elasticsearch-0` when Jaeger should send spans to that inventory host.
    elasticsearch_host: "string"
    # Sets the local directory containing fetched artifacts used by Jaeger. Example: `/tmp/fabricx-artifacts` when copying the ElasticSearch CA certificate into Jaeger config.
    fetched_artifacts_dir: "string"
    # Sets the shared remote configuration base directory. Example: `/var/lib/fabricx/jaeger/config` on the control or remote host.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. Example: `/var/lib/fabricx/jaeger/config` so the container and Kubernetes ConfigMap use the same path.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/transfer
```

### config/rm

> Remove Jaeger configuration assets

Deletes the remote Jaeger configuration directory and any copied certificate material.

Nested Kubernetes config cleanup validates its own required arguments before removing the ConfigMap.

```yaml
- name: Remove Jaeger configuration assets
  vars:
    # Sets the shared remote configuration base directory. Example: `/var/lib/fabricx/jaeger/config` on the control or remote host.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. Example: `/var/lib/fabricx/jaeger/config` so the container and Kubernetes ConfigMap use the same path.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/rm
```

### k8s/config/transfer

> Create the Jaeger Kubernetes ConfigMap

Creates the ConfigMap that projects the Jaeger config path and ElasticSearch CA certificate into the pod.

```yaml
- name: Create the Jaeger Kubernetes ConfigMap
  vars:
    # Names the inventory host running ElasticSearch for Jaeger span storage. Example: `elasticsearch-0` when Jaeger should send spans to that inventory host.
    elasticsearch_host: "string"
    # Sets the Kubernetes resource name used for Jaeger objects.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the shared remote configuration base directory. Example: `/var/lib/fabricx/jaeger/config` on the control or remote host.
    remote_config_dir: "string"
    # Sets the remote directory mounted into the Jaeger container for configuration and certificates. Example: `/var/lib/fabricx/jaeger/config` so the container and Kubernetes ConfigMap use the same path.
    jaeger_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the Kubernetes namespace used for Jaeger resources. Example: `tracing` when Jaeger shares a namespace with other observability services.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the Jaeger Kubernetes ConfigMap

Deletes the Jaeger ConfigMap from Kubernetes when container config data is no longer needed.

```yaml
- name: Remove the Jaeger Kubernetes ConfigMap
  vars:
    # Sets the Kubernetes resource name used for Jaeger objects.
    jaeger_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used for Jaeger resources. Example: `tracing` when Jaeger shares a namespace with other observability services.
    k8s_namespace: "string"
    # Runs the Kubernetes Jaeger path when set to `true`.
    jaeger_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: k8s/config/rm
```
