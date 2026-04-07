# hyperledger.fabricx.orderer

The role `hyperledger.fabricx.orderer` can be used to run the Fabric-X `orderer` components (i.e. `consenter`, `batcher`, `assembler` and `router`).

Three deployment modes are supported:

| Mode                | Variable                                           | Description                                 |
| ------------------- | -------------------------------------------------- | ------------------------------------------- |
| Container (default) | `orderer_use_bin: false`, `orderer_use_k8s: false` | Runs components as Docker/Podman containers |
| Binary              | `orderer_use_bin: true`                            | Runs components as native OS processes      |
| Kubernetes          | `orderer_use_k8s: true`                            | Deploys components as K8s StatefulSets      |

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
- [Kubernetes mode](#kubernetes-mode)
  - [K8s resources per component instance](#k8s-resources-per-component-instance)
  - [Inventory setup](#inventory-setup)

## Variables

| Variable                       | Default                                                         | Description                                                                  |
| ------------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `orderer_registry_endpoint`    | `$ORDERER_REGISTRY_ENDPOINT` or `docker.io/hyperledger`         | Container registry endpoint                                                  |
| `orderer_image_name`           | `fabric-x-orderer`                                              | Container image name                                                         |
| `orderer_image_tag`            | `0.0.21-1`                                                      | Container image tag                                                          |
| `orderer_image`                | `{{ registry }}/{{ name }}:{{ tag }}`                           | Full container image reference                                               |
| `orderer_container_name`       | `{{ inventory_hostname }}`                                      | Name given to the container                                                  |
| `orderer_git_uri`              | `https://github.com/hyperledger/fabric-x-orderer.git`           | Git repository used to build the binary                                      |
| `orderer_git_commit`           | `v0.0.21-1`                                                     | Git ref (tag or commit) to check out                                         |
| `orderer_source_code_package`  | `cmd/arma`                                                      | Go source package path within the repository                                 |
| `orderer_bin_package`          | `github.com/hyperledger/fabric-x-orderer/cmd/arma`              | Fully-qualified Go package used for `go install`                             |
| `orderer_bin_name`             | `arma`                                                          | Name of the produced binary                                                  |
| `orderer_use_bin`              | `false`                                                         | Set to `true` to use the native binary instead of a container                |
| `orderer_use_k8s`              | `false`                                                         | Set to `true` to deploy as Kubernetes StatefulSets                           |
| `orderer_k8s_resource_name`    | `{{ inventory_hostname }}`                                      | K8s resource name prefix (StatefulSet, Services, Secret, ConfigMap)          |
| `orderer_k8s_wait`             | `true`                                                          | Wait for StatefulSet pods to become Ready after apply                        |
| `orderer_k8s_wait_timeout`     | `120`                                                           | Timeout in seconds when waiting for pods to become Ready                     |
| `orderer_remote_config_dir`    | `{{ remote_config_dir }}`                                       | Configuration directory on the remote node                                   |
| `orderer_remote_data_dir`      | `{{ remote_data_dir }}`                                         | Data directory on the remote node                                            |
| `orderer_container_config_dir` | `/config`                                                       | Configuration directory inside the container                                 |
| `orderer_container_data_dir`   | `/data`                                                         | Data directory inside the container                                          |
| `orderer_config_dir`           | auto-selected                                                   | Active config directory (remote or container, based on `orderer_use_bin`)    |
| `orderer_data_dir`             | auto-selected                                                   | Active data directory (remote or container, based on `orderer_use_bin`)      |
| `orderer_config_file`          | `node_config.yaml`                                              | Orderer node configuration file name                                         |
| `orderer_use_tls`              | `false`                                                         | Enable TLS                                                                   |
| `orderer_use_mtls`             | `false`                                                         | Enable mutual TLS                                                            |
| `orderer_http_protocol`        | `https` or `http`                                               | HTTP protocol derived from `orderer_use_tls`                                 |
| `orderer_crypto_name`          | `{{ organization.orderer.name }}` or `{{ inventory_hostname }}` | Identity name used for crypto material lookup                                |
| `orderer_genesis_block_file`   | `{{ channel_id }}_block.pb`                                     | Genesis block file name                                                      |

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate and/or transfer the crypto material needed to run a Fabric-X Orderer component. The task supports two modes to run:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

In Kubernetes mode, this task additionally creates a Secret containing all crypto material for the component (see [Kubernetes mode](#kubernetes-mode)).

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

The task `crypto/rm` removes the crypto material generated for a Fabric-X Orderer. In Kubernetes mode, this also deletes the Secret.

```yaml
- name: Remove the Fabric-X Orderer crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` allows to transfer the configuration files for a Fabric-X Orderer on the remote node. In Kubernetes mode, this creates a ConfigMap containing the node configuration, genesis block, and any mTLS CA certs.

```yaml
- name: Transfer the Fabric-X Orderer configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Fabric-X Orderer configuration files on the remote node. In Kubernetes mode, this deletes the ConfigMap.

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

## Kubernetes mode

In Kubernetes mode (`orderer_use_k8s: true`), Ansible runs entirely on the control node (`ansible_connection: local`) and applies K8s manifests via the API server. The crypto and config lifecycle maps to the same task names as the other deployment modes:

| Phase             | Task              | K8s resource created / deleted                                  |
| ----------------- | ----------------- | --------------------------------------------------------------- |
| `crypto/setup`    | generate + apply  | **Secret** — all own crypto material                            |
| `crypto/rm`       | delete            | Secret                                                          |
| `config/transfer` | render + apply    | **ConfigMap** — node config + genesis                           |
| `config/rm`       | delete            | ConfigMap                                                       |
| `start`           | apply             | StatefulSet, headless Service, (NodePort Service)               |
| `teardown`        | delete            | StatefulSet, Services, PVC — Secret and ConfigMap **preserved** |
| `wipe`            | teardown + delete | additionally deletes Secret and ConfigMap                       |

### K8s resources per component instance

**Secret** (`<resource-name>-secret`): created during `crypto/setup`, contains all crypto files read directly from the control node:

| Secret key             | Source file                              |
| ---------------------- | ---------------------------------------- |
| `msp-keystore-priv-sk` | `msp/keystore/priv_sk`                   |
| `msp-signcert.pem`     | `msp/signcerts/<name>.pem`               |
| `msp-cacert.pem`       | `msp/cacerts/<name>.pem`                 |
| `msp-config.yaml`      | `msp/config.yaml`                        |
| `tls-server.key`       | `tls/server.key`                         |
| `tls-server.crt`       | `tls/server.crt`                         |
| `tls-ca.crt`           | `tls/ca.crt`                             |

**ConfigMap** (`<resource-name>-config`): created during `config/transfer`, contains:

| ConfigMap key                | Content                                                                     |
| ---------------------------- | --------------------------------------------------------------------------- |
| `node-config.yaml`           | Rendered node configuration                                                 |
| `genesis.block` (binaryData) | Genesis block (binary-safe via `slurp`)                                     |
| `mtls-client-<name>-ca.crt`  | mTLS client CA cert (one per `orderer_mtls_clients` entry, if mTLS enabled) |
| `mtls-org-<domain>-ca.crt`   | mTLS org CA cert (one per `orderer_mtls_orgs` entry, if mTLS enabled)       |

**StatefulSet** (`<resource-name>`): single replica with crypto mounted from the Secret and config from the ConfigMap, plus a PVC for persistent data.

**Headless Service** (`<resource-name>`): required by the StatefulSet for stable pod DNS (`<resource-name>.<namespace>.svc.cluster.local`). This is also the address used as `ansible_host` for inter-component communication within the cluster.

**NodePort Service** (`<resource-name>-nodeport`): always deployed alongside the headless Service. Exposes `orderer_rpc_port` and `orderer_metrics_port` as NodePorts — port values must therefore fall in the Kubernetes NodePort range (30000–32767).

### Inventory setup

Use the dedicated K8s inventory at `examples/inventory/k8s/fabric-x-orderer.yaml` as a starting point. Common cluster-wide settings belong in `group_vars/all/env.yaml`:

```yaml
# group_vars/all/env.yaml
ansible_connection: local
ansible_host: "{{ inventory_hostname }}.{{ k8s_namespace | default('default') }}.svc.cluster.local"

k8s_namespace: default
k8s_storage_size: 500Mi
k8s_image_pull_policy: IfNotPresent
# k8s_storage_class:     # omit to use the cluster default
# k8s_image_pull_secret: # e.g. regcred
```

Per-host port values must be in the Kubernetes NodePort range (30000–32767):

```yaml
# fabric-x-orderer.yaml (excerpt)
orderer-router-1:
  orderer_component_type: router
  orderer_rpc_port: 30050
  orderer_metrics_port: 30060
```

> **TLS and NodePort**: TLS certificate SANs are generated for the internal k8s DNS name. For TLS to work over NodePort from outside the cluster, add a matching `/etc/hosts` entry mapping `<inventory_hostname>.<namespace>.svc.cluster.local` to the node IP (e.g. `127.0.0.1` for minikube).

**Prerequisites** on the control node:

```bash
pip install kubernetes
ansible-galaxy collection install kubernetes.core
```
