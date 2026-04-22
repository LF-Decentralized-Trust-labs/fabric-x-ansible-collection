
# hyperledger.fabricx.configtxgen

> Runs the `configtxgen` CLI tool to generate Fabric-X genesis blocks.


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [config/build](#task-config-build)
  - [bin/build](#task-bin-build)
  - [bin/install](#task-bin-install)
  - [bin/start](#task-bin-start)
  - [container/start](#task-container-start)
  - [start](#task-start)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-config-build"></a>

### config/build

Build the configtxgen configuration file


Generate `configtx.yaml` for Fabric-X genesis block creation.

Render the config template using the provided inputs, including the path selection controlled by `configtxgen_use_bin`.


```yaml
- name: Build the configtxgen configuration file
  vars:
    # Base build directory used to derive `configtxgen_artifacts_dir`.
    config_build_dir: "string"
    # Directory used for the generated config file and genesis block artifacts. The default derives from `config_build_dir`.
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
    # Directory containing fetched crypto artifacts used by the binary path and container mounts.
    fetched_artifacts_dir: "string"
    # Directory containing armageddon artifacts used by the binary path and container mounts.
    armageddon_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: config/build
```

<a id="task-bin-build"></a>

### bin/build

Build the configtxgen binary


Build the `configtxgen` binary from the Fabric-X source tree on the control node.

This entry point passes the binary destination to the shared `bin` role.


```yaml
- name: Build the configtxgen binary
  vars:
    # Git host used to derive `configtxgen_bin_package`.
    configtxgen_git_hub_url: github.com
    # Repository path used to derive `configtxgen_bin_package`.
    configtxgen_git_repo: hyperledger/fabric-x
    # Git reference used by the binary build and install entry points.
    configtxgen_git_commit: v0.0.8
    # Go package path for the `configtxgen` source tree.
    configtxgen_source_code_package: tools/configtxgen
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Directory used as the `configtxgen` binary destination or lookup path.
    cli_bin_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: bin/build
```

<a id="task-bin-install"></a>

### bin/install

Install the configtxgen binary


Install the `configtxgen` Go package through the shared `bin` role.

The package default derives from `configtxgen_git_hub_url`, `configtxgen_git_repo`, and `configtxgen_source_code_package`.


```yaml
- name: Install the configtxgen binary
  vars:
    # Git host used to derive `configtxgen_bin_package`.
    configtxgen_git_hub_url: github.com
    # Repository path used to derive `configtxgen_bin_package`.
    configtxgen_git_repo: hyperledger/fabric-x
    # Go package path for the `configtxgen` source tree.
    configtxgen_source_code_package: tools/configtxgen
    # Go package reference used by `bin/install`. The default derives from `configtxgen_git_hub_url`, `configtxgen_git_repo`, and `configtxgen_source_code_package`.
    configtxgen_bin_package: "{{ configtxgen_git_hub_url }}/{{ configtxgen_git_repo }}/{{ configtxgen_source_code_package }}"
    # Git reference used by the binary build and install entry points.
    configtxgen_git_commit: v0.0.8
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Directory used as the `configtxgen` binary destination or lookup path.
    cli_bin_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: bin/install
```

<a id="task-bin-start"></a>

### bin/start

Generate a genesis block with the configtxgen binary


Run the local `configtxgen` binary to generate the channel genesis block.

The artifacts directory default derives from `config_build_dir`, and the channel ID default derives from `channel_id`.


```yaml
- name: Generate a genesis block with the configtxgen binary
  vars:
    # Channel identifier used to derive `configtxgen_channel_id`.
    channel_id: "string"
    # Base build directory used to derive `configtxgen_artifacts_dir`.
    config_build_dir: "string"
    # Directory used as the `configtxgen` binary destination or lookup path.
    cli_bin_dir: "string"
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Channel identifier passed to `configtxgen` and used in the output block filename. The default derives from `channel_id`.
    configtxgen_channel_id: "{{ channel_id }}"
    # Config profile passed to `configtxgen`.
    configtxgen_profile_id: OrgsChannel
    # Directory used for the generated config file and genesis block artifacts. The default derives from `config_build_dir`.
    configtxgen_artifacts_dir: "{{ config_build_dir }}/configtxgen-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: bin/start
```

<a id="task-container-start"></a>

### container/start

Generate a genesis block with the configtxgen container


Run `configtxgen` in a container to generate the channel genesis block.

The image, artifacts directory, and channel ID defaults derive from the base registry, build, and channel inputs.


```yaml
- name: Generate a genesis block with the configtxgen container
  vars:
    # Channel identifier used to derive `configtxgen_channel_id`.
    channel_id: "string"
    # Base build directory used to derive `configtxgen_artifacts_dir`.
    config_build_dir: "string"
    # Directory used for the generated config file and genesis block artifacts. The default derives from `config_build_dir`.
    configtxgen_artifacts_dir: "{{ config_build_dir }}/configtxgen-artifacts"
    # Container name used by the container entry point.
    configtxgen_container_name: configtxgen
    # Image registry endpoint used to derive `configtxgen_image`. The default reads `CONFIGTXGEN_REGISTRY_ENDPOINT` and falls back to `docker.io/hyperledger`.
    configtxgen_registry_endpoint: "{{ lookup('env', 'CONFIGTXGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Image repository name used to derive `configtxgen_image`.
    configtxgen_image_name: fabric-x-tools
    # Image tag used to derive `configtxgen_image`.
    configtxgen_image_tag: 0.0.8
    # Full container image reference for `configtxgen`. The default derives from `configtxgen_registry_endpoint`, `configtxgen_image_name`, and `configtxgen_image_tag`.
    configtxgen_image: "{{ configtxgen_registry_endpoint }}/{{ configtxgen_image_name }}:{{ configtxgen_image_tag }}"
    # Executable name used by the binary and container entry points.
    configtxgen_bin_name: configtxgen
    # Channel identifier passed to `configtxgen` and used in the output block filename. The default derives from `channel_id`.
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
    # Directory containing armageddon artifacts used by the binary path and container mounts.
    armageddon_artifacts_dir: "string"
    # Directory containing fetched crypto artifacts used by the binary path and container mounts.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: container/start
```

<a id="task-start"></a>

### start

Dispatch genesis block generation


Select the binary or container execution path for `configtxgen`.

The concrete entry point validates the remaining inputs.


```yaml
- name: Dispatch genesis block generation
  vars:
    # Dispatch selector for the public start entry point and the config template branch selection. When false, the container path is used.
    configtxgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxgen
    tasks_from: start
```


