# hyperledger.fabricx.alloy

> Ansible role to deploy Grafana Alloy for log collection and forwarding to Loki.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [container/start](#containerstart)
  - [container/rm](#containerrm)
  - [data/rm](#datarm)
  - [config/rm](#configrm)
  - [k8s/start](#k8sstart)
  - [k8s/rm](#k8srm)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)
  - [config/transfer](#configtransfer)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.alloy
```

## Tasks

### start

> Start Alloy

Dispatches to container or Kubernetes deployment based on deployment mode flags.

```yaml
- name: Start Alloy
  vars:
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: start
```

### stop

> Stop Alloy container

Stops the Grafana Alloy container without removing it.

```yaml
- name: Stop Alloy container
  vars:
    # Name of the Alloy container.
    alloy_container_name: alloy
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: stop
```

### teardown

> Teardown Alloy

Removes the Alloy container, Kubernetes/OpenShift workload, and data directory.

```yaml
- name: Teardown Alloy
  vars:
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: teardown
```

### wipe

> Wipe Alloy configuration

Removes the Alloy configuration directory. Intended to be called explicitly, not as part of routine teardown.

```yaml
- name: Wipe Alloy configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: wipe
```

### container/start

> Start Alloy container

Starts the Alloy container via hyperledger.fabricx.container, mounting config, data, and (when enabled) the Docker/Podman socket.

```yaml
- name: Start Alloy container
  vars:
    # Name of the Alloy container.
    alloy_container_name: alloy
    # Sets the Grafana image reference.
    alloy_image: "{{ alloy_registry_endpoint }}/{{ alloy_image_name }}:{{ alloy_image_tag }}"
    # Sets the Grafana image tag.
    alloy_image_tag: v1.15.0
    # Port Alloy's HTTP server listens on.
    alloy_http_port: 12345
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Directory for Alloy data and state files on the remote host.
    alloy_remote_data_dir: "{{ remote_data_dir }}"
    # Docker-compatible API endpoint Alloy uses for container log discovery. Use `unix:///var/run/docker.sock` for a mounted socket or `tcp://host:port` for a TCP endpoint.
    alloy_docker_host: "unix:///var/run/docker.sock"
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: container/start
```

### container/rm

> Remove Alloy container

Removes the Alloy container via hyperledger.fabricx.container.

```yaml
- name: Remove Alloy container
  vars:
    # Name of the Alloy container.
    alloy_container_name: alloy
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: container/rm
```

### data/rm

> Remove Alloy data directory

Deletes the Alloy data directory from the remote host.

```yaml
- name: Remove Alloy data directory
  vars:
    # Directory for Alloy data and state files on the remote host.
    alloy_remote_data_dir: "{{ remote_data_dir }}"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: data/rm
```

### config/rm

> Remove Alloy configuration directory

Deletes the Alloy configuration directory from the remote host.

```yaml
- name: Remove Alloy configuration directory
  vars:
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: config/rm
```

### k8s/start

> Deploy Alloy on Kubernetes

Creates RBAC, ConfigMap, Deployment, and Service for Alloy on Kubernetes. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Alloy on Kubernetes
  vars:
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Alloy resources.
    alloy_k8s_part_of: monitoring
    # Seconds to wait for the Alloy Deployment to become Available on Kubernetes.
    alloy_k8s_wait_timeout: 120
    # Filesystem group used by the Alloy pod security context for writable mounted volumes.
    alloy_k8s_fs_group: 1000
    # Sets the Grafana image reference.
    alloy_image: "{{ alloy_registry_endpoint }}/{{ alloy_image_name }}:{{ alloy_image_tag }}"
    # Sets the Grafana image tag.
    alloy_image_tag: v1.15.0
    # Port Alloy's HTTP server listens on.
    alloy_http_port: 12345
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Name of the image pull secret to attach to the Alloy Kubernetes ServiceAccount/Deployment.
    k8s_image_pull_secret: "string"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/start
```

### k8s/rm

> Remove Alloy Kubernetes workload

Deletes the Alloy Deployment, Service, ConfigMap, and RBAC resources from Kubernetes. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Alloy Kubernetes workload
  vars:
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Use cluster-scoped RBAC for Alloy pod discovery. Set to `false` when Alloy only collects logs from `alloy_k8s_namespaces` and the deployment user cannot create ClusterRoles.
    alloy_k8s_cluster_scope: true
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/rm
```

### k8s/config/transfer

> Apply Alloy RBAC and ConfigMap

Applies Alloy's RBAC (cluster- or namespace-scoped) and ConfigMap on Kubernetes/OpenShift.

```yaml
- name: Apply Alloy RBAC and ConfigMap
  vars:
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Alloy resources.
    alloy_k8s_part_of: monitoring
    # Use cluster-scoped RBAC for Alloy pod discovery. Set to `false` when Alloy only collects logs from `alloy_k8s_namespaces` and the deployment user cannot create ClusterRoles.
    alloy_k8s_cluster_scope: true
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove Alloy RBAC and ConfigMap

Deletes Alloy's ConfigMap and RBAC (cluster- or namespace-scoped) from Kubernetes/OpenShift.

```yaml
- name: Remove Alloy RBAC and ConfigMap
  vars:
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Use cluster-scoped RBAC for Alloy pod discovery. Set to `false` when Alloy only collects logs from `alloy_k8s_namespaces` and the deployment user cannot create ClusterRoles.
    alloy_k8s_cluster_scope: true
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/config/rm
```

### openshift/start

> Deploy Alloy on OpenShift

Delegates to k8s/start against an OpenShift-authenticated client context. Optionally exposes Alloy's HTTP endpoint via an OpenShift Route when `alloy_openshift_route` is set. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Alloy on OpenShift
  vars:
    # Hostname for the OpenShift Route exposing Alloy's HTTP endpoint. When omitted, no Route is created.
    alloy_openshift_route: "string"
    # Enable TLS termination on the Alloy OpenShift Route.
    alloy_use_tls: false
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Alloy resources.
    alloy_k8s_part_of: monitoring
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: openshift/start
```

### openshift/rm

> Remove Alloy OpenShift workload

Deletes the Alloy OpenShift Route (if configured), then delegates to k8s/rm. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Alloy OpenShift workload
  vars:
    # Hostname for the OpenShift Route exposing Alloy's HTTP endpoint. When omitted, no Route is created.
    alloy_openshift_route: "string"
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: openshift/rm
```

### config/transfer

> Transfer Alloy configuration

Renders and uploads the Alloy River configuration file to the remote host.

```yaml
- name: Transfer Alloy configuration
  vars:
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Directory for Alloy data and state files on the remote host.
    alloy_remote_data_dir: "{{ remote_data_dir }}"
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Labels attached to every log line collected by this Alloy instance.
    alloy_default_labels:
      host: "{{ ansible_host }}"
    # Extra file paths (glob patterns accepted) to tail in addition to the defaults. Example: `['/var/log/app/*.log']`
    alloy_extra_log_paths:
      - "/var/log/app/*.log"
    # Docker-compatible API endpoint Alloy uses for container log discovery. Use `unix:///var/run/docker.sock` for a mounted socket or `tcp://host:port` for a TCP endpoint.
    alloy_docker_host: "unix:///var/run/docker.sock"
    # Regex matching Docker container names to exclude from log collection.
    alloy_docker_exclude_container_regex: ""
    # Enable collection of systemd journal logs.
    alloy_journal_logs_enabled: false
    # JSON fields to promote to Loki stream labels. Avoid high-cardinality fields such as txn_id or duration_ms.
    alloy_json_label_fields:
      - level
      - component
    # Optional Kubernetes namespaces Alloy should discover pod logs from. When omitted, Alloy discovers pods from all namespaces its service account can read.
    alloy_k8s_namespaces: ["entry1", "entry2"]
    # Optional regex used to keep only pods whose `app.kubernetes.io/part-of` label matches. Useful when the target namespace contains unrelated workloads.
    alloy_k8s_keep_part_of_regex: "string"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: config/transfer
```
