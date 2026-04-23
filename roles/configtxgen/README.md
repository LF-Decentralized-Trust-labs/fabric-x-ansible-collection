# hyperledger.fabricx.configtxgen

> Generates Fabric-X `configtx.yaml` and genesis block artifacts with `configtxgen` through binary or container entry points.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [config/build](#configbuild)
  - [bin/build](#binbuild)
  - [bin/install](#bininstall)
  - [bin/start](#binstart)
  - [container/start](#containerstart)
  - [start](#start)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.configtxgen
```

## Tasks

### config/build

> Render the configtxgen configuration file

Generate `configtx.yaml` for Fabric-X genesis block creation.Render the config template from the selected crypto and armageddon artifact roots, then place it under `configtxgen_artifacts_dir`.The template switches between the binary and container artifact paths based on `configtxgen_use_bin`.

```yaml
- name: Render the configtxgen configuration file
  vars:
    # Base build directory for `configtxgen_artifacts_dir`. Example: `/opt/fabricx/build/configtxgen`.
    config_build_dir: "/opt/fabricx/build/configtxgen"
    # Directory used for the generated config file and genesis block artifacts.
    configtxgen_artifacts_dir: "{{ config_build_dir }}/configtxgen-artifacts"
    # Dispatch selector for the public start entry point and the config template branch selection. When false, the container path is used.
    configtxgen_use_bin: false
    # Container mount path for fetched crypto artifacts.
    configtxgen_container_crypto_artifacts_dir: /tmp/crypto-artifacts
    # Container mount path for armageddon artifacts.
    configtxgen_armageddon_container_artifacts_dir: /tmp/armageddon-artifacts
    # Generated configuration file name written by `config/build` and mounted by `container/start`.
    configtxgen_config_file: configtx.yaml
    # Shared config binary file name consumed by the config template.
    configtxgen_armageddon_binpb_file: shared_config.binpb
    # Orderer organization map rendered into `configtx.yaml`.
    configtxgen_orderers_by_org: {}
    # Peer organization map rendered into `configtx.yaml`.
    configtxgen_peers_by_org: {}
    # Directory containing fetched crypto artifacts used by the binary path and container mounts. Example: `/opt/fabricx/artifacts/crypto`.
    fetched_artifacts_dir: "/opt/fabricx/artifacts/crypto"
    # Directory containing armageddon artifacts used by the binary path and container mounts. Example: `/opt/fabricx/artifacts/armageddon`.
    armageddon_artifacts_dir: "/opt/fabricx/artifacts/armageddon"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: config/build
```

### bin/build

> Build the configtxgen binary on the control node

Build the `configtxgen` binary from the Fabric-X source tree on the control node.The compiled executable is written to `cli_bin_dir` and reused by the binary start entry point.

```yaml
- name: Build the configtxgen binary on the control node
  vars:
    # Git host for `configtxgen_bin_package`.
    configtxgen_git_hub_url: github.com
    # Repository path for `configtxgen_bin_package`.
    configtxgen_git_repo: hyperledger/fabric-x
    # Git reference used by the binary build and install entry points.
    configtxgen_git_commit: v0.0.8
    # Go package path for the `configtxgen` source tree.
    configtxgen_source_code_package: tools/configtxgen
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Directory used as the `configtxgen` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: bin/build
```

### bin/install

> Install the configtxgen binary into the local bin directory

Install the `configtxgen` Go package through the shared `bin` role.The installed executable lands in `cli_bin_dir` and is then used by the binary start entry point.

```yaml
- name: Install the configtxgen binary into the local bin directory
  vars:
    # Git host for `configtxgen_bin_package`.
    configtxgen_git_hub_url: github.com
    # Repository path for `configtxgen_bin_package`.
    configtxgen_git_repo: hyperledger/fabric-x
    # Go package path for the `configtxgen` source tree.
    configtxgen_source_code_package: tools/configtxgen
    # Go package reference used by `bin/install`.
    configtxgen_bin_package: "{{ configtxgen_git_hub_url }}/{{ configtxgen_git_repo }}/{{ configtxgen_source_code_package }}"
    # Git reference used by the binary build and install entry points.
    configtxgen_git_commit: v0.0.8
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Directory used as the `configtxgen` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: bin/install
```

### bin/start

> Generate a genesis block with the configtxgen binary

Run the local `configtxgen` binary to generate the channel genesis block.The output block is written beneath `configtxgen_artifacts_dir` as `<channel_id>_block.pb`; with the bundled example channel, that becomes `fabricx-main-channel_block.pb`.

```yaml
- name: Generate a genesis block with the configtxgen binary
  vars:
    # Channel identifier for `configtxgen_channel_id`. Example: `fabricx-main-channel`.
    channel_id: "fabricx-main-channel"
    # Base build directory for `configtxgen_artifacts_dir`. Example: `/opt/fabricx/build/configtxgen`.
    config_build_dir: "/opt/fabricx/build/configtxgen"
    # Directory used as the `configtxgen` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Channel identifier passed to `configtxgen` and used in the output block filename.
    configtxgen_channel_id: "{{ channel_id }}"
    # Config profile passed to `configtxgen`.
    configtxgen_profile_id: OrgsChannel
    # Directory used for the generated config file and genesis block artifacts.
    configtxgen_artifacts_dir: "{{ config_build_dir }}/configtxgen-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: bin/start
```

### container/start

> Generate a genesis block with the configtxgen container

Run `configtxgen` in a container to generate the channel genesis block.The container consumes the rendered `configtx.yaml` plus mounted crypto and armageddon artifacts, then writes `<channel_id>_block.pb` beneath `configtxgen_container_artifacts_dir`.

```yaml
- name: Generate a genesis block with the configtxgen container
  vars:
    # Channel identifier for `configtxgen_channel_id`. Example: `fabricx-main-channel`.
    channel_id: "fabricx-main-channel"
    # Base build directory for `configtxgen_artifacts_dir`. Example: `/opt/fabricx/build/configtxgen`.
    config_build_dir: "/opt/fabricx/build/configtxgen"
    # Directory used for the generated config file and genesis block artifacts.
    configtxgen_artifacts_dir: "{{ config_build_dir }}/configtxgen-artifacts"
    # Container name used by the container entry point.
    configtxgen_container_name: configtxgen
    # Image registry endpoint for `configtxgen_image`.
    configtxgen_registry_endpoint: "{{ lookup('env', 'CONFIGTXGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image repository name for `configtxgen_image`.
    configtxgen_image_name: fabric-x-tools
    # Image tag for `configtxgen_image`.
    configtxgen_image_tag: 0.0.8
    # Full container image reference for `configtxgen`.
    configtxgen_image: "{{ configtxgen_registry_endpoint }}/{{ configtxgen_image_name }}:{{ configtxgen_image_tag }}"
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Channel identifier passed to `configtxgen` and used in the output block filename.
    configtxgen_channel_id: "{{ channel_id }}"
    # Config profile passed to `configtxgen`.
    configtxgen_profile_id: OrgsChannel
    # Container mount path for `configtx.yaml`.
    configtxgen_container_config_dir: /tmp/config
    # Container output directory used by `container/start`.
    configtxgen_container_artifacts_dir: /tmp/configtxgen-artifacts
    # Generated configuration file name written by `config/build` and mounted by `container/start`.
    configtxgen_config_file: configtx.yaml
    # Container mount path for armageddon artifacts.
    configtxgen_armageddon_container_artifacts_dir: /tmp/armageddon-artifacts
    # Container mount path for fetched crypto artifacts.
    configtxgen_container_crypto_artifacts_dir: /tmp/crypto-artifacts
    # Shared config binary file name consumed by the config template.
    configtxgen_armageddon_binpb_file: shared_config.binpb
    # Directory containing armageddon artifacts used by the binary path and container mounts. Example: `/opt/fabricx/artifacts/armageddon`.
    armageddon_artifacts_dir: "/opt/fabricx/artifacts/armageddon"
    # Directory containing fetched crypto artifacts used by the binary path and container mounts. Example: `/opt/fabricx/artifacts/crypto`.
    fetched_artifacts_dir: "/opt/fabricx/artifacts/crypto"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: container/start
```

### start

> Dispatch genesis block generation to binary or container

Select the binary or container execution path for `configtxgen` based on `configtxgen_use_bin`.Both execution paths consume the rendered configuration and emit the same `<channel_id>_block.pb` artifact name.

```yaml
- name: Dispatch genesis block generation to binary or container
  vars:
    # Dispatch selector for the public start entry point and the config template branch selection. When false, the container path is used.
    configtxgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: start
```
