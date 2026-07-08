# hyperledger.fabricx.loki

> Deploys Grafana Loki for log aggregation. Supports container (local/dev), Kubernetes, and OpenShift deployment modes with filesystem and PVC storage backends.


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [container/start](#containerstart)
  - [k8s/start](#k8sstart)
  - [k8s/rm](#k8srm)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)
  - [config/transfer](#configtransfer)
  - [config/transfer\_grafana\_datasource](#configtransfer_grafana_datasource)

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
    tasks_from: stop
```

### teardown

> Teardown Loki

Removes the Loki workload and all config/data directories.

```yaml
- name: Teardown Loki
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Directory for Loki configuration files on the remote host.
    loki_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Directory for Loki data on the remote host.
    loki_data_dir: "{{ remote_deploy_dir }}/loki/data"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
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

### container/start

> Start Loki container

Starts the Loki container via hyperledger.fabricx.container.

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

### k8s/start

> Deploy Loki on Kubernetes

Creates PVC, ConfigMap, Deployment, and Service for Loki on Kubernetes. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Loki on Kubernetes
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Container image name for Grafana Loki.
    loki_image: grafana/loki
    # Image tag for Grafana Loki. Example: `3.4.2`
    loki_version: 3.4.2
    # Port Loki listens on.
    loki_port: 3100
    # PersistentVolumeClaim size for Loki storage on Kubernetes/OpenShift.
    loki_pvc_size: 50Gi
    # StorageClass name for the Loki PVC. Leave empty to use the cluster default. Example: `ibmc-file`
    loki_storage_class: ""
    # Seconds to wait for the Loki Deployment to become Available on Kubernetes/OpenShift.
    loki_k8s_wait_timeout: 120
    # Directory for Loki configuration files on the remote host.
    loki_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/start
```

### k8s/rm

> Remove Loki Kubernetes workload

Deletes the Loki Deployment, Service, ConfigMap, and PVC from Kubernetes. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Loki Kubernetes workload
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/rm
```

### openshift/start

> Deploy Loki on OpenShift

Creates PVC, ConfigMap, Deployment, and Service for Loki on OpenShift. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Deploy Loki on OpenShift
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Container image name for Grafana Loki.
    loki_image: grafana/loki
    # Image tag for Grafana Loki. Example: `3.4.2`
    loki_version: 3.4.2
    # Port Loki listens on.
    loki_port: 3100
    # PersistentVolumeClaim size for Loki storage on Kubernetes/OpenShift.
    loki_pvc_size: 50Gi
    # StorageClass name for the Loki PVC. Leave empty to use the cluster default. Example: `ibmc-file`
    loki_storage_class: ""
    # Seconds to wait for the Loki Deployment to become Available on Kubernetes/OpenShift.
    loki_k8s_wait_timeout: 120
    # Filesystem group used by the Loki pod security context for writable mounted volumes.
    loki_k8s_fs_group: 10001
    # Directory for Loki configuration files on the remote host.
    loki_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Path to the kubeconfig file used to authenticate to the OpenShift cluster.
    loki_kubeconfig: "string"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: openshift/start
```

### openshift/rm

> Remove Loki OpenShift workload

Deletes the Loki Deployment, Service, ConfigMap, and PVC from OpenShift. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Loki OpenShift workload
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: openshift/rm
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
    # Directory for Loki data on the remote host.
    loki_data_dir: "{{ remote_deploy_dir }}/loki/data"
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

### config/transfer_grafana_datasource

> Transfer Loki Grafana datasource

Drops a Loki datasource provisioning file into Grafana's datasources directory.

```yaml
- name: Transfer Loki Grafana datasource
  vars:
    # Filename for the provisioned Loki datasource dropped into Grafana's datasources directory.
    grafana_datasource_file: "string"
    # Kubernetes resource name of the Grafana Deployment/ConfigMap, used when provisioning the datasource via the API/ConfigMap instead of a local file.
    grafana_k8s_resource_name: "string"
    # Directory on the remote host where Grafana provisioning files are read from.
    grafana_remote_config_dir: "string"
    # Whether the target Grafana instance is deployed on Kubernetes.
    grafana_use_k8s: false
    # Whether the target Grafana instance is deployed on OpenShift.
    grafana_use_openshift: false
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: config/transfer_grafana_datasource
```
