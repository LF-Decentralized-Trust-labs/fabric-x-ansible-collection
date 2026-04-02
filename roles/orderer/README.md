# hyperledger.fabricx.orderer

The role `hyperledger.fabricx.orderer` can be used to run the Fabric-X `orderer` components (i.e. `consenter`, `batcher`, `assembler` and `router`).

Three deployment modes are supported:

| Mode                | Variable                                           | Description                                 |
| ------------------- | -------------------------------------------------- | ------------------------------------------- |
| Container (default) | `orderer_use_bin: false`, `orderer_use_k8s: false` | Runs components as Docker/Podman containers |
| Binary              | `orderer_use_bin: true`                            | Runs components as native OS processes      |
| Kubernetes          | `orderer_use_k8s: true`                            | Deploys components as K8s StatefulSets      |

## Kubernetes mode

In Kubernetes mode, Ansible runs on the control node (`ansible_connection: local`) and applies K8s manifests via the API server. Crypto material and configuration are generated locally (same flow as container/binary modes) and shipped to the cluster as ConfigMaps and Secrets. Each component instance gets:

- **ConfigMap** — node configuration, genesis block (`binaryData`), MSP/TLS public material
- **Secret** — private key (`msp/keystore/priv_sk`) and TLS private key (`tls/server.key`)
- **Service** — headless ClusterIP for stable StatefulSet DNS
- **StatefulSet** — single replica with `subPath`-mounted config/secret volumes + PVC for `/data`

Use the dedicated K8s inventory at `examples/inventory/k8s/fabric-x-orderer.yaml` as a starting point. Key inventory settings:

```yaml
# group_vars
ansible_connection: local
orderer_use_k8s: true
k8s_namespace: "fabricx"

# per-host: ansible_host must resolve to the K8s Service DNS
orderer-consenter-1:
  ansible_host: orderer-consenter-1.fabricx.svc.cluster.local
```

**Prerequisites**: `pip install kubernetes` and `ansible-galaxy collection install kubernetes.core` on the control node.

## Table of Contents <!-- omit in toc -->

- [Kubernetes mode](#kubernetes-mode)
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

## Variables

| Variable                       | Default                                                         | Description                                                               |
| ------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `orderer_registry_endpoint`    | `$ORDERER_REGISTRY_ENDPOINT` or `docker.io/hyperledger`         | Container registry endpoint                                               |
| `orderer_image_name`           | `fabric-x-orderer`                                              | Container image name                                                      |
| `orderer_image_tag`            | `0.0.21-1`                                                      | Container image tag                                                       |
| `orderer_image`                | `{{ registry }}/{{ name }}:{{ tag }}`                           | Full container image reference                                            |
| `orderer_container_name`       | `{{ inventory_hostname }}`                                      | Name given to the container                                               |
| `orderer_git_uri`              | `https://github.com/hyperledger/fabric-x-orderer.git`           | Git repository used to build the binary                                   |
| `orderer_git_commit`           | `v0.0.21-1`                                                     | Git ref (tag or commit) to check out                                      |
| `orderer_source_code_package`  | `cmd/arma`                                                      | Go source package path within the repository                              |
| `orderer_bin_package`          | `github.com/hyperledger/fabric-x-orderer/cmd/arma`              | Fully-qualified Go package used for `go install`                          |
| `orderer_bin_name`             | `arma`                                                          | Name of the produced binary                                               |
| `orderer_use_bin`              | `false`                                                         | Set to `true` to use the native binary instead of a container             |
| `orderer_remote_config_dir`    | `{{ remote_config_dir }}`                                       | Configuration directory on the remote node                                |
| `orderer_remote_data_dir`      | `{{ remote_data_dir }}`                                         | Data directory on the remote node                                         |
| `orderer_container_config_dir` | `/config`                                                       | Configuration directory inside the container                              |
| `orderer_container_data_dir`   | `/data`                                                         | Data directory inside the container                                       |
| `orderer_config_dir`           | auto-selected                                                   | Active config directory (remote or container, based on `orderer_use_bin`) |
| `orderer_data_dir`             | auto-selected                                                   | Active data directory (remote or container, based on `orderer_use_bin`)   |
| `orderer_config_file`          | `node_config.yaml`                                              | Orderer node configuration file name                                      |
| `orderer_use_tls`              | `false`                                                         | Enable TLS                                                                |
| `orderer_use_mtls`             | `false`                                                         | Enable mutual TLS                                                         |
| `orderer_http_protocol`        | `https` or `http`                                               | HTTP protocol derived from `orderer_use_tls`                              |
| `orderer_crypto_name`          | `{{ organization.orderer.name }}` or `{{ inventory_hostname }}` | Identity name used for crypto material lookup                             |
| `orderer_genesis_block_file`   | `{{ channel_id }}_block.pb`                                     | Genesis block file name                                                   |

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate and/or transfer the crypto material needed to run a Fabric-X Orderer component. The task supports two modes to run:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Setup the crypto material for Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` allows to fetch the Fabric-X Orderer certificates on the control node. This operation is important for the generation of the genesis block on the control node, which will embed the certificates of the orderers.

```yaml
- name: Fetch the Fabric-X Orderer certificates
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for a Fabric-X Orderer:

```yaml
- name: Remove the Fabric-X Orderer crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` allows to transfer the configuration files for a Fabric-X Orderer on the remote node:

```yaml
- name: Transfer the Fabric-X Orderer configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Fabric-X Orderer configuration files on the remote node:

```yaml
- name: Remove the Fabric-X Orderer configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/rm
```

### start

The task `start` allows to start the Fabric-X Orderer either as binary or as container. The sub-component to start is determined by the `orderer_component_type` variable (`consenter`, `batcher`, `assembler`, or `router`):

```yaml
- name: Start the Fabric-X Orderer
  vars:
    orderer_component_type: consenter # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: start
```

### stop

The task `stop` allows to stop the Fabric-X Orderer running as binary or as container. The sub-component to stop is determined by the `orderer_component_type` variable:

```yaml
- name: Stop the Fabric-X Orderer
  vars:
    orderer_component_type: consenter # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Fabric-X Orderer running as binary or as container and remove all the artifacts being generated during runtime. The sub-component to teardown is determined by the `orderer_component_type` variable:

```yaml
- name: Teardown the Fabric-X Orderer
  vars:
    orderer_component_type: consenter # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Fabric-X Orderer running as binary or as container, remove all the artifacts (configuration files, binaries and all the runtime-generated artifacts). The sub-component to wipe is determined by the `orderer_component_type` variable:

```yaml
- name: Wipe the Fabric-X Orderer
  vars:
    orderer_component_type: consenter # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Fabric-X Orderer components from the remote hosts to the control node. The sub-component whose logs are fetched is determined by the `orderer_component_type` variable:

```yaml
- name: Fetch the Fabric-X Orderer logs
  vars:
    orderer_component_type: consenter # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Fabric-X Orderer components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: ping
```

### get_metrics

The task `get_metrics` allows to fetch the metrics from the Fabric-X Orderer components and print them on stdout.

```yaml
- name: Fetch the Fabric-X Orderer metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: get_metrics
```
