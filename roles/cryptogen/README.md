# hyperledger.fabricx.cryptogen

The role `hyperledger.fabricx.cryptogen` can be used to run the `cryptogen` CLI tool.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [start](#start)
  - [fetch](#fetch)

## Prerequisites

The role requires:

- `go` to be installed.

## Variables

| Variable                            | Default                                                   | Description                                                   |
| ----------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------- |
| `cryptogen_registry_endpoint`       | `$CRYPTOGEN_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                   |
| `cryptogen_image_name`              | `fabric-x-tools`                                          | Container image name                                          |
| `cryptogen_image_tag`               | `0.0.8`                                                   | Container image tag                                           |
| `cryptogen_image`                   | `{{ registry }}/{{ name }}:{{ tag }}`                     | Full container image reference                                |
| `cryptogen_container_name`          | `cryptogen`                                               | Name given to the ephemeral container                         |
| `cryptogen_git_uri`                 | `https://github.com/hyperledger/fabric-x.git`             | Git repository used to build the binary                       |
| `cryptogen_git_commit`              | `v0.0.8`                                                  | Git ref (tag or commit) to check out                          |
| `cryptogen_source_code_package`     | `tools/cryptogen`                                         | Go source package path within the repository                  |
| `cryptogen_bin_package`             | `github.com/hyperledger/fabric-x/tools/cryptogen`         | Fully-qualified Go package used for `go install`              |
| `cryptogen_bin_name`                | `cryptogen`                                               | Name of the produced binary                                   |
| `cryptogen_use_bin`                 | `false`                                                   | Set to `true` to use the native binary instead of a container |
| `cryptogen_artifacts_dir`           | `{{ config_build_dir }}/cryptogen-artifacts`              | Directory on the controller where artifacts are written       |
| `cryptogen_output_dir`              | `{{ cryptogen_artifacts_dir }}/crypto`                    | Crypto output directory on the controller                     |
| `cryptogen_container_artifacts_dir` | `/tmp/cryptogen-artifacts`                                | Artifacts directory inside the container                      |
| `cryptogen_container_output_dir`    | `{{ cryptogen_container_artifacts_dir }}/crypto`          | Crypto output directory inside the container                  |
| `cryptogen_config_file`             | `crypto-config.yaml`                                      | Name of the cryptogen configuration file                      |
| `cryptogen_orderers_by_org`         | `{}`                                                      | Map of orderers grouped by organization                       |
| `cryptogen_peers_by_org`            | `{}`                                                      | Map of peers grouped by organization                          |
| `cryptogen_users_by_org`            | `{}`                                                      | Map of users grouped by organization                          |

## Tasks

### config/build

The task `config/build` allows to generate the `crypto-config.yaml` configuration file which is later used to generate the crypto material with `cryptogen`.

```yaml
- name: Generate crypto-config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: config/build
```

### start

The task `start` allows to start `cryptogen` for the generation of the crypto material needed to run the Fabric-X network.

```yaml
- name: Generate the crypto material for Fabric-X with cryptogen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: start
```

### fetch

The task `fetch` allows to _emulate_ the fetch operation that is performed to collect the MSP folder of each organization when run using Fabric-CA (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)).

```yaml
- name: Copy the MSP folder of each Fabric-X organization
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: fetch
```
