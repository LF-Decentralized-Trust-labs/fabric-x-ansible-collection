# hyperledger.fabricx.configtxlator

> Wraps the configtxlator CLI for one-shot proto_encode, proto_decode, and compute_update operations through binary or container entry points.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [bin/build](#binbuild)
  - [bin/install](#bininstall)
  - [bin/proto\_encode](#binproto_encode)
  - [bin/proto\_decode](#binproto_decode)
  - [bin/compute\_update](#bincompute_update)
  - [container/proto\_encode](#containerproto_encode)
  - [container/proto\_decode](#containerproto_decode)
  - [container/compute\_update](#containercompute_update)
  - [proto\_encode](#proto_encode)
  - [proto\_decode](#proto_decode)
  - [compute\_update](#compute_update)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.configtxlator
```

## Tasks

### bin/build

> Build the configtxlator binary on the control node

Build the `configtxlator` binary from the Fabric-X source tree on the control node. The compiled executable is written to `cli_bin_dir` and reused by binary entry points.

```yaml
- name: Build the configtxlator binary on the control node
  vars:
    # Directory used as the `configtxlator` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Git reference used by the binary build and install entry points.
    configtxlator_git_commit: v1.0.0
    # Git host for `configtxlator_bin_package`.
    configtxlator_git_hub_url: github.com
    # Repository path for `configtxlator_bin_package`.
    configtxlator_git_repo: hyperledger/fabric-x
    # Go package path for the `configtxlator` source tree.
    configtxlator_source_code_package: tools/configtxlator
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: bin/build
```

### bin/install

> Install the configtxlator binary into the local bin directory

Install the `configtxlator` Go package through the shared `bin` role. The installed executable lands in `cli_bin_dir` and is then used by the binary entry points.

```yaml
- name: Install the configtxlator binary into the local bin directory
  vars:
    # Directory used as the `configtxlator` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Go package reference used by `bin/install`.
    configtxlator_bin_package: "{{ configtxlator_git_hub_url }}/{{ configtxlator_git_repo }}/{{ configtxlator_source_code_package }}"
    # Git reference used by the binary build and install entry points.
    configtxlator_git_commit: v1.0.0
    # Git host for `configtxlator_bin_package`.
    configtxlator_git_hub_url: github.com
    # Repository path for `configtxlator_bin_package`.
    configtxlator_git_repo: hyperledger/fabric-x
    # Go package path for the `configtxlator` source tree.
    configtxlator_source_code_package: tools/configtxlator
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: bin/install
```

### bin/proto_encode

> Run configtxlator proto_encode with the binary

Run `configtxlator proto_encode` one-shot through the locally installed binary.

```yaml
- name: Run configtxlator proto_encode with the binary
  vars:
    # Directory used as the `configtxlator` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Fully qualified protobuf message type passed to `proto_encode` and `proto_decode`. Example: `common.Block`.
    configtxlator_proto_type: "common.Block"
    # Path to the input file for `proto_encode` and `proto_decode`.
    configtxlator_input_file: "string"
    # Path to the output file written by `proto_encode`, `proto_decode`, and `compute_update`.
    configtxlator_output_file: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: bin/proto_encode
```

### bin/proto_decode

> Run configtxlator proto_decode with the binary

Run `configtxlator proto_decode` one-shot through the locally installed binary.

```yaml
- name: Run configtxlator proto_decode with the binary
  vars:
    # Directory used as the `configtxlator` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Fully qualified protobuf message type passed to `proto_encode` and `proto_decode`. Example: `common.Block`.
    configtxlator_proto_type: "common.Block"
    # Path to the input file for `proto_encode` and `proto_decode`.
    configtxlator_input_file: "string"
    # Path to the output file written by `proto_encode`, `proto_decode`, and `compute_update`.
    configtxlator_output_file: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: bin/proto_decode
```

### bin/compute_update

> Run configtxlator compute_update with the binary

Run `configtxlator compute_update` one-shot through the locally installed binary.

```yaml
- name: Run configtxlator compute_update with the binary
  vars:
    # Directory used as the `configtxlator` binary destination or lookup path. Example: `/opt/fabricx/bin`.
    cli_bin_dir: "/opt/fabricx/bin"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Channel identifier passed to the `compute_update` sub-command.
    configtxlator_channel_id: "string"
    # Path to the original config proto passed to `compute_update`.
    configtxlator_original_file: "string"
    # Path to the updated config proto passed to `compute_update`.
    configtxlator_updated_file: "string"
    # Path to the output file written by `proto_encode`, `proto_decode`, and `compute_update`.
    configtxlator_output_file: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: bin/compute_update
```

### container/proto_encode

> Run configtxlator proto_encode in a container

Run `configtxlator proto_encode` as a one-shot auto-removing container. Mounts `configtxlator_artifacts_dir` for input and output file access.

```yaml
- name: Run configtxlator proto_encode in a container
  vars:
    # Base build directory for `configtxlator_artifacts_dir`. Example: `/opt/fabricx/build`.
    config_build_dir: "/opt/fabricx/build"
    # Host directory mounted into the container for CLI operation input and output.
    configtxlator_artifacts_dir: "{{ config_build_dir }}/configtxlator-artifacts"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Directory path used inside the container for CLI operation input and output.
    configtxlator_container_artifacts_dir: /tmp/configtxlator-artifacts
    # Container name used by the container entry points.
    configtxlator_container_name: "configtxlator-{{ inventory_hostname }}"
    # Full container image reference for `configtxlator`.
    configtxlator_image: "{{ configtxlator_registry_endpoint }}/{{ configtxlator_image_name }}:{{ configtxlator_image_tag }}"
    # Image repository name for `configtxlator_image`.
    configtxlator_image_name: fabric-x-tools
    # Image tag for `configtxlator_image`.
    configtxlator_image_tag: 1.0.0
    # Path to the input file for `proto_encode` and `proto_decode`.
    configtxlator_input_file: "string"
    # Path to the output file written by `proto_encode`, `proto_decode`, and `compute_update`.
    configtxlator_output_file: "string"
    # Fully qualified protobuf message type passed to `proto_encode` and `proto_decode`. Example: `common.Block`.
    configtxlator_proto_type: "common.Block"
    # Image registry endpoint for `configtxlator_image`.
    configtxlator_registry_endpoint: "{{ lookup('env', 'CONFIGTXLATOR_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: container/proto_encode
```

### container/proto_decode

> Run configtxlator proto_decode in a container

Run `configtxlator proto_decode` as a one-shot auto-removing container. Mounts `configtxlator_artifacts_dir` for input and output file access.

```yaml
- name: Run configtxlator proto_decode in a container
  vars:
    # Base build directory for `configtxlator_artifacts_dir`. Example: `/opt/fabricx/build`.
    config_build_dir: "/opt/fabricx/build"
    # Host directory mounted into the container for CLI operation input and output.
    configtxlator_artifacts_dir: "{{ config_build_dir }}/configtxlator-artifacts"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Directory path used inside the container for CLI operation input and output.
    configtxlator_container_artifacts_dir: /tmp/configtxlator-artifacts
    # Container name used by the container entry points.
    configtxlator_container_name: "configtxlator-{{ inventory_hostname }}"
    # Full container image reference for `configtxlator`.
    configtxlator_image: "{{ configtxlator_registry_endpoint }}/{{ configtxlator_image_name }}:{{ configtxlator_image_tag }}"
    # Image repository name for `configtxlator_image`.
    configtxlator_image_name: fabric-x-tools
    # Image tag for `configtxlator_image`.
    configtxlator_image_tag: 1.0.0
    # Path to the input file for `proto_encode` and `proto_decode`.
    configtxlator_input_file: "string"
    # Path to the output file written by `proto_encode`, `proto_decode`, and `compute_update`.
    configtxlator_output_file: "string"
    # Fully qualified protobuf message type passed to `proto_encode` and `proto_decode`. Example: `common.Block`.
    configtxlator_proto_type: "common.Block"
    # Image registry endpoint for `configtxlator_image`.
    configtxlator_registry_endpoint: "{{ lookup('env', 'CONFIGTXLATOR_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: container/proto_decode
```

### container/compute_update

> Run configtxlator compute_update in a container

Run `configtxlator compute_update` as a one-shot auto-removing container. Mounts `configtxlator_artifacts_dir` for input and output file access.

```yaml
- name: Run configtxlator compute_update in a container
  vars:
    # Base build directory for `configtxlator_artifacts_dir`. Example: `/opt/fabricx/build`.
    config_build_dir: "/opt/fabricx/build"
    # Host directory mounted into the container for CLI operation input and output.
    configtxlator_artifacts_dir: "{{ config_build_dir }}/configtxlator-artifacts"
    # Executable name used by the binary and container entry points.
    configtxlator_bin_name: configtxlator
    # Channel identifier passed to the `compute_update` sub-command.
    configtxlator_channel_id: "string"
    # Directory path used inside the container for CLI operation input and output.
    configtxlator_container_artifacts_dir: /tmp/configtxlator-artifacts
    # Container name used by the container entry points.
    configtxlator_container_name: "configtxlator-{{ inventory_hostname }}"
    # Full container image reference for `configtxlator`.
    configtxlator_image: "{{ configtxlator_registry_endpoint }}/{{ configtxlator_image_name }}:{{ configtxlator_image_tag }}"
    # Image repository name for `configtxlator_image`.
    configtxlator_image_name: fabric-x-tools
    # Image tag for `configtxlator_image`.
    configtxlator_image_tag: 1.0.0
    # Path to the original config proto passed to `compute_update`.
    configtxlator_original_file: "string"
    # Path to the output file written by `proto_encode`, `proto_decode`, and `compute_update`.
    configtxlator_output_file: "string"
    # Image registry endpoint for `configtxlator_image`.
    configtxlator_registry_endpoint: "{{ lookup('env', 'CONFIGTXLATOR_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Path to the updated config proto passed to `compute_update`.
    configtxlator_updated_file: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: container/compute_update
```

### proto_encode

> Dispatch proto_encode to binary or container

Select the binary or container execution path for `proto_encode` based on `configtxlator_use_bin`.

```yaml
- name: Dispatch proto_encode to binary or container
  vars:
    # Dispatch selector for the public entry points. When false, the container path is used.
    configtxlator_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: proto_encode
```

### proto_decode

> Dispatch proto_decode to binary or container

Select the binary or container execution path for `proto_decode` based on `configtxlator_use_bin`.

```yaml
- name: Dispatch proto_decode to binary or container
  vars:
    # Dispatch selector for the public entry points. When false, the container path is used.
    configtxlator_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: proto_decode
```

### compute_update

> Dispatch compute_update to binary or container

Select the binary or container execution path for `compute_update` based on `configtxlator_use_bin`.

```yaml
- name: Dispatch compute_update to binary or container
  vars:
    # Dispatch selector for the public entry points. When false, the container path is used.
    configtxlator_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.configtxlator
    tasks_from: compute_update
```
