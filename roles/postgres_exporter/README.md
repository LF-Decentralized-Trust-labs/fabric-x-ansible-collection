# hyperledger.fabricx.postgres_exporter

> Runs a [Prometheus Postgres Exporter](https://github.com/prometheus-community/postgres_exporter) to collect PostgreSQL metrics.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
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

## Tasks

### start

Start Postgres Exporter

Dispatches to the container or Kubernetes startup path for Postgres Exporter.

The backend selection is controlled by `postgres_exporter_use_container` and `postgres_exporter_use_k8s`.

```yaml
- name: Start Postgres Exporter
  vars:
    # Enables the container backend when set to `true`. The default derives from `postgres_exporter_use_k8s`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: start
```

### stop

Stop Postgres Exporter

Stops a container-based Postgres Exporter deployment.

This entry point only dispatches when `postgres_exporter_use_container` resolves to `true`.

```yaml
- name: Stop Postgres Exporter
  vars:
    # Enables the container backend when set to `true`. The default derives from `postgres_exporter_use_k8s`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: stop
```

### teardown

Remove Postgres Exporter runtime resources

Removes the active Postgres Exporter runtime resources for the enabled backend.

This dispatches to the container removal path or the Kubernetes removal path.

```yaml
- name: Remove Postgres Exporter runtime resources
  vars:
    # Enables the container backend when set to `true`. The default derives from `postgres_exporter_use_k8s`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: teardown
```

### wipe

Remove all Postgres Exporter artifacts

Removes runtime resources, TLS artifacts, and generated configuration for Postgres Exporter.

This entry point combines `teardown`, `crypto/rm`, and `config/rm`, so it validates the variables needed by all three paths.

```yaml
- name: Remove all Postgres Exporter artifacts
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: wipe
```

### fetch_logs

Fetch Postgres Exporter logs

Collects logs from the Postgres Exporter container or Kubernetes pod.

The backend selection is controlled by `postgres_exporter_use_container` and `postgres_exporter_use_k8s`.

```yaml
- name: Fetch Postgres Exporter logs
  vars:
    # Enables the container backend when set to `true`. The default derives from `postgres_exporter_use_k8s`.
    postgres_exporter_use_container: "{{ not postgres_exporter_use_k8s }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
    # Sets the Postgres Exporter container name. The default derives from `inventory_hostname`.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: fetch_logs
```

### ping

Check Postgres Exporter reachability

Checks whether the Postgres Exporter metrics port is reachable on the current host.

```yaml
- name: Check Postgres Exporter reachability
  vars:
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 1000
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: ping
```

### container/start

Start the Postgres Exporter container

Builds the exporter database connection string and starts the Postgres Exporter container.

The default `postgres_exporter_image` value derives from `postgres_exporter_registry_endpoint`, `postgres_exporter_image_name`, and `postgres_exporter_image_tag`.

```yaml
- name: Start the Postgres Exporter container
  vars:
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "string"
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Sets the registry endpoint used to build the default Postgres Exporter image reference. The default derives from the `POSTGRES_EXPORTER_REGISTRY_ENDPOINT` environment variable and falls back to `docker.io/prometheuscommunity`.
    postgres_exporter_registry_endpoint: "{{ lookup('env', 'POSTGRES_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prometheuscommunity' }}"
    # Sets the image name used to build the default `postgres_exporter_image` value.
    postgres_exporter_image_name: postgres-exporter
    # Sets the image tag used to build the default `postgres_exporter_image` value.
    postgres_exporter_image_tag: latest
    # Sets the full Postgres Exporter image reference. The default derives from `postgres_exporter_registry_endpoint`, `postgres_exporter_image_name`, and `postgres_exporter_image_tag`.
    postgres_exporter_image: "{{ postgres_exporter_registry_endpoint }}/{{ postgres_exporter_image_name }}:{{ postgres_exporter_image_tag }}"
    # Sets the Postgres Exporter container name. The default derives from `inventory_hostname`.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 1000
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
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

Stop the Postgres Exporter container

Stops the Postgres Exporter container.

```yaml
- name: Stop the Postgres Exporter container
  vars:
    # Sets the Postgres Exporter container name. The default derives from `inventory_hostname`.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: container/stop
```

### container/rm

Remove the Postgres Exporter container

Removes the Postgres Exporter container.

```yaml
- name: Remove the Postgres Exporter container
  vars:
    # Sets the Postgres Exporter container name. The default derives from `inventory_hostname`.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: container/rm
```

### container/fetch_logs

Fetch Postgres Exporter container logs

Fetches logs from the Postgres Exporter container.

```yaml
- name: Fetch Postgres Exporter container logs
  vars:
    # Sets the Postgres Exporter container name. The default derives from `inventory_hostname`.
    postgres_exporter_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: container/fetch_logs
```

### config/transfer

Generate and transfer Postgres Exporter configuration

Generates the Postgres Exporter configuration files and copies the PostgreSQL CA certificate when the monitored database uses TLS.

For Kubernetes deployments this also applies the ConfigMap.

```yaml
- name: Generate and transfer Postgres Exporter configuration
  vars:
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "string"
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Provides the control-node directory used to fetch or stage Postgres Exporter TLS artifacts.
    fetched_artifacts_dir: "string"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
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

Remove Postgres Exporter configuration

Removes generated Postgres Exporter configuration files from the remote host.

For Kubernetes deployments this also deletes the related ConfigMap.

```yaml
- name: Remove Postgres Exporter configuration
  vars:
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Enables the Kubernetes backend and Kubernetes cleanup path when set to `true`.
    postgres_exporter_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/rm
```

### config/transfer_grafana_dashboard

Transfer the packaged Grafana dashboard

Sets the packaged Postgres Exporter dashboard path and delegates dashboard copy to the Grafana role.

This entry point does not validate any Postgres Exporter variables because it only derives paths from `role_path`.

```yaml
- name: Transfer the packaged Grafana dashboard
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: config/transfer_grafana_dashboard
```

### crypto/setup

Generate Postgres Exporter TLS artifacts

Generates the Postgres Exporter TLS files when `postgres_exporter_use_tls` is true.

For Kubernetes deployments this also applies the Secret used by the pod.

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

Fetch Postgres Exporter TLS artifacts

Fetches the generated Postgres Exporter TLS CA certificate and server certificate to the control node.

This entry point only transfers files when `postgres_exporter_use_tls` is true.

```yaml
- name: Fetch Postgres Exporter TLS artifacts
  vars:
    # Provides the control-node directory used to fetch or stage Postgres Exporter TLS artifacts.
    fetched_artifacts_dir: "string"
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
    postgres_exporter_remote_config_dir: "{{ remote_config_dir }}"
    # Enables Postgres Exporter TLS assets and HTTPS listener configuration when set to `true`.
    postgres_exporter_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: crypto/fetch
```

### crypto/rm

Remove Postgres Exporter TLS artifacts

Removes generated Postgres Exporter TLS files from the remote host.

For Kubernetes deployments this also deletes the related Secret.

```yaml
- name: Remove Postgres Exporter TLS artifacts
  vars:
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
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

Generate Postgres Exporter TLS files with OpenSSL

Delegates self-signed certificate generation to the OpenSSL role using Postgres Exporter-specific file paths.

The default `postgres_exporter_remote_config_dir` value derives from `remote_config_dir`.

```yaml
- name: Generate Postgres Exporter TLS files with OpenSSL
  vars:
    # Provides organization metadata forwarded to the OpenSSL role. The role falls back to `inventory_hostname` when the organization domain is not provided.
    organization: {}
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
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

Start Postgres Exporter on Kubernetes

Applies the Service, optional NodePort Service, and Deployment for Postgres Exporter.

The NodePort Service is optional and only rendered when `postgres_exporter_k8s_use_node_port` is true.

The default `postgres_exporter_k8s_port_node_port` value derives from `postgres_exporter_port`, and the default `postgres_exporter_image` value derives from `postgres_exporter_registry_endpoint`, `postgres_exporter_image_name`, and `postgres_exporter_image_tag`.

```yaml
- name: Start Postgres Exporter on Kubernetes
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources.
    k8s_namespace: "string"
    # Sets the optional Kubernetes image pull secret used by the Postgres Exporter Deployment.
    k8s_image_pull_secret: "string"
    # Overrides the Deployment readiness probe initial delay. The template default is 10 seconds when this variable is unset.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Overrides the Deployment readiness probe period. The template default is 10 seconds when this variable is unset.
    k8s_readiness_probe_period_seconds: 1000
    # Overrides the Deployment readiness probe timeout. The template default is 5 seconds when this variable is unset.
    k8s_readiness_probe_timeout_seconds: 1000
    # Overrides the Deployment readiness probe failure threshold. The template default is 3 failures when this variable is unset.
    k8s_readiness_probe_failure_threshold: 1000
    # Overrides the Deployment liveness probe initial delay. The template default is 30 seconds when this variable is unset.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Overrides the Deployment liveness probe period. The template default is 15 seconds when this variable is unset.
    k8s_liveness_probe_period_seconds: 1000
    # Overrides the Deployment liveness probe timeout. The template default is 5 seconds when this variable is unset.
    k8s_liveness_probe_timeout_seconds: 1000
    # Overrides the Deployment liveness probe failure threshold. The template default is 5 failures when this variable is unset.
    k8s_liveness_probe_failure_threshold: 1000
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "string"
    # Sets the registry endpoint used to build the default Postgres Exporter image reference. The default derives from the `POSTGRES_EXPORTER_REGISTRY_ENDPOINT` environment variable and falls back to `docker.io/prometheuscommunity`.
    postgres_exporter_registry_endpoint: "{{ lookup('env', 'POSTGRES_EXPORTER_REGISTRY_ENDPOINT') or 'docker.io/prometheuscommunity' }}"
    # Sets the image name used to build the default `postgres_exporter_image` value.
    postgres_exporter_image_name: postgres-exporter
    # Sets the image tag used to build the default `postgres_exporter_image` value.
    postgres_exporter_image_tag: latest
    # Sets the full Postgres Exporter image reference. The default derives from `postgres_exporter_registry_endpoint`, `postgres_exporter_image_name`, and `postgres_exporter_image_tag`.
    postgres_exporter_image: "{{ postgres_exporter_registry_endpoint }}/{{ postgres_exporter_image_name }}:{{ postgres_exporter_image_tag }}"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments. The default derives from `inventory_hostname`.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Deployment wait timeout in seconds.
    postgres_exporter_k8s_wait_timeout: 120
    # Sets the pod filesystem group used by the Postgres Exporter Deployment.
    postgres_exporter_k8s_fs_group: 65534
    # Enables the optional NodePort Service used to expose Postgres Exporter externally from Kubernetes. When set to `true`, `postgres_exporter_k8s_port_node_port` is used to populate the Service's node port.
    postgres_exporter_k8s_use_node_port: false
    # Sets the NodePort value exposed by the optional Postgres Exporter Kubernetes Service. The default derives from `postgres_exporter_port` so the NodePort stays aligned with the exporter metrics port.
    postgres_exporter_k8s_port_node_port: "{{ postgres_exporter_port }}"
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 1000
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

Check Postgres Exporter node port reachability

Checks whether the optional Postgres Exporter NodePort Service is reachable.

The default `postgres_exporter_k8s_port_node_port` value derives from `postgres_exporter_port`.

```yaml
- name: Check Postgres Exporter node port reachability
  vars:
    # Sets the Postgres Exporter metrics port. Example: `9187`.
    postgres_exporter_port: 1000
    # Enables the optional NodePort Service used to expose Postgres Exporter externally from Kubernetes. When set to `true`, `postgres_exporter_k8s_port_node_port` is used to populate the Service's node port.
    postgres_exporter_k8s_use_node_port: false
    # Sets the NodePort value exposed by the optional Postgres Exporter Kubernetes Service. The default derives from `postgres_exporter_port` so the NodePort stays aligned with the exporter metrics port.
    postgres_exporter_k8s_port_node_port: "{{ postgres_exporter_port }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/ping
```

### k8s/rm

Remove Postgres Exporter Kubernetes resources

Removes the Postgres Exporter Deployment and Services from Kubernetes.

```yaml
- name: Remove Postgres Exporter Kubernetes resources
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources.
    k8s_namespace: "string"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments. The default derives from `inventory_hostname`.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/rm
```

### k8s/fetch_logs

Fetch Postgres Exporter pod logs

Delegates Postgres Exporter pod log collection to the shared Kubernetes role.

```yaml
- name: Fetch Postgres Exporter pod logs
  vars:
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments. The default derives from `inventory_hostname`.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

Apply the Postgres Exporter ConfigMap

Ensures the Kubernetes namespace exists and applies the ConfigMap rendered from the local Postgres Exporter configuration files.

The default `postgres_exporter_remote_config_dir` value derives from `remote_config_dir`.

```yaml
- name: Apply the Postgres Exporter ConfigMap
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources.
    k8s_namespace: "string"
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "string"
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments. The default derives from `inventory_hostname`.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
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

Remove the Postgres Exporter ConfigMap

Deletes the Postgres Exporter ConfigMap from Kubernetes.

```yaml
- name: Remove the Postgres Exporter ConfigMap
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources.
    k8s_namespace: "string"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments. The default derives from `inventory_hostname`.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/config/rm
```

### k8s/crypto/transfer

Apply the Postgres Exporter Secret

Builds the exporter database connection string for Kubernetes and applies the Secret that stores TLS material and connection data.

The default `postgres_exporter_remote_config_dir` value derives from `remote_config_dir`.

```yaml
- name: Apply the Postgres Exporter Secret
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources.
    k8s_namespace: "string"
    # Sets the inventory host name of the PostgreSQL instance that Postgres Exporter monitors. The referenced host must expose the Postgres role facts consumed through `hostvars[postgres_db_host]`.
    postgres_db_host: "string"
    # Provides the shared remote configuration directory consumed by the default value of `postgres_exporter_remote_config_dir`. This option is only required when callers rely on that default instead of setting `postgres_exporter_remote_config_dir` explicitly.
    remote_config_dir: "string"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments. The default derives from `inventory_hostname`.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote directory that stores Postgres Exporter configuration and TLS files. The default derives from `remote_config_dir`.
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

Remove the Postgres Exporter Secret

Deletes the Postgres Exporter Secret from Kubernetes.

```yaml
- name: Remove the Postgres Exporter Secret
  vars:
    # Sets the Kubernetes namespace used for Postgres Exporter resources.
    k8s_namespace: "string"
    # Sets the Kubernetes resource base name used for ConfigMaps, Secrets, Services, and Deployments. The default derives from `inventory_hostname`.
    postgres_exporter_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: k8s/crypto/rm
```

### prometheus/get_scrapers

Build Prometheus scrape definitions for Postgres Exporter

Builds the `postgres_exporter_prometheus_scrape_services` fact for the Postgres Exporter hosts listed in `postgres_exporter_hosts`.

The TLS CA path for each host derives from `fetched_artifacts_dir` and the current loop host.

```yaml
- name: Build Prometheus scrape definitions for Postgres Exporter
  vars:
    # Provides the control-node directory used to fetch or stage Postgres Exporter TLS artifacts.
    fetched_artifacts_dir: "string"
    # Lists the inventory hosts that run Postgres Exporter and should be exposed to Prometheus.
    postgres_exporter_hosts: ["entry1", "entry2"]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.postgres_exporter
    tasks_from: prometheus/get_scrapers
```
