# hyperledger.fabricx.armageddon

The role `hyperledger.fabricx.armageddon` can be used to run the `armageddon` CLI tool. The role allows to run it both as binary and as container.

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [create\_shared\_config](#create_shared_config)

## Variables

| Variable                                    | Default                                                    | Description                                                   |
| ------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------- |
| `armageddon_registry_endpoint`              | `$ARMAGEDDON_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                   |
| `armageddon_image_name`                     | `fabric-x-orderer`                                         | Container image name                                          |
| `armageddon_image_tag`                      | `0.0.21-1`                                                   | Container image tag                                           |
| `armageddon_image`                          | `{{ registry }}/{{ name }}:{{ tag }}`                      | Full container image reference                                |
| `armageddon_container_name`                 | `armageddon`                                               | Name given to the ephemeral container                         |
| `armageddon_git_uri`                        | `https://github.com/hyperledger/fabric-x-orderer.git`      | Git repository used to build the binary                       |
| `armageddon_git_commit`                     | `v0.0.21-1`                                                  | Git ref (tag or commit) to check out                          |
| `armageddon_source_code_package`            | `cmd/armageddon`                                           | Go source package path within the repository                  |
| `armageddon_bin_package`                    | `github.com/hyperledger/fabric-x-orderer/cmd/armageddon`   | Fully-qualified Go package used for `go install`              |
| `armageddon_bin_name`                       | `armageddon`                                               | Name of the produced binary                                   |
| `armageddon_use_bin`                        | `false`                                                    | Set to `true` to use the native binary instead of a container |
| `armageddon_artifacts_dir`                  | `{{ config_build_dir }}/armageddon-artifacts`              | Directory on the controller where artifacts are written       |
| `armageddon_container_output_dir`           | `/tmp/out`                                                 | Output directory inside the container                         |
| `armageddon_container_config_dir`           | `/tmp/config`                                              | Config directory inside the container                         |
| `armageddon_container_crypto_artifacts_dir` | `/tmp/crypto`                                              | Crypto artifacts directory inside the container               |
| `armageddon_config_file`                    | `armageddon.yaml`                                          | Name of the armageddon configuration file                     |
| `armageddon_shared_config_file`             | `shared_config.yaml`                                       | Name of the shared configuration file                         |

## Tasks

### config/build

The task `config/build` allows to generate the `shared_config.yaml` configuration file which is later used to build the `shared_config.binpb` protobuf.

```yaml
- name: Generate shared_config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: config/build
```

### create_shared_config

The task `create_shared_config` allows to generate the `shared_config.binpb` serialized protobuf which contains all the necessary configuration to bootstrap the Fabric-X Orderer. This block can be embedded in the genesis block to provide such configuration to the orderers.

```yaml
- name: Generate shared_config.binpb
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: create_shared_config
```
