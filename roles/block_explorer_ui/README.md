# hyperledger.fabricx.block_explorer_ui

> Deploys and manages the Fabric-X Block Explorer Next.js UI across container and Kubernetes modes.

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
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [openshift/start](#openshiftstart)
  - [openshift/ping](#openshiftping)
  - [openshift/rm](#openshiftrm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.block_explorer_ui
```

## Tasks

### start

> Start the Block Explorer UI

Starts the Block Explorer UI by dispatching to the container or Kubernetes entry point. Set exactly one deployment mode flag for the target host.

```yaml
- name: Start the Block Explorer UI
  vars:
    # Run the container runtime.
    block_explorer_ui_use_container: "{{ (not block_explorer_ui_use_k8s) and (not block_explorer_ui_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_ui_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_ui_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: start
```

### stop

> Stop the Block Explorer UI in container mode

Stops the Block Explorer UI container without removing generated artifacts.

```yaml
- name: Stop the Block Explorer UI in container mode
  vars:
    # Run the container runtime.
    block_explorer_ui_use_container: "{{ (not block_explorer_ui_use_k8s) and (not block_explorer_ui_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_ui_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_ui_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: stop
```

### teardown

> Remove the Block Explorer UI in the selected deployment mode

Removes the Block Explorer UI container or Kubernetes workload by dispatching to the matching entry point.

```yaml
- name: Remove the Block Explorer UI in the selected deployment mode
  vars:
    # Run the container runtime.
    block_explorer_ui_use_container: "{{ (not block_explorer_ui_use_k8s) and (not block_explorer_ui_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_ui_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_ui_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: teardown
```

### wipe

> Remove all Block Explorer UI data

Removes the Block Explorer UI workload.

```yaml
- name: Remove all Block Explorer UI data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: wipe
```

### fetch_logs

> Collect Block Explorer UI logs for the selected deployment mode

Collects Block Explorer UI logs from the container deployment or from the Kubernetes pod for troubleshooting.

```yaml
- name: Collect Block Explorer UI logs for the selected deployment mode
  vars:
    # Run the container runtime.
    block_explorer_ui_use_container: "{{ (not block_explorer_ui_use_k8s) and (not block_explorer_ui_use_openshift) }}"
    # Use Kubernetes resources.
    block_explorer_ui_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_ui_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: fetch_logs
```

### ping

> Check that the Block Explorer UI web port is reachable

Verifies that the Block Explorer UI web interface port is reachable on the target host. In Kubernetes mode, also validates the optional NodePort configuration when enabled.

```yaml
- name: Check that the Block Explorer UI web port is reachable
  vars:
    # Use Kubernetes resources.
    block_explorer_ui_use_k8s: false
    # Selects the OpenShift deployment branch.
    block_explorer_ui_use_openshift: false
    # Web port exposed by the Block Explorer UI. Example: `18000`.
    block_explorer_ui_port: 18000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: ping
```

### container/start

> Start the Block Explorer UI container

Starts the containerized Block Explorer UI with `BACKEND_URL` pointed at the resolved Block Explorer server address.

```yaml
- name: Start the Block Explorer UI container
  vars:
    # Container name used by the runtime.
    block_explorer_ui_container_name: "{{ inventory_hostname }}"
    # Block Explorer UI container image.
    block_explorer_ui_image: "{{ block_explorer_ui_registry_endpoint }}/{{ block_explorer_ui_image_name }}:{{ block_explorer_ui_image_tag }}"
    # Image registry endpoint.
    block_explorer_ui_registry_endpoint: "{{ lookup('env', 'BLOCK_EXPLORER_UI_REGISTRY_ENDPOINT') or 'ghcr.io/lf-decentralized-trust-labs' }}"
    # Image name used by the Block Explorer UI container.
    block_explorer_ui_image_name: fabric-x-block-explorer-ui
    # Image tag used by the Block Explorer UI container.
    block_explorer_ui_image_tag: latest
    # Web port exposed by the Block Explorer UI. Example: `18000`.
    block_explorer_ui_port: 18000
    # Sets the inventory host name of the Block Explorer server instance used by the UI. Example: `block-explorer`. The referenced host must expose the `block_explorer_port` inventory var.
    block_explorer_host: "block-explorer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: container/start
```

### container/stop

> Stop the Block Explorer UI container

Stops the running Block Explorer UI container by name without deleting associated artifacts.

```yaml
- name: Stop the Block Explorer UI container
  vars:
    # Container name used by the runtime.
    block_explorer_ui_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: container/stop
```

### container/rm

> Remove the Block Explorer UI container

Removes the Block Explorer UI container by name.

```yaml
- name: Remove the Block Explorer UI container
  vars:
    # Container name used by the runtime.
    block_explorer_ui_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch logs from the Block Explorer UI container

Collects logs from the named Block Explorer UI container for post-startup inspection.

```yaml
- name: Fetch logs from the Block Explorer UI container
  vars:
    # Container name used by the runtime.
    block_explorer_ui_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: container/fetch_logs
```

### k8s/start

> Start the Block Explorer UI on Kubernetes

Applies the Block Explorer UI Service, optional NodePort and LoadBalancer Services, and Deployment on Kubernetes.

```yaml
- name: Start the Block Explorer UI on Kubernetes
  vars:
    # Kubernetes resource name used for the Deployment, Service, and optional NodePort Service.
    block_explorer_ui_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Block Explorer UI resources.
    block_explorer_ui_k8s_part_of: block-explorer
    # Web port exposed by the Block Explorer UI. Example: `18000`.
    block_explorer_ui_port: 18000
    # Kubernetes NodePort value used by the external web Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30600`.
    block_explorer_ui_k8s_node_port: 30600
    # Deployment rollout wait timeout in seconds.
    block_explorer_ui_k8s_wait_timeout: 120
    # Block Explorer UI container image.
    block_explorer_ui_image: "{{ block_explorer_ui_registry_endpoint }}/{{ block_explorer_ui_image_name }}:{{ block_explorer_ui_image_tag }}"
    # Image registry endpoint.
    block_explorer_ui_registry_endpoint: "{{ lookup('env', 'BLOCK_EXPLORER_UI_REGISTRY_ENDPOINT') or 'ghcr.io/lf-decentralized-trust-labs' }}"
    # Image name used by the Block Explorer UI container.
    block_explorer_ui_image_name: fabric-x-block-explorer-ui
    # Image tag used by the Block Explorer UI container.
    block_explorer_ui_image_tag: latest
    # Sets the inventory host name of the Block Explorer server instance used by the UI. Example: `block-explorer`. The referenced host must expose the `block_explorer_port` inventory var.
    block_explorer_host: "block-explorer"
    # Kubernetes namespace used for Block Explorer UI resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Optional image pull secret used by the Block Explorer UI Deployment. Example: `fabricx-registry-pull`.
    k8s_image_pull_secret: "fabricx-registry-pull"
    # Sets the Block Explorer UI readiness probe initial delay. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Sets the Block Explorer UI readiness probe period. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Sets the Block Explorer UI readiness probe timeout. Example: `5`.
    k8s_readiness_probe_timeout_seconds: 5
    # Sets the Block Explorer UI readiness probe failure threshold. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Sets the Block Explorer UI liveness probe initial delay. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Sets the Block Explorer UI liveness probe period. Example: `15`.
    k8s_liveness_probe_period_seconds: 15
    # Sets the Block Explorer UI liveness probe timeout. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Sets the Block Explorer UI liveness probe failure threshold. Example: `5`.
    k8s_liveness_probe_failure_threshold: 5
    # Set to `true` to create a LoadBalancer Service entry that exposes the web port externally. When undefined or `false`, the web port is not included in the LoadBalancer Service.
    block_explorer_ui_k8s_loadbalancer_expose_port: false
    # Optional Kubernetes container resource requests and limits. Example: `{'requests': {'memory': '256Mi', 'cpu': '100m'}, 'limits': {'memory': '512Mi', 'cpu': '500m'}}`.
    k8s_resources:
      requests:
        memory: "256Mi"
        cpu: "100m"
      limits:
        memory: "512Mi"
        cpu: "500m"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: k8s/start
```

### k8s/ping

> Check that the Block Explorer UI Kubernetes service is reachable

Probes configured Kubernetes NodePort values and LoadBalancer-exposed service ports for external reachability.

```yaml
- name: Check that the Block Explorer UI Kubernetes service is reachable
  vars:
    # Web port exposed by the Block Explorer UI. Example: `18000`.
    block_explorer_ui_port: 18000
    # Kubernetes NodePort value used by the external web Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30600`.
    block_explorer_ui_k8s_node_port: 30600
    # Set to `true` to create a LoadBalancer Service entry that exposes the web port externally. When undefined or `false`, the web port is not included in the LoadBalancer Service.
    block_explorer_ui_k8s_loadbalancer_expose_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: k8s/ping
```

### k8s/rm

> Remove Block Explorer UI Kubernetes resources

Deletes the Block Explorer UI Deployment, Service, and NodePort Service from Kubernetes.

```yaml
- name: Remove Block Explorer UI Kubernetes resources
  vars:
    # Kubernetes resource name used for the Deployment, Service, and optional NodePort Service.
    block_explorer_ui_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for Block Explorer UI resources. Example: `fabricx-block-explorer`.
    k8s_namespace: "fabricx-block-explorer"
    # Kubernetes NodePort value used by the external web Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30600`.
    block_explorer_ui_k8s_node_port: 30600
    # Set to `true` to create a LoadBalancer Service entry that exposes the web port externally. When undefined or `false`, the web port is not included in the LoadBalancer Service.
    block_explorer_ui_k8s_loadbalancer_expose_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch logs from the Block Explorer UI pod

Collects logs from the Block Explorer UI pod selected by the application label.

```yaml
- name: Fetch logs from the Block Explorer UI pod
  vars:
    # Kubernetes resource name used for the Deployment, Service, and optional NodePort Service.
    block_explorer_ui_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: k8s/fetch_logs
```

### openshift/start

> Start the OpenShift deployment

Reuses the Kubernetes workload flow and manages an OpenShift Route for the web port.

```yaml
- name: Start the OpenShift deployment
  vars:
    # Kubernetes resource name used for the Deployment, Service, and optional NodePort Service.
    block_explorer_ui_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Block Explorer UI resources.
    block_explorer_ui_k8s_part_of: block-explorer
    # Specifies the OpenShift Route host. Example: `block-explorer-ui.apps.example.com`.
    block_explorer_ui_openshift_route: "block-explorer-ui.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: openshift/start
```

### openshift/ping

> Check the OpenShift deployment

Checks the configured OpenShift Route and reuses the Kubernetes service ping flow.

```yaml
- name: Check the OpenShift deployment
  vars:
    # Specifies the OpenShift Route host. Example: `block-explorer-ui.apps.example.com`.
    block_explorer_ui_openshift_route: "block-explorer-ui.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: openshift/ping
```

### openshift/rm

> Remove the OpenShift deployment

Reuses the Kubernetes workload flow and removes the OpenShift Route for the web port.

```yaml
- name: Remove the OpenShift deployment
  vars:
    # Kubernetes resource name used for the Deployment, Service, and optional NodePort Service.
    block_explorer_ui_k8s_resource_name: "{{ inventory_hostname }}"
    # Specifies the OpenShift Route host. Example: `block-explorer-ui.apps.example.com`.
    block_explorer_ui_openshift_route: "block-explorer-ui.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.block_explorer_ui
    tasks_from: openshift/rm
```
