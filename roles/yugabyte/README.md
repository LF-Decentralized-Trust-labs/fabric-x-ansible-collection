# hyperledger.fabricx.yugabyte

> Deploys and manages YugabyteDB masters and tablet servers for Fabric-X in container or Kubernetes mode, including TLS, initialization config, logs, data cleanup, and Prometheus scraper metadata.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)
  - [k8s/ping](#k8sping)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate\_csr](#cryptoopensslgenerate_csr)
  - [crypto/openssl/fetch\_csr](#cryptoopensslfetch_csr)
  - [crypto/openssl/transfer\_cert](#cryptoopenssltransfer_cert)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric\_ca/enroll](#cryptofabric_caenroll)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [config/transfer\_grafana\_dashboard](#configtransfer_grafana_dashboard)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [container/master/start](#containermasterstart)
  - [container/tablet/start](#containertabletstart)
  - [k8s/start](#k8sstart)
  - [k8s/rm](#k8srm)
  - [k8s/fetch\_logs](#k8sfetch_logs)
  - [k8s/config/transfer](#k8sconfigtransfer)
  - [k8s/master/start](#k8smasterstart)
  - [k8s/master/rm](#k8smasterrm)
  - [k8s/tablet/start](#k8stabletstart)
  - [k8s/tablet/rm](#k8stabletrm)
  - [k8s/crypto/transfer](#k8scryptotransfer)
  - [data/rm](#datarm)
  - [prometheus/get\_scrapers](#prometheusget_scrapers)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)
  - [openshift/ping](#openshiftping)
  - [openshift/master/start](#openshiftmasterstart)
  - [openshift/master/rm](#openshiftmasterrm)
  - [openshift/tablet/start](#openshifttabletstart)
  - [openshift/tablet/rm](#openshifttabletrm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.yugabyte
```

## Tasks

### start

> Start a YugabyteDB cluster

Builds master and tablet topology facts from `yugabyte_cluster`, derives the master RPC endpoint list, and dispatches each host to the container or Kubernetes startup path. Master hosts run `yb-master` with a replication factor based on the master host list; tablet hosts run `yb-tserver` and the first tablet initializes the configured database.

```yaml
- name: Start a YugabyteDB cluster
  vars:
    # Lists the inventory hosts that belong to the YugabyteDB cluster. Example: `['yb-master-1', 'yb-master-2', 'yb-master-3', 'yb-tserver-1', 'yb-tserver-2', 'yb-tserver-3']`.
    yugabyte_cluster:
      - "yb-master-1"
      - "yb-master-2"
      - "yb-master-3"
      - "yb-tserver-1"
      - "yb-tserver-2"
      - "yb-tserver-3"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Enables container mode for the YugabyteDB role.
    yugabyte_use_container: "{{ (not yugabyte_use_k8s) and (not yugabyte_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: start
```

### stop

> Stop YugabyteDB runtime

Stops the YugabyteDB runtime for container deployments. Kubernetes mode is managed through the removal entry points because StatefulSets and Services are reconciled resources.

```yaml
- name: Stop YugabyteDB runtime
  vars:
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Enables container mode for the YugabyteDB role.
    yugabyte_use_container: "{{ (not yugabyte_use_k8s) and (not yugabyte_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: stop
```

### teardown

> Remove YugabyteDB runtime artifacts

Removes the active YugabyteDB runtime in the selected deployment mode and then removes persisted role-managed data. Container mode deletes the running container and host data directory; Kubernetes mode deletes StatefulSets, Services, optional NodePort Services, and PVCs.

```yaml
- name: Remove YugabyteDB runtime artifacts
  vars:
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Enables container mode for the YugabyteDB role.
    yugabyte_use_container: "{{ (not yugabyte_use_k8s) and (not yugabyte_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: teardown
```

### wipe

> Wipe YugabyteDB state

Runs teardown, removes persisted data, and deletes role-managed TLS and initialization configuration artifacts. Use this entry point when the YugabyteDB node should be returned to a clean state before regeneration.

```yaml
- name: Wipe YugabyteDB state
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: wipe
```

### fetch_logs

> Collect YugabyteDB logs

Collects YugabyteDB logs through the selected deployment mode. Container mode fetches logs from the named container; Kubernetes mode fetches pod logs selected by the resource labels.

```yaml
- name: Collect YugabyteDB logs
  vars:
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Enables container mode for the YugabyteDB role.
    yugabyte_use_container: "{{ (not yugabyte_use_k8s) and (not yugabyte_use_openshift) }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: fetch_logs
```

### ping

> Check YugabyteDB service ports

Selects the expected master or tablet service ports for the current host and delegates reachability checks. Masters expose RPC and webserver ports; tablets expose YSQL, RPC, webserver, YSQL web UI, YCQL, and YCQL web UI ports.

```yaml
- name: Check YugabyteDB service ports
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
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

### k8s/ping

> Check that the YugabyteDB Kubernetes service is reachable

Probes configured Kubernetes NodePort values and LoadBalancer-exposed service ports for external reachability.

```yaml
- name: Check that the YugabyteDB Kubernetes service is reachable
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Kubernetes NodePort value used by the external master RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32100`.
    yugabyte_k8s_master_rpc_node_port: 32100
    # Kubernetes NodePort value used by the external master webserver Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32000`.
    yugabyte_k8s_master_webserver_node_port: 32000
    # Kubernetes NodePort value used by the external tablet YSQL Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31433`.
    yugabyte_k8s_tablet_pgsql_node_port: 31433
    # Kubernetes NodePort value used by the external tablet RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32101`.
    yugabyte_k8s_tablet_rpc_node_port: 32101
    # Kubernetes NodePort value used by the external tablet webserver Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32001`.
    yugabyte_k8s_tablet_webserver_node_port: 32001
    # Kubernetes NodePort value used by the external tablet YSQL web UI Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32300`.
    yugabyte_k8s_tablet_pgsql_web_node_port: 32300
    # Kubernetes NodePort value used by the external tablet YCQL bind Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32042`.
    yugabyte_k8s_tablet_cql_bind_node_port: 32042
    # Kubernetes NodePort value used by the external tablet YCQL web UI Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32200`.
    yugabyte_k8s_tablet_cql_web_node_port: 32200
    # Set to `true` to create a LoadBalancer Service entry that exposes the master RPC port externally. When undefined or `false`, the master RPC port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_master_rpc_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the master webserver port externally. When undefined or `false`, the master webserver port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_master_webserver_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YSQL port externally. When undefined or `false`, the tablet YSQL port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_pgsql_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet RPC port externally. When undefined or `false`, the tablet RPC port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_rpc_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet webserver port externally. When undefined or `false`, the tablet webserver port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_webserver_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YSQL web UI port externally. When undefined or `false`, the tablet YSQL web UI port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_pgsql_web_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YCQL bind port externally. When undefined or `false`, the tablet YCQL bind port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_cql_bind_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YCQL web UI port externally. When undefined or `false`, the tablet YCQL web UI port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_cql_web_port: false
    # Sets the master RPC bind port.
    yugabyte_master_rpc_bind_port: 7100
    # Sets the master webserver port.
    yugabyte_master_webserver_port: 7000
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
    tasks_from: k8s/ping
```

### crypto/setup

> Prepare YugabyteDB TLS assets

Prepares TLS assets for YugabyteDB when TLS is enabled, using the configured crypto source. The flow can generate CSRs, fetch certificates, transfer cryptogen material, enroll through Fabric CA, and create the Kubernetes Secret used by pods.

```yaml
- name: Prepare YugabyteDB TLS assets
  vars:
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Provides the organization metadata consumed by the crypto entry points. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'yb-tserver-1', 'secret': 'yb-tserver-1pw'}, 'fabric_ca_host': 'ca-org1'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "yb-tserver-1"
        secret: "yb-tserver-1pw"
      fabric_ca_host: "ca-org1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/setup
```

### crypto/fetch

> Fetch YugabyteDB TLS certificates

Copies generated YugabyteDB node and CA certificates from the remote host to the control-node artifact directory. Fetched artifacts are reused by certificate transfer, Kubernetes Secret generation, and TLS-enabled Prometheus scraper configuration.

```yaml
- name: Fetch YugabyteDB TLS certificates
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled. Example: `/tmp/fabric-x/artifacts/yugabyte`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/yugabyte"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/fetch
```

### crypto/rm

> Remove YugabyteDB TLS artifacts

Deletes the remote YugabyteDB TLS directory and, in Kubernetes mode, removes the generated TLS Secret. This removes role-managed key, certificate, and CA material without changing database data.

```yaml
- name: Remove YugabyteDB TLS artifacts
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/rm
```

### crypto/openssl/generate_csr

> Generate a YugabyteDB TLS CSR

Builds the YugabyteDB TLS SAN list from host addresses and organization metadata, then delegates CSR generation to the OpenSSL role. The generated key, CSR, and extension file are written under the remote YugabyteDB TLS configuration path.

```yaml
- name: Generate a YugabyteDB TLS CSR
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'yb-tserver-1', 'secret': 'yb-tserver-1pw'}, 'fabric_ca_host': 'ca-org1'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "yb-tserver-1"
        secret: "yb-tserver-1pw"
      fabric_ca_host: "ca-org1"
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Specifies the OpenShift Route host. Example: `yugabyte-master-web.apps.example.com`.
    yugabyte_openshift_master_webserver_route: "yugabyte-master-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-web.apps.example.com`.
    yugabyte_openshift_tablet_webserver_route: "yugabyte-tablet-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-pgsql-web.apps.example.com`.
    yugabyte_openshift_tablet_pgsql_web_route: "yugabyte-tablet-pgsql-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-cql-web.apps.example.com`.
    yugabyte_openshift_tablet_cql_web_route: "yugabyte-tablet-cql-web.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/generate_csr
```

### crypto/openssl/fetch_csr

> Fetch a YugabyteDB TLS CSR

Copies the YugabyteDB CSR and OpenSSL extension file from the remote TLS directory to the control-node artifact directory. Use this before signing the node certificate outside the target host.

```yaml
- name: Fetch a YugabyteDB TLS CSR
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled. Example: `/tmp/fabric-x/artifacts/yugabyte`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/yugabyte"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/fetch_csr
```

### crypto/openssl/transfer_cert

> Transfer a signed YugabyteDB TLS certificate

Copies the signed YugabyteDB node certificate and trusted organization TLS CA certificate to the remote TLS directory. The transferred files are consumed by container volume mounts or by Kubernetes Secret generation.

```yaml
- name: Transfer a signed YugabyteDB TLS certificate
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled. Example: `/tmp/fabric-x/artifacts/yugabyte`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/yugabyte"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'yb-tserver-1', 'secret': 'yb-tserver-1pw'}, 'fabric_ca_host': 'ca-org1'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "yb-tserver-1"
        secret: "yb-tserver-1pw"
      fabric_ca_host: "ca-org1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/transfer_cert
```

### crypto/cryptogen/transfer

> Copy cryptogen TLS material for YugabyteDB

Transfers the YugabyteDB TLS key, certificate, and CA certificate generated by cryptogen to the target host. The source path is resolved from the organization domain and peer identity, with the inventory host used as the peer name when no peer name is provided.

```yaml
- name: Copy cryptogen TLS material for YugabyteDB
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores cryptogen-generated artifacts. Example: `/tmp/fabric-x/crypto-config`.
    cryptogen_artifacts_dir: "/tmp/fabric-x/crypto-config"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'yb-tserver-1', 'secret': 'yb-tserver-1pw'}, 'fabric_ca_host': 'ca-org1'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "yb-tserver-1"
        secret: "yb-tserver-1pw"
      fabric_ca_host: "ca-org1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

> Enroll YugabyteDB TLS material with Fabric CA

Copies the Fabric CA TLS root when needed and delegates YugabyteDB TLS enrollment to the Fabric CA role. Enrollment uses organization metadata, peer credentials, and the actual external host so generated certificates include the expected SANs.

```yaml
- name: Enroll YugabyteDB TLS material with Fabric CA
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled. Example: `/tmp/fabric-x/artifacts/yugabyte`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/yugabyte"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Provides the organization metadata consumed by the crypto entry points that require it. The mapping is expected to expose `domain`, `role`, `peer.name`, `peer.secret`, and `fabric_ca_host` when relevant. Example: `{'domain': 'org1.example.com', 'role': 'peer', 'peer': {'name': 'yb-tserver-1', 'secret': 'yb-tserver-1pw'}, 'fabric_ca_host': 'ca-org1'}`.
    organization:
      domain: "org1.example.com"
      role: "peer"
      peer:
        name: "yb-tserver-1"
        secret: "yb-tserver-1pw"
      fabric_ca_host: "ca-org1"
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Specifies the OpenShift Route host. Example: `yugabyte-master-web.apps.example.com`.
    yugabyte_openshift_master_webserver_route: "yugabyte-master-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-web.apps.example.com`.
    yugabyte_openshift_tablet_webserver_route: "yugabyte-tablet-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-pgsql-web.apps.example.com`.
    yugabyte_openshift_tablet_pgsql_web_route: "yugabyte-tablet-pgsql-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-cql-web.apps.example.com`.
    yugabyte_openshift_tablet_cql_web_route: "yugabyte-tablet-cql-web.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/fabric_ca/enroll
```

### config/transfer

> Transfer YugabyteDB initialization config

Renders the YugabyteDB initialization SQL script that creates the configured database user and database. Container mode places the script in the remote config directory; Kubernetes mode also creates the ConfigMap mounted by tablet pods.

```yaml
- name: Transfer YugabyteDB initialization config
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Sets the YugabyteDB database name created by the initialization SQL script. Example: `fabricx`.
    yugabyte_db: "fabricx"
    # Sets the YugabyteDB database user created by the initialization SQL script. Example: `fabricx_user`.
    yugabyte_user: "fabricx_user"
    # Sets the password for the YugabyteDB database user. Store this value in Ansible Vault. Example: `my_yugabyte_password`.
    yugabyte_password: "my_yugabyte_password"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/transfer
```

### config/rm

> Remove YugabyteDB configuration

Deletes the remote YugabyteDB configuration directory and, in Kubernetes mode, removes the generated initialization ConfigMap. This cleans role-managed config without removing running resources unless paired with teardown or wipe.

```yaml
- name: Remove YugabyteDB configuration
  vars:
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/rm
```

### config/transfer_grafana_dashboard

> Transfer the YugabyteDB Grafana dashboard

Selects the built-in YugabyteDB dashboard JSON file and delegates the copy step to the Grafana role. The dashboard complements the Prometheus scraper configuration generated by this role.

```yaml
- name: Transfer the YugabyteDB Grafana dashboard
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/transfer_grafana_dashboard
```

### container/start

> Dispatch YugabyteDB container startup

Selects the master or tablet container startup path for the current host. The selected path starts either `yb-master` or `yb-tserver` with the role-managed data, config, TLS, and port settings.

```yaml
- name: Dispatch YugabyteDB container startup
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/start
```

### container/stop

> Stop a YugabyteDB container

Stops the container associated with the current YugabyteDB host. This leaves host data and configuration directories in place for a later restart.

```yaml
- name: Stop a YugabyteDB container
  vars:
    # Names the YugabyteDB container associated with the current host.
    yugabyte_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/stop
```

### container/rm

> Remove a YugabyteDB container

Deletes the container associated with the current YugabyteDB host. This removes the runtime container only; data cleanup is handled by `data/rm` or `teardown`.

```yaml
- name: Remove a YugabyteDB container
  vars:
    # Names the YugabyteDB container associated with the current host.
    yugabyte_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch logs from a YugabyteDB container

Delegates log collection for the current YugabyteDB container. Collected logs come from the named master or tablet container for troubleshooting.

```yaml
- name: Fetch logs from a YugabyteDB container
  vars:
    # Names the YugabyteDB container associated with the current host.
    yugabyte_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/fetch_logs
```

### container/master/start

> Start a YugabyteDB master container

Creates the host data directory, assembles the `yb-master` command line, and starts the master container. The container publishes master RPC and webserver ports, mounts the data directory, and mounts TLS material when TLS is enabled.

```yaml
- name: Start a YugabyteDB master container
  vars:
    # Sets the shared remote data directory consumed by YugabyteDB. Example: `/var/hyperledger/fabric-x/yugabyte/data`.
    remote_data_dir: "/var/hyperledger/fabric-x/yugabyte/data"
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Sets the remote data directory used by YugabyteDB tasks.
    yugabyte_remote_data_dir: "{{ remote_data_dir }}"
    # Sets the in-container data directory used by YugabyteDB.
    yugabyte_container_data_dir: /var/data
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the YugabyteDB container associated with the current host.
    yugabyte_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Sets the YugabyteDB container image.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks. Example: `yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100`.
    yugabyte_master_endpoints: "yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100"
    # Sets the master RPC bind port.
    yugabyte_master_rpc_bind_port: 7100
    # Sets the master webserver port.
    yugabyte_master_webserver_port: 7000
    # Provides the ordered list of master hosts used to compute replication factors. Example: `['yb-master-1', 'yb-master-2', 'yb-master-3']`.
    yugabyte_master_hosts:
      - "yb-master-1"
      - "yb-master-2"
      - "yb-master-3"
    # Sets the YugabyteDB log verbosity threshold.
    yugabyte_logs_level: 3
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables node-to-node TLS for YugabyteDB.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/master/start
```

### container/tablet/start

> Start a YugabyteDB tablet container

Creates the host data directory, assembles the `yb-tserver` command line, starts the tablet container, and initializes the database on the first tablet host. The container publishes YSQL, RPC, webserver, and YCQL ports, mounts initialization config, and mounts TLS material when TLS is enabled.

```yaml
- name: Start a YugabyteDB tablet container
  vars:
    # Sets the shared remote data directory consumed by YugabyteDB. Example: `/var/hyperledger/fabric-x/yugabyte/data`.
    remote_data_dir: "/var/hyperledger/fabric-x/yugabyte/data"
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Sets the remote data directory used by YugabyteDB tasks.
    yugabyte_remote_data_dir: "{{ remote_data_dir }}"
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the in-container data directory used by YugabyteDB.
    yugabyte_container_data_dir: /var/data
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Names the YugabyteDB container associated with the current host.
    yugabyte_container_name: "{{ inventory_hostname }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Sets the YugabyteDB container image.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks. Example: `yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100`.
    yugabyte_master_endpoints: "yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100"
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
    # Provides the ordered list of tablet hosts used to initialize the first tablet. Example: `['yb-tserver-1', 'yb-tserver-2', 'yb-tserver-3']`.
    yugabyte_tablet_hosts:
      - "yb-tserver-1"
      - "yb-tserver-2"
      - "yb-tserver-3"
    # Sets the YugabyteDB log verbosity threshold.
    yugabyte_logs_level: 3
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
    # Enables node-to-node TLS for YugabyteDB.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: container/tablet/start
```

### k8s/start

> Dispatch YugabyteDB Kubernetes startup

Selects the master or tablet Kubernetes startup path for the current host. The selected path applies the Service, optional NodePort Service, StatefulSet, PVC template, image pull secret reference, and probe settings for the node type.

```yaml
- name: Dispatch YugabyteDB Kubernetes startup
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/start
```

### k8s/rm

> Dispatch YugabyteDB Kubernetes removal

Selects the master or tablet Kubernetes removal path for the current host. The selected path removes the StatefulSet, ClusterIP Service, and optional NodePort Service for the node type.

```yaml
- name: Dispatch YugabyteDB Kubernetes removal
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/rm
```

### k8s/fetch_logs

> Fetch logs from YugabyteDB pods

Delegates pod log collection for the Kubernetes resource associated with the current host. Pods are selected by the role-managed Kubernetes resource label for the master or tablet StatefulSet.

```yaml
- name: Fetch logs from YugabyteDB pods
  vars:
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/fetch_logs
```

### k8s/config/transfer

> Create a YugabyteDB ConfigMap

Creates the ConfigMap that exposes the initialization SQL script to tablet pods. The ConfigMap is only populated for tablet components because tablets run the YSQL initialization command.

```yaml
- name: Create a YugabyteDB ConfigMap
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/config/transfer
```

### k8s/master/start

> Start a YugabyteDB master StatefulSet

Applies the master ClusterIP Service, optional NodePort and LoadBalancer Services, and StatefulSet for the current YugabyteDB master node. The StatefulSet runs `yb-master`, configures replication from the master host list, attaches persistent storage, mounts TLS Secrets when enabled, and waits for readiness when requested.

```yaml
- name: Start a YugabyteDB master StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the YugabyteDB container image.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks. Example: `yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100`.
    yugabyte_master_endpoints: "yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100"
    # Sets the master RPC bind port.
    yugabyte_master_rpc_bind_port: 7100
    # Sets the master webserver port.
    yugabyte_master_webserver_port: 7000
    # Provides the ordered list of master hosts used to compute replication factors. Example: `['yb-master-1', 'yb-master-2', 'yb-master-3']`.
    yugabyte_master_hosts:
      - "yb-master-1"
      - "yb-master-2"
      - "yb-master-3"
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
    # Enables node-to-node TLS for YugabyteDB.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
    # Kubernetes NodePort value used by the external master RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32100`.
    yugabyte_k8s_master_rpc_node_port: 32100
    # Kubernetes NodePort value used by the external master webserver Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32000`.
    yugabyte_k8s_master_webserver_node_port: 32000
    # Sets the image pull secret used by Kubernetes deployments when defined. Example: `registry-pull-secret`.
    k8s_image_pull_secret: "registry-pull-secret"
    # Sets the storage class used by Kubernetes PersistentVolumeClaims when defined. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Sets the requested persistent storage size for Kubernetes deployments. Example: `20Gi`.
    k8s_storage_size: "20Gi"
    # Overrides the readiness probe initial delay used by Kubernetes templates when defined. Example: `30`.
    k8s_readiness_probe_initial_delay_seconds: 30
    # Overrides the readiness probe period used by Kubernetes templates when defined. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Overrides the readiness probe timeout used by Kubernetes templates when defined. Example: `5`.
    k8s_readiness_probe_timeout_seconds: 5
    # Overrides the readiness probe failure threshold used by Kubernetes templates when defined. Example: `12`.
    k8s_readiness_probe_failure_threshold: 12
    # Overrides the liveness probe initial delay used by Kubernetes templates when defined. Example: `60`.
    k8s_liveness_probe_initial_delay_seconds: 60
    # Overrides the liveness probe period used by Kubernetes templates when defined. Example: `20`.
    k8s_liveness_probe_period_seconds: 20
    # Overrides the liveness probe timeout used by Kubernetes templates when defined. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Overrides the liveness probe failure threshold used by Kubernetes templates when defined. Example: `6`.
    k8s_liveness_probe_failure_threshold: 6
    # Set to `true` to create a LoadBalancer Service entry that exposes the master RPC port externally. When undefined or `false`, the master RPC port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_master_rpc_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the master webserver port externally. When undefined or `false`, the master webserver port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_master_webserver_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/master/start
```

### k8s/master/rm

> Remove a YugabyteDB master StatefulSet

Deletes the master StatefulSet and its Services for the current YugabyteDB master node. PersistentVolumeClaims are left for `data/rm` so runtime removal and data removal stay separate.

```yaml
- name: Remove a YugabyteDB master StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes NodePort value used by the external master RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32100`.
    yugabyte_k8s_master_rpc_node_port: 32100
    # Set to `true` to create a LoadBalancer Service entry that exposes the master RPC port externally. When undefined or `false`, the master RPC port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_master_rpc_port: false
    # Kubernetes NodePort value used by the external master webserver Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32000`.
    yugabyte_k8s_master_webserver_node_port: 32000
    # Set to `true` to create a LoadBalancer Service entry that exposes the master webserver port externally. When undefined or `false`, the master webserver port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_master_webserver_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/master/rm
```

### k8s/tablet/start

> Start a YugabyteDB tablet StatefulSet

Applies the tablet ClusterIP Service, optional NodePort and LoadBalancer Services, and StatefulSet for the current YugabyteDB tablet node, then initializes the database on the first tablet. The StatefulSet runs `yb-tserver`, connects to the configured masters, attaches persistent storage, mounts the initialization ConfigMap and TLS Secret when enabled, and waits for readiness when requested.

```yaml
- name: Start a YugabyteDB tablet StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the YugabyteDB container image.
    yugabyte_image: "{{ yugabyte_registry_endpoint }}/{{ yugabyte_image_name }}:{{ yugabyte_image_tag }}"
    # Sets the registry endpoint used to resolve the YugabyteDB image.
    yugabyte_registry_endpoint: "{{ lookup('env', 'YUGABYTE_REGISTRY_ENDPOINT') or 'docker.io/yugabytedb' }}"
    # Sets the YugabyteDB image name.
    yugabyte_image_name: yugabyte
    # Sets the YugabyteDB image tag.
    yugabyte_image_tag: 2025.2.1.0-b141
    # Lists the master RPC endpoints used to bootstrap YugabyteDB tablets and health checks. Example: `yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100`.
    yugabyte_master_endpoints: "yb-master-1.example.com:7100,yb-master-2.example.com:7100,yb-master-3.example.com:7100"
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
    # Enables node-to-node TLS for YugabyteDB.
    yugabyte_node_to_node_use_tls: "{{ yugabyte_use_tls }}"
    # Enables client-to-server TLS for YugabyteDB RPC and SQL access.
    yugabyte_client_to_server_use_tls: "{{ yugabyte_use_tls }}"
    # Enables HTTPS for the YugabyteDB webserver.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
    # Kubernetes NodePort value used by the external tablet YSQL Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31433`.
    yugabyte_k8s_tablet_pgsql_node_port: 31433
    # Kubernetes NodePort value used by the external tablet RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32101`.
    yugabyte_k8s_tablet_rpc_node_port: 32101
    # Kubernetes NodePort value used by the external tablet webserver Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32001`.
    yugabyte_k8s_tablet_webserver_node_port: 32001
    # Kubernetes NodePort value used by the external tablet YSQL web UI Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32300`.
    yugabyte_k8s_tablet_pgsql_web_node_port: 32300
    # Kubernetes NodePort value used by the external tablet YCQL bind Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32042`.
    yugabyte_k8s_tablet_cql_bind_node_port: 32042
    # Kubernetes NodePort value used by the external tablet YCQL web UI Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32200`.
    yugabyte_k8s_tablet_cql_web_node_port: 32200
    # Names the SQL initialization script used by tablet pods.
    yugabyte_init_script_file: 01-yb-init.sql
    # Provides the ordered list of tablet hosts used to initialize the first tablet. Example: `['yb-tserver-1', 'yb-tserver-2', 'yb-tserver-3']`.
    yugabyte_tablet_hosts:
      - "yb-tserver-1"
      - "yb-tserver-2"
      - "yb-tserver-3"
    # Sets the image pull secret used by Kubernetes deployments when defined. Example: `registry-pull-secret`.
    k8s_image_pull_secret: "registry-pull-secret"
    # Sets the storage class used by Kubernetes PersistentVolumeClaims when defined. Example: `fast-ssd`.
    k8s_storage_class: "fast-ssd"
    # Sets the requested persistent storage size for Kubernetes deployments. Example: `20Gi`.
    k8s_storage_size: "20Gi"
    # Overrides the readiness probe initial delay used by Kubernetes templates when defined. Example: `30`.
    k8s_readiness_probe_initial_delay_seconds: 30
    # Overrides the readiness probe period used by Kubernetes templates when defined. Example: `10`.
    k8s_readiness_probe_period_seconds: 10
    # Overrides the readiness probe timeout used by Kubernetes templates when defined. Example: `5`.
    k8s_readiness_probe_timeout_seconds: 5
    # Overrides the readiness probe failure threshold used by Kubernetes templates when defined. Example: `12`.
    k8s_readiness_probe_failure_threshold: 12
    # Overrides the liveness probe initial delay used by Kubernetes templates when defined. Example: `60`.
    k8s_liveness_probe_initial_delay_seconds: 60
    # Overrides the liveness probe period used by Kubernetes templates when defined. Example: `20`.
    k8s_liveness_probe_period_seconds: 20
    # Overrides the liveness probe timeout used by Kubernetes templates when defined. Example: `5`.
    k8s_liveness_probe_timeout_seconds: 5
    # Overrides the liveness probe failure threshold used by Kubernetes templates when defined. Example: `6`.
    k8s_liveness_probe_failure_threshold: 6
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YSQL port externally. When undefined or `false`, the tablet YSQL port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_pgsql_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet RPC port externally. When undefined or `false`, the tablet RPC port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_rpc_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet webserver port externally. When undefined or `false`, the tablet webserver port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_webserver_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YSQL web UI port externally. When undefined or `false`, the tablet YSQL web UI port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_pgsql_web_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YCQL bind port externally. When undefined or `false`, the tablet YCQL bind port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_cql_bind_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YCQL web UI port externally. When undefined or `false`, the tablet YCQL web UI port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_cql_web_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/tablet/start
```

### k8s/tablet/rm

> Remove a YugabyteDB tablet StatefulSet

Deletes the tablet StatefulSet and its Services for the current YugabyteDB tablet node. PersistentVolumeClaims are left for `data/rm` so runtime removal and data removal stay separate.

```yaml
- name: Remove a YugabyteDB tablet StatefulSet
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Kubernetes NodePort value used by the external tablet YSQL Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `31433`.
    yugabyte_k8s_tablet_pgsql_node_port: 31433
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YSQL port externally. When undefined or `false`, the tablet YSQL port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_pgsql_port: false
    # Kubernetes NodePort value used by the external tablet RPC Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32101`.
    yugabyte_k8s_tablet_rpc_node_port: 32101
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet RPC port externally. When undefined or `false`, the tablet RPC port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_rpc_port: false
    # Kubernetes NodePort value used by the external tablet webserver Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32001`.
    yugabyte_k8s_tablet_webserver_node_port: 32001
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet webserver port externally. When undefined or `false`, the tablet webserver port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_webserver_port: false
    # Kubernetes NodePort value used by the external tablet YSQL web UI Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32300`.
    yugabyte_k8s_tablet_pgsql_web_node_port: 32300
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YSQL web UI port externally. When undefined or `false`, the tablet YSQL web UI port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_pgsql_web_port: false
    # Kubernetes NodePort value used by the external tablet YCQL bind Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32042`.
    yugabyte_k8s_tablet_cql_bind_node_port: 32042
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YCQL bind port externally. When undefined or `false`, the tablet YCQL bind port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_cql_bind_port: false
    # Kubernetes NodePort value used by the external tablet YCQL web UI Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `32200`.
    yugabyte_k8s_tablet_cql_web_node_port: 32200
    # Set to `true` to create a LoadBalancer Service entry that exposes the tablet YCQL web UI port externally. When undefined or `false`, the tablet YCQL web UI port is not included in the LoadBalancer Service.
    yugabyte_k8s_loadbalancer_expose_tablet_cql_web_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/tablet/rm
```

### k8s/crypto/transfer

> Create a YugabyteDB TLS Secret

Creates the Kubernetes Secret that exposes the YugabyteDB TLS key pair and CA certificate to pods. The Secret is mounted by master and tablet StatefulSets when YugabyteDB TLS is enabled.

```yaml
- name: Create a YugabyteDB TLS Secret
  vars:
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Sets the shared remote configuration directory consumed by YugabyteDB. Example: `/opt/hyperledger/fabric-x/yugabyte/config`.
    remote_config_dir: "/opt/hyperledger/fabric-x/yugabyte/config"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the remote configuration directory used by YugabyteDB tasks.
    yugabyte_remote_config_dir: "{{ remote_config_dir }}"
    # Enables TLS asset handling for YugabyteDB.
    yugabyte_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: k8s/crypto/transfer
```

### data/rm

> Remove YugabyteDB persisted data

Deletes persisted YugabyteDB data for the selected deployment mode. Container mode removes the host data directory; Kubernetes mode removes the PVC associated with the StatefulSet volume claim.

```yaml
- name: Remove YugabyteDB persisted data
  vars:
    # Sets the shared remote data directory consumed by YugabyteDB. Example: `/var/hyperledger/fabric-x/yugabyte/data`.
    remote_data_dir: "/var/hyperledger/fabric-x/yugabyte/data"
    # Enables container mode for the YugabyteDB role.
    yugabyte_use_container: "{{ (not yugabyte_use_k8s) and (not yugabyte_use_openshift) }}"
    # Enables Kubernetes mode for the YugabyteDB role.
    yugabyte_use_k8s: false
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
    # Sets the remote data directory used by YugabyteDB tasks.
    yugabyte_remote_data_dir: "{{ remote_data_dir }}"
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: data/rm
```

### prometheus/get_scrapers

> Build Prometheus scrapers for YugabyteDB

Groups YugabyteDB hosts by cluster and assembles Prometheus scrape configuration for exposed master and tablet metrics endpoints. When webserver TLS is enabled, the generated scraper references the fetched organization TLS CA artifact for HTTPS scraping.

```yaml
- name: Build Prometheus scrapers for YugabyteDB
  vars:
    # Lists the inventory hosts that belong to the YugabyteDB clusters monitored by Prometheus. Example: `['yb-master-1', 'yb-master-2', 'yb-master-3', 'yb-tserver-1', 'yb-tserver-2', 'yb-tserver-3']`.
    yugabyte_hosts:
      - "yb-master-1"
      - "yb-master-2"
      - "yb-master-3"
      - "yb-tserver-1"
      - "yb-tserver-2"
      - "yb-tserver-3"
    # Defines the control-node directory that stores fetched YugabyteDB artifacts. Required when TLS-enabled tasks need access to fetched CA or certificate artifacts, such as when `yugabyte_use_tls` or webserver TLS is enabled. Example: `/tmp/fabric-x/artifacts/yugabyte`.
    fetched_artifacts_dir: "/tmp/fabric-x/artifacts/yugabyte"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: prometheus/get_scrapers
```

### openshift/start

> Dispatch YugabyteDB OpenShift startup

Reuses the Kubernetes workload flow and manages OpenShift Routes for configured HTTP-capable ports.

```yaml
- name: Dispatch YugabyteDB OpenShift startup
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: openshift/start
```

### openshift/rm

> Dispatch YugabyteDB OpenShift removal

Reuses the Kubernetes workload flow and manages OpenShift Routes for configured HTTP-capable ports.

```yaml
- name: Dispatch YugabyteDB OpenShift removal
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Selects the OpenShift deployment branch.
    yugabyte_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: openshift/rm
```

### openshift/ping

> Check the YugabyteDB OpenShift deployment

Checks configured OpenShift Routes and reuses the Kubernetes service ping flow.

```yaml
- name: Check the YugabyteDB OpenShift deployment
  vars:
    # Selects whether the current host is handled as a YugabyteDB master or tablet node. Example: `tablet`.
    yugabyte_component_type: "tablet"
    # Enables HTTPS for the YugabyteDB webserver.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
    # Specifies the OpenShift Route host. Example: `yugabyte-master-web.apps.example.com`.
    yugabyte_openshift_master_webserver_route: "yugabyte-master-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-web.apps.example.com`.
    yugabyte_openshift_tablet_webserver_route: "yugabyte-tablet-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-pgsql-web.apps.example.com`.
    yugabyte_openshift_tablet_pgsql_web_route: "yugabyte-tablet-pgsql-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-cql-web.apps.example.com`.
    yugabyte_openshift_tablet_cql_web_route: "yugabyte-tablet-cql-web.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: openshift/ping
```

### openshift/master/start

> Start the YugabyteDB master OpenShift deployment

Reuses the Kubernetes workload flow and manages OpenShift Routes for configured HTTP-capable ports.

```yaml
- name: Start the YugabyteDB master OpenShift deployment
  vars:
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables HTTPS for the YugabyteDB webserver.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Specifies the OpenShift Route host. Example: `yugabyte-master-web.apps.example.com`.
    yugabyte_openshift_master_webserver_route: "yugabyte-master-web.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: openshift/master/start
```

### openshift/master/rm

> Remove the YugabyteDB master OpenShift deployment

Reuses the Kubernetes workload flow and manages OpenShift Routes for configured HTTP-capable ports.

```yaml
- name: Remove the YugabyteDB master OpenShift deployment
  vars:
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Specifies the OpenShift Route host. Example: `yugabyte-master-web.apps.example.com`.
    yugabyte_openshift_master_webserver_route: "yugabyte-master-web.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: openshift/master/rm
```

### openshift/tablet/start

> Start the YugabyteDB tablet OpenShift deployment

Reuses the Kubernetes workload flow and manages OpenShift Routes for configured HTTP-capable ports.

```yaml
- name: Start the YugabyteDB tablet OpenShift deployment
  vars:
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables HTTPS for the YugabyteDB webserver.
    yugabyte_webserver_use_tls: "{{ yugabyte_use_tls }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-web.apps.example.com`.
    yugabyte_openshift_tablet_webserver_route: "yugabyte-tablet-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-pgsql-web.apps.example.com`.
    yugabyte_openshift_tablet_pgsql_web_route: "yugabyte-tablet-pgsql-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-cql-web.apps.example.com`.
    yugabyte_openshift_tablet_cql_web_route: "yugabyte-tablet-cql-web.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: openshift/tablet/start
```

### openshift/tablet/rm

> Remove the YugabyteDB tablet OpenShift deployment

Reuses the Kubernetes workload flow and manages OpenShift Routes for configured HTTP-capable ports.

```yaml
- name: Remove the YugabyteDB tablet OpenShift deployment
  vars:
    # Names the Kubernetes resources associated with the current host, including the derived NodePort Service when enabled.
    yugabyte_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Kubernetes namespace used by YugabyteDB resources. Example: `fabricx-yugabyte`.
    k8s_namespace: "fabricx-yugabyte"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-web.apps.example.com`.
    yugabyte_openshift_tablet_webserver_route: "yugabyte-tablet-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-pgsql-web.apps.example.com`.
    yugabyte_openshift_tablet_pgsql_web_route: "yugabyte-tablet-pgsql-web.apps.example.com"
    # Specifies the OpenShift Route host. Example: `yugabyte-tablet-cql-web.apps.example.com`.
    yugabyte_openshift_tablet_cql_web_route: "yugabyte-tablet-cql-web.apps.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: openshift/tablet/rm
```
