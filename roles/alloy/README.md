# hyperledger.fabricx.alloy

> Deploys Grafana Alloy — the strategic successor to Promtail and Grafana Agent. Supports container, Kubernetes, and OpenShift deployment modes. Collects logs from containers, systemd journal, and arbitrary log files; parses JSON; and ships to Grafana Loki.


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [k8s/start](#k8sstart)
  - [k8s/rm](#k8srm)
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
    # Name of the Alloy container.
    alloy_container_name: alloy
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Container image name for Grafana Alloy.
    alloy_image: grafana/alloy
    # Image tag for Grafana Alloy. Example: `v1.15.0`
    alloy_version: v1.15.0
    # Port Alloy's HTTP server listens on.
    alloy_http_port: 12345
    # Directory for Alloy configuration files on the remote host.
    alloy_config_dir: "{{ remote_deploy_dir }}/alloy/config"
    # Directory for Alloy data and state files on the remote host. Mounted into the container at `/var/lib/alloy`.
    alloy_data_dir: "{{ remote_deploy_dir }}/alloy/data"
    # Path to the container runtime socket mounted into Alloy. Required when `alloy_docker_logs_enabled` is true and `alloy_docker_host` uses a Unix socket.
    alloy_docker_socket: "string"
    # Docker-compatible API endpoint Alloy uses for container log discovery. Use `unix:///var/run/docker.sock` for a mounted socket or `tcp://host:port` for a TCP endpoint.
    alloy_docker_host: "unix:///var/run/docker.sock"
    # Enable collection of container logs via the Docker/Podman socket.
    alloy_docker_logs_enabled: true
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
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

Removes the Alloy container and configuration directory.

```yaml
- name: Teardown Alloy
  vars:
    # Name of the Alloy container.
    alloy_container_name: alloy
    # Directory for Alloy configuration files on the remote host.
    alloy_config_dir: "{{ remote_deploy_dir }}/alloy/config"
    # Directory for Alloy data and state files on the remote host. Mounted into the container at `/var/lib/alloy`.
    alloy_data_dir: "{{ remote_deploy_dir }}/alloy/data"
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
    tasks_from: teardown
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
    # Use cluster-scoped RBAC for Alloy pod discovery. Set to `false` when Alloy only collects logs from `alloy_k8s_namespaces` and the deployment user cannot create ClusterRoles.
    alloy_k8s_cluster_scope: true
    # Container image name for Grafana Alloy.
    alloy_image: grafana/alloy
    # Image tag for Grafana Alloy. Example: `v1.15.0`
    alloy_version: v1.15.0
    # Port Alloy's HTTP server listens on.
    alloy_http_port: 12345
    # Directory for Alloy configuration files on the remote host.
    alloy_config_dir: "{{ remote_deploy_dir }}/alloy/config"
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

### openshift/start

> Deploy Alloy on OpenShift

Delegates to k8s/start against an OpenShift-authenticated client context. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Alloy on OpenShift
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: openshift/start
```

### openshift/rm

> Remove Alloy OpenShift workload

Delegates to k8s/rm against an OpenShift-authenticated client context. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Alloy OpenShift workload
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
    alloy_config_dir: "{{ remote_deploy_dir }}/alloy/config"
    # Directory for Alloy data and state files on the remote host. Mounted into the container at `/var/lib/alloy`.
    alloy_data_dir: "{{ remote_deploy_dir }}/alloy/data"
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Full push URL for the Loki instance.
    alloy_loki_url: "string"
    # Labels attached to every log line collected by this Alloy instance.
    alloy_default_labels:
      platform: cbdc
    # Extra file paths (glob patterns accepted) to tail in addition to the defaults. Example: `[/var/log/app/*.log]`
    alloy_extra_log_paths:

    # Enable collection of container logs via the Docker/Podman socket.
    alloy_docker_logs_enabled: true
    # Docker-compatible API endpoint Alloy uses for container log discovery. Use `unix:///var/run/docker.sock` for a mounted socket or `tcp://host:port` for a TCP endpoint.
    alloy_docker_host: "unix:///var/run/docker.sock"
    # Path to the container runtime socket mounted into Alloy. Required when `alloy_docker_logs_enabled` is true and `alloy_docker_host` uses a Unix socket.
    alloy_docker_socket: "string"
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
