# hyperledger.fabricx.postgres

> Deploys and manages a PostgreSQL instance for Fabric-X in container, Kubernetes, or OpenShift mode.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [ping](#ping)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [data/rm](#datarm)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate\_cert](#cryptoopensslgenerate_cert)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric\_ca/enroll](#cryptofabric_caenroll)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/mtls/transfer](#configmtlstransfer)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.postgres
```

## Tasks

### ping

> Check PostgreSQL reachability

Validates PostgreSQL reachability for the selected deployment mode. In container mode, waits for the target host to accept connections on `postgres_port`. In Kubernetes mode, delegates to `k8s/ping`, which checks the configured NodePort when `postgres_k8s_use_node_port` is enabled and checks `actual_host`:`postgres_port` when `postgres_k8s_use_load_balancer` is enabled. Also checks `postgres_exporter_port` when the exporter is defined for the host.

```yaml
- name: Check PostgreSQL reachability
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 5432
    # Optional postgres_exporter port to probe after PostgreSQL itself. This entry point only runs when the variable is defined. Example: `9187`.
    postgres_exporter_port: 9187
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: ping
```

### start

> Start PostgreSQL

Starts PostgreSQL using the selected deployment mode and dispatches to the matching runtime entry point. Container mode is the default unless `postgres_use_k8s` or `postgres_use_openshift` is enabled. Kubernetes mode creates or updates the namespace, headless Service, optional NodePort Service, and StatefulSet. OpenShift mode reuses the Kubernetes resource flow with the OpenShift deployment flag.

```yaml
- name: Start PostgreSQL
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: start
```

### stop

> Stop PostgreSQL

Stops PostgreSQL runtime processes for deployments managed as a local container. Kubernetes and OpenShift deployments are not stopped by this entry point; use `teardown` or `wipe` to remove cluster resources. `postgres_use_container` is enabled when neither `postgres_use_k8s` nor `postgres_use_openshift` is enabled.

```yaml
- name: Stop PostgreSQL
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: stop
```

### teardown

> Remove PostgreSQL runtime resources

Removes PostgreSQL runtime resources for the selected deployment mode while leaving configuration, TLS files, and persistent data to their dedicated cleanup paths. Container mode removes the container instance. Kubernetes and OpenShift modes remove the StatefulSet and Services; the PVC is removed separately through `data/rm`.

```yaml
- name: Remove PostgreSQL runtime resources
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: teardown
```

### wipe

> Wipe PostgreSQL data and configuration

Fully removes PostgreSQL runtime resources, persistent data, TLS materials, and configuration files for the selected deployment mode. Sequences `teardown`, `data/rm`, `crypto/rm`, and `config/rm` so container directories and Kubernetes or OpenShift resources are cleaned consistently.

```yaml
- name: Wipe PostgreSQL data and configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: wipe
```

### fetch_logs

> Fetch PostgreSQL logs

Collects PostgreSQL logs from the selected deployment mode without changing runtime state. Container mode fetches logs from `postgres_container_name`. Kubernetes and OpenShift modes fetch pod logs selected by `postgres_k8s_resource_name` in `k8s_namespace`.

```yaml
- name: Fetch PostgreSQL logs
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: fetch_logs
```

### data/rm

> Remove PostgreSQL data storage

Removes PostgreSQL persistent data for the selected deployment mode. Container mode deletes `postgres_remote_data_dir`, such as `/var/lib/fabricx/postgres/postgres0/data`. Kubernetes and OpenShift modes delete the StatefulSet PVC in `k8s_namespace`.

```yaml
- name: Remove PostgreSQL data storage
  vars:
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Run PostgreSQL as a container when set to `true`.
    postgres_use_container: "{{ (not postgres_use_k8s) and (not postgres_use_openshift) }}"
    # Remote directory used for PostgreSQL persistent data.
    postgres_remote_data_dir: "{{ remote_data_dir }}"
    # Outer remote data directory consumed by `postgres_remote_data_dir`. This dependency is validated wherever PostgreSQL persistent data is used. Example: `/var/lib/fabricx/postgres/postgres0/data`.
    remote_data_dir: "/var/lib/fabricx/postgres/postgres0/data"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: data/rm
```

### container/start

> Start PostgreSQL in a container

Creates the PostgreSQL data directory, fixes TLS file permissions when TLS is enabled, and starts `postgres_container_name`. Passes initialization credentials through `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`. Mounts `postgres_remote_config_dir` and `postgres_remote_data_dir` into the container and waits for `postgres_port` to become reachable. Appends TLS, mTLS, and `postgres_extra_cmd_opts` command-line options when they are enabled.

```yaml
- name: Start PostgreSQL in a container
  vars:
    # Container name for the PostgreSQL instance.
    postgres_container_name: "{{ inventory_hostname }}"
    # Container registry endpoint used to build `postgres_image`.
    postgres_registry_endpoint: "{{ lookup('env', 'POSTGRES_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # PostgreSQL image repository name.
    postgres_image_name: postgres
    # PostgreSQL image tag.
    postgres_image_tag: 16.4
    # Full container image reference for PostgreSQL.
    postgres_image: "{{ postgres_registry_endpoint }}/{{ postgres_image_name }}:{{ postgres_image_tag }}"
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Remote directory used for PostgreSQL persistent data.
    postgres_remote_data_dir: "{{ remote_data_dir }}"
    # Outer remote data directory consumed by `postgres_remote_data_dir`. This dependency is validated wherever PostgreSQL persistent data is used. Example: `/var/lib/fabricx/postgres/postgres0/data`.
    remote_data_dir: "/var/lib/fabricx/postgres/postgres0/data"
    # Configuration directory path inside the PostgreSQL container.
    postgres_container_config_dir: /var/lib/postgresql/config
    # Data directory path inside the PostgreSQL container.
    postgres_container_data_dir: /var/lib/postgresql/data
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "fabricx"
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "postgres"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault. Example: `my_postgres_password`.
    postgres_password: "my_postgres_password"
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 5432
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled. Example: `['committer0', 'orderer0']`.
    postgres_mtls_clients:
      - "committer0"
      - "orderer0"
    # Additional PostgreSQL command-line options appended to the start command. Example: `-c max_connections=200 -c log_directory=/var/lib/postgresql/data/pg_log`.
    postgres_extra_cmd_opts: "-c max_connections=200 -c log_directory=/var/lib/postgresql/data/pg_log"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/start
```

### container/stop

> Stop the PostgreSQL container

Stops the PostgreSQL container instance named by `postgres_container_name`. Uses the container helper role internally.

```yaml
- name: Stop the PostgreSQL container
  vars:
    # Container name for the PostgreSQL instance.
    postgres_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/stop
```

### container/rm

> Remove the PostgreSQL container

Removes the PostgreSQL container instance named by `postgres_container_name`. Container volumes are handled separately by the `data/rm` entry point.

```yaml
- name: Remove the PostgreSQL container
  vars:
    # Container name for the PostgreSQL instance.
    postgres_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch PostgreSQL container logs

Collects logs from the PostgreSQL container instance named by `postgres_container_name`. Uses the container helper role internally.

```yaml
- name: Fetch PostgreSQL container logs
  vars:
    # Container name for the PostgreSQL instance.
    postgres_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: container/fetch_logs
```

### k8s/start

> Start PostgreSQL on Kubernetes

Ensures `k8s_namespace` exists and applies the PostgreSQL headless Service and StatefulSet named by `postgres_k8s_resource_name`. Applies `postgres_k8s_resource_name`-nodeport when `postgres_k8s_use_node_port` is enabled; the PostgreSQL port is included only when `postgres_k8s_node_port` is defined. Applies `postgres_k8s_resource_name`-loadbalancer when `postgres_k8s_use_load_balancer` is enabled. Uses the role templates to configure credentials, PVC storage, TLS Secret mounts, optional mTLS ConfigMap mounts, image pull secrets, and readiness and liveness probes. Waits up to `postgres_k8s_wait_timeout` seconds for the StatefulSet rollout to complete.

```yaml
- name: Start PostgreSQL on Kubernetes
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
    # Timeout in seconds while waiting for the StatefulSet rollout to complete.
    postgres_k8s_wait_timeout: 120
    # Kubernetes pod `fsGroup` applied so mounted files are readable by the postgres process.
    postgres_k8s_fs_group: 999
    # Enable the Kubernetes NodePort Service for PostgreSQL when set to `true`.
    postgres_k8s_use_node_port: false
    # Enable the Kubernetes LoadBalancer Service for PostgreSQL when set to `true`.
    postgres_k8s_use_load_balancer: false
    # Kubernetes NodePort value used by the external PostgreSQL Service. The PostgreSQL port is only exposed by the NodePort Service when this value is defined and `postgres_k8s_use_node_port` is `true`. Example: `30432`.
    postgres_k8s_node_port: 30432
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 5432
    # Container registry endpoint used to build `postgres_image`.
    postgres_registry_endpoint: "{{ lookup('env', 'POSTGRES_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # PostgreSQL image repository name.
    postgres_image_name: postgres
    # PostgreSQL image tag.
    postgres_image_tag: 16.4
    # Full container image reference for PostgreSQL.
    postgres_image: "{{ postgres_registry_endpoint }}/{{ postgres_image_name }}:{{ postgres_image_tag }}"
    # Configuration directory path inside the PostgreSQL container.
    postgres_container_config_dir: /var/lib/postgresql/config
    # Data directory path inside the PostgreSQL container.
    postgres_container_data_dir: /var/lib/postgresql/data
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "fabricx"
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "postgres"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault. Example: `my_postgres_password`.
    postgres_password: "my_postgres_password"
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled. Example: `['committer0', 'orderer0']`.
    postgres_mtls_clients:
      - "committer0"
      - "orderer0"
    # Additional PostgreSQL command-line options appended to the start command. Example: `-c max_connections=200 -c log_directory=/var/lib/postgresql/data/pg_log`.
    postgres_extra_cmd_opts: "-c max_connections=200 -c log_directory=/var/lib/postgresql/data/pg_log"
    # Requested persistent storage size for the PostgreSQL PVC. Example: `500Mi`.
    k8s_storage_size: "500Mi"
    # Kubernetes storage class name for the PostgreSQL PVC when a non-default class is required. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Existing Kubernetes `imagePullSecret` name used when the PostgreSQL image is stored in a private registry. Example: `postgres-registry-pull-secret`.
    k8s_image_pull_secret: "postgres-registry-pull-secret"
    # Override for the readiness probe initial delay in seconds. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Override for the readiness probe period in seconds. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Override for the readiness probe timeout in seconds. Example: `5`.
    k8s_readiness_probe_timeout_seconds: 5
    # Override for the readiness probe failure threshold. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Override for the liveness probe initial delay in seconds. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Override for the liveness probe period in seconds. Example: `15`.
    k8s_liveness_probe_period_seconds: 15
    # Override for the liveness probe timeout in seconds. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Override for the liveness probe failure threshold. Example: `5`.
    k8s_liveness_probe_failure_threshold: 5
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/start
```

### k8s/ping

> Check PostgreSQL external Service reachability on Kubernetes

Probes the PostgreSQL NodePort Service when `postgres_k8s_use_node_port` is enabled and `postgres_k8s_node_port` is defined. Probes `actual_host`:`postgres_port` when `postgres_k8s_use_load_balancer` is enabled. This entry point is invoked internally by `ping` when PostgreSQL runs on Kubernetes.

```yaml
- name: Check PostgreSQL external Service reachability on Kubernetes
  vars:
    # Resolved host name used for external reachability checks and in the Fabric CA CSR SAN list. Example: `postgres0.example.com`.
    actual_host: "postgres0.example.com"
    # Enable the Kubernetes NodePort Service for PostgreSQL when set to `true`.
    postgres_k8s_use_node_port: false
    # Enable the Kubernetes LoadBalancer Service for PostgreSQL when set to `true`.
    postgres_k8s_use_load_balancer: false
    # Kubernetes NodePort value used by the external PostgreSQL Service. The PostgreSQL port is only exposed by the NodePort Service when this value is defined and `postgres_k8s_use_node_port` is `true`. Example: `30432`.
    postgres_k8s_node_port: 30432
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 5432
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/ping
```

### k8s/rm

> Remove PostgreSQL Kubernetes resources

Deletes the PostgreSQL StatefulSet, headless Service, optional NodePort Service, and optional LoadBalancer Service resources from `k8s_namespace`. The persistent volume claim is removed separately by the `data/rm` entry point.

```yaml
- name: Remove PostgreSQL Kubernetes resources
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch PostgreSQL pod logs

Collects logs from the PostgreSQL pod in `k8s_namespace`. Selects pods using `postgres_k8s_resource_name` as the PostgreSQL application label.

```yaml
- name: Fetch PostgreSQL pod logs
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/fetch_logs
```

### k8s/crypto/transfer

> Apply the PostgreSQL Kubernetes Secret

Applies the Kubernetes Secret named `postgres_k8s_resource_name`-secret. Stores PostgreSQL database, user, and password values plus optional server TLS files under the Secret. Ensures `k8s_namespace` exists before applying the Secret.

```yaml
- name: Apply the PostgreSQL Kubernetes Secret
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "postgres"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault. Example: `my_postgres_password`.
    postgres_password: "my_postgres_password"
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "fabricx"
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Remove the PostgreSQL Kubernetes Secret

Deletes the Kubernetes Secret named `postgres_k8s_resource_name`-secret from `k8s_namespace`. The Secret stores PostgreSQL credentials and TLS materials. This entry point is typically invoked from the PostgreSQL crypto cleanup workflow.

```yaml
- name: Remove the PostgreSQL Kubernetes Secret
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/crypto/rm
```

### k8s/config/transfer

> Apply the PostgreSQL Kubernetes ConfigMap

Applies the Kubernetes ConfigMap named `postgres_k8s_resource_name`-config. Stores `pg_hba.conf` and the PostgreSQL mTLS client CA bundle when mTLS clients are configured. Ensures `k8s_namespace` exists before applying the ConfigMap.

```yaml
- name: Apply the PostgreSQL Kubernetes ConfigMap
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled. Example: `['committer0', 'orderer0']`.
    postgres_mtls_clients:
      - "committer0"
      - "orderer0"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the PostgreSQL Kubernetes ConfigMap

Deletes the Kubernetes ConfigMap named `postgres_k8s_resource_name`-config from `k8s_namespace`. The ConfigMap stores PostgreSQL mTLS configuration. This entry point is typically invoked from the PostgreSQL config cleanup workflow.

```yaml
- name: Remove the PostgreSQL Kubernetes ConfigMap
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: k8s/config/rm
```

### openshift/start

> Start PostgreSQL on OpenShift

Starts PostgreSQL on OpenShift by reusing the generic `k8s/start` resource flow. Creates or updates the namespace, headless Service, optional external Services, StatefulSet, PVC, credentials Secret, and optional mTLS ConfigMap. Uses the same storage, probe, TLS, and image pull settings as Kubernetes mode.

```yaml
- name: Start PostgreSQL on OpenShift
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
    # Timeout in seconds while waiting for the StatefulSet rollout to complete.
    postgres_k8s_wait_timeout: 120
    # Kubernetes pod `fsGroup` applied so mounted files are readable by the postgres process.
    postgres_k8s_fs_group: 999
    # Enable the Kubernetes NodePort Service for PostgreSQL when set to `true`.
    postgres_k8s_use_node_port: false
    # Enable the Kubernetes LoadBalancer Service for PostgreSQL when set to `true`.
    postgres_k8s_use_load_balancer: false
    # Kubernetes NodePort value used by the external PostgreSQL Service. The PostgreSQL port is only exposed by the NodePort Service when this value is defined and `postgres_k8s_use_node_port` is `true`. Example: `30432`.
    postgres_k8s_node_port: 30432
    # PostgreSQL listener port used by the container, Kubernetes Service, and optional NodePort Service target port. Example: `5432`.
    postgres_port: 5432
    # Container registry endpoint used to build `postgres_image`.
    postgres_registry_endpoint: "{{ lookup('env', 'POSTGRES_REGISTRY_ENDPOINT') or 'docker.io/library' }}"
    # PostgreSQL image repository name.
    postgres_image_name: postgres
    # PostgreSQL image tag.
    postgres_image_tag: 16.4
    # Full container image reference for PostgreSQL.
    postgres_image: "{{ postgres_registry_endpoint }}/{{ postgres_image_name }}:{{ postgres_image_tag }}"
    # Configuration directory path inside the PostgreSQL container.
    postgres_container_config_dir: /var/lib/postgresql/config
    # Data directory path inside the PostgreSQL container.
    postgres_container_data_dir: /var/lib/postgresql/data
    # PostgreSQL database name used during initialization and in the readiness checks. Example: `fabricx`.
    postgres_db: "fabricx"
    # PostgreSQL user name used during initialization and in the readiness checks. Example: `postgres`.
    postgres_user: "postgres"
    # Password for `postgres_user` used during initialization. Store this value in an Ansible Vault. Example: `my_postgres_password`.
    postgres_password: "my_postgres_password"
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled. Example: `['committer0', 'orderer0']`.
    postgres_mtls_clients:
      - "committer0"
      - "orderer0"
    # Additional PostgreSQL command-line options appended to the start command. Example: `-c max_connections=200 -c log_directory=/var/lib/postgresql/data/pg_log`.
    postgres_extra_cmd_opts: "-c max_connections=200 -c log_directory=/var/lib/postgresql/data/pg_log"
    # Requested persistent storage size for the PostgreSQL PVC. Example: `500Mi`.
    k8s_storage_size: "500Mi"
    # Kubernetes storage class name for the PostgreSQL PVC when a non-default class is required. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Existing Kubernetes `imagePullSecret` name used when the PostgreSQL image is stored in a private registry. Example: `postgres-registry-pull-secret`.
    k8s_image_pull_secret: "postgres-registry-pull-secret"
    # Override for the readiness probe initial delay in seconds. Example: `10`.
    k8s_readiness_probe_initial_delay_seconds: 10
    # Override for the readiness probe period in seconds. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Override for the readiness probe timeout in seconds. Example: `5`.
    k8s_readiness_probe_timeout_seconds: 5
    # Override for the readiness probe failure threshold. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Override for the liveness probe initial delay in seconds. Example: `30`.
    k8s_liveness_probe_initial_delay_seconds: 30
    # Override for the liveness probe period in seconds. Example: `15`.
    k8s_liveness_probe_period_seconds: 15
    # Override for the liveness probe timeout in seconds. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Override for the liveness probe failure threshold. Example: `5`.
    k8s_liveness_probe_failure_threshold: 5
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: openshift/start
```

### openshift/rm

> Remove PostgreSQL OpenShift resources

Removes PostgreSQL OpenShift resources by reusing the generic `k8s/rm` resource flow. Deletes the StatefulSet, headless Service, optional NodePort Service, and optional LoadBalancer Service from `k8s_namespace`. The persistent volume claim is removed separately by the `data/rm` entry point.

```yaml
- name: Remove PostgreSQL OpenShift resources
  vars:
    # Base Kubernetes resource name used for PostgreSQL objects, including the StatefulSet and Services.
    postgres_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes namespace used for PostgreSQL resources. This dependency is validated by every Kubernetes leaf entry point. Example: `fabricx-postgres`.
    k8s_namespace: "fabricx-postgres"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: openshift/rm
```

### crypto/setup

> Prepare PostgreSQL TLS materials

Selects the PostgreSQL TLS generation path for OpenSSL, cryptogen, or Fabric CA based on the supplied organization inputs. Applies the Kubernetes or OpenShift Secret when cluster deployment mode is enabled so credentials and optional TLS materials are available before startup.

```yaml
- name: Prepare PostgreSQL TLS materials
  vars:
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'postgres0', 'secret': '<fabric-ca-secret>'}, 'fabric_ca_host': 'fabric-ca0'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "postgres0"
        secret: "<fabric-ca-secret>"
      fabric_ca_host: "fabric-ca0"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/setup
