# hyperledger.fabricx.yugabyte

The role `hyperledger.fabricx.yugabyte` can be used to run a `yugabyte` distributed DB cluster.

The role supports **container** and **Kubernetes** deployment modes (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [crypto/openssl/generate\_csr](#cryptoopensslgenerate_csr)
  - [crypto/openssl/fetch\_csr](#cryptoopensslfetch_csr)
  - [crypto/openssl/transfer\_cert](#cryptoopenssltransfer_cert)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)

## Variables

| Variable                                  | Default                                                 | Description                                               |
| ----------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| `yugabyte_registry_endpoint`              | `$YUGABYTE_REGISTRY_ENDPOINT` or `docker.io/yugabytedb` | Container registry endpoint                               |
| `yugabyte_image_name`                     | `yugabyte`                                              | Container image name                                      |
| `yugabyte_image_tag`                      | `2025.2.1.0-b141`                                       | Container image tag                                       |
| `yugabyte_image`                          | `{{ registry }}/{{ name }}:{{ tag }}`                   | Full container image reference                            |
| `yugabyte_container_name`                 | `{{ inventory_hostname }}`                              | Name given to the container                               |
| `yugabyte_remote_config_dir`              | `{{ remote_config_dir }}`                               | Configuration directory on the remote node                |
| `yugabyte_remote_data_dir`                | `{{ remote_data_dir }}`                                 | Data directory on the remote node                         |
| `yugabyte_container_data_dir`             | `/var/data`                                             | Data directory inside the container                       |
| `yugabyte_init_script_file`               | `01-yb-init.sql`                                        | Initialization SQL script file name                       |
| `yugabyte_logs_level`                     | `3`                                                     | Log verbosity level (0=INFO, 1=WARNING, 2=ERROR, 3=FATAL) |
| `yugabyte_use_tls`                        | `false`                                                 | Enable TLS for all YugabyteDB channels                    |
| `yugabyte_webserver_use_tls`              | `{{ yugabyte_use_tls }}`                                | Enable TLS for the webserver                              |
| `yugabyte_client_to_server_use_tls`       | `{{ yugabyte_use_tls }}`                                | Enable client-to-server TLS                               |
| `yugabyte_node_to_node_use_tls`           | `{{ yugabyte_use_tls }}`                                | Enable node-to-node TLS                                   |
| `yugabyte_master_rpc_bind_port`           | `7100`                                                  | Master RPC port                                           |
| `yugabyte_master_webserver_port`          | `7000`                                                  | Master webserver port                                     |
| `yugabyte_tablet_pgsql_bind_port`         | `5433`                                                  | YSQL (PostgreSQL-compatible) client port                  |
| `yugabyte_tablet_rpc_bind_port`           | `9100`                                                  | Tablet server RPC port                                    |
| `yugabyte_tablet_webserver_port`          | `9000`                                                  | Tablet server webserver port                              |
| `yugabyte_tablet_cql_web_port`            | `12000`                                                 | YCQL webserver port                                       |
| `yugabyte_tablet_pgsql_web_port`          | `13000`                                                 | YSQL webserver port                                       |
| `yugabyte_tablet_cql_bind_port`           | `9042`                                                  | YCQL (Cassandra-compatible) client port                   |
| `yugabyte_use_k8s`                        | `false`                                                 | Deploy on Kubernetes instead of container                 |
| `yugabyte_use_container`                  | `{{ not yugabyte_use_k8s }}`                            | Deploy as container (computed)                            |
| `yugabyte_k8s_resource_name`              | `{{ inventory_hostname }}`                              | Name used for all Kubernetes resources                    |
| `yugabyte_k8s_wait`                       | `true`                                                  | Wait for StatefulSet pods to become ready                 |
| `yugabyte_k8s_wait_timeout`               | `300`                                                   | Timeout in seconds when waiting for pods                  |
| `yugabyte_k8s_fs_group`                   | `1001`                                                  | fsGroup for pod security context (matches yugabyte UID)   |
| `yugabyte_k8s_master_rpc_node_port`       | `{{ yugabyte_master_rpc_bind_port }}`                   | NodePort for master RPC                                   |
| `yugabyte_k8s_master_webserver_node_port` | `{{ yugabyte_master_webserver_port }}`                  | NodePort for master webserver                             |
| `yugabyte_k8s_tablet_pgsql_node_port`     | `{{ yugabyte_tablet_pgsql_bind_port }}`                 | NodePort for YSQL client                                  |
| `yugabyte_k8s_tablet_rpc_node_port`       | `{{ yugabyte_tablet_rpc_bind_port }}`                   | NodePort for tablet RPC                                   |
| `yugabyte_k8s_tablet_webserver_node_port` | `{{ yugabyte_tablet_webserver_port }}`                  | NodePort for tablet webserver                             |
| `yugabyte_k8s_tablet_pgsql_web_node_port` | `{{ yugabyte_tablet_pgsql_web_port }}`                  | NodePort for YSQL webserver/metrics                       |
| `yugabyte_k8s_tablet_cql_bind_node_port`  | `{{ yugabyte_tablet_cql_bind_port }}`                   | NodePort for YCQL client                                  |
| `yugabyte_k8s_tablet_cql_web_node_port`   | `{{ yugabyte_tablet_cql_web_port }}`                    | NodePort for YCQL webserver/metrics                       |

## Tasks

### crypto/setup

The task `crypto/setup` transfers or generates directly on the remote node the crypto material needed to run YugabyteDB. The task supports two operating modes:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Setup the crypto material for Yugabyte DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` fetches on the control node the TLS certificate of a Yugabyte DB:

```yaml
- name: Fetch the TLS certificate of Yugabyte DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for Yugabyte. In Kubernetes mode it also deletes the associated Secret:

```yaml
- name: Remove the Yugabyte crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/rm
```

### crypto/openssl/generate_csr

The task `crypto/openssl/generate_csr` allows to generate a private key and a CSR to be used to request a TLS certificate.

The task uses `openssl` (see [hyperledger.fabricx.openssl](../openssl/README.md)) to generate the key and the corresponding CSR. Differently from Postgres, we produce a CSR to be able to generate certificates under the same CA for the entire Yugabyte cluster ([official Yugabyte guide](https://docs.yugabyte.com/stable/secure/tls-encryption/server-certificates/)).

```yaml
- name: Generate a CSR for Yugabyte DB
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/generate_csr
```

### crypto/openssl/fetch_csr

The task `crypto/openssl/fetch_csr` allows to fetch the CSR certificate of a Yugabyte DB on the control node, so that it could be used by a CA to generate a certificate.

```yaml
- name: Fetch the Yugabyte DB CSR
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/fetch_csr
```

### crypto/openssl/transfer_cert

The task `crypto/openssl/transfer_cert` allows to transfer the TLS certificate generated by the CA on the control node to the Yugabyte DB.

```yaml
- name: Transfer the Yugabyte DB TLS certificate
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: crypto/openssl/transfer_cert
```

### config/transfer

The task `config/transfer` generates the Yugabyte initialization SQL script. In Kubernetes mode it also creates the associated ConfigMap:

```yaml
- name: Transfer the Yugabyte configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Yugabyte configuration files. In Kubernetes mode it also deletes the associated ConfigMap:

```yaml
- name: Remove the Yugabyte configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: config/rm
```

### start

The task `start` allows to start the Yugabyte DB Cluster. Set `yugabyte_use_k8s: true` to deploy on Kubernetes.

```yaml
- name: Start the Yugabyte DB Cluster
  vars:
    yugabyte_use_k8s: true   # omit or set false for container mode
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: start
```

### stop

The task `stop` allows to stop the Yugabyte DB Cluster (container mode only; Kubernetes manages pod liveness).

```yaml
- name: Stop the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Yugabyte DB Cluster and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Yugabyte DB Cluster, remove all the artifacts (configuration files and all the runtime-generated artifacts).

```yaml
- name: Wipe the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Yugabyte DB Cluster components from the remote hosts (or Kubernetes pods) to the control node.

```yaml
- name: Fetch the Yugabyte DB Cluster logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Yugabyte DB Cluster components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: ping
```
