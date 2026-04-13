# hyperledger.fabricx.loadgen

The role `hyperledger.fabricx.loadgen` can be used to run a Load generator to test the throughput of the system.

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)
  - [get_metrics](#get_metrics)
  - [limit_rate](#limit_rate)
- [Kubernetes](#kubernetes)
  - [Deployments](#deployments)
  - [Services](#services)
  - [Kubernetes Variables](#kubernetes-variables)

## Variables

| Variable                        | Default                                                 | Description                                                   |
| ------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------- |
| `loadgen_registry_endpoint`     | `$LOADGEN_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                   |
| `loadgen_image_name`            | `fabric-x-loadgen`                                      | Container image name                                          |
| `loadgen_image_tag`             | `0.1.9`                                                 | Container image tag                                           |
| `loadgen_image`                 | `{{ registry }}/{{ name }}:{{ tag }}`                   | Full container image reference                                |
| `loadgen_container_name`        | `{{ inventory_hostname }}`                              | Name given to the container                                   |
| `loadgen_git_hub_url`           | `github.com`                                            | GitHub URL for the source repository                          |
| `loadgen_git_repo`              | `hyperledger/fabric-x-committer`                        | Git repository used to build the binary                       |
| `loadgen_git_commit`            | `v0.1.9`                                                | Git ref (tag or commit) to check out                          |
| `loadgen_source_code_package`   | `cmd/loadgen`                                           | Go source package path within the repository                  |
| `loadgen_bin_package`           | `github.com/hyperledger/fabric-x-committer/cmd/loadgen` | Fully-qualified Go package used for `go install`              |
| `loadgen_bin_name`              | `loadgen`                                               | Name of the produced binary                                   |
| `loadgen_use_bin`               | `false`                                                 | Set to `true` to use the native binary instead of a container |
| `loadgen_remote_config_dir`     | `{{ remote_config_dir }}`                               | Configuration directory on the remote node                    |
| `loadgen_container_config_dir`  | `/config`                                               | Configuration directory inside the container                  |
| `loadgen_config_file`           | `config-loadgen.yaml`                                   | Load generator configuration file name                        |
| `loadgen_admin_pub_key_file`    | `admin_pub_key.pem`                                     | Admin public key file name                                    |
| `loadgen_admin_priv_key_file`   | `admin_priv_key.pem`                                    | Admin private key file name                                   |
| `loadgen_assert_metrics`        | `false`                                                 | Assert metrics values after the load test                     |
| `loadgen_generate_config_block` | `false`                                                 | Generate configuration block                                  |
| `loadgen_use_tls`               | `false`                                                 | Enable TLS for the gRPC server                                |
| `loadgen_monitoring_use_tls`    | `{{ loadgen_use_tls }}`                                 | Enable TLS for the monitoring endpoint                        |
| `loadgen_http_protocol`         | `{{ 'https' if loadgen_use_tls else 'http' }}`          | HTTP protocol scheme                                          |
| `loadgen_use_mtls`              | `false`                                                 | Enable mTLS for the gRPC server                               |
| `loadgen_monitoring_use_mtls`   | `{{ loadgen_use_mtls }}`                                | Enable mTLS for the monitoring endpoint                       |
| `loadgen_log_level`             | `info`                                                  | Log level                                                     |
| `loadgen_log_format`            | (see defaults)                                          | Log format string                                             |
| `loadgen_web_port`              | —                                                       | HTTP API port for rate-limit control and health checks        |
| `loadgen_metrics_port`          | —                                                       | Prometheus metrics scrape port                                |
| `loadgen_rpc_port`              | —                                                       | gRPC API port for programmatic control of load generation     |

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate and/or transfer the crypto material needed to run a Fabric-X Loadgen component. The task supports two modes to run:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Setup the crypto material for Fabric-X Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` allows to fetch the Fabric-X Loadgen certificates on the control node. This operation is important for the generation of the genesis block on the control node in case the Loadgen user is set as **Meta Namespace Admin** (with the `meta_namespace_admin` flag).

```yaml
- name: Fetch the Fabric-X Loadgen certificates
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for a Fabric-X Loadgen:

```yaml
- name: Remove the Fabric-X Loadgen crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` allows to transfer the configuration files for a Fabric-X Loadgen on the remote node:

```yaml
- name: Transfer the Fabric-X Loadgen configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Fabric-X Loadgen configuration files on the remote node:

```yaml
- name: Remove the Fabric-X Loadgen configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/rm
```

### start

The task `start` allows to start the Fabric-X Load Generator either as binary or as container.

```yaml
- name: Start the Fabric-X Load Generator
  vars:
    loadgen_web_port: 12000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: start
```

### stop

The task `stop` allows to stop the Fabric-X Load Generator running as binary or as container.

```yaml
- name: Stop the Fabric-X Load Generator
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Fabric-X Load Generator running as binary or as container and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown the Fabric-X Load Generator
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Fabric-X Load Generator running as binary or as container, remove all the artifacts (configuration files, binaries and all the runtime-generated artifacts).

```yaml
- name: Wipe the Fabric-X Load Generator
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Fabric-X Load Generator components from the remote hosts to the control node.

```yaml
- name: Fetch the Fabric-X Load Generator logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Fabric-X Load Generator components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Fabric-X Load Generator
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: ping
```

### get_metrics

The task `get_metrics` allows to fetch the metrics from the Fabric-X Load Generator components and print them on stdout.

```yaml
- name: Fetch the Fabric-X Load Generator metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: get_metrics
```

### limit_rate

The task `limit_rate` allows to limit the load generator throughput at runtime to a specified value.

```yaml
- name: Set the upper TPS limit for the Fabric-X Load Generator
  vars:
    loadgen_limit_rate: 2000 # limit to 2000 TPS
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: limit_rate
```

## Kubernetes

The loadgen role supports deployment to Kubernetes. When `loadgen_use_k8s: true` is set in the inventory, the role deploys loadgen client pods using the k8s templates under `templates/k8s/`.

### Deployments

Five client types are supported, each deployed as a separate Deployment:

| Client Type          | Description                                 |
| -------------------- | ------------------------------------------- |
| `orderer-client`     | Load generator targeting orderer components |
| `coordinator-client` | Load generator targeting the coordinator    |
| `sidecar-client`     | Load generator targeting the sidecar        |
| `validator-client`   | Load generator targeting the validators     |
| `verifier-client`    | Load generator targeting the verifiers      |

Each Deployment exposes three ports:

| Port      | Purpose                                              |
| --------- | ---------------------------------------------------- |
| `web`     | HTTP API for rate-limit control and health checks    |
| `metrics` | Prometheus metrics scrape endpoint                   |
| `rpc`     | gRPC API for programmatic control of load generation |

### Services

Two Service types are created per loadgen instance:

- **ClusterIP Service** (`{{ loadgen_k8s_resource_name }}`): Internal service with `web`, `metrics`, and `rpc` ports.
- **NodePort Service** (`{{ loadgen_k8s_resource_name }}-nodeport`): External access via NodePort for `web`, `metrics`, and `rpc`.

### Kubernetes Variables

| Variable                        | Default                             | Description                                                  |
| ------------------------------- | ----------------------------------- | ------------------------------------------------------------ |
| `loadgen_use_k8s`               | `false`                             | Set to `true` to deploy to Kubernetes                        |
| `loadgen_use_container`         | `{{ not use_bin and not use_k8s }}` | Fallback to container mode when neither bin nor k8s is set   |
| `loadgen_k8s_resource_name`     | `{{ inventory_hostname }}`          | Name used for k8s resources (Deployment, Service, ConfigMap) |
| `loadgen_k8s_wait`              | `true`                              | Wait for k8s resources to be ready                           |
| `loadgen_k8s_wait_timeout`      | `120`                               | Timeout in seconds for waiting for k8s resources             |
| `loadgen_k8s_fs_group`          | `10001`                             | fsGroup for the pod security context                         |
| `loadgen_k8s_web_node_port`     | `{{ loadgen_web_port }}`            | NodePort for the web service                                 |
| `loadgen_k8s_metrics_node_port` | `{{ loadgen_metrics_port }}`        | NodePort for the metrics service                             |
| `loadgen_k8s_rpc_node_port`     | `{{ loadgen_rpc_port }}`            | NodePort for the gRPC API service                            |

#### mTLS in Kubernetes

When mTLS is enabled, CA certificates are embedded into the ConfigMap and mounted as volumeMounts in the Deployment. The following variables control mTLS behavior:

| Variable                          | Description                                                  |
| --------------------------------- | ------------------------------------------------------------ |
| `loadgen_mtls_clients`            | List of client names whose CA certs are mounted (server)     |
| `loadgen_mtls_orgs`               | List of org dicts whose CA certs are mounted (server)        |
| `loadgen_monitoring_mtls_clients` | List of client names whose CA certs are mounted (monitoring) |
| `loadgen_monitoring_mtls_orgs`    | List of org dicts whose CA certs are mounted (monitoring)    |

Duplicate avoidance: monitoring mTLS clients/orgs that already appear in the server mTLS lists are skipped to prevent duplicate ConfigMap keys.
