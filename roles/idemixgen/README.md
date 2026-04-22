
# hyperledger.fabricx.idemixgen

> Runs the `idemixgen` CLI tool for Idemix CA key generation and signer configuration.


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [ca-keygen](#task-ca-keygen)
  - [signerconfig](#task-signerconfig)
  - [bin/build](#task-bin-build)
  - [bin/install](#task-bin-install)
  - [bin/ca-keygen](#task-bin-ca-keygen)
  - [bin/signerconfig](#task-bin-signerconfig)
  - [container/ca-keygen](#task-container-ca-keygen)
  - [container/signerconfig](#task-container-signerconfig)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-ca-keygen"></a>

### ca-keygen

Dispatch Idemix CA key generation


Runs Idemix CA key generation through the container or binary path.

Set `idemixgen_use_bin` to choose the execution mode.


```yaml
- name: Dispatch Idemix CA key generation
  vars:
    # Runs idemixgen through the locally installed binary instead of a container.
    idemixgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: ca-keygen
```

<a id="task-signerconfig"></a>

### signerconfig

Dispatch Idemix signer configuration generation


Runs Idemix signer configuration generation through the container or binary path.

Set `idemixgen_use_bin` to choose the execution mode.


```yaml
- name: Dispatch Idemix signer configuration generation
  vars:
    # Runs idemixgen through the locally installed binary instead of a container.
    idemixgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: signerconfig
```

<a id="task-bin-build"></a>

### bin/build

Build the idemixgen binary


Builds the idemixgen CLI from source on the control node.

This entry point passes the configured git source and package path to the shared binary builder.


```yaml
- name: Build the idemixgen binary
  vars:
    # Sets the shared directory used by the binary execution path.
    cli_bin_dir: "string"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Pins the git ref used for the idemixgen binary install or build.
    idemixgen_git_commit: v0.0.2
    # Defines the git hosting domain for the idemixgen source repository.
    idemixgen_git_hub_url: github.com
    # Defines the owner and repository path for the idemixgen source.
    idemixgen_git_repo: IBM/idemix
    # Defines the source package path built into the idemixgen binary.
    idemixgen_source_code_package: tools/idemixgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: bin/build
```

<a id="task-bin-install"></a>

### bin/install

Install the idemixgen binary


Installs the idemixgen CLI from the configured repository and commit.

This entry point is used before binary-mode execution.


```yaml
- name: Install the idemixgen binary
  vars:
    # Sets the shared directory used by the binary execution path.
    cli_bin_dir: "string"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Defines the Go package path used to install idemixgen. The default derives from `idemixgen_git_hub_url`, `idemixgen_git_repo`, and `idemixgen_source_code_package`.
    idemixgen_bin_package: "{{ idemixgen_git_hub_url }}/{{ idemixgen_git_repo }}/{{ idemixgen_source_code_package }}"
    # Pins the git ref used for the idemixgen binary install or build.
    idemixgen_git_commit: v0.0.2
    # Defines the git hosting domain for the idemixgen source repository.
    idemixgen_git_hub_url: github.com
    # Defines the owner and repository path for the idemixgen source.
    idemixgen_git_repo: IBM/idemix
    # Defines the source package path built into the idemixgen binary.
    idemixgen_source_code_package: tools/idemixgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: bin/install
```

<a id="task-bin-ca-keygen"></a>

### bin/ca-keygen

Generate Idemix CA key material with the binary


Runs `idemixgen ca-keygen` through the locally installed binary.

The task removes any existing CA and MSP output directories before generating fresh artifacts.


```yaml
- name: Generate Idemix CA key material with the binary
  vars:
    # Sets the shared directory used by the binary execution path.
    cli_bin_dir: "string"
    # Sets the shared build root used by `idemixgen_output_dir`. Required when relying on the default of `idemixgen_output_dir`.
    config_build_dir: "string"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Sets the host directory where the generated artifacts are written. The default derives from `config_build_dir`.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: bin/ca-keygen
```

<a id="task-bin-signerconfig"></a>

### bin/signerconfig

Generate Idemix signer configuration with the binary


Runs `idemixgen signerconfig` through the locally installed binary.

The task removes any existing MSP and user output directories before generating fresh artifacts.


```yaml
- name: Generate Idemix signer configuration with the binary
  vars:
    # Sets the shared directory used by the binary execution path.
    cli_bin_dir: "string"
    # Sets the shared build root used by `idemixgen_output_dir`. Required when relying on the default of `idemixgen_output_dir`.
    config_build_dir: "string"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Sets the directory containing the CA material consumed by `signerconfig`.
    idemixgen_ca_input_dir: "string"
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Defines the enrollment identifier embedded in the signer configuration. The default derives from `inventory_hostname`.
    idemixgen_enrollment_id: "{{ inventory_hostname }}"
    # Sets the organization unit passed to `signerconfig`.
    idemixgen_org_domain: "string"
    # Sets the host directory where the generated artifacts are written. The default derives from `config_build_dir`.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Defines the revocation handle embedded in the signer configuration. The default is a random integer from 100 to 998.
    idemixgen_rev_handle: "{{ range(100, 999) | random }}"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: bin/signerconfig
```

<a id="task-container-ca-keygen"></a>

### container/ca-keygen

Generate Idemix CA key material in a container


Runs `idemixgen ca-keygen` in the configured container image.

The task removes any existing CA and MSP output directories before generating fresh artifacts.


```yaml
- name: Generate Idemix CA key material in a container
  vars:
    # Sets the shared build root used by `idemixgen_output_dir`. Required when relying on the default of `idemixgen_output_dir`.
    config_build_dir: "string"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Defines the container name used for the idemixgen run. The default derives from `inventory_hostname`.
    idemixgen_container_name: "idemixgen-{{ inventory_hostname }}"
    # Sets the output directory path used inside the container.
    idemixgen_container_output_dir: /tmp/out
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Defines the container image used to run idemixgen. The default derives from `idemixgen_registry_endpoint`, `idemixgen_image_name`, and `idemixgen_image_tag`.
    idemixgen_image: "{{ idemixgen_registry_endpoint }}/{{ idemixgen_image_name }}:{{ idemixgen_image_tag }}"
    # Defines the image name used for the idemixgen container.
    idemixgen_image_name: fabric-x-tools
    # Defines the image tag used for the idemixgen container.
    idemixgen_image_tag: 0.0.14
    # Sets the host directory where the generated artifacts are written. The default derives from `config_build_dir`.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Defines the container registry used for the idemixgen image. The default derives from `IDEMIXGEN_REGISTRY_ENDPOINT` or `docker.io/hyperledger`.
    idemixgen_registry_endpoint: "{{ lookup('env', 'IDEMIXGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: container/ca-keygen
```

<a id="task-container-signerconfig"></a>

### container/signerconfig

Generate Idemix signer configuration in a container


Runs `idemixgen signerconfig` in the configured container image.

The task removes any existing MSP and user output directories before generating fresh artifacts.


```yaml
- name: Generate Idemix signer configuration in a container
  vars:
    # Sets the shared build root used by `idemixgen_output_dir`. Required when relying on the default of `idemixgen_output_dir`.
    config_build_dir: "string"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Sets the directory containing the CA material consumed by `signerconfig`.
    idemixgen_ca_input_dir: "string"
    # Defines the container name used for the idemixgen run. The default derives from `inventory_hostname`.
    idemixgen_container_name: "idemixgen-{{ inventory_hostname }}"
    # Sets the output directory path used inside the container.
    idemixgen_container_output_dir: /tmp/out
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Defines the enrollment identifier embedded in the signer configuration. The default derives from `inventory_hostname`.
    idemixgen_enrollment_id: "{{ inventory_hostname }}"
    # Defines the container image used to run idemixgen. The default derives from `idemixgen_registry_endpoint`, `idemixgen_image_name`, and `idemixgen_image_tag`.
    idemixgen_image: "{{ idemixgen_registry_endpoint }}/{{ idemixgen_image_name }}:{{ idemixgen_image_tag }}"
    # Defines the image name used for the idemixgen container.
    idemixgen_image_name: fabric-x-tools
    # Defines the image tag used for the idemixgen container.
    idemixgen_image_tag: 0.0.14
    # Sets the organization unit passed to `signerconfig`.
    idemixgen_org_domain: "string"
    # Sets the host directory where the generated artifacts are written. The default derives from `config_build_dir`.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Defines the container registry used for the idemixgen image. The default derives from `IDEMIXGEN_REGISTRY_ENDPOINT` or `docker.io/hyperledger`.
    idemixgen_registry_endpoint: "{{ lookup('env', 'IDEMIXGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the revocation handle embedded in the signer configuration. The default is a random integer from 100 to 998.
    idemixgen_rev_handle: "{{ range(100, 999) | random }}"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: container/signerconfig
```


