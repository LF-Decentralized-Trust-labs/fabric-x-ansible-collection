# hyperledger.fabricx.idemixgen

The role `hyperledger.fabricx.idemixgen` can be used to run the `idemixgen` CLI tool. The role allows to run it both as a binary and as a container.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [ca-keygen](#ca-keygen)
  - [signerconfig](#signerconfig)

## Prerequisites

When running in binary mode (`idemixgen_use_bin: true`), the role requires:

- `go` to be installed.

## Variables

| Variable                         | Default                                                   | Description                                                   |
| -------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------- |
| `idemixgen_registry_endpoint`    | `$IDEMIXGEN_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                   |
| `idemixgen_image_name`           | `fabric-x-tools`                                          | Container image name                                          |
| `idemixgen_image_tag`            | `0.0.13`                                                  | Container image tag                                           |
| `idemixgen_image`                | `{{ registry }}/{{ name }}:{{ tag }}`                     | Full container image reference                                |
| `idemixgen_container_name`       | `idemixgen`                                               | Name given to the ephemeral container                         |
| `idemixgen_git_uri`              | `https://github.com/IBM/idemix.git`                       | Git repository used to build the binary                       |
| `idemixgen_git_commit`           | `v0.0.2`                                                  | Git ref (tag or commit) to check out                          |
| `idemixgen_source_code_package`  | `tools/idemixgen`                                         | Go source package path within the repository                  |
| `idemixgen_bin_package`          | `github.com/IBM/idemix/tools/idemixgen`                   | Fully-qualified Go package used for `go install`              |
| `idemixgen_bin_name`             | `idemixgen`                                               | Name of the produced binary                                   |
| `idemixgen_use_bin`              | `false`                                                   | Set to `true` to use the native binary instead of a container |
| `idemixgen_output_dir`           | `{{ config_build_dir }}/idemixgen-artifacts`              | Directory on the controller where artifacts are written       |
| `idemixgen_container_output_dir` | `/tmp/out`                                                | Output directory inside the container                         |
| `idemixgen_use_aries`            | `false`                                                   | Enable Aries-compatible output                                |
| `idemixgen_curve_id`             | `BLS12_381_BBS`                                           | Elliptic curve to use for key generation                      |
| `idemixgen_enrollment_id`        | `{{ inventory_hostname }}`                                | Enrollment ID written into the signer config                  |
| `idemixgen_rev_handle`           | random integer in `[100, 999)`                            | Revocation handle written into the signer config              |

## Tasks

### ca-keygen

The task `ca-keygen` generates the Idemix CA key material (issuer public key and secret key) and writes them to `idemixgen_output_dir`. Depending on `idemixgen_use_bin`, it runs either via container or native binary.

```yaml
- name: Generate Idemix CA key material
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: ca-keygen
```

### signerconfig

The task `signerconfig` generates the Idemix signer configuration (credential and revocation handle) for an enrollment identity and writes it to `idemixgen_output_dir`. Depending on `idemixgen_use_bin`, it runs either via container or native binary.

```yaml
- name: Generate Idemix signer configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: signerconfig
```
