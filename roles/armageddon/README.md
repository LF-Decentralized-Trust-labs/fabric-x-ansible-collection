# hyperledger.fabricx.armageddon

> Runs the `armageddon` CLI tool for genesis block and shared config generation.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [create_shared_config](#create_shared_config)
  - [bin/install](#bininstall)
  - [bin/build](#binbuild)
  - [bin/create_shared_config](#bincreate_shared_config)
  - [container/create_shared_config](#containercreate_shared_config)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### config/build

Render the shared Armageddon config

Render `shared_config.yaml` for the Fabric-X orderer topology.

When `armageddon_use_bin` is true, the template reads `fetched_artifacts_dir`; otherwise it uses `armageddon_container_crypto_artifacts_dir`.

```yaml
- name: Render the shared Armageddon config
  vars:
    # Inventory hosts that form the Fabric-X orderer topology. Each host must expose `orderer_group`, `orderer_component_type`, `organization`, `ansible_host`, and `orderer_rpc_port`.
    armageddon_orderer_hosts: ["entry1", "entry2"]
    # Run Armageddon as a local binary instead of a container. Default is `false`.
    armageddon_use_bin: false
    # Base directory for the default `armageddon_artifacts_dir` value.
    config_build_dir: "string"
    # Directory for rendered Armageddon config and generated protobuf output. The default derives from `config_build_dir`.
    armageddon_artifacts_dir: "{{ config_build_dir }}/armageddon-artifacts"
    # Host directory with fetched crypto artifacts. The config build flow reads it in binary mode and the container flow mounts it read-only.
    fetched_artifacts_dir: "string"
    # Container directory for mounted crypto artifacts. Default is `/tmp/crypto`.
    armageddon_container_crypto_artifacts_dir: /tmp/crypto
    # Shared-config filename. Default is `shared_config.yaml`.
    armageddon_shared_config_file: shared_config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: config/build
```

### create_shared_config

Dispatch shared-config generation

Dispatch shared-config generation to the binary or container flow.

`armageddon_use_bin` selects which sub-entry point runs.

```yaml
- name: Dispatch shared-config generation
  vars:
    # Run Armageddon as a local binary instead of a container. Default is `false`.
    armageddon_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: create_shared_config
```

### bin/install

Install the Armageddon binary

Install Armageddon through the shared binary helper.

`armageddon_bin_package` defaults to the Go module path built from `armageddon_git_hub_url`, `armageddon_git_repo`, and `armageddon_source_code_package`.

```yaml
- name: Install the Armageddon binary
  vars:
    # Armageddon executable name. Default is `armageddon`.
    armageddon_bin_name: armageddon
    # Go module path used to install Armageddon. The default derives from `armageddon_git_hub_url`, `armageddon_git_repo`, and `armageddon_source_code_package`.
    armageddon_bin_package: "{{ armageddon_git_hub_url }}/{{ armageddon_git_repo }}/{{ armageddon_source_code_package }}"
    # Git host used for the Armageddon source repository. Default is `github.com`.
    armageddon_git_hub_url: github.com
    # Armageddon source repository path. Default is `hyperledger/fabric-x-orderer`.
    armageddon_git_repo: hyperledger/fabric-x-orderer
    # Go package that builds the Armageddon binary. Default is `cmd/armageddon`.
    armageddon_source_code_package: cmd/armageddon
    # Git ref used for Armageddon builds and installs. Default is `v0.0.23`.
    armageddon_git_commit: v0.0.23
    # Directory where the Armageddon binary is installed or executed. The binary helper roles use this as the local or remote binary directory.
    cli_bin_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: bin/install
```

### bin/build

Build the Armageddon binary from source

Build Armageddon from source through the shared Go helper.

The Go source package comes from `armageddon_source_code_package`.

```yaml
- name: Build the Armageddon binary from source
  vars:
    # Armageddon executable name. Default is `armageddon`.
    armageddon_bin_name: armageddon
    # Git host used for the Armageddon source repository. Default is `github.com`.
    armageddon_git_hub_url: github.com
    # Armageddon source repository path. Default is `hyperledger/fabric-x-orderer`.
    armageddon_git_repo: hyperledger/fabric-x-orderer
    # Git ref used for Armageddon builds and installs. Default is `v0.0.23`.
    armageddon_git_commit: v0.0.23
    # Go package that builds the Armageddon binary. Default is `cmd/armageddon`.
    armageddon_source_code_package: cmd/armageddon
    # Directory where the Armageddon binary is installed or executed. The binary helper roles use this as the local or remote binary directory.
    cli_bin_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: bin/build
```

### bin/create_shared_config

Generate shared-config protobuf with the binary

Run the installed Armageddon binary to generate `shared_config.binpb`.

The input config is read from `armageddon_artifacts_dir`/`armageddon_shared_config_file` and the output is written back to `armageddon_artifacts_dir`.

```yaml
- name: Generate shared-config protobuf with the binary
  vars:
    # Armageddon executable name. Default is `armageddon`.
    armageddon_bin_name: armageddon
    # Base directory for the default `armageddon_artifacts_dir` value.
    config_build_dir: "string"
    # Directory for rendered Armageddon config and generated protobuf output. The default derives from `config_build_dir`.
    armageddon_artifacts_dir: "{{ config_build_dir }}/armageddon-artifacts"
    # Shared-config filename. Default is `shared_config.yaml`.
    armageddon_shared_config_file: shared_config.yaml
    # Directory where the Armageddon binary is installed or executed. The binary helper roles use this as the local or remote binary directory.
    cli_bin_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: bin/create_shared_config
```

### container/create_shared_config

Generate shared-config protobuf with a container

Run the Armageddon container to generate `shared_config.binpb`.

The image default derives from `armageddon_registry_endpoint`, `armageddon_image_name`, and `armageddon_image_tag`.

```yaml
- name: Generate shared-config protobuf with a container
  vars:
    # Armageddon container name. Default is `armageddon`.
    armageddon_container_name: armageddon
    # Registry endpoint for the Armageddon image. The default reads `ARMAGEDDON_REGISTRY_ENDPOINT` and falls back to `docker.io/hyperledger`.
    armageddon_registry_endpoint: "{{ lookup('env', 'ARMAGEDDON_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Armageddon image name. Default is `fabric-x-orderer`.
    armageddon_image_name: fabric-x-orderer
    # Armageddon image tag. Default is `0.0.21-1`.
    armageddon_image_tag: 0.0.21-1
    # Fully qualified Armageddon image reference. The default derives from `armageddon_registry_endpoint`, `armageddon_image_name`, and `armageddon_image_tag`.
    armageddon_image: "{{ armageddon_registry_endpoint }}/{{ armageddon_image_name }}:{{ armageddon_image_tag }}"
    # Container directory for the rendered shared config file. Default is `/tmp/config`.
    armageddon_container_config_dir: /tmp/config
    # Shared-config filename. Default is `shared_config.yaml`.
    armageddon_shared_config_file: shared_config.yaml
    # Container directory for generated protobuf output. Default is `/tmp/out`.
    armageddon_container_output_dir: /tmp/out
    # Base directory for the default `armageddon_artifacts_dir` value.
    config_build_dir: "string"
    # Directory for rendered Armageddon config and generated protobuf output. The default derives from `config_build_dir`.
    armageddon_artifacts_dir: "{{ config_build_dir }}/armageddon-artifacts"
    # Container directory for mounted crypto artifacts. Default is `/tmp/crypto`.
    armageddon_container_crypto_artifacts_dir: /tmp/crypto
    # Host directory with fetched crypto artifacts. The config build flow reads it in binary mode and the container flow mounts it read-only.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: container/create_shared_config
```
