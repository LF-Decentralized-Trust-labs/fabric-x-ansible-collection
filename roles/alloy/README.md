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
  - [k8s/data/rm](#k8sdatarm)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)
  - [config/transfer](#configtransfer)
  - [crypto/setup](#cryptosetup)
  - [crypto/openssl/generate\_cert](#cryptoopensslgenerate_cert)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [k8s/crypto/rm](#k8scryptorm)

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
    alloy_port: 12345
    # Sets the Grafana image registry endpoint.
    alloy_registry_endpoint: "{{ lookup('env', 'ALLOY_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana image name.
    alloy_image_name: alloy
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Directory for Alloy configuration files within the container.
    alloy_container_config_dir: /etc/alloy
    # Directory for Alloy data and state files on the remote host.
    alloy_remote_data_dir: "{{ remote_data_dir }}"
    # Directory for Alloy data and state files within the container.
    alloy_container_data_dir: /var/lib/alloy
    # Docker-compatible API endpoint Alloy uses for container log discovery. Use `unix:///var/run/docker.sock` for a mounted socket or `tcp://host:port` for a TCP endpoint.
    alloy_docker_host: "unix:///var/run/docker.sock"
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
    # Remote data directory consumed by `alloy_remote_data_dir`.
    remote_data_dir: "string"
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

> Remove Alloy data

Deletes Alloy data from the active deployment mode.

```yaml
- name: Remove Alloy data
  vars:
    # Directory for Alloy data and state files on the remote host.
    alloy_remote_data_dir: "{{ remote_data_dir }}"
    # Deploy Alloy as a local container. Automatically true when neither `alloy_use_k8s` nor `alloy_use_openshift` is set.
    alloy_use_container: "{{ (not alloy_use_k8s) and (not alloy_use_openshift) }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Remote data directory consumed by `alloy_remote_data_dir`.
    remote_data_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: data/rm
```

### config/rm

> Remove Alloy configuration

Deletes the Alloy configuration directory from the remote host and, in Kubernetes/OpenShift mode, the Alloy ConfigMap.

```yaml
- name: Remove Alloy configuration
  vars:
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: config/rm
```

### k8s/start

> Deploy Alloy on Kubernetes

Creates RBAC, ConfigMap, headless Service, and StatefulSet (with a PVC via volumeClaimTemplates) for Alloy on Kubernetes. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Alloy on Kubernetes
  vars:
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Alloy resources.
    alloy_k8s_part_of: monitoring
    # Seconds to wait for the Alloy StatefulSet to become ready on Kubernetes.
    alloy_k8s_wait_timeout: 120
    # Filesystem group used by the Alloy pod security context for writable mounted volumes.
    alloy_k8s_fs_group: 1000
    # Kubernetes NodePort value used by the external Alloy HTTP Service port. Defining this variable enables the NodePort Service.
    alloy_k8s_node_port: 1000
    # Set to `true` to create a LoadBalancer Service entry that exposes the Alloy HTTP port externally.
    alloy_k8s_loadbalancer_expose_port: false
    # Sets the Grafana image registry endpoint.
    alloy_registry_endpoint: "{{ lookup('env', 'ALLOY_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana image name.
    alloy_image_name: alloy
    # Sets the Grafana image reference.
    alloy_image: "{{ alloy_registry_endpoint }}/{{ alloy_image_name }}:{{ alloy_image_tag }}"
    # Sets the Grafana image tag.
    alloy_image_tag: v1.15.0
    # Port Alloy's HTTP server listens on.
    alloy_port: 12345
    # Enable HTTPS for Alloy's HTTP endpoint and TLS-aware Kubernetes/OpenShift probes.
    alloy_use_tls: false
    # Filename used for the Alloy TLS private key.
    alloy_tls_private_key_file: server.key
    # Filename used for the Alloy TLS certificate.
    alloy_tls_cert_file: server.crt
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Directory for Alloy configuration files within the container.
    alloy_container_config_dir: /etc/alloy
    # Directory for Alloy data and state files within the container.
    alloy_container_data_dir: /var/lib/alloy
    # Inventory host name of the Loki instance Alloy forwards logs to.
    loki_host: "string"
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Persistent volume size requested for Alloy's data volume (WAL, positions file). Example: `1Gi`.
    k8s_storage_size: "1Gi"
    # Optional Kubernetes storage class name for the Alloy PVC. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Name of the image pull secret to attach to the Alloy Kubernetes ServiceAccount/StatefulSet.
    k8s_image_pull_secret: "string"
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/start
```

### k8s/rm

> Remove Alloy Kubernetes workload

Deletes the Alloy StatefulSet, Service, ConfigMap, and RBAC resources from Kubernetes. Does not delete the underlying PersistentVolumeClaim; see `k8s/data/rm`. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Alloy Kubernetes workload
  vars:
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes NodePort value used by the external Alloy HTTP Service port. Defining this variable enables the NodePort Service.
    alloy_k8s_node_port: 1000
    # Set to `true` to create a LoadBalancer Service entry that exposes the Alloy HTTP port externally.
    alloy_k8s_loadbalancer_expose_port: false
    # Use cluster-scoped RBAC for Alloy pod discovery. Set to `false` when Alloy only collects logs from `alloy_k8s_namespaces` and the deployment user cannot create ClusterRoles.
    alloy_k8s_cluster_scope: true
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/rm
```

### k8s/data/rm

> Remove the Alloy data PVC

Deletes the PersistentVolumeClaim created for the Alloy StatefulSet.

```yaml
- name: Remove the Alloy data PVC
  vars:
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/data/rm
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
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
    # Inventory host name of the Loki instance Alloy forwards logs to.
    loki_host: "string"
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
    # Enable HTTPS for Alloy's HTTP endpoint and TLS-aware Kubernetes/OpenShift probes.
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

Renders and uploads the Alloy River configuration file to the remote host. Applies the Kubernetes ConfigMap when Kubernetes/OpenShift mode is enabled.

```yaml
- name: Transfer Alloy configuration
  vars:
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Directory for Alloy configuration files within the container.
    alloy_container_config_dir: /etc/alloy
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
    # Enable HTTPS for Alloy's HTTP endpoint and TLS-aware Kubernetes/OpenShift probes.
    alloy_use_tls: false
    # Filename used for the Alloy TLS private key.
    alloy_tls_private_key_file: server.key
    # Filename used for the Alloy TLS certificate.
    alloy_tls_cert_file: server.crt
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
    # Inventory host name of the Loki instance Alloy forwards logs to.
    loki_host: "string"
    # Control-node directory where fetched TLS artifacts are written and read.
    fetched_artifacts_dir: "string"
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: config/transfer
```

### crypto/setup

> Generate Alloy TLS materials

Generates TLS assets for Alloy and applies the Kubernetes Secret when Kubernetes/OpenShift mode is enabled.

```yaml
- name: Generate Alloy TLS materials
  vars:
    # Enable HTTPS for Alloy's HTTP endpoint and TLS-aware Kubernetes/OpenShift probes.
    alloy_use_tls: false
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: crypto/setup
```

### crypto/openssl/generate_cert

> Generate a self-signed TLS certificate for Alloy

Delegates certificate creation to the shared OpenSSL role using Alloy-specific output paths.

```yaml
- name: Generate a self-signed TLS certificate for Alloy
  vars:
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
    # Optional certificate organization data forwarded to OpenSSL.
    organization: {}
    # Filename used for the Alloy TLS private key.
    alloy_tls_private_key_file: server.key
    # Filename used for the Alloy TLS certificate.
    alloy_tls_cert_file: server.crt
    # Hostname for the OpenShift Route exposing Alloy's HTTP endpoint. When omitted, no Route is created.
    alloy_openshift_route: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: crypto/openssl/generate_cert
```

### k8s/crypto/transfer

> Apply the Alloy TLS Secret on Kubernetes

Creates or updates the Kubernetes Secret that stores the Alloy TLS server keypair.

```yaml
- name: Apply the Alloy TLS Secret on Kubernetes
  vars:
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
    # Filename used for the Alloy TLS private key.
    alloy_tls_private_key_file: server.key
    # Filename used for the Alloy TLS certificate.
    alloy_tls_cert_file: server.crt
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Alloy resources.
    alloy_k8s_part_of: monitoring
    # Enable HTTPS for Alloy's HTTP endpoint and TLS-aware Kubernetes/OpenShift probes.
    alloy_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/crypto/transfer
```

### crypto/fetch

> Fetch Alloy TLS certificates

Fetches the generated Alloy TLS certificate material to the control node.

```yaml
- name: Fetch Alloy TLS certificates
  vars:
    # Control-node directory where fetched TLS artifacts are written and read.
    fetched_artifacts_dir: "string"
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
    # Filename used for the Alloy TLS certificate.
    alloy_tls_cert_file: server.crt
    # Enable HTTPS for Alloy's HTTP endpoint and TLS-aware Kubernetes/OpenShift probes.
    alloy_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove Alloy TLS materials

Deletes the Alloy TLS directory and removes the Kubernetes Secret when Kubernetes/OpenShift mode is enabled.

```yaml
- name: Remove Alloy TLS materials
  vars:
    # Directory for Alloy configuration files on the remote host.
    alloy_remote_config_dir: "{{ remote_config_dir }}"
    # Remote configuration directory consumed by `alloy_remote_config_dir`.
    remote_config_dir: "string"
    # Enable HTTPS for Alloy's HTTP endpoint and TLS-aware Kubernetes/OpenShift probes.
    alloy_use_tls: false
    # Deploy Alloy on Kubernetes.
    alloy_use_k8s: false
    # Deploy Alloy on OpenShift.
    alloy_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: crypto/rm
```

### k8s/crypto/rm

> Remove the Alloy TLS Secret

Deletes the Kubernetes Secret that stores the Alloy TLS server keypair.

```yaml
- name: Remove the Alloy TLS Secret
  vars:
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Base Kubernetes resource name for Alloy.
    alloy_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.alloy
    tasks_from: k8s/crypto/rm
```
