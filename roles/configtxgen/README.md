# hyperledger.fabricx.configtxgen

The role `hyperledger.fabricx.configtxgen` can be used to run the `configtxgen` CLI tool.

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [start](#start)

## Variables

| Variable                                         | Default                                                     | Description                                                   |
| ------------------------------------------------ | ----------------------------------------------------------- | ------------------------------------------------------------- |
| `configtxgen_registry_endpoint`                  | `$CONFIGTXGEN_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                   |
| `configtxgen_image_name`                         | `fabric-x-tools`                                            | Container image name                                          |
| `configtxgen_image_tag`                          | `0.0.8`                                                     | Container image tag                                           |
| `configtxgen_image`                              | `{{ registry }}/{{ name }}:{{ tag }}`                       | Full container image reference                                |
| `configtxgen_container_name`                     | `configtxgen`                                               | Name given to the ephemeral container                         |
| `configtxgen_git_uri`                            | `https://github.com/hyperledger/fabric-x.git`               | Git repository used to build the binary                       |
| `configtxgen_git_commit`                         | `v0.0.8`                                                    | Git ref (tag or commit) to check out                          |
| `configtxgen_source_code_package`                | `tools/configtxgen`                                         | Go source package path within the repository                  |
| `configtxgen_bin_package`                        | `github.com/hyperledger/fabric-x/tools/configtxgen`         | Fully-qualified Go package used for `go install`              |
| `configtxgen_bin_name`                           | `configtxgen`                                               | Name of the produced binary                                   |
| `configtxgen_use_bin`                            | `false`                                                     | Set to `true` to use the native binary instead of a container |
| `configtxgen_artifacts_dir`                      | `{{ config_build_dir }}/configtxgen-artifacts`              | Directory on the controller where artifacts are written       |
| `configtxgen_container_artifacts_dir`            | `/tmp/configtxgen-artifacts`                                | Artifacts directory inside the container                      |
| `configtxgen_container_config_dir`               | `/tmp/config`                                               | Configuration directory inside the container                  |
| `configtxgen_container_crypto_artifacts_dir`     | `/tmp/crypto-artifacts`                                     | Crypto artifacts directory inside the container               |
| `configtxgen_armageddon_container_artifacts_dir` | `/tmp/armageddon-artifacts`                                 | Armageddon artifacts directory inside the container           |
| `configtxgen_armageddon_binpb_file`              | `shared_config.binpb`                                       | Armageddon shared config protobuf file name                   |
| `configtxgen_config_file`                        | `configtx.yaml`                                             | Name of the configtxgen configuration file                    |
| `configtxgen_channel_id`                         | `{{ channel_id }}`                                          | Channel ID for the genesis block                              |
| `configtxgen_profile_id`                         | `OrgsChannel`                                               | Profile ID used to generate the genesis block                 |
| `configtxgen_orderers_by_org`                    | `{}`                                                        | Map of orderers grouped by organization                       |
| `configtxgen_peers_by_org`                       | `{}`                                                        | Map of peers grouped by organization                          |

## Tasks

### config/build

The task `config/build` allows to generate the `configtx.yaml` configuration file which is later used to build the genesis block.

```yaml
- name: Generate configtx.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: config/build
```

### start

The task `start` allows to start `configtxgen` for the generation of the genesis block needed to bootstrap the Fabric-X network.

```yaml
- name: Generate the genesis block for Fabric-X
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: start
```
