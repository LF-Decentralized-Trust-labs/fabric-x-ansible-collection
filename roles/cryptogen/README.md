# hyperledger.fabricx.cryptogen

> Renders cryptogen configuration, generates Fabric-X crypto material, and fetches MSP artifacts for orderer and peer organizations.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [fetch](#fetch)
  - [config/build](#configbuild)
  - [container/start](#containerstart)
  - [bin/install](#bininstall)
  - [bin/build](#binbuild)
  - [bin/start](#binstart)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.cryptogen
```

## Tasks

### start

> Select the cryptogen execution mode

Choose whether cryptogen runs as a binary or in a container. This dispatcher selects either the `bin/start` or `container/start` entry point so the role can render configuration and generate crypto material in the requested execution mode.

```yaml
- name: Select the cryptogen execution mode
  vars:
    # Selects binary mode when true; otherwise container mode is used.
    cryptogen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: start
```

### fetch

> Fetch generated MSP directories

Copy generated MSP directories for orderer and peer organizations into the fetched artifacts directory. The role mirrors each organization MSP subtree from `cryptogen_output_dir` into `{{ fetched_artifacts_dir }}/crypto/ordererOrganizations` and `{{ fetched_artifacts_dir }}/crypto/peerOrganizations`. Run this after crypto material has already been generated so downstream roles can consume the fetched artifacts.

```yaml
- name: Fetch generated MSP directories
  vars:
    # Sets the base directory for generated configuration artifacts. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Sets the destination directory for fetched MSP folders. Example: `/opt/hyperledger/fabricx/build/fetched-artifacts`.
    fetched_artifacts_dir: "/opt/hyperledger/fabricx/build/fetched-artifacts"
    # Sets the directory where cryptogen writes generated crypto material.
    cryptogen_output_dir: "{{ cryptogen_artifacts_dir }}/crypto"
    # Maps orderer organization domains to their organization definitions.
    cryptogen_orderers_by_org: {}
    # Maps peer organization domains to their organization definitions.
    cryptogen_peers_by_org: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: fetch
```

### config/build

> Build the cryptogen configuration file

Render `crypto-config.yaml` for the cryptogen CLI. This entry point gathers host IPv4 facts for referenced orderer and peer hosts before templating `{{ cryptogen_artifacts_dir }}/{{ cryptogen_config_file }}`. The rendered file captures the Fabric-X organization layout that cryptogen uses to generate orderer and peer MSP and TLS material.

```yaml
- name: Build the cryptogen configuration file
  vars:
    # Sets the base directory for generated configuration artifacts. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Sets the directory that stores cryptogen inputs and generated files.
    cryptogen_artifacts_dir: "{{ config_build_dir }}/cryptogen-artifacts"
    # Sets the cryptogen configuration filename.
    cryptogen_config_file: crypto-config.yaml
    # Maps orderer organization domains to their organization definitions.
    cryptogen_orderers_by_org: {}
    # Maps peer organization domains to their organization definitions.
    cryptogen_peers_by_org: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: config/build
```

### container/start

> Generate crypto material with a container

Clean the output directory and run the cryptogen CLI in a container. The container mounts the rendered configuration from `{{ cryptogen_artifacts_dir }}` and writes generated material to `{{ cryptogen_output_dir }}`. This entry point delegates container startup to `hyperledger.fabricx.container`.

```yaml
- name: Generate crypto material with a container
  vars:
    # Sets the base directory for generated configuration artifacts. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Sets the directory that stores cryptogen inputs and generated files.
    cryptogen_artifacts_dir: "{{ config_build_dir }}/cryptogen-artifacts"
    # Sets the directory where cryptogen writes generated crypto material.
    cryptogen_output_dir: "{{ cryptogen_artifacts_dir }}/crypto"
    # Sets the registry used for the cryptogen container image.
    cryptogen_registry_endpoint: "{{ lookup('env', 'CRYPTOGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the cryptogen image name.
    cryptogen_image_name: fabric-x-tools
    # Sets the cryptogen image tag.
    cryptogen_image_tag: 1.0.0-alpha
    # Sets the full cryptogen image reference.
    cryptogen_image: "{{ cryptogen_registry_endpoint }}/{{ cryptogen_image_name }}:{{ cryptogen_image_tag }}"
    # Sets the container name used for the cryptogen run.
    cryptogen_container_name: cryptogen
    # Sets the cryptogen executable name.
    cryptogen_bin_name: cryptogen
    # Sets the container directory that receives the mounted cryptogen inputs.
    cryptogen_container_artifacts_dir: /tmp/cryptogen-artifacts
    # Sets the container directory where cryptogen writes generated crypto material.
    cryptogen_container_output_dir: "{{ cryptogen_container_artifacts_dir }}/crypto"
    # Sets the cryptogen configuration filename.
    cryptogen_config_file: crypto-config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: container/start
```

### bin/install

> Install the cryptogen binary

Install the cryptogen binary through `hyperledger.fabricx.bin`. This entry point is intended for binary-mode deployments that execute cryptogen on the target host.

```yaml
- name: Install the cryptogen binary
  vars:
    # Sets the directory that receives the cryptogen binary. Example: `/opt/hyperledger/fabricx/bin`.
    cli_bin_dir: "/opt/hyperledger/fabricx/bin"
    # Sets the cryptogen executable name.
    cryptogen_bin_name: cryptogen
    # Sets the Git host used for the cryptogen source repository.
    cryptogen_git_hub_url: github.com
    # Sets the cryptogen source repository path.
    cryptogen_git_repo: hyperledger/fabric-x
    # Pins the cryptogen source revision.
    cryptogen_git_commit: v1.0.0-alpha
    # Sets the Go package path that contains the cryptogen source.
    cryptogen_source_code_package: tools/cryptogen
    # Sets the Go package path used to install cryptogen.
    cryptogen_bin_package: "{{ cryptogen_git_hub_url }}/{{ cryptogen_git_repo }}/{{ cryptogen_source_code_package }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: bin/install
```

### bin/build

> Build the cryptogen binary from source

Build the cryptogen binary from the configured source repository through `hyperledger.fabricx.bin`. This entry point builds on the control node and writes the binary into `cli_bin_dir` for later reuse by the binary start path.

```yaml
- name: Build the cryptogen binary from source
  vars:
    # Sets the directory that receives the cryptogen binary. Example: `/opt/hyperledger/fabricx/bin`.
    cli_bin_dir: "/opt/hyperledger/fabricx/bin"
    # Sets the cryptogen executable name.
    cryptogen_bin_name: cryptogen
    # Sets the Git host used for the cryptogen source repository.
    cryptogen_git_hub_url: github.com
    # Sets the cryptogen source repository path.
    cryptogen_git_repo: hyperledger/fabric-x
    # Pins the cryptogen source revision.
    cryptogen_git_commit: v1.0.0-alpha
    # Sets the Go package path that contains the cryptogen source.
    cryptogen_source_code_package: tools/cryptogen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: bin/build
```

### bin/start

> Generate crypto material with the binary

Clean the output directory and run the cryptogen binary on the target host. The binary consumes the rendered configuration from `{{ cryptogen_artifacts_dir }}` and writes generated material to `{{ cryptogen_output_dir }}`. This entry point delegates command execution to `hyperledger.fabricx.bin`.

```yaml
- name: Generate crypto material with the binary
  vars:
    # Sets the directory that receives the cryptogen binary. Example: `/opt/hyperledger/fabricx/bin`.
    cli_bin_dir: "/opt/hyperledger/fabricx/bin"
    # Sets the base directory for generated configuration artifacts. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Sets the directory that stores cryptogen inputs and generated files.
    cryptogen_artifacts_dir: "{{ config_build_dir }}/cryptogen-artifacts"
    # Sets the directory where cryptogen writes generated crypto material.
    cryptogen_output_dir: "{{ cryptogen_artifacts_dir }}/crypto"
    # Sets the cryptogen executable name.
    cryptogen_bin_name: cryptogen
    # Sets the cryptogen configuration filename.
    cryptogen_config_file: crypto-config.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: bin/start
```
