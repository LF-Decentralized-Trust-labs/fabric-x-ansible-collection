# hyperledger.fabricx.cryptogen

> Generates crypto material for Hyperledger Fabric-X networks using the `cryptogen` CLI tool.

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

Select the cryptogen execution mode

Choose whether cryptogen runs as a binary or in a container.

This dispatcher includes either the `bin/start` or `container/start` entry point.

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

Fetch generated MSP directories

Copy generated MSP directories for orderer and peer organizations into the fetched artifacts directory.

Run this after crypto material has already been generated.

```yaml
- name: Fetch generated MSP directories
  vars:
    # Sets the base directory for generated configuration artifacts.
    config_build_dir: "string"
    # Sets the destination directory for fetched MSP folders.
    fetched_artifacts_dir: "string"
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

Build the cryptogen configuration file

Render `crypto-config.yaml` for the cryptogen CLI.

This entry point gathers host IPv4 facts for referenced orderer and peer hosts before templating.

```yaml
- name: Build the cryptogen configuration file
  vars:
    # Sets the base directory for generated configuration artifacts.
    config_build_dir: "string"
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

Generate crypto material with a container

Clean the output directory and run the cryptogen CLI in a container.

This entry point delegates container startup to `hyperledger.fabricx.container`.

```yaml
- name: Generate crypto material with a container
  vars:
    # Sets the base directory for generated configuration artifacts.
    config_build_dir: "string"
    # Sets the directory that stores cryptogen inputs and generated files.
    cryptogen_artifacts_dir: "{{ config_build_dir }}/cryptogen-artifacts"
    # Sets the directory where cryptogen writes generated crypto material.
    cryptogen_output_dir: "{{ cryptogen_artifacts_dir }}/crypto"
    # Sets the registry used for the cryptogen container image.
    cryptogen_registry_endpoint: "{{ lookup('env', 'CRYPTOGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the cryptogen image name.
    cryptogen_image_name: fabric-x-tools
    # Sets the cryptogen image tag.
    cryptogen_image_tag: 0.0.8
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

Install the cryptogen binary

Install the cryptogen binary through `hyperledger.fabricx.bin`.

This entry point is intended for binary-mode deployments.

```yaml
- name: Install the cryptogen binary
  vars:
    # Sets the directory that receives the cryptogen binary.
    cli_bin_dir: "string"
    # Sets the cryptogen executable name.
    cryptogen_bin_name: cryptogen
    # Sets the Git host used for the cryptogen source repository.
    cryptogen_git_hub_url: github.com
    # Sets the cryptogen source repository path.
    cryptogen_git_repo: hyperledger/fabric-x
    # Pins the cryptogen source revision.
    cryptogen_git_commit: v0.0.8
    # Sets the Go package path that contains the cryptogen source.
    cryptogen_source_code_package: tools/cryptogen
    # Sets the Go package path used to install cryptogen.
    cryptogen_bin_package: "{{ cryptogen_git_hub_url }}/{{ cryptogen_git_repo }}/{{ cryptogen_source_code_package }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: bin/install
```

### bin/build

Build the cryptogen binary from source

Build the cryptogen binary from the configured source repository through `hyperledger.fabricx.bin`.

This entry point builds on the control node and writes the binary into `cli_bin_dir`.

```yaml
- name: Build the cryptogen binary from source
  vars:
    # Sets the directory that receives the cryptogen binary.
    cli_bin_dir: "string"
    # Sets the cryptogen executable name.
    cryptogen_bin_name: cryptogen
    # Sets the Git host used for the cryptogen source repository.
    cryptogen_git_hub_url: github.com
    # Sets the cryptogen source repository path.
    cryptogen_git_repo: hyperledger/fabric-x
    # Pins the cryptogen source revision.
    cryptogen_git_commit: v0.0.8
    # Sets the Go package path that contains the cryptogen source.
    cryptogen_source_code_package: tools/cryptogen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: bin/build
```

### bin/start

Generate crypto material with the binary

Clean the output directory and run the cryptogen binary on the target host.

This entry point delegates command execution to `hyperledger.fabricx.bin`.

```yaml
- name: Generate crypto material with the binary
  vars:
    # Sets the directory that receives the cryptogen binary.
    cli_bin_dir: "string"
    # Sets the base directory for generated configuration artifacts.
    config_build_dir: "string"
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
