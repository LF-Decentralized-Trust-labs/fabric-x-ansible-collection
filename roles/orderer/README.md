# hyperledger.fabricx.orderer

The role `hyperledger.fabricx.orderer` can be used to run the Fabric-X `orderer` components (i.e. `consensus`, `batcher`, `assembler` and `router`).

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
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)
  - [get\_metrics](#get_metrics)
- [Kubernetes mode](#kubernetes-mode)
  - [K8s resources per component instance](#k8s-resources-per-component-instance)
  - [Inventory setup](#inventory-setup)

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
| `orderer_use_k8s`              | `false`                                                         | Set to `true` to deploy as Kubernetes StatefulSets                        |
| `orderer_k8s_resource_name`    | `{{ inventory_hostname }}`                                      | K8s resource name prefix (StatefulSet, Services, Secret, ConfigMap)       |
| `orderer_k8s_wait`             | `true`                                                          | Wait for StatefulSet pods to become Ready after apply                     |
| `orderer_k8s_wait_timeout`     | `120`                                                           | Timeout in seconds when waiting for pods to become Ready                  |
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

The task `config/transfer` allows to transfer the configuration files for a Fabric-X Orderer on the remote node. The node configuration is rendered from a component-specific template (`config-{{ orderer_component_type }}.yaml.j2`) so the correct template is selected automatically from `orderer_component_type`. In Kubernetes mode, this creates a ConfigMap containing the node configuration, genesis block, and any mTLS CA certs.

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

The task `start` starts the Fabric-X Orderer component determined by `orderer_component_type` (`consensus`, `batcher`, `assembler`, or `router`) in the deployment mode selected by `orderer_use_k8s` / `orderer_use_bin`.

Components are started in dependency order: `consensus` → `batcher` → `assembler` → `router`. Ansible's sequential task execution across all hosts enforces this ordering naturally when all components belong to the same play.

```yaml
- name: Start the Fabric-X Orderer
  vars:
    orderer_component_type: consensus # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: start
```

### stop

The task `stop` stops the Fabric-X Orderer component. Components are stopped in reverse dependency order: `router` → `assembler` → `batcher` → `consensus`.

```yaml
- name: Stop the Fabric-X Orderer
  vars:
    orderer_component_type: consensus # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: stop
```

### teardown

The task `teardown` stops the Fabric-X Orderer component and removes all runtime-generated artifacts (data directory, K8s StatefulSet and Services). Configuration and crypto material are preserved. Components are torn down in reverse dependency order: `router` → `assembler` → `batcher` → `consensus`.

```yaml
- name: Teardown the Fabric-X Orderer
  vars:
    orderer_component_type: consensus # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: teardown
```

### wipe

The task `wipe` tears down the Fabric-X Orderer component and additionally removes all configuration files, binaries, and crypto material. Components are wiped in reverse dependency order: `router` → `assembler` → `batcher` → `consensus`.

```yaml
- name: Wipe the Fabric-X Orderer
  vars:
    orderer_component_type: consensus # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` fetches the logs from the Fabric-X Orderer component to the control node.

```yaml
- name: Fetch the Fabric-X Orderer logs
  vars:
    orderer_component_type: consensus # or batcher, assembler, router
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: fetch_logs
```

### ping

The task `ping` pings the Fabric-X Orderer component on its opened ports to verify it is running and reachable.

```yaml
- name: Ping the Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: ping
```

### get_metrics

The task `get_metrics` fetches the metrics from the Fabric-X Orderer component and prints them on stdout.

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
| `start`           | apply             | StatefulSet, headless Service, NodePort Service                 |
| `teardown`        | delete            | StatefulSet, Services, PVC — Secret and ConfigMap **preserved** |
| `wipe`            | teardown + delete | additionally deletes Secret and ConfigMap                       |

### K8s resources per component instance

**Secret** (`<resource-name>-secret`): created during `crypto/setup`, contains all crypto files read directly from the control node. Admin identity is derived from the genesis block via NodeOUs — no `admincerts` are needed on disk.

| Secret key             | Source file                |
| ---------------------- | -------------------------- |
| `msp-keystore-priv-sk` | `msp/keystore/priv_sk`     |
| `msp-signcert.pem`     | `msp/signcerts/<name>.pem` |
| `msp-cacert.pem`       | `msp/cacerts/<name>.pem`   |
| `msp-config.yaml`      | `msp/config.yaml`          |
| `tls-server.key`       | `tls/server.key`           |
| `tls-server.crt`       | `tls/server.crt`           |
| `tls-ca.crt`           | `tls/ca.crt`               |

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
