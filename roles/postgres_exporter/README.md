# hyperledger.fabricx.postgres_exporter

> Deploys and manages the Prometheus Postgres Exporter in container or Kubernetes mode to collect PostgreSQL metrics.

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
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/transfer_grafana_dashboard](#configtransfer_grafana_dashboard)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate_cert](#cryptoopensslgenerate_cert)
  - [k8s/start](#k8sstart)
  - [k8s/ping](#k8sping)
  - [k8s/rm](#k8srm)
  - [k8s/fetch_logs](#k8sfetch_logs)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [k8s/crypto/rm](#k8scryptorm)
  - [prometheus/get_scrapers](#prometheusget_scrapers)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.postgres_exporter
```

## Tasks

### start

> Start Postgres Exporter

Dispatches to the container or Kubernetes startup path for Postgres Exporter.In container mode it renders the exporter config, builds the PostgreSQL datasource from the monitored host facts, and starts the exporter container.In Kubernetes mode it renders the ConfigMap, Secret, and Service resources needed to run the exporter Deployment against the same datasource.The backend selection is controlled by `postgres_exporter_use_container` and `postgres_exporter_use_k8s`.

```yaml
- name: Start Postgres Exporter
  vars:
    # Enables the container backend when set to `true`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: start
```

### stop

> Stop Postgres Exporter

Stops a container-based Postgres Exporter deployment without removing generated configuration or TLS artifacts.This entry point only dispatches when `postgres_exporter_use_container` resolves to `true`.

```yaml
- name: Stop Postgres Exporter
  vars:
    # Enables the container backend when set to `true`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: stop
```

### teardown

> Remove Postgres Exporter runtime resources

Removes the active Postgres Exporter runtime resources for the enabled backend.This dispatches to the container removal path or the Kubernetes removal path, depending on the selected backend.

```yaml
- name: Remove Postgres Exporter runtime resources
  vars:
    # Enables the container backend when set to `true`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: teardown
```

### wipe

> Remove all Postgres Exporter artifacts

Removes runtime resources, TLS artifacts, and generated configuration for Postgres Exporter.This entry point combines `teardown`, `crypto/rm`, and `config/rm`, so it validates the variables needed by all three paths.

```yaml
- name: Remove all Postgres Exporter artifacts
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: wipe
```

### fetch_logs

> Fetch Postgres Exporter logs

Collects logs from the Postgres Exporter container or Kubernetes pod for the active backend.The backend selection is controlled by `postgres_exporter_use_container` and `postgres_exporter_use_k8s`.

```yaml
- name: Fetch Postgres Exporter logs
  vars:
    # Enables the container backend when set to `true`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
    # Sets the Postgres Exporter container name.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: fetch_logs
```

### ping

> Check Postgres Exporter reachability

Checks whether the Postgres Exporter metrics port is reachable on the current host.In Kubernetes mode this validates the optional NodePort exposure instead of the container listener.

```yaml
- name: Check Postgres Exporter reachability
  vars:
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 9187
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: ping
```

### container/start

> Start the Postgres Exporter container

Builds the exporter PostgreSQL datasource from the monitored host facts, renders the container configuration, and starts the Postgres Exporter container.When the monitored database uses TLS, the exporter mounts the copied CA certificate and connects with `sslmode=verify-full`.

```yaml
- name: Start the Postgres Exporter container
  vars:
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. Example: `postgres-db-01`. The exporter builds its datasource from the referenced host's `postgres_user`, `postgres_password`, `ansible_host`, `postgres_port`, and `postgres_db` facts. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "postgres-db-01"
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Sets the registry endpoint used to build the Postgres Exporter image reference.
    postgres_exporter_registry_endpoint: "{{ lookup('env', 'POSTGRES_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prometheuscommunity' }}"
    # Sets the image name used to build `postgres_exporter_image`.
    postgres_exporter_image_name: postgres-exporter
    # Sets the image tag used to build `postgres_exporter_image`.
    postgres_exporter_image_tag: latest
    # Sets the full Postgres Exporter image reference.
    postgres_exporter_image: "{{ postgres_exporter_registry_endpoint }}/{{ postgres_exporter_image_name }}:{{ postgres_exporter_image_tag }}"
    # Sets the Postgres Exporter container name.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 9187
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the configuration directory mounted inside the container or pod.
    postgres_exporter_container_config_dir: /var/config
    # Sets the main Postgres Exporter configuration file name.
    postgres_exporter_config_file: postgres_exporter.yaml
    # Sets the HTTPS web configuration file name used when `postgres_exporter_use_tls` is true.
    postgres_exporter_web_config_file: web-config.yaml
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: container/start
```

### container/stop

> Stop the Postgres Exporter container

Stops the Postgres Exporter container while leaving generated configuration and artifacts in place.

```yaml
- name: Stop the Postgres Exporter container
  vars:
    # Sets the Postgres Exporter container name.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: container/stop
```

### container/rm

> Remove the Postgres Exporter container

Removes the Postgres Exporter container and clears the runtime instance name used for container lifecycle operations.

```yaml
- name: Remove the Postgres Exporter container
  vars:
    # Sets the Postgres Exporter container name.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch Postgres Exporter container logs

Fetches logs from the Postgres Exporter container using the configured container name.

```yaml
- name: Fetch Postgres Exporter container logs
  vars:
    # Sets the Postgres Exporter container name.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: container/fetch_logs
```

### config/transfer

> Generate and transfer Postgres Exporter configuration

Generates the Postgres Exporter configuration files and copies the PostgreSQL CA certificate when the monitored database uses TLS.The rendered configuration includes the datasource assembled from the monitored PostgreSQL host facts.For Kubernetes deployments this also applies the ConfigMap.

```yaml
- name: Generate and transfer Postgres Exporter configuration
  vars:
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. Example: `postgres-db-01`. The exporter builds its datasource from the referenced host's `postgres_user`, `postgres_password`, `ansible_host`, `postgres_port`, and `postgres_db` facts. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "postgres-db-01"
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Provides the control-node directory used to fetch or stage Postgres Exporter TLS artifacts. Example: `/tmp/postgres-exporter-artifacts`.
    fetched_artifacts_dir: "/tmp/postgres-exporter-artifacts"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the configuration directory mounted inside the container or pod.
    postgres_exporter_container_config_dir: /var/config
    # Sets the main Postgres Exporter configuration file name.
    postgres_exporter_config_file: postgres_exporter.yaml
    # Sets the HTTPS web configuration file name used when `postgres_exporter_use_tls` is true.
    postgres_exporter_web_config_file: web-config.yaml
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
    # Sets the TLS private key file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_private_key_file: server.key
    # Sets the TLS certificate file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_cert_file: server.crt
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/transfer
```

### config/rm

> Remove Postgres Exporter configuration

Removes generated Postgres Exporter configuration files from the remote host.For Kubernetes deployments this also deletes the related ConfigMap.

```yaml
- name: Remove Postgres Exporter configuration
  vars:
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/rm
```

### config/transfer_grafana_dashboard

> Transfer the packaged Grafana dashboard

Sets the packaged Postgres Exporter dashboard path and delegates dashboard copy to the Grafana role.This entry point does not validate any Postgres Exporter variables because it only derives paths from `role_path`.

```yaml
- name: Transfer the packaged Grafana dashboard
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/transfer_grafana_dashboard
```

### crypto/setup

> Generate Postgres Exporter TLS artifacts

Generates the Postgres Exporter TLS files when `postgres_exporter_use_tls` is true.For Kubernetes deployments this also applies the Secret used by the pod.

```yaml
- name: Generate Postgres Exporter TLS artifacts
  vars:
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/setup
```

### crypto/fetch

> Fetch Postgres Exporter TLS artifacts

Fetches the generated Postgres Exporter TLS CA certificate and server certificate to the control node.This entry point only transfers files when `postgres_exporter_use_tls` is true.

```yaml
- name: Fetch Postgres Exporter TLS artifacts
  vars:
    # Provides the control-node directory used to fetch or stage Postgres Exporter TLS artifacts. Example: `/tmp/postgres-exporter-artifacts`.
    fetched_artifacts_dir: "/tmp/postgres-exporter-artifacts"
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove Postgres Exporter TLS artifacts

Removes generated Postgres Exporter TLS files from the remote host.For Kubernetes deployments this also deletes the related Secret.

```yaml
- name: Remove Postgres Exporter TLS artifacts
  vars:
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/rm
```

### crypto/openssl/generate_cert

> Generate Postgres Exporter TLS files with OpenSSL

Delegates self-signed certificate generation to the OpenSSL role using Postgres Exporter-specific file paths.

```yaml
- name: Generate Postgres Exporter TLS files with OpenSSL
  vars:
    # Provides organization metadata forwarded to the OpenSSL role. Example: `{'domain': 'org1.example.com'}`.
    organization:
      domain: 'org1.example.com'
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the TLS private key file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_private_key_file: server.key
    # Sets the TLS certificate file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/openssl/generate_cert
```

### k8s/start

> Start Postgres Exporter on Kubernetes

Applies the Service, optional NodePort Service, and Deployment for Postgres Exporter.The Deployment connects to the monitored PostgreSQL host using the same datasource facts used by the container path.The NodePort Service is optional and only rendered when `postgres_exporter_k8s_use_node_port` is true.

```yaml
- name: Start Postgres Exporter on Kubernetes
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources. Example: `postgres-exporter`.
    k8s_namespace: "postgres-exporter"
    # Sets the optional Kubernetes image pull secret used by the Postgres Exporter Deployment. Example: `registry-credentials`.
    k8s_image_pull_secret: "registry-credentials"
    # Overrides the Deployment readiness probe initial delay. Example: `5`.
    k8s_readiness_probe_initial_delay_seconds: 5
    # Overrides the Deployment readiness probe period. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Overrides the Deployment readiness probe timeout. Example: `2`.
    k8s_readiness_probe_timeout_seconds: 2
    # Overrides the Deployment readiness probe failure threshold. Example: `3`.
    k8s_readiness_probe_failure_threshold: 3
    # Overrides the Deployment liveness probe initial delay. Example: `15`.
    k8s_liveness_probe_initial_delay_seconds: 15
    # Overrides the Deployment liveness probe period. Example: `20`.
    k8s_liveness_probe_period_seconds: 20
    # Overrides the Deployment liveness probe timeout. Example: `2`.
    k8s_liveness_probe_timeout_seconds: 2
    # Overrides the Deployment liveness probe failure threshold. Example: `3`.
    k8s_liveness_probe_failure_threshold: 3
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. Example: `postgres-db-01`. The exporter builds its datasource from the referenced host's `postgres_user`, `postgres_password`, `ansible_host`, `postgres_port`, and `postgres_db` facts. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "postgres-db-01"
    # Sets the registry endpoint used to build the Postgres Exporter image reference.
    postgres_exporter_registry_endpoint: "{{ lookup('env', 'POSTGRES_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prometheuscommunity' }}"
    # Sets the image name used to build `postgres_exporter_image`.
    postgres_exporter_image_name: postgres-exporter
    # Sets the image tag used to build `postgres_exporter_image`.
    postgres_exporter_image_tag: latest
    # Sets the full Postgres Exporter image reference.
    postgres_exporter_image: "{{ postgres_exporter_registry_endpoint }}/{{ postgres_exporter_image_name }}:{{ postgres_exporter_image_tag }}"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Deployment wait timeout in seconds.
    postgres_exporter_k8s_wait_timeout: 120
    # Sets the pod filesystem group used by the Postgres Exporter Deployment.
    postgres_exporter_k8s_fs_group: 65534
    # Enables the optional NodePort Service used to expose Postgres Exporter externally from Kubernetes. When set to `true`, `postgres_exporter_k8s_port_node_port` is used to populate the Service's node port.
    postgres_exporter_k8s_use_node_port: false
    # Sets the NodePort value exposed by the optional Postgres Exporter Kubernetes Service. Example: `30987`.
    postgres_exporter_k8s_port_node_port: 30987
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 9187
    # Sets the configuration directory mounted inside the container or pod.
    postgres_exporter_container_config_dir: /var/config
    # Sets the main Postgres Exporter configuration file name.
    postgres_exporter_config_file: postgres_exporter.yaml
    # Sets the HTTPS web configuration file name used when `postgres_exporter_use_tls` is true.
    postgres_exporter_web_config_file: web-config.yaml
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
    # Sets the TLS private key file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_private_key_file: server.key
    # Sets the TLS certificate file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/start
```

### k8s/ping

> Check Postgres Exporter node port reachability

Checks whether the optional Postgres Exporter NodePort Service is reachable.This verifies the exposed service port rather than the pod-local metrics listener.

```yaml
- name: Check Postgres Exporter node port reachability
  vars:
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 9187
    # Enables the optional NodePort Service used to expose Postgres Exporter externally from Kubernetes. When set to `true`, `postgres_exporter_k8s_port_node_port` is used to populate the Service's node port.
    postgres_exporter_k8s_use_node_port: false
    # Sets the NodePort value exposed by the optional Postgres Exporter Kubernetes Service. Example: `30987`.
    postgres_exporter_k8s_port_node_port: 30987
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/ping
```

### k8s/rm

> Remove Postgres Exporter Kubernetes resources

Removes the Postgres Exporter Deployment and Services from Kubernetes.

```yaml
- name: Remove Postgres Exporter Kubernetes resources
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources. Example: `postgres-exporter`.
    k8s_namespace: "postgres-exporter"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch Postgres Exporter pod logs

Delegates Postgres Exporter pod log collection to the shared Kubernetes role.

```yaml
- name: Fetch Postgres Exporter pod logs
  vars:
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

> Apply the Postgres Exporter ConfigMap

Ensures the Kubernetes namespace exists and applies the ConfigMap rendered from the local Postgres Exporter configuration files.The generated configuration points the exporter at the monitored PostgreSQL host facts.

```yaml
- name: Apply the Postgres Exporter ConfigMap
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources. Example: `postgres-exporter`.
    k8s_namespace: "postgres-exporter"
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. Example: `postgres-db-01`. The exporter builds its datasource from the referenced host's `postgres_user`, `postgres_password`, `ansible_host`, `postgres_port`, and `postgres_db` facts. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "postgres-db-01"
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the main Postgres Exporter configuration file name.
    postgres_exporter_config_file: postgres_exporter.yaml
    # Sets the HTTPS web configuration file name used when `postgres_exporter_use_tls` is true.
    postgres_exporter_web_config_file: web-config.yaml
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/config/transfer
```

### k8s/config/rm

> Remove the Postgres Exporter ConfigMap

Deletes the Postgres Exporter ConfigMap from Kubernetes.

```yaml
- name: Remove the Postgres Exporter ConfigMap
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources. Example: `postgres-exporter`.
    k8s_namespace: "postgres-exporter"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

> Apply the Postgres Exporter Secret

Builds the exporter PostgreSQL datasource for Kubernetes from the monitored host facts and applies the Secret that stores TLS material and connection data.

```yaml
- name: Apply the Postgres Exporter Secret
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources. Example: `postgres-exporter`.
    k8s_namespace: "postgres-exporter"
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. Example: `postgres-db-01`. The exporter builds its datasource from the referenced host's `postgres_user`, `postgres_password`, `ansible_host`, `postgres_port`, and `postgres_db` facts. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "postgres-db-01"
    # Provides the shared remote configuration directory used by Postgres Exporter. Example: `/opt/fabricx/postgres-exporter/config`.
    remote_config_dir: "/opt/fabricx/postgres-exporter/config"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the configuration directory mounted inside the container or pod.
    postgres_exporter_container_config_dir: /var/config
    # Sets the TLS private key file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_private_key_file: server.key
    # Sets the TLS certificate file name used under `postgres_exporter_remote_config_dir`/tls.
    postgres_exporter_tls_cert_file: server.crt
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/crypto/transfer
```

### k8s/crypto/rm

> Remove the Postgres Exporter Secret

Deletes the Postgres Exporter Secret from Kubernetes.

```yaml
- name: Remove the Postgres Exporter Secret
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources. Example: `postgres-exporter`.
    k8s_namespace: "postgres-exporter"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/crypto/rm
```

### prometheus/get_scrapers

> Build Prometheus scrape definitions for Postgres Exporter

Builds the `postgres_exporter_prometheus_scrape_services` fact for the Postgres Exporter hosts listed in `postgres_exporter_hosts`.The TLS CA path for each host derives from `fetched_artifacts_dir` and the current loop host.

```yaml
- name: Build Prometheus scrape definitions for Postgres Exporter
  vars:
    # Provides the control-node directory used to fetch or stage Postgres Exporter TLS artifacts. Example: `/tmp/postgres-exporter-artifacts`.
    fetched_artifacts_dir: "/tmp/postgres-exporter-artifacts"
    # Lists the inventory hosts that run Postgres Exporter and should be exposed to Prometheus. Example: `['postgres-exporter-a', 'postgres-exporter-b']`.
    postgres_exporter_hosts:
      - postgres-exporter-a
      - postgres-exporter-b
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: prometheus/get_scrapers
```
