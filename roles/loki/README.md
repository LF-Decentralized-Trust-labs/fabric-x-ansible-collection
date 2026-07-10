# hyperledger.fabricx.loki

> Ansible role to deploy and configure Loki, a log aggregation system.

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
    # Sets the Grafana Loki image registry endpoint.
    loki_registry_endpoint: "{{ lookup('env', 'LOKI_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana Loki image name.
    loki_image_name: loki
    # Sets the Grafana Loki image tag. Example: `3.4.2`
    loki_image_tag: 3.4.2
    # Sets the Grafana Loki image reference.
    loki_image: "{{ loki_registry_endpoint }}/{{ loki_image_name }}:{{ loki_image_tag }}"
    # Port Loki listens on. Example: `9200`.
    loki_port: 9200
    # gRPC port Loki listens on, used for the query/ingest API and inter-component RPC. Example: `9201`.
    loki_grpc_port: 9201
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Directory for Loki configuration files within the container.
    loki_container_config_dir: /etc/loki
    # Directory for Loki data on the remote host.
    loki_remote_data_dir: "{{ remote_deploy_dir }}/loki/data"
    # Directory for Loki data and state files within the container.
    loki_container_data_dir: /loki
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
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

> Remove Loki data

Deletes the Loki data directory from the remote host and, in Kubernetes/OpenShift mode, the Loki PersistentVolumeClaim.

```yaml
- name: Remove Loki data
  vars:
    # Directory for Loki data on the remote host.
    loki_remote_data_dir: "{{ remote_deploy_dir }}/loki/data"
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: data/rm
```

### config/transfer

> Transfer Loki configuration

Renders and uploads the Loki config file to the remote host. Applies the Kubernetes ConfigMap when Kubernetes/OpenShift mode is enabled.

```yaml
- name: Transfer Loki configuration
  vars:
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Directory for Loki configuration files within the container.
    loki_container_config_dir: /etc/loki
    # Directory for Loki data and state files within the container.
    loki_container_data_dir: /loki
    # Port Loki listens on. Example: `9200`.
    loki_port: 9200
    # gRPC port Loki listens on, used for the query/ingest API and inter-component RPC. Example: `9201`.
    loki_grpc_port: 9201
    # Address this Loki node advertises to peers in its hash ring. Cosmetic for the single-node inmemory ring; set to a routable address for multi-node HA.
    loki_instance_addr: "{{ ansible_host }}"
    # Log retention period. Default is 31 days. Example: `744h`
    loki_retention_period: 744h
    # Maximum ingestion rate in MB/s per distributor.
    loki_ingestion_rate_mb: 16
    # Maximum ingestion burst size in MB per distributor.
    loki_ingestion_burst_size_mb: 32
    # Replication factor. Use 1 for single-node/dev; 2+ for HA.
    loki_replication_factor: 1
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
    # Filename used for the Loki TLS private key.
    loki_tls_private_key_file: server.key
    # Filename used for the Loki TLS certificate.
    loki_tls_cert_file: server.crt
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: config/transfer
```

### config/rm

> Remove Loki configuration

Deletes the Loki configuration directory from the remote host and, in Kubernetes/OpenShift mode, the Loki ConfigMap.

```yaml
- name: Remove Loki configuration
  vars:
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
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
    # Sets the Grafana Loki image registry endpoint.
    loki_registry_endpoint: "{{ lookup('env', 'LOKI_REGISTRY_ENDPOINT') or 'docker.io/grafana' }}"
    # Sets the Grafana Loki image name.
    loki_image_name: loki
    # Sets the Grafana Loki image tag. Example: `3.4.2`
    loki_image_tag: 3.4.2
    # Sets the Grafana Loki image reference.
    loki_image: "{{ loki_registry_endpoint }}/{{ loki_image_name }}:{{ loki_image_tag }}"
    # Port Loki listens on. Example: `9200`.
    loki_port: 9200
    # gRPC port Loki listens on, used for the query/ingest API and inter-component RPC. Example: `9201`.
    loki_grpc_port: 9201
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Loki resources.
    loki_k8s_part_of: monitoring
    # Kubernetes NodePort value used by the external Loki HTTP Service port. Defining this variable enables the NodePort Service.
    loki_k8s_node_port: 1000
    # Set to `true` to create a LoadBalancer Service entry that exposes the Loki HTTP port externally.
    loki_k8s_loadbalancer_expose_port: false
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
    # Directory for Loki configuration files within the container.
    loki_container_config_dir: /etc/loki
    # Directory for Loki data and state files within the container.
    loki_container_data_dir: /loki
    # Seconds to wait for the Loki StatefulSet to become ready on Kubernetes/OpenShift.
    loki_k8s_wait_timeout: 120
    # Filesystem group used by the Loki pod security context for writable mounted volumes.
    loki_k8s_fs_group: 10001
    # Requested storage size for the Loki StatefulSet's volumeClaimTemplate on Kubernetes/OpenShift.
    loki_pvc_size: 50Gi
    # StorageClass name for the Loki volumeClaimTemplate. Leave empty to use the cluster default. Example: `ibmc-file`
    loki_storage_class: ""
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Name of the image pull secret to attach to the Loki Kubernetes StatefulSet.
    k8s_image_pull_secret: "string"
    # Readiness probe initial delay for the Loki StatefulSet. Defaults to 30 when omitted.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Readiness probe period for the Loki StatefulSet. Defaults to 10 when omitted.
    k8s_readiness_probe_period_seconds: 1000
    # Liveness probe initial delay for the Loki StatefulSet. Defaults to 60 when omitted.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Liveness probe period for the Loki StatefulSet. Defaults to 30 when omitted.
    k8s_liveness_probe_period_seconds: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/start
```