```

### crypto/fetch

> Fetch PostgreSQL TLS certificates

Fetches the PostgreSQL TLS CA certificate and server certificate from `postgres_remote_config_dir` to `fetched_artifacts_dir`. This task runs only when `postgres_use_tls` is true.

```yaml
- name: Fetch PostgreSQL TLS certificates
  vars:
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Control-node directory where fetched PostgreSQL artifacts are written. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/fetched-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove PostgreSQL TLS materials

Deletes PostgreSQL TLS files from `postgres_remote_config_dir` when TLS is enabled. Also removes the Kubernetes or OpenShift Secret used for credentials and TLS materials when cluster deployment mode is enabled.

```yaml
- name: Remove PostgreSQL TLS materials
  vars:
    # Enable server-side TLS for PostgreSQL.
    postgres_use_tls: false
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/rm
```

### crypto/openssl/generate_cert

> Generate PostgreSQL TLS materials with OpenSSL

Generates a self-signed TLS keypair for PostgreSQL under `postgres_remote_config_dir` on the target host. Used when PostgreSQL TLS is enabled without a peer organization definition.

```yaml
- name: Generate PostgreSQL TLS materials with OpenSSL
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'postgres0', 'secret': '<fabric-ca-secret>'}, 'fabric_ca_host': 'fabric-ca0'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "postgres0"
        secret: "<fabric-ca-secret>"
      fabric_ca_host: "fabric-ca0"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/openssl/generate_cert
```

