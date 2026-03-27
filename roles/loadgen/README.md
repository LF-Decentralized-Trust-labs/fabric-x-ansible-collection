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
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)
  - [get\_metrics](#get_metrics)
  - [limit\_rate](#limit_rate)

## Variables

| Variable                       | Default                                                 | Description                                                   |
| ------------------------------ | ------------------------------------------------------- | ------------------------------------------------------------- |
| `loadgen_registry_endpoint`    | `$LOADGEN_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                   |
| `loadgen_image_name`           | `fabric-x-loadgen`                                      | Container image name                                          |
| `loadgen_image_tag`            | `0.1.7`                                                 | Container image tag                                           |
| `loadgen_image`                | `{{ registry }}/{{ name }}:{{ tag }}`                   | Full container image reference                                |
| `loadgen_container_name`       | `{{ inventory_hostname }}`                              | Name given to the container                                   |
| `loadgen_git_uri`              | `https://github.com/hyperledger/fabric-x-committer.git` | Git repository used to build the binary                       |
| `loadgen_git_commit`           | `v0.1.7`                                                | Git ref (tag or commit) to check out                          |
| `loadgen_source_code_package`  | `cmd/loadgen`                                           | Go source package path within the repository                  |
| `loadgen_bin_package`          | `github.com/hyperledger/fabric-x-committer/cmd/loadgen` | Fully-qualified Go package used for `go install`              |
| `loadgen_bin_name`             | `loadgen`                                               | Name of the produced binary                                   |
| `loadgen_use_bin`              | `false`                                                 | Set to `true` to use the native binary instead of a container |
| `loadgen_remote_config_dir`    | `{{ remote_config_dir }}`                               | Configuration directory on the remote node                    |
| `loadgen_container_config_dir` | `/config`                                               | Configuration directory inside the container                  |
| `loadgen_config_file`          | `config-loadgen.yaml`                                   | Load generator configuration file name                        |
| `loadgen_admin_pub_key_file`   | `admin_pub_key.pem`                                     | Admin public key file name                                    |
| `loadgen_admin_priv_key_file`  | `admin_priv_key.pem`                                    | Admin private key file name                                   |
| `loadgen_assert_metrics`       | `false`                                                 | Assert metrics values after the load test                     |
| `loadgen_use_tls`              | `false`                                                 | Enable TLS                                                    |

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
