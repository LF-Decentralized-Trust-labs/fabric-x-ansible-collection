# hyperledger.fabricx.idemixgen

> Runs the `idemixgen` CLI tool for Idemix CA key generation and signer configuration.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Lifecycle](#lifecycle)
    - [ca-keygen](#ca-keygen)
    - [signerconfig](#signerconfig)
- [Variables](#variables)

## Prerequisites

When running in binary mode (`idemixgen_use_bin: true`), the role requires:

- `go` to be installed.

## Tasks

### Lifecycle

| Task                                      | Description                           |
| ----------------------------------------- | ------------------------------------- |
| [ca-keygen](./tasks/ca-keygen.yaml)       | Generates Idemix CA key material      |
| [signerconfig](./tasks/signerconfig.yaml) | Generates Idemix signer configuration |

#### ca-keygen

Generates the Idemix CA key material (issuer public key and secret key) and writes them to `idemixgen_output_dir`. Depending on `idemixgen_use_bin`, it runs either via container or native binary.

```yaml
- name: Generate Idemix CA key material
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: ca-keygen
```

#### signerconfig

Generates the Idemix signer configuration (credential and revocation handle) for an enrollment identity and writes it to `idemixgen_output_dir`. Depending on `idemixgen_use_bin`, it runs either via container or native binary.

```yaml
- name: Generate Idemix signer configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.idemixgen
    tasks_from: signerconfig
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