### crypto/cryptogen/transfer

> Transfer PostgreSQL TLS materials from cryptogen

Copies PostgreSQL TLS files generated by cryptogen from `cryptogen_artifacts_dir` on the control node to `postgres_remote_config_dir` on the target host. Used when PostgreSQL belongs to a peer organization without a Fabric CA host.

```yaml
- name: Transfer PostgreSQL TLS materials from cryptogen
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # Control-node directory containing cryptogen output for PostgreSQL. Example: `/tmp/fabricx/cryptogen-artifacts`.
    cryptogen_artifacts_dir: "/tmp/fabricx/cryptogen-artifacts"
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'postgres0', 'secret': '<fabric-ca-secret>'}, 'fabric_ca_host': 'fabric-ca0'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "postgres0"
        secret: "<fabric-ca-secret>"
      fabric_ca_host: "fabric-ca0"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

> Enroll PostgreSQL with Fabric CA for TLS

Enrolls PostgreSQL through Fabric CA to generate TLS materials under `postgres_remote_config_dir` on the target host. Uses `actual_host` in the CSR SAN list and writes fetched CA artifacts under `fetched_artifacts_dir`. Requires the organization definition to reference a Fabric CA host and peer identity.

```yaml
- name: Enroll PostgreSQL with Fabric CA for TLS
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Filename of the PostgreSQL TLS private key under the TLS config directory.
    postgres_tls_private_key_file: server.key
    # Filename of the PostgreSQL TLS certificate under the TLS config directory.
    postgres_tls_cert_file: server.crt
    # Control-node directory where fetched PostgreSQL artifacts are written. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/fetched-artifacts"
    # Fabric organization inputs used by PostgreSQL TLS generation paths. The exact required fields depend on whether PostgreSQL TLS is sourced from OpenSSL, cryptogen, or Fabric CA. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'postgres0', 'secret': '<fabric-ca-secret>'}, 'fabric_ca_host': 'fabric-ca0'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "postgres0"
        secret: "<fabric-ca-secret>"
      fabric_ca_host: "fabric-ca0"
    # Resolved host name used for external reachability checks and in the Fabric CA CSR SAN list. Example: `postgres0.example.com`.
    actual_host: "postgres0.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: crypto/fabric_ca/enroll
