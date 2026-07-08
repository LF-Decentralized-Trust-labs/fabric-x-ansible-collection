# hyperledger.fabricx.loki

> Deploys Grafana Loki for log aggregation. Supports container (local/dev), Kubernetes, and OpenShift deployment modes with filesystem and PVC storage backends.


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [data/rm](#datarm)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [k8s/start](#k8sstart)
  - [k8s/rm](#k8srm)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/data/rm](#k8sdatarm)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.loki
```

## Tasks

### start

> Start Loki

Dispatches to container/start, k8s/start, or openshift/start based on deployment mode flags.

```yaml
- name: Start Loki
  vars:
    # Deploy Loki as a local container. Automatically true when neither loki_use_k8s nor loki_use_openshift is set.
    loki_use_container: "{{ (not loki_use_k8s) and (not loki_use_openshift) }}"
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: start
```

### stop

> Stop Loki

Stops the Loki container. No-op for Kubernetes/OpenShift deployments.

```yaml
- name: Stop Loki
  vars:
    # Deploy Loki as a local container. Automatically true when neither loki_use_k8s nor loki_use_openshift is set.
    loki_use_container: "{{ (not loki_use_k8s) and (not loki_use_openshift) }}"
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: stop
```

### teardown

> Teardown Loki

Removes the Loki container, Kubernetes/OpenShift workload, and data directory.

```yaml
- name: Teardown Loki
  vars:
    # Deploy Loki as a local container. Automatically true when neither loki_use_k8s nor loki_use_openshift is set.
    loki_use_container: "{{ (not loki_use_k8s) and (not loki_use_openshift) }}"
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: teardown
```

### wipe

> Wipe Loki configuration

Removes the Loki configuration directory. Intended to be called explicitly, not as part of routine teardown.

```yaml
- name: Wipe Loki configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: wipe
```

### container/start

> Start Loki container

Creates the Loki data directory and starts the Loki container via hyperledger.fabricx.container.

```yaml
- name: Start Loki container
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Container image name for Grafana Loki.
    loki_image: grafana/loki
    # Image tag for Grafana Loki. Example: `3.4.2`
    loki_version: 3.4.2
    # Port Loki listens on.
    loki_port: 3100
    # Directory for Loki configuration files on the remote host.
    loki_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Directory for Loki data on the remote host.
    loki_data_dir: "{{ remote_deploy_dir }}/loki/data"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: container/start
```

### container/stop

> Stop Loki container

Stops the Loki container via hyperledger.fabricx.container.

```yaml
- name: Stop Loki container
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Deploy Loki as a local container. Automatically true when neither loki_use_k8s nor loki_use_openshift is set.
    loki_use_container: "{{ (not loki_use_k8s) and (not loki_use_openshift) }}"
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: container/stop
```

### container/rm

> Remove Loki container

Removes the Loki container via hyperledger.fabricx.container.

```yaml
- name: Remove Loki container
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Deploy Loki as a local container. Automatically true when neither loki_use_k8s nor loki_use_openshift is set.
    loki_use_container: "{{ (not loki_use_k8s) and (not loki_use_openshift) }}"
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: container/rm
```

### data/rm

> Remove Loki data directory

Deletes the Loki data directory from the remote host.

```yaml
- name: Remove Loki data directory
  vars:
    # Directory for Loki data on the remote host.
    loki_data_dir: "{{ remote_deploy_dir }}/loki/data"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: data/rm
```

### config/transfer

> Transfer Loki configuration

Renders and uploads the Loki config file to the remote host.

```yaml
- name: Transfer Loki configuration
  vars:
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Directory for Loki configuration files on the remote host.
    loki_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Port Loki listens on.
    loki_port: 3100
    # Log retention period. Default is 31 days. Example: `744h`
    loki_retention_period: 744h
    # Maximum ingestion rate in MB/s per distributor.
    loki_ingestion_rate_mb: 16
    # Maximum ingestion burst size in MB per distributor.
    loki_ingestion_burst_size_mb: 32
    # Replication factor. Use 1 for single-node/dev; 2+ for HA.
    loki_replication_factor: 1
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: config/transfer
```

### config/rm

> Remove Loki configuration directory

Deletes the Loki configuration directory from the remote host.

```yaml
- name: Remove Loki configuration directory
  vars:
    # Directory for Loki configuration files on the remote host.
    loki_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: config/rm
```

### k8s/start

> Deploy Loki on Kubernetes

Applies the ConfigMap, a headless Service, and a StatefulSet (with a PVC via volumeClaimTemplates) for Loki on Kubernetes. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Loki on Kubernetes
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Port Loki listens on.
    loki_port: 3100
    # Seconds to wait for the Loki StatefulSet to become ready on Kubernetes/OpenShift.
    loki_k8s_wait_timeout: 120
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/start
```

### k8s/rm

> Remove Loki Kubernetes workload

Deletes the Loki StatefulSet, Service, and ConfigMap from Kubernetes. When `loki_wipe` is true, also deletes the underlying PersistentVolumeClaim. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Loki Kubernetes workload
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # When true, also removes the Loki PersistentVolumeClaim during k8s/rm.
    loki_wipe: false
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/rm
```

### k8s/config/transfer

> Apply Loki ConfigMap

Applies the Loki ConfigMap on Kubernetes/OpenShift.

```yaml
- name: Apply Loki ConfigMap
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Directory for Loki configuration files on the remote host.
    loki_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove Loki ConfigMap

Deletes the Loki ConfigMap from Kubernetes/OpenShift.

```yaml
- name: Remove Loki ConfigMap
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/config/rm
```

### k8s/data/rm

> Remove Loki PersistentVolumeClaim

Deletes the Loki PersistentVolumeClaim from Kubernetes/OpenShift.

```yaml
- name: Remove Loki PersistentVolumeClaim
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/data/rm
```

### openshift/start

> Deploy Loki on OpenShift

Delegates to k8s/start against an OpenShift-authenticated client context. Optionally exposes Loki's HTTP endpoint via an OpenShift Route when `loki_openshift_route` is set. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Loki on OpenShift
  vars:
    # Hostname for the OpenShift Route exposing Loki's HTTP endpoint. When omitted, no Route is created.
    loki_openshift_route: "string"
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
    # Name of the Loki container.
    loki_container_name: loki
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: openshift/start
```

### openshift/rm

> Remove Loki OpenShift workload

Deletes the Loki OpenShift Route (if configured), then delegates to k8s/rm. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Loki OpenShift workload
  vars:
    # Hostname for the OpenShift Route exposing Loki's HTTP endpoint. When omitted, no Route is created.
    loki_openshift_route: "string"
    # Name of the Loki container.
    loki_container_name: loki
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: openshift/rm
```
