
# hyperledger.fabricx.yugabyte

> Runs a Yugabyte distributed DB cluster (container and Kubernetes modes).


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [start](#task-start)
  - [stop](#task-stop)
  - [teardown](#task-teardown)
  - [wipe](#task-wipe)
  - [fetch_logs](#task-fetch_logs)
  - [ping](#task-ping)
  - [k8s/ping](#task-k8s-ping)
  - [crypto/setup](#task-crypto-setup)
  - [crypto/fetch](#task-crypto-fetch)
  - [crypto/rm](#task-crypto-rm)
  - [crypto/openssl/generate_csr](#task-crypto-openssl-generate_csr)
  - [crypto/openssl/fetch_csr](#task-crypto-openssl-fetch_csr)
  - [crypto/openssl/transfer_cert](#task-crypto-openssl-transfer_cert)
  - [crypto/cryptogen/transfer](#task-crypto-cryptogen-transfer)
  - [crypto/fabric_ca/enroll](#task-crypto-fabric_ca-enroll)
  - [config/transfer](#task-config-transfer)
  - [config/rm](#task-config-rm)
  - [config/transfer_grafana_dashboard](#task-config-transfer_grafana_dashboard)
  - [container/start](#task-container-start)
  - [container/stop](#task-container-stop)
  - [container/rm](#task-container-rm)
  - [container/fetch_logs](#task-container-fetch_logs)
  - [container/master/start](#task-container-master-start)
  - [container/tablet/start](#task-container-tablet-start)
  - [k8s/start](#task-k8s-start)
  - [k8s/rm](#task-k8s-rm)
  - [k8s/fetch_logs](#task-k8s-fetch_logs)
  - [k8s/config/transfer](#task-k8s-config-transfer)
  - [k8s/master/start](#task-k8s-master-start)
  - [k8s/master/rm](#task-k8s-master-rm)
  - [k8s/tablet/start](#task-k8s-tablet-start)
  - [k8s/tablet/rm](#task-k8s-tablet-rm)
  - [k8s/crypto/transfer](#task-k8s-crypto-transfer)
  - [data/rm](#task-data-rm)
  - [prometheus/get_scrapers](#task-prometheus-get_scrapers)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-start"></a>

### start

Start a YugabyteDB cluster


Builds the master and tablet topology facts and dispatches to the container or Kubernetes startup path.


```yaml
- name: Start a YugabyteDB cluster
  vars:
    # Lists the inventory hosts that belong to the YugabyteDB cluster.
    yugabyte_cluster: ["entry1", "entry2"]
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Enables container mode for the YugabyteDB role. The default derives from `yugabyte_use_k8s`.
    yugabyte_use_container: "{{ not yugabyte_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: start
```

<a id="task-stop"></a>

### stop

Stop YugabyteDB runtime


Dispatches to the container stop path when the role is running in container mode.


```yaml
- name: Stop YugabyteDB runtime
  vars:
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Enables container mode for the YugabyteDB role. The default derives from `yugabyte_use_k8s`.
    yugabyte_use_container: "{{ not yugabyte_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: stop
```

<a id="task-teardown"></a>

### teardown

Remove YugabyteDB runtime artifacts


Removes running Kubernetes resources or containers, then deletes persisted data.


```yaml
- name: Remove YugabyteDB runtime artifacts
  vars:
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Enables container mode for the YugabyteDB role. The default derives from `yugabyte_use_k8s`.
    yugabyte_use_container: "{{ not yugabyte_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: teardown
```

<a id="task-wipe"></a>

### wipe

Wipe YugabyteDB state


Runs teardown and removes the role-managed crypto and configuration files.


```yaml
- name: Wipe YugabyteDB state
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: wipe
```

<a id="task-fetch_logs"></a>

### fetch_logs

Collect YugabyteDB logs


Dispatches to the container or Kubernetes log collection path.


```yaml
- name: Collect YugabyteDB logs
  vars:
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Enables container mode for the YugabyteDB role. The default derives from `yugabyte_use_k8s`.
    yugabyte_use_container: "{{ not yugabyte_use_k8s }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: fetch_logs
```

<a id="task-ping"></a>

### ping

Check YugabyteDB service ports


Selects the expected ports for a master or tablet host and delegates the reachability check.


```yaml
- name: Check YugabyteDB service ports
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node.
    yugabyte_component_type: "string"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Sets the master webserver port.
    yugabyte_master_webserver_port: 7000
    # Sets the master RPC bind port.
    yugabyte_master_rpc_bind_port: 7100
    # Sets the tablet YSQL bind port.
    yugabyte_tablet_pgsql_bind_port: 5433
    # Sets the tablet RPC bind port.
    yugabyte_tablet_rpc_bind_port: 9100
    # Sets the tablet webserver port.
    yugabyte_tablet_webserver_port: 9000
    # Sets the tablet YSQL web UI port.
    yugabyte_tablet_pgsql_web_port: 13000
    # Sets the tablet YCQL bind port.
    yugabyte_tablet_cql_bind_port: 9042
    # Sets the tablet YCQL web UI port.
    yugabyte_tablet_cql_web_port: 12000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: ping
```

<a id="task-k8s-ping"></a>

### k8s/ping

Check YugabyteDB Kubernetes NodePorts


Checks the configured YugabyteDB Kubernetes NodePort Services for the current master or tablet host when NodePort exposure is enabled.


```yaml
- name: Check YugabyteDB Kubernetes NodePorts
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node.
    yugabyte_component_type: "string"
    # Enables creation of the master and tablet NodePort Services for YugabyteDB Kubernetes deployments. The flag also enables the matching NodePort reachability checks in `k8s/ping`.
    yugabyte_k8s_use_node_port: false
    # Optionally sets the NodePort used to expose the master RPC service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_master_rpc_node_port: 1000
    # Optionally sets the NodePort used to expose the master webserver service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_master_webserver_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet YSQL service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_pgsql_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet RPC service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_rpc_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet webserver service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_webserver_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet YSQL web UI service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_pgsql_web_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet YCQL bind service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_cql_bind_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet YCQL web UI service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_cql_web_node_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/ping
```

<a id="task-crypto-setup"></a>

### crypto/setup

Prepare YugabyteDB TLS assets


Transfers or enrolls TLS material for YugabyteDB and creates the Kubernetes Secret when needed.


```yaml
- name: Prepare YugabyteDB TLS assets
  vars:
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Provides the organization metadata consumed by the crypto entry points. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/setup
```

<a id="task-crypto-fetch"></a>

### crypto/fetch

Fetch YugabyteDB TLS certificates


Copies the generated node and CA certificates from the remote host to the control node.


```yaml
- name: Fetch YugabyteDB TLS certificates
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/fetch
```

<a id="task-crypto-rm"></a>

### crypto/rm

Remove YugabyteDB TLS artifacts


Deletes the remote TLS directory and the Kubernetes Secret when Kubernetes mode is enabled.


```yaml
- name: Remove YugabyteDB TLS artifacts
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/rm
```

<a id="task-crypto-openssl-generate_csr"></a>

### crypto/openssl/generate_csr

Generate a YugabyteDB TLS CSR


Builds the SAN list and delegates CSR generation to the OpenSSL role.


```yaml
- name: Generate a YugabyteDB TLS CSR
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/generate_csr
```

<a id="task-crypto-openssl-fetch_csr"></a>

### crypto/openssl/fetch_csr

Fetch a YugabyteDB TLS CSR


Copies the CSR and OpenSSL extension file from the remote host to the control node.


```yaml
- name: Fetch a YugabyteDB TLS CSR
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/fetch_csr
```

<a id="task-crypto-openssl-transfer_cert"></a>

### crypto/openssl/transfer_cert

Transfer a signed YugabyteDB TLS certificate


Copies the signed node certificate and trusted CA certificate to the remote host.


```yaml
- name: Transfer a signed YugabyteDB TLS certificate
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled.
    fetched_artifacts_dir: "string"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/transfer_cert
```

<a id="task-crypto-cryptogen-transfer"></a>

### crypto/cryptogen/transfer

Copy cryptogen TLS material for YugabyteDB


Transfers the TLS key, certificate, and CA certificate generated by cryptogen to the target host.


```yaml
- name: Copy cryptogen TLS material for YugabyteDB
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores cryptogen-generated artifacts.
    cryptogen_artifacts_dir: "string"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/cryptogen/transfer
```

<a id="task-crypto-fabric_ca-enroll"></a>

### crypto/fabric_ca/enroll

Enroll YugabyteDB TLS material with Fabric CA


Copies the Fabric CA TLS root when needed and delegates the TLS enrollment flow to the Fabric CA role.


```yaml
- name: Enroll YugabyteDB TLS material with Fabric CA
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled.
    fetched_artifacts_dir: "string"
    # Provides the externally reachable host name or address added to TLS SAN entries.
    actual_host: "string"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/fabric_ca/enroll
```

<a id="task-config-transfer"></a>

### config/transfer

Transfer YugabyteDB initialization config


Renders the initialization SQL script and creates the Kubernetes ConfigMap when Kubernetes mode is enabled.


```yaml
- name: Transfer YugabyteDB initialization config
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Sets the YugabyteDB database name created by the initialization SQL script.
    yugabyte_db: "string"
    # Sets the YugabyteDB database user created by the initialization SQL script.
    yugabyte_user: "string"
    # Sets the password for the YugabyteDB database user. Store this value in Ansible Vault.
    yugabyte_password: "string"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/transfer
```

<a id="task-config-rm"></a>

### config/rm

Remove YugabyteDB configuration


Deletes the remote configuration directory and the Kubernetes ConfigMap when Kubernetes mode is enabled.


```yaml
- name: Remove YugabyteDB configuration
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/rm
```

<a id="task-config-transfer_grafana_dashboard"></a>

### config/transfer_grafana_dashboard

Transfer the YugabyteDB Grafana dashboard


Selects the built-in dashboard JSON file and delegates the copy step to the Grafana role.


```yaml
- name: Transfer the YugabyteDB Grafana dashboard
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/transfer_grafana_dashboard
```

<a id="task-container-start"></a>

### container/start

Dispatch YugabyteDB container startup


Selects the master or tablet container startup path for the current host.


```yaml
- name: Dispatch YugabyteDB container startup
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node.
    yugabyte_component_type: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/start
```

<a id="task-container-stop"></a>

### container/stop

Stop a YugabyteDB container


Stops the container associated with the current YugabyteDB host.


```yaml
- name: Stop a YugabyteDB container
  vars:
    # Names the YugabyteDB container associated with the current host. The default derives from `inventory_hostname`.
    yugabyte_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/stop
```

<a id="task-container-rm"></a>

### container/rm

Remove a YugabyteDB container


Deletes the container associated with the current YugabyteDB host.


```yaml
- name: Remove a YugabyteDB container
  vars:
    # Names the YugabyteDB container associated with the current host. The default derives from `inventory_hostname`.
    yugabyte_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/rm
```

<a id="task-container-fetch_logs"></a>

### container/fetch_logs

Fetch logs from a YugabyteDB container


Delegates log collection for the current YugabyteDB container.


```yaml
- name: Fetch logs from a YugabyteDB container
  vars:
    # Names the YugabyteDB container associated with the current host. The default derives from `inventory_hostname`.
    yugabyte_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/fetch_logs
```

<a id="task-container-master-start"></a>

### container/master/start

Start a YugabyteDB master container


Creates the data directory, assembles the master command line, and starts the master container.


```yaml
- name: Start a YugabyteDB master container
  vars:
    # Sets the shared remote data directory consumed by YugabyteDB.
    remote_data_dir: "string"
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Sets the remote data directory used by YugabyteDB tasks. The default derives from `remote_data_dir`.
    yugabyte_remote_data_dir: "{{ remote_data_dir }}"
    # Sets the in-container data directory used by YugabyteDB.
    yugabyte_container_data_dir: /var/data
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the YugabyteDB container associated with the current host. The default derives from `inventory_hostname`.
    yugabyte_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image. The default derives from `YUGABYTE_REGISTRY_ENDPOINT` or falls back to a built-in registry.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Sets the YugabyteDB container image. The default derives from `yugabyte_registry_endpoint`, `yugabyte_image_name`, and `yugabyte_image_tag`.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks.
    yugabyte_master_endpoints: "string"
    # Sets the master RPC bind port.
    yugabyte_master_rpc_bind_port: 7100
    # Sets the master webserver port.
    yugabyte_master_webserver_port: 7000
    # Provides the ordered list of master hosts used to compute replication factors.
    yugabyte_master_hosts: ["entry1", "entry2"]
    # Sets the YugabyteDB log verbosity threshold.
    yugabyte_logs_level: 3
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables node-to-node TLS for YugabyteDB. The default derives from `yugabyte_use_tls`.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access. The default derives from `yugabyte_use_tls`.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver. The default derives from `yugabyte_use_tls`.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/master/start
```

<a id="task-container-tablet-start"></a>

### container/tablet/start

Start a YugabyteDB tablet container


Creates the data directory, assembles the tablet command line, starts the container, and initializes the database on the first tablet.


```yaml
- name: Start a YugabyteDB tablet container
  vars:
    # Sets the shared remote data directory consumed by YugabyteDB.
    remote_data_dir: "string"
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Sets the remote data directory used by YugabyteDB tasks. The default derives from `remote_data_dir`.
    yugabyte_remote_data_dir: "{{ remote_data_dir }}"
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the in-container data directory used by YugabyteDB.
    yugabyte_container_data_dir: /var/data
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Names the YugabyteDB container associated with the current host. The default derives from `inventory_hostname`.
    yugabyte_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image. The default derives from `YUGABYTE_REGISTRY_ENDPOINT` or falls back to a built-in registry.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Sets the YugabyteDB container image. The default derives from `yugabyte_registry_endpoint`, `yugabyte_image_name`, and `yugabyte_image_tag`.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks.
    yugabyte_master_endpoints: "string"
    # Sets the tablet YSQL bind port.
    yugabyte_tablet_pgsql_bind_port: 5433
    # Sets the tablet RPC bind port.
    yugabyte_tablet_rpc_bind_port: 9100
    # Sets the tablet webserver port.
    yugabyte_tablet_webserver_port: 9000
    # Sets the tablet YSQL web UI port.
    yugabyte_tablet_pgsql_web_port: 13000
    # Sets the tablet YCQL bind port.
    yugabyte_tablet_cql_bind_port: 9042
    # Sets the tablet YCQL web UI port.
    yugabyte_tablet_cql_web_port: 12000
    # Provides the ordered list of tablet hosts used to initialize the first tablet.
    yugabyte_tablet_hosts: ["entry1", "entry2"]
    # Sets the YugabyteDB log verbosity threshold.
    yugabyte_logs_level: 3
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables node-to-node TLS for YugabyteDB. The default derives from `yugabyte_use_tls`.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access. The default derives from `yugabyte_use_tls`.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver. The default derives from `yugabyte_use_tls`.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/tablet/start
```

<a id="task-k8s-start"></a>

### k8s/start

Dispatch YugabyteDB Kubernetes startup


Selects the master or tablet Kubernetes startup path for the current host.


```yaml
- name: Dispatch YugabyteDB Kubernetes startup
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node.
    yugabyte_component_type: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/start
```

<a id="task-k8s-rm"></a>

### k8s/rm

Dispatch YugabyteDB Kubernetes removal


Selects the master or tablet Kubernetes removal path for the current host.


```yaml
- name: Dispatch YugabyteDB Kubernetes removal
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node.
    yugabyte_component_type: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/rm
```

<a id="task-k8s-fetch_logs"></a>

### k8s/fetch_logs

Fetch logs from YugabyteDB pods


Delegates pod log collection for the Kubernetes resource associated with the current host.


```yaml
- name: Fetch logs from YugabyteDB pods
  vars:
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/fetch_logs
```

<a id="task-k8s-config-transfer"></a>

### k8s/config/transfer

Create a YugabyteDB ConfigMap


Creates the ConfigMap that exposes the initialization SQL script to tablet pods.


```yaml
- name: Create a YugabyteDB ConfigMap
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node.
    yugabyte_component_type: "string"
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/config/transfer
```

<a id="task-k8s-master-start"></a>

### k8s/master/start

Start a YugabyteDB master StatefulSet


Applies the master Services and StatefulSet for the current YugabyteDB master node.


```yaml
- name: Start a YugabyteDB master StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
    # Enables creation of the master and tablet NodePort Services for YugabyteDB Kubernetes deployments. The flag also enables the matching NodePort reachability checks in `k8s/ping`.
    yugabyte_k8s_use_node_port: false
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the YugabyteDB container image. The default derives from `yugabyte_registry_endpoint`, `yugabyte_image_name`, and `yugabyte_image_tag`.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image. The default derives from `YUGABYTE_REGISTRY_ENDPOINT` or falls back to a built-in registry.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks.
    yugabyte_master_endpoints: "string"
    # Sets the master RPC bind port.
    yugabyte_master_rpc_bind_port: 7100
    # Sets the master webserver port.
    yugabyte_master_webserver_port: 7000
    # Provides the ordered list of master hosts used to compute replication factors.
    yugabyte_master_hosts: ["entry1", "entry2"]
    # Sets the YugabyteDB log verbosity threshold.
    yugabyte_logs_level: 3
    # Sets the in-container data directory used by YugabyteDB.
    yugabyte_container_data_dir: /var/data
    # Waits for YugabyteDB Kubernetes resources to become ready.
    yugabyte_k8s_wait: true
    # Sets the Kubernetes readiness wait timeout in seconds.
    yugabyte_k8s_wait_timeout: 300
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables node-to-node TLS for YugabyteDB. The default derives from `yugabyte_use_tls`.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access. The default derives from `yugabyte_use_tls`.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver. The default derives from `yugabyte_use_tls`.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
    # Optionally sets the NodePort used to expose the master RPC service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_master_rpc_node_port: 1000
    # Optionally sets the NodePort used to expose the master webserver service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_master_webserver_node_port: 1000
    # Sets the image pull secret used by Kubernetes deployments when defined.
    k8s_image_pull_secret: "string"
    # Sets the storage class used by Kubernetes PersistentVolumeClaims when defined.
    k8s_storage_class: "string"
    # Sets the requested persistent storage size for Kubernetes deployments. Example: `20Gi`.
    k8s_storage_size: "string"
    # Overrides the readiness probe initial delay used by Kubernetes templates when defined.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Overrides the readiness probe period used by Kubernetes templates when defined.
    k8s_readiness_probe_period_seconds: 1000
    # Overrides the readiness probe timeout used by Kubernetes templates when defined.
    k8s_readiness_probe_timeout_seconds: 1000
    # Overrides the readiness probe failure threshold used by Kubernetes templates when defined.
    k8s_readiness_probe_failure_threshold: 1000
    # Overrides the liveness probe initial delay used by Kubernetes templates when defined.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Overrides the liveness probe period used by Kubernetes templates when defined.
    k8s_liveness_probe_period_seconds: 1000
    # Overrides the liveness probe timeout used by Kubernetes templates when defined.
    k8s_liveness_probe_timeout_seconds: 1000
    # Overrides the liveness probe failure threshold used by Kubernetes templates when defined.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/master/start
```

<a id="task-k8s-master-rm"></a>

### k8s/master/rm

Remove a YugabyteDB master StatefulSet


Deletes the master StatefulSet and its Services for the current YugabyteDB master node.


```yaml
- name: Remove a YugabyteDB master StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/master/rm
```

<a id="task-k8s-tablet-start"></a>

### k8s/tablet/start

Start a YugabyteDB tablet StatefulSet


Applies the tablet Services and StatefulSet for the current YugabyteDB tablet node, then initializes the database on the first tablet.


```yaml
- name: Start a YugabyteDB tablet StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
    # Enables creation of the master and tablet NodePort Services for YugabyteDB Kubernetes deployments. The flag also enables the matching NodePort reachability checks in `k8s/ping`.
    yugabyte_k8s_use_node_port: false
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the YugabyteDB container image. The default derives from `yugabyte_registry_endpoint`, `yugabyte_image_name`, and `yugabyte_image_tag`.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image. The default derives from `YUGABYTE_REGISTRY_ENDPOINT` or falls back to a built-in registry.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks.
    yugabyte_master_endpoints: "string"
    # Sets the tablet YSQL bind port.
    yugabyte_tablet_pgsql_bind_port: 5433
    # Sets the tablet RPC bind port.
    yugabyte_tablet_rpc_bind_port: 9100
    # Sets the tablet webserver port.
    yugabyte_tablet_webserver_port: 9000
    # Sets the tablet YSQL web UI port.
    yugabyte_tablet_pgsql_web_port: 13000
    # Sets the tablet YCQL bind port.
    yugabyte_tablet_cql_bind_port: 9042
    # Sets the tablet YCQL web UI port.
    yugabyte_tablet_cql_web_port: 12000
    # Sets the YugabyteDB log verbosity threshold.
    yugabyte_logs_level: 3
    # Sets the in-container data directory used by YugabyteDB.
    yugabyte_container_data_dir: /var/data
    # Waits for YugabyteDB Kubernetes resources to become ready.
    yugabyte_k8s_wait: true
    # Sets the Kubernetes readiness wait timeout in seconds.
    yugabyte_k8s_wait_timeout: 300
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables node-to-node TLS for YugabyteDB. The default derives from `yugabyte_use_tls`.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access. The default derives from `yugabyte_use_tls`.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver. The default derives from `yugabyte_use_tls`.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
    # Optionally sets the NodePort used to expose the tablet YSQL service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_pgsql_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet RPC service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_rpc_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet webserver service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_webserver_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet YSQL web UI service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_pgsql_web_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet YCQL bind service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_cql_bind_node_port: 1000
    # Optionally sets the NodePort used to expose the tablet YCQL web UI service when `yugabyte_k8s_use_node_port` is enabled.
    yugabyte_k8s_tablet_cql_web_node_port: 1000
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Provides the ordered list of tablet hosts used to initialize the first tablet.
    yugabyte_tablet_hosts: ["entry1", "entry2"]
    # Sets the image pull secret used by Kubernetes deployments when defined.
    k8s_image_pull_secret: "string"
    # Sets the storage class used by Kubernetes PersistentVolumeClaims when defined.
    k8s_storage_class: "string"
    # Sets the requested persistent storage size for Kubernetes deployments. Example: `20Gi`.
    k8s_storage_size: "string"
    # Overrides the readiness probe initial delay used by Kubernetes templates when defined.
    k8s_readiness_probe_initial_delay_seconds: 1000
    # Overrides the readiness probe period used by Kubernetes templates when defined.
    k8s_readiness_probe_period_seconds: 1000
    # Overrides the readiness probe timeout used by Kubernetes templates when defined.
    k8s_readiness_probe_timeout_seconds: 1000
    # Overrides the readiness probe failure threshold used by Kubernetes templates when defined.
    k8s_readiness_probe_failure_threshold: 1000
    # Overrides the liveness probe initial delay used by Kubernetes templates when defined.
    k8s_liveness_probe_initial_delay_seconds: 1000
    # Overrides the liveness probe period used by Kubernetes templates when defined.
    k8s_liveness_probe_period_seconds: 1000
    # Overrides the liveness probe timeout used by Kubernetes templates when defined.
    k8s_liveness_probe_timeout_seconds: 1000
    # Overrides the liveness probe failure threshold used by Kubernetes templates when defined.
    k8s_liveness_probe_failure_threshold: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/tablet/start
```

<a id="task-k8s-tablet-rm"></a>

### k8s/tablet/rm

Remove a YugabyteDB tablet StatefulSet


Deletes the tablet StatefulSet and its Services for the current YugabyteDB tablet node.


```yaml
- name: Remove a YugabyteDB tablet StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/tablet/rm
```

<a id="task-k8s-crypto-transfer"></a>

### k8s/crypto/transfer

Create a YugabyteDB TLS Secret


Creates the Kubernetes Secret that exposes the YugabyteDB TLS key pair and CA certificate.


```yaml
- name: Create a YugabyteDB TLS Secret
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
    # Sets the shared remote configuration directory consumed by YugabyteDB.
    remote_config_dir: "string"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote configuration directory used by YugabyteDB tasks. The default derives from `remote_config_dir`.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/crypto/transfer
```

<a id="task-data-rm"></a>

### data/rm

Remove YugabyteDB persisted data


Deletes the local data directory in container mode or the Kubernetes PVC in Kubernetes mode.


```yaml
- name: Remove YugabyteDB persisted data
  vars:
    # Sets the shared remote data directory consumed by YugabyteDB.
    remote_data_dir: "string"
    # Enables container mode for the YugabyteDB role. The default derives from `yugabyte_use_k8s`.
    yugabyte_use_container: "{{ not yugabyte_use_k8s }}"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Sets the remote data directory used by YugabyteDB tasks. The default derives from `remote_data_dir`.
    yugabyte_remote_data_dir: "{{ remote_data_dir }}"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled. The default derives from `inventory_hostname`.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: data/rm
```

<a id="task-prometheus-get_scrapers"></a>

### prometheus/get_scrapers

Build Prometheus scrapers for YugabyteDB


Groups YugabyteDB hosts by cluster and assembles the Prometheus scrape configuration for their exposed metrics endpoints.


```yaml
- name: Build Prometheus scrapers for YugabyteDB
  vars:
    # Lists the inventory hosts that belong to the YugabyteDB clusters monitored by Prometheus.
    yugabyte_hosts: ["entry1", "entry2"]
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: prometheus/get_scrapers
```