```

### config/transfer

> Transfer PostgreSQL configuration

Ensures `postgres_remote_config_dir` exists and prepares optional mTLS configuration for PostgreSQL. Also applies the PostgreSQL ConfigMap when Kubernetes or OpenShift mode is enabled.

```yaml
- name: Transfer PostgreSQL configuration
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Enable mutual TLS for PostgreSQL clients.
    postgres_use_mtls: false
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled. Example: `['committer0', 'orderer0']`.
    postgres_mtls_clients:
      - "committer0"
      - "orderer0"
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/transfer
```

### config/rm

> Remove PostgreSQL configuration

Deletes PostgreSQL configuration files from `postgres_remote_config_dir` on the remote host. Also removes the PostgreSQL ConfigMap when Kubernetes or OpenShift mode is enabled.

```yaml
- name: Remove PostgreSQL configuration
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # Run PostgreSQL on Kubernetes when set to `true`.
    postgres_use_k8s: false
    # Run PostgreSQL on OpenShift when set to `true`.
    postgres_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/rm
```

### config/mtls/transfer

> Transfer PostgreSQL mTLS configuration

Renders `pg_hba.conf` and assembles the PostgreSQL client CA bundle used for mTLS. Copies client certificates from `fetched_artifacts_dir` on the control node.

```yaml
- name: Transfer PostgreSQL mTLS configuration
  vars:
    # Remote directory used for PostgreSQL configuration and TLS files.
    postgres_remote_config_dir: "{{ remote_config_dir }}"
    # Outer remote configuration directory consumed by `postgres_remote_config_dir`. This dependency is validated wherever PostgreSQL configuration files or TLS materials are used. Example: `/opt/fabricx/postgres/postgres0/config`.
    remote_config_dir: "/opt/fabricx/postgres/postgres0/config"
    # List of client artifact names whose certificates are assembled into the PostgreSQL mTLS bundle. This value is only required when PostgreSQL mTLS is enabled. Example: `['committer0', 'orderer0']`.
    postgres_mtls_clients:
      - "committer0"
      - "orderer0"
    # Control-node directory where fetched PostgreSQL artifacts are written. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/fetched-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres
    tasks_from: config/mtls/transfer
```
