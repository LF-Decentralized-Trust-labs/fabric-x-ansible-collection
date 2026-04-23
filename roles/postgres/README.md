# hyperledger.fabricx.postgres

> Runs a PostgreSQL database instance as a container.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [ping](#ping)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [data/rm](#datarm)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch_logs](#containerfetch_logs)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch_logs](#k8sfetch_logs)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate_cert](#cryptoopensslgenerate_cert)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric_ca/enroll](#cryptofabric_caenroll)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/mtls/transfer](#configmtlstransfer)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### ping

Check PostgreSQL reachability

Validates that the PostgreSQL port is reachable on the target host.

In container mode, probes `postgres_port` directly.

In Kubernetes mode, delegates to the `k8s/ping` entry point which probes the NodePort when `postgres_k8s_use_node_port` is enabled and `postgres_k8s_port_node_port` is defined.

Also probes the postgres_exporter port when it is defined.

```yaml
- name: Check PostgreSQL reachability
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 1000
    # Optional postgres_exporter port to probe after PostgreSQL itself. This entry point only runs when the variable is defined.
    postgres_exporter_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: ping
```

### start

Start PostgreSQL

Starts PostgreSQL using the selected deployment mode.

The container mode is the default unless `postgres_use_k8s` or `postgres_use_openshift` is enabled.

When Kubernetes mode is selected, validates the Service and StatefulSet inputs, plus optional NodePort inputs used by the k8s startup path.

When OpenShift mode is selected, validates the Service and StatefulSet inputs required by the openshift startup path.

```yaml
- name: Start PostgreSQL
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`. The default derives from `postgres_use_k8s` and `postgres_use_openshift`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: start
```

### stop

Stop PostgreSQL

Stops PostgreSQL when it runs in container mode.

`postgres_use_container` defaults from `postgres_use_k8s` and `postgres_use_openshift`.

```yaml
- name: Stop PostgreSQL
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`. The default derives from `postgres_use_k8s` and `postgres_use_openshift`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: stop
```

### teardown

Remove PostgreSQL runtime resources

Removes PostgreSQL runtime resources for the selected deployment mode.

Persistent data is removed through the `data/rm` entry point.

```yaml
- name: Remove PostgreSQL runtime resources
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`. The default derives from `postgres_use_k8s` and `postgres_use_openshift`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: teardown
```

### wipe

Wipe PostgreSQL data and configuration

Removes PostgreSQL runtime resources, TLS materials, and configuration files.

This entry point sequences the teardown, crypto cleanup, and config cleanup flows.

```yaml
- name: Wipe PostgreSQL data and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: wipe
```

### fetch_logs

Fetch PostgreSQL logs

Collects PostgreSQL logs from the selected deployment mode.

Delegates to the container or Kubernetes log collection entry point.

```yaml
- name: Fetch PostgreSQL logs
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`. The default derives from `postgres_use_k8s` and `postgres_use_openshift`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: fetch_logs
```

### data/rm

Remove PostgreSQL data storage

Removes the PostgreSQL persistent data directory in container deployments.

Deletes the PostgreSQL PVC in Kubernetes and OpenShift deployments.

```yaml
- name: Remove PostgreSQL data storage
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`. The default derives from `postgres_use_k8s` and `postgres_use_openshift`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
    # Remote directory used for PostgreSQL persistent data. The default derives from `remote_data_dir`.
    postgres_remote_data_dir: "{{ remote_data_dir }}"
    # Outer remote data directory consumed by `postgres_remote_data_dir`. This dependency is validated wherever PostgreSQL persistent data is used.
    remote_data_dir: "string"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: data/rm
```

### container/start

Start PostgreSQL in a container

Creates the required data volume and starts the PostgreSQL container.

Configures TLS and mTLS command-line options when those features are enabled.

```yaml
- name: Start PostgreSQL in a container
  vars:
    # Container name for the PostgreSQL instance. The default derives from `inventory_hostname`.
    postgres_container_name: "{{ inventory_hostname }}"
    # Container registry endpoint used to build `postgres_image`. The default derives from `POSTGRES_REGISTRY_ENDPOINT` and falls back to `docker.io/library`.
    postgres_registry_endpoint: "{{ lookup('env', 'POSTGRES_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # PostgreSQL image repository name.
    postgres_image_name: postgres
    # PostgreSQL image tag.
    postgres_image_tag: 16.4
    # Full container image reference for PostgreSQL. The default derives from `postgres_registry_endpoint`, `postgres_image_name`, and `postgres_image_tag`.
    postgres_image: "{{ postgres_registry_endpoint }}/{{ postgres_image_name }}:{{ postgres_image_tag }}"
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Remote directory used for PostgreSQL persistent data. The default derives from `remote_data_dir`.
    postgres_remote_data_dir: "{{ remote_data_dir }}"
    # Outer remote data directory consumed by `postgres_remote_data_dir`. This dependency is validated wherever PostgreSQL persistent data is used.
    remote_data_dir: "string"
    # Configuration directory path inside the PostgreSQL container.
    postgres_container_config_dir: /var/lib/postgresql/config
    # Data directory path inside the PostgreSQL container.
    postgres_container_data_dir: /var/lib/postgresql/data
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "string"
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "string"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault.
    postgres_password: "string"
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 1000
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled.
    postgres_mtls_clients: ["entry1", "entry2"]
    # Additional PostgreSQL command-line options appended to the start command.
    postgres_extra_cmd_opts: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/start
```

### container/stop

Stop the PostgreSQL container

Stops the PostgreSQL container instance.

Uses the container helper role internally.

```yaml
- name: Stop the PostgreSQL container
  vars:
    # Container name for the PostgreSQL instance. The default derives from `inventory_hostname`.
    postgres_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/stop
```

### container/rm

Remove the PostgreSQL container

Removes the PostgreSQL container instance.

Container volumes are handled separately by the `data/rm` entry point.

```yaml
- name: Remove the PostgreSQL container
  vars:
    # Container name for the PostgreSQL instance. The default derives from `inventory_hostname`.
    postgres_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/rm
```

### container/fetch_logs

Fetch PostgreSQL container logs

Collects logs from the PostgreSQL container instance.

Uses the container helper role internally.

```yaml
- name: Fetch PostgreSQL container logs
  vars:
    # Container name for the PostgreSQL instance. The default derives from `inventory_hostname`.
    postgres_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/fetch_logs
```

### k8s/start

Start PostgreSQL on Kubernetes

Ensures the Kubernetes namespace exists and applies the PostgreSQL Service and StatefulSet resources.

Applies the optional NodePort Service when `postgres_k8s_use_node_port` is enabled.

Uses the role templates to configure storage, credentials, TLS, and optional mTLS mounts.

```yaml
- name: Start PostgreSQL on Kubernetes
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
    # Timeout in seconds while waiting for the StatefulSet rollout to complete.
    postgres_k8s_wait_timeout: 120
    # Kubernetes pod `fsGroup` applied so mounted files are readable by the postgres process.
    postgres_k8s_fs_group: 999
    # Enable the Kubernetes NodePort Service for PostgreSQL when set to `true`.
    postgres_k8s_use_node_port: false
    # Kubernetes NodePort value used by the external PostgreSQL Service. When undefined, the NodePort is allocated automatically by Kubernetes.
    postgres_k8s_port_node_port: 1000
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 1000
    # Container registry endpoint used to build `postgres_image`. The default derives from `POSTGRES_REGISTRY_ENDPOINT` and falls back to `docker.io/library`.
    postgres_registry_endpoint: "{{ lookup('env', 'POSTGRES_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # PostgreSQL image repository name.
    postgres_image_name: postgres
    # PostgreSQL image tag.
    postgres_image_tag: 16.4
    # Full container image reference for PostgreSQL. The default derives from `postgres_registry_endpoint`, `postgres_image_name`, and `postgres_image_tag`.
    postgres_image: "{{ postgres_registry_endpoint }}/{{ postgres_image_name }}:{{ postgres_image_tag }}"
    # Configuration directory path inside the PostgreSQL container.
    postgres_container_config_dir: /var/lib/postgresql/config
    # Data directory path inside the PostgreSQL container.
    postgres_container_data_dir: /var/lib/postgresql/data
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "string"
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "string"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault.
    postgres_password: "string"
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled.
    postgres_mtls_clients: ["entry1", "entry2"]
    # Additional PostgreSQL command-line options appended to the start command.
    postgres_extra_cmd_opts: "string"
    # Requested persistent storage size for the PostgreSQL PVC. Example: `500Mi`.
    k8s_storage_size: "string"
    # Kubernetes storage class name for the PostgreSQL PVC when a non-default class is required.
    k8s_storage_class: "string"
    # Existing Kubernetes `imagePullSecret` name used when the PostgreSQL image is stored in a private registry.
    k8s_image_pull_secret: "string"
    # Override for the readiness probe initial delay in seconds. The template default is `10`.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Override for the readiness probe period in seconds. The template default is `10`.
    k8s_readiness_probe_period_seconds: 1000
    # Override for the readiness probe timeout in seconds. The template default is `5`.
    k8s_readiness_probe_timeout_seconds: 1000
    # Override for the readiness probe failure threshold. The template default is `3`.
    k8s_readiness_probe_failure_threshold: 1000
    # Override for the liveness probe initial delay in seconds. The template default is `30`.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Override for the liveness probe period in seconds. The template default is `15`.
    k8s_liveness_probe_period_seconds: 1000
    # Override for the liveness probe timeout in seconds. The template default is `5`.
    k8s_liveness_probe_timeout_seconds: 1000
    # Override for the liveness probe failure threshold. The template default is `5`.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/start
```

### k8s/ping

Check PostgreSQL NodePort reachability on Kubernetes

Probes the PostgreSQL NodePort when `postgres_k8s_use_node_port` is enabled and `postgres_k8s_port_node_port` is defined.

This entry point is invoked internally by `ping` when PostgreSQL runs on Kubernetes.

```yaml
- name: Check PostgreSQL NodePort reachability on Kubernetes
  vars:
    # Enable the Kubernetes NodePort Service for PostgreSQL when set to `true`.
    postgres_k8s_use_node_port: false
    # Kubernetes NodePort value used by the external PostgreSQL Service. When undefined, the NodePort is allocated automatically by Kubernetes.
    postgres_k8s_port_node_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/ping
```

### k8s/rm

Remove PostgreSQL Kubernetes resources

Deletes the PostgreSQL StatefulSet, Service, and NodePort Service resources from Kubernetes.

The persistent volume claim is removed separately by the `data/rm` entry point.

```yaml
- name: Remove PostgreSQL Kubernetes resources
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/rm
```

### k8s/fetch_logs

Fetch PostgreSQL pod logs

Collects logs from the PostgreSQL pod in Kubernetes.

Selects pods using the PostgreSQL application label.

```yaml
- name: Fetch PostgreSQL pod logs
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/fetch_logs
```

### k8s/crypto/transfer

Apply the PostgreSQL Kubernetes Secret

Applies the Kubernetes Secret that stores PostgreSQL credentials and optional TLS materials.

Ensures the Kubernetes namespace exists before applying the Secret.

```yaml
- name: Apply the PostgreSQL Kubernetes Secret
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "string"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault.
    postgres_password: "string"
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "string"
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

Remove the PostgreSQL Kubernetes Secret

Deletes the Kubernetes Secret that stores PostgreSQL credentials and TLS materials.

This entry point is typically invoked from the PostgreSQL crypto cleanup workflow.

```yaml
- name: Remove the PostgreSQL Kubernetes Secret
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/crypto/rm
```

### k8s/config/transfer

Apply the PostgreSQL Kubernetes ConfigMap

Applies the Kubernetes ConfigMap that stores PostgreSQL mTLS configuration files.

Ensures the Kubernetes namespace exists before applying the ConfigMap.

```yaml
- name: Apply the PostgreSQL Kubernetes ConfigMap
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled.
    postgres_mtls_clients: ["entry1", "entry2"]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

Remove the PostgreSQL Kubernetes ConfigMap

Deletes the Kubernetes ConfigMap that stores PostgreSQL mTLS configuration.

This entry point is typically invoked from the PostgreSQL config cleanup workflow.

```yaml
- name: Remove the PostgreSQL Kubernetes ConfigMap
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/config/rm
```

### openshift/start

Start PostgreSQL on OpenShift

Reuses the generic `k8s/start` flow for OpenShift.

Namespace creation and optional NodePort behavior are controlled by the shared Kubernetes variables consumed by `k8s/start`.

Uses the same role templates to configure storage, credentials, TLS, and optional mTLS mounts.

```yaml
- name: Start PostgreSQL on OpenShift
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
    # Timeout in seconds while waiting for the StatefulSet rollout to complete.
    postgres_k8s_wait_timeout: 120
    # Kubernetes pod `fsGroup` applied so mounted files are readable by the postgres process.
    postgres_k8s_fs_group: 999
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 1000
    # Container registry endpoint used to build `postgres_image`. The default derives from `POSTGRES_REGISTRY_ENDPOINT` and falls back to `docker.io/library`.
    postgres_registry_endpoint: "{{ lookup('env', 'POSTGRES_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # PostgreSQL image repository name.
    postgres_image_name: postgres
    # PostgreSQL image tag.
    postgres_image_tag: 16.4
    # Full container image reference for PostgreSQL. The default derives from `postgres_registry_endpoint`, `postgres_image_name`, and `postgres_image_tag`.
    postgres_image: "{{ postgres_registry_endpoint }}/{{ postgres_image_name }}:{{ postgres_image_tag }}"
    # Configuration directory path inside the PostgreSQL container.
    postgres_container_config_dir: /var/lib/postgresql/config
    # Data directory path inside the PostgreSQL container.
    postgres_container_data_dir: /var/lib/postgresql/data
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "string"
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "string"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault.
    postgres_password: "string"
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled.
    postgres_mtls_clients: ["entry1", "entry2"]
    # Additional PostgreSQL command-line options appended to the start command.
    postgres_extra_cmd_opts: "string"
    # Requested persistent storage size for the PostgreSQL PVC. Example: `500Mi`.
    k8s_storage_size: "string"
    # Kubernetes storage class name for the PostgreSQL PVC when a non-default class is required.
    k8s_storage_class: "string"
    # Existing Kubernetes `imagePullSecret` name used when the PostgreSQL image is stored in a private registry.
    k8s_image_pull_secret: "string"
    # Override for the readiness probe initial delay in seconds. The template default is `10`.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Override for the readiness probe period in seconds. The template default is `10`.
    k8s_readiness_probe_period_seconds: 1000
    # Override for the readiness probe timeout in seconds. The template default is `5`.
    k8s_readiness_probe_timeout_seconds: 1000
    # Override for the readiness probe failure threshold. The template default is `3`.
    k8s_readiness_probe_failure_threshold: 1000
    # Override for the liveness probe initial delay in seconds. The template default is `30`.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Override for the liveness probe period in seconds. The template default is `15`.
    k8s_liveness_probe_period_seconds: 1000
    # Override for the liveness probe timeout in seconds. The template default is `5`.
    k8s_liveness_probe_timeout_seconds: 1000
    # Override for the liveness probe failure threshold. The template default is `5`.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: openshift/start
```

### openshift/rm

Remove PostgreSQL OpenShift resources

Reuses the generic `k8s/rm` flow for OpenShift resource removal.

The persistent volume claim is removed separately by the `data/rm` entry point.

```yaml
- name: Remove PostgreSQL OpenShift resources
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services. The default derives from `inventory_hostname`.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: openshift/rm
```

### crypto/setup

Prepare PostgreSQL TLS materials

Selects the PostgreSQL TLS generation path for OpenSSL, cryptogen, or Fabric CA.

Also applies the Kubernetes Secret when Kubernetes or OpenShift mode is enabled.

```yaml
- name: Prepare PostgreSQL TLS materials
  vars:
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/setup
```

### crypto/fetch

Fetch PostgreSQL TLS certificates

Fetches the PostgreSQL TLS CA certificate and server certificate to the control node.

This task runs only when `postgres_use_tls` is true.

```yaml
- name: Fetch PostgreSQL TLS certificates
  vars:
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Control-node directory where fetched PostgreSQL artifacts are written. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/fetch
```

### crypto/rm

Remove PostgreSQL TLS materials

Deletes PostgreSQL TLS files from the remote host when TLS is enabled.

Also removes the Kubernetes Secret used for TLS materials when Kubernetes or OpenShift mode is enabled.

```yaml
- name: Remove PostgreSQL TLS materials
  vars:
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/rm
```

### crypto/openssl/generate_cert

Generate PostgreSQL TLS materials with OpenSSL

Generates a self-signed TLS keypair for PostgreSQL on the target host.

Used when PostgreSQL TLS is enabled without a peer organization definition.

```yaml
- name: Generate PostgreSQL TLS materials with OpenSSL
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/openssl/generate_cert
```

### crypto/cryptogen/transfer

Transfer PostgreSQL TLS materials from cryptogen

Copies PostgreSQL TLS files generated by cryptogen from the control node to the target host.

Used when PostgreSQL belongs to a peer organization without a Fabric CA host.

```yaml
- name: Transfer PostgreSQL TLS materials from cryptogen
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # Control-node directory containing cryptogen output for PostgreSQL. Example: `/tmp/fabricx/cryptogen-artifacts`.
    cryptogen_artifacts_dir: "string"
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

Enroll PostgreSQL with Fabric CA for TLS

Enrolls PostgreSQL through Fabric CA to generate TLS materials on the target host.

Requires the organization definition to reference a Fabric CA host and peer identity.

```yaml
- name: Enroll PostgreSQL with Fabric CA for TLS
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # Control-node directory where fetched PostgreSQL artifacts are written. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "string"
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA.
    organization: {}
    # Resolved host name used in the Fabric CA CSR SAN list. Required by the Fabric CA TLS enrollment path.
    actual_host: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/fabric_ca/enroll
```

### config/transfer

Transfer PostgreSQL configuration

Ensures the PostgreSQL configuration directory exists and prepares optional mTLS configuration.

Also applies the PostgreSQL ConfigMap when Kubernetes or OpenShift mode is enabled.

```yaml
- name: Transfer PostgreSQL configuration
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled.
    postgres_mtls_clients: ["entry1", "entry2"]
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/transfer
```

### config/rm

Remove PostgreSQL configuration

Deletes PostgreSQL configuration files from the remote host.

Also removes the PostgreSQL ConfigMap when Kubernetes or OpenShift mode is enabled.

```yaml
- name: Remove PostgreSQL configuration
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/rm
```

### config/mtls/transfer

Transfer PostgreSQL mTLS configuration

Renders `pg_hba.conf` and assembles the PostgreSQL client CA bundle used for mTLS.

Copies client certificates from previously fetched artifacts on the control node.

```yaml
- name: Transfer PostgreSQL mTLS configuration
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used.
    remote_config_dir: "string"
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled.
    postgres_mtls_clients: ["entry1", "entry2"]
    # Control-node directory where fetched PostgreSQL artifacts are written. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/mtls/transfer
```