### k8s/rm

> Remove Loki Kubernetes workload

Deletes the Loki StatefulSet and Service from Kubernetes. Does not delete the ConfigMap or PersistentVolumeClaim; see `k8s/config/rm` and `k8s/data/rm`. Uses the shared `k8s_namespace` inventory variable for the target namespace.

```yaml
- name: Remove Loki Kubernetes workload
  vars:
    # Name of the Loki container.
    loki_container_name: loki
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
    # Kubernetes NodePort value used by the external Loki HTTP Service port. Defining this variable enables the NodePort Service.
    loki_k8s_node_port: 1000
    # Set to `true` to create a LoadBalancer Service entry that exposes the Loki HTTP port externally.
    loki_k8s_loadbalancer_expose_port: false
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
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Loki resources.
    loki_k8s_part_of: monitoring
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
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
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
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
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
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
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Loki resources.
    loki_k8s_part_of: monitoring
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
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: openshift/rm
```

### crypto/setup

> Generate Loki TLS materials

Generates TLS assets for Loki and applies the Kubernetes Secret when Kubernetes/OpenShift mode is enabled.

```yaml
- name: Generate Loki TLS materials
  vars:
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: crypto/setup
```

### crypto/openssl/generate_cert

> Generate a self-signed TLS certificate for Loki

Delegates certificate creation to the shared OpenSSL role using Loki-specific output paths.

```yaml
- name: Generate a self-signed TLS certificate for Loki
  vars:
    # Optional certificate organization data forwarded to OpenSSL.
    organization: {}
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Filename used for the Loki TLS private key.
    loki_tls_private_key_file: server.key
    # Filename used for the Loki TLS certificate.
    loki_tls_cert_file: server.crt
    # Hostname for the OpenShift Route exposing Loki's HTTP endpoint. When omitted, no Route is created.
    loki_openshift_route: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: crypto/openssl/generate_cert
```

### k8s/crypto/transfer

> Apply the Loki TLS Secret on Kubernetes

Creates or updates the Kubernetes Secret that stores the Loki TLS server keypair.

```yaml
- name: Apply the Loki TLS Secret on Kubernetes
  vars:
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Name of the Loki container.
    loki_container_name: loki
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Filename used for the Loki TLS private key.
    loki_tls_private_key_file: server.key
    # Filename used for the Loki TLS certificate.
    loki_tls_cert_file: server.crt
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
    # Value for the Kubernetes `app.kubernetes.io/part-of` label applied to Loki resources.
    loki_k8s_part_of: monitoring
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/crypto/transfer
```

### crypto/fetch

> Fetch Loki TLS certificates

Fetches the generated Loki TLS certificate material to the control node.

```yaml
- name: Fetch Loki TLS certificates
  vars:
    # Control-node directory where fetched Loki TLS artifacts are written.
    fetched_artifacts_dir: "string"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Filename used for the Loki TLS certificate.
    loki_tls_cert_file: server.crt
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove Loki TLS materials

Deletes the Loki TLS directory and removes the Kubernetes Secret when Kubernetes/OpenShift mode is enabled.

```yaml
- name: Remove Loki TLS materials
  vars:
    # Directory for Loki configuration files on the remote host.
    loki_remote_config_dir: "{{ remote_deploy_dir }}/loki/config"
    # Base deployment root directory on the remote host under which per-component config/data directories are created.
    remote_deploy_dir: "string"
    # Whether Loki serves HTTPS. Also controls the Loki Grafana datasource URL scheme and the OpenShift Route TLS setting.
    loki_use_tls: false
    # Deploy Loki on Kubernetes.
    loki_use_k8s: false
    # Deploy Loki on OpenShift.
    loki_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: crypto/rm
```

### k8s/crypto/rm

> Remove the Loki TLS Secret

Deletes the Kubernetes Secret that stores the Loki TLS server keypair.

```yaml
- name: Remove the Loki TLS Secret
  vars:
    # Target Kubernetes/OpenShift namespace for this host's resources.
    k8s_namespace: "string"
    # Name of the Loki container.
    loki_container_name: loki
    # Base Kubernetes resource name used for the Loki StatefulSet and Services.
    loki_k8s_resource_name: "{{ loki_container_name }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loki
    tasks_from: k8s/crypto/rm
```
