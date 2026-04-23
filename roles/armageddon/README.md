# hyperledger.fabricx.armageddon

> Automates the `armageddon` CLI for Fabric-X shared orderer configuration generation. The role renders `shared_config.yaml` from the orderer inventory and then runs Armageddon in binary or container mode to produce `shared_config.binpb`. It consumes the crypto artifacts prepared by the crypto roles and the artifact directory selected for the chosen run mode.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [create_shared_config](#create_shared_config)
  - [bin/install](#bininstall)
  - [bin/build](#binbuild)
  - [bin/create_shared_config](#bincreate_shared_config)
  - [container/create_shared_config](#containercreate_shared_config)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.armageddon
```

## Tasks

### config/build

> Render the shared Armageddon config

Render `shared_config.yaml` for the Fabric-X orderer topology.This entry point prepares the config consumed by both the binary and container shared-config flows.When `armageddon_use_bin` is true, the template reads `fetched_artifacts_dir`; otherwise it uses `armageddon_container_crypto_artifacts_dir`.

```yaml
- name: Render the shared Armageddon config
  vars:
    # Inventory hosts that form the Fabric-X orderer topology. Each host must expose `orderer_group`, `orderer_component_type`, `organization`, `ansible_host`, and `orderer_rpc_port`. Example: `['orderer1', 'orderer2', 'orderer3']`
    armageddon_orderer_hosts:
      - orderer1
      - orderer2
      - orderer3
    # Run Armageddon as a local binary instead of a container.
    armageddon_use_bin: false
    # Base directory for `armageddon_artifacts_dir`. Example: `/opt/fabricx/build/armageddon`.
    config_build_dir: "/opt/fabricx/build/armageddon"
    # Directory for rendered Armageddon config and generated protobuf output.
    armageddon_artifacts_dir: "{{ config_build_dir }}/armageddon-artifacts"
    # Host directory with fetched crypto artifacts. The binary flow reads this directory directly and the container flow mounts it read-only. Example: `/opt/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "/opt/fabricx/fetched-artifacts"
    # Container directory for mounted crypto artifacts.
    armageddon_container_crypto_artifacts_dir: /tmp/crypto
    # Armageddon config filename.
    armageddon_config_file: armageddon.yaml
    # Shared-config filename.
    armageddon_shared_config_file: shared_config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: config/build
```

### create_shared_config

> Dispatch shared-config generation

Dispatch shared-config generation to the binary or container flow.This is the top-level Armageddon entry point for producing `shared_config.binpb` from the rendered shared config.`armageddon_use_bin` selects which sub-entry point runs.

```yaml
- name: Dispatch shared-config generation
  vars:
    # Run Armageddon as a local binary instead of a container.
    armageddon_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: create_shared_config
```

### bin/install

> Install the Armageddon binary

Install the Armageddon CLI through the shared binary helper for binary-mode deployments.The helper installs `armageddon_bin_name` into `cli_bin_dir` from `armageddon_bin_package` at `armageddon_git_commit`.

```yaml
- name: Install the Armageddon binary
  vars:
    # Armageddon executable name.
    armageddon_bin_name: armageddon
    # Go module path used to install Armageddon.
    armageddon_bin_package: "{{ armageddon_git_hub_url }}/{{ armageddon_git_repo }}/{{ armageddon_source_code_package }}"
    # Git host used for the Armageddon source repository.
    armageddon_git_hub_url: github.com
    # Armageddon source repository path.
    armageddon_git_repo: hyperledger/fabric-x-orderer
    # Go package that builds the Armageddon binary.
    armageddon_source_code_package: cmd/armageddon
    # Git ref used for Armageddon builds and installs.
    armageddon_git_commit: v0.0.23
    # Directory where the Armageddon binary is installed or executed. The binary helper roles use this as the local or remote binary directory. Example: `/usr/local/bin`.
    cli_bin_dir: "/usr/local/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: bin/install
```

### bin/build

> Build the Armageddon binary from source

Build the Armageddon CLI from source through the shared Go helper for binary-mode deployments.The helper checks out `armageddon_git_repo` at `armageddon_git_commit`, builds `armageddon_source_code_package`, and places the executable in `cli_bin_dir`.

```yaml
- name: Build the Armageddon binary from source
  vars:
    # Armageddon executable name.
    armageddon_bin_name: armageddon
    # Git host used for the Armageddon source repository.
    armageddon_git_hub_url: github.com
    # Armageddon source repository path.
    armageddon_git_repo: hyperledger/fabric-x-orderer
    # Git ref used for Armageddon builds and installs.
    armageddon_git_commit: v0.0.23
    # Go package that builds the Armageddon binary.
    armageddon_source_code_package: cmd/armageddon
    # Directory where the Armageddon binary is installed or executed. The binary helper roles use this as the local or remote binary directory. Example: `/usr/local/bin`.
    cli_bin_dir: "/usr/local/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: bin/build
```

### bin/create_shared_config

> Generate shared-config protobuf with the binary

Run the installed Armageddon binary to generate `shared_config.binpb`.This binary-mode entry point reads `armageddon_artifacts_dir`/`armageddon_shared_config_file` and writes the protobuf output back to `armageddon_artifacts_dir`.

```yaml
- name: Generate shared-config protobuf with the binary
  vars:
    # Armageddon executable name.
    armageddon_bin_name: armageddon
    # Base directory for `armageddon_artifacts_dir`. Example: `/opt/fabricx/build/armageddon`.
    config_build_dir: "/opt/fabricx/build/armageddon"
    # Directory for rendered Armageddon config and generated protobuf output.
    armageddon_artifacts_dir: "{{ config_build_dir }}/armageddon-artifacts"
    # Armageddon config filename.
    armageddon_config_file: armageddon.yaml
    # Shared-config filename.
    armageddon_shared_config_file: shared_config.yaml
    # Directory where the Armageddon binary is installed or executed. The binary helper roles use this as the local or remote binary directory. Example: `/usr/local/bin`.
    cli_bin_dir: "/usr/local/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: bin/create_shared_config
```

### container/create_shared_config

> Generate shared-config protobuf with a container

Run the Armageddon container to generate `shared_config.binpb` for container-mode deployments.The container mounts the rendered shared config, crypto artifacts, and output directory before invoking the Armageddon CLI.

```yaml
- name: Generate shared-config protobuf with a container
  vars:
    # Armageddon container name.
    armageddon_container_name: armageddon
    # Registry endpoint for the Armageddon image.
    armageddon_registry_endpoint: "{{ lookup('env', 'ARMAGEDDON_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Armageddon image name.
    armageddon_image_name: fabric-x-orderer
    # Armageddon image tag.
    armageddon_image_tag: 0.0.21-1
    # Fully qualified Armageddon image reference.
    armageddon_image: "{{ armageddon_registry_endpoint }}/{{ armageddon_image_name }}:{{ armageddon_image_tag }}"
    # Container directory for the rendered shared config file.
    armageddon_container_config_dir: /tmp/config
    # Armageddon config filename.
    armageddon_config_file: armageddon.yaml
    # Shared-config filename.
    armageddon_shared_config_file: shared_config.yaml
    # Container directory for generated protobuf output.
    armageddon_container_output_dir: /tmp/out
    # Base directory for `armageddon_artifacts_dir`. Example: `/opt/fabricx/build/armageddon`.
    config_build_dir: "/opt/fabricx/build/armageddon"
    # Directory for rendered Armageddon config and generated protobuf output.
    armageddon_artifacts_dir: "{{ config_build_dir }}/armageddon-artifacts"
    # Container directory for mounted crypto artifacts.
    armageddon_container_crypto_artifacts_dir: /tmp/crypto
    # Host directory with fetched crypto artifacts. The binary flow reads this directory directly and the container flow mounts it read-only. Example: `/opt/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "/opt/fabricx/fetched-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.armageddon
    tasks_from: container/create_shared_config
```
