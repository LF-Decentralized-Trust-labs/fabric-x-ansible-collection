# hyperledger.fabricx.idemixgen

> Generates Idemix CA key material and signer configuration artifacts with the `idemixgen` CLI in binary or container mode.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [ca-keygen](#ca-keygen)
  - [signerconfig](#signerconfig)
  - [bin/build](#binbuild)
  - [bin/install](#bininstall)
  - [bin/ca-keygen](#binca-keygen)
  - [bin/signerconfig](#binsignerconfig)
  - [container/ca-keygen](#containerca-keygen)
  - [container/signerconfig](#containersignerconfig)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.idemixgen
```

## Tasks

### ca-keygen

> Dispatch Idemix CA key generation in binary or container mode

Select whether Idemix CA key generation runs in a container or through the locally installed binary. The generated CA key material is written under `idemixgen_output_dir`/ca and the CA MSP material under `idemixgen_output_dir`/msp. Set `idemixgen_use_bin` to choose the execution mode.

```yaml
- name: Dispatch Idemix CA key generation in binary or container mode
  vars:
    # Runs idemixgen through the locally installed binary instead of a container.
    idemixgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: ca-keygen
```

### signerconfig

> Dispatch Idemix signer configuration generation in binary or container mode

Select whether Idemix signer configuration generation runs in a container or through the locally installed binary. The signer configuration consumes `idemixgen_ca_input_dir` and writes MSP and user artifacts under `idemixgen_output_dir`. Set `idemixgen_use_bin` to choose the execution mode.

```yaml
- name: Dispatch Idemix signer configuration generation in binary or container mode
  vars:
    # Runs idemixgen through the locally installed binary instead of a container.
    idemixgen_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: signerconfig
```

### bin/build

> Build the idemixgen binary

Builds the idemixgen CLI from source on the control node so binary-mode CA key generation and signer configuration can run locally. This entry point passes the configured git source and package path to the shared binary builder.

```yaml
- name: Build the idemixgen binary
  vars:
    # Sets the shared directory used by the binary execution path. Example: `/opt/hyperledger/fabricx/bin`.
    cli_bin_dir: "/opt/hyperledger/fabricx/bin"
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

### bin/install

> Install the idemixgen binary

Installs the idemixgen CLI from the configured repository and commit before binary-mode CA key generation or signer configuration. This entry point is used before binary-mode execution.

```yaml
- name: Install the idemixgen binary
  vars:
    # Sets the shared directory used by the binary execution path. Example: `/opt/hyperledger/fabricx/bin`.
    cli_bin_dir: "/opt/hyperledger/fabricx/bin"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Defines the Go package path used to install idemixgen.
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

### bin/ca-keygen

> Generate Idemix CA key material with the binary

Runs `idemixgen ca-keygen` through the locally installed binary. The task removes any existing CA and MSP output directories before generating fresh artifacts under `idemixgen_output_dir`.

```yaml
- name: Generate Idemix CA key material with the binary
  vars:
    # Sets the shared directory used by the binary execution path. Example: `/opt/hyperledger/fabricx/bin`.
    cli_bin_dir: "/opt/hyperledger/fabricx/bin"
    # Sets the shared build root used by `idemixgen_output_dir`. Required when using `idemixgen_output_dir`. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Sets the host directory where the generated artifacts are written.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: bin/ca-keygen
```

### bin/signerconfig

> Generate Idemix signer configuration with the binary

Runs `idemixgen signerconfig` through the locally installed binary. The task removes any existing MSP and user output directories before generating fresh artifacts under `idemixgen_output_dir`.

```yaml
- name: Generate Idemix signer configuration with the binary
  vars:
    # Sets the shared directory used by the binary execution path. Example: `/opt/hyperledger/fabricx/bin`.
    cli_bin_dir: "/opt/hyperledger/fabricx/bin"
    # Sets the shared build root used by `idemixgen_output_dir`. Required when using `idemixgen_output_dir`. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Sets the directory containing the CA material consumed by `signerconfig`. Example: `/opt/hyperledger/fabricx/build/idemixgen-artifacts/ca`.
    idemixgen_ca_input_dir: "/opt/hyperledger/fabricx/build/idemixgen-artifacts/ca"
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Defines the enrollment identifier embedded in the signer configuration.
    idemixgen_enrollment_id: "{{ inventory_hostname }}"
    # Sets the organization unit passed to `signerconfig`. Example: `org1.example.com`.
    idemixgen_org_domain: "org1.example.com"
    # Sets the host directory where the generated artifacts are written.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Defines the revocation handle embedded in the signer configuration. The default is a random integer from 100 to 998.
    idemixgen_rev_handle: "{{ range(100, 999) | random }}"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: bin/signerconfig
```

### container/ca-keygen

> Generate Idemix CA key material in a container

Runs `idemixgen ca-keygen` in the configured container image. The task removes any existing CA and MSP output directories before generating fresh artifacts under `idemixgen_output_dir`.

```yaml
- name: Generate Idemix CA key material in a container
  vars:
    # Sets the shared build root used by `idemixgen_output_dir`. Required when using `idemixgen_output_dir`. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Defines the container name used for the idemixgen run.
    idemixgen_container_name: "idemixgen-{{ inventory_hostname }}"
    # Sets the output directory path used inside the container.
    idemixgen_container_output_dir: /tmp/out
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Defines the container image used to run idemixgen.
    idemixgen_image: "{{ idemixgen_registry_endpoint }}/{{ idemixgen_image_name }}:{{ idemixgen_image_tag }}"
    # Defines the image name used for the idemixgen container.
    idemixgen_image_name: fabric-x-tools
    # Defines the image tag used for the idemixgen container.
    idemixgen_image_tag: 0.0.14
    # Sets the host directory where the generated artifacts are written.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Defines the container registry used for the idemixgen image.
    idemixgen_registry_endpoint: "{{ lookup('env', 'IDEMIXGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: container/ca-keygen
```

### container/signerconfig

> Generate Idemix signer configuration in a container

Runs `idemixgen signerconfig` in the configured container image. The task removes any existing MSP and user output directories before generating fresh artifacts under `idemixgen_output_dir`.

```yaml
- name: Generate Idemix signer configuration in a container
  vars:
    # Sets the shared build root used by `idemixgen_output_dir`. Required when using `idemixgen_output_dir`. Example: `/opt/hyperledger/fabricx/build`.
    config_build_dir: "/opt/hyperledger/fabricx/build"
    # Defines the idemixgen binary name.
    idemixgen_bin_name: idemixgen
    # Sets the directory containing the CA material consumed by `signerconfig`. Example: `/opt/hyperledger/fabricx/build/idemixgen-artifacts/ca`.
    idemixgen_ca_input_dir: "/opt/hyperledger/fabricx/build/idemixgen-artifacts/ca"
    # Defines the container name used for the idemixgen run.
    idemixgen_container_name: "idemixgen-{{ inventory_hostname }}"
    # Sets the output directory path used inside the container.
    idemixgen_container_output_dir: /tmp/out
    # Selects the cryptographic curve passed to idemixgen.
    idemixgen_curve_id: BLS12_381_BBS
    # Defines the enrollment identifier embedded in the signer configuration.
    idemixgen_enrollment_id: "{{ inventory_hostname }}"
    # Defines the container image used to run idemixgen.
    idemixgen_image: "{{ idemixgen_registry_endpoint }}/{{ idemixgen_image_name }}:{{ idemixgen_image_tag }}"
    # Defines the image name used for the idemixgen container.
    idemixgen_image_name: fabric-x-tools
    # Defines the image tag used for the idemixgen container.
    idemixgen_image_tag: 0.0.14
    # Sets the organization unit passed to `signerconfig`. Example: `org1.example.com`.
    idemixgen_org_domain: "org1.example.com"
    # Sets the host directory where the generated artifacts are written.
    idemixgen_output_dir: "{{ config_build_dir }}/idemixgen-artifacts"
    # Defines the container registry used for the idemixgen image.
    idemixgen_registry_endpoint: "{{ lookup('env', 'IDEMIXGEN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the revocation handle embedded in the signer configuration. The default is a random integer from 100 to 998.
    idemixgen_rev_handle: "{{ range(100, 999) | random }}"
    # Enables Aries-based Idemix material generation.
    idemixgen_use_aries: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: container/signerconfig
```
