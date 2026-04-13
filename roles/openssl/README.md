# hyperledger.fabricx.openssl

> Runs the `openssl` CLI utility for certificate and key generation.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [Lifecycle](#lifecycle)

## Tasks

### Lifecycle

| Task                                                                | Description                       |
| ------------------------------------------------------------------- | --------------------------------- |
| [install](./tasks/install.yaml)                                     | Installs openssl                  |
| [generate_keypair](./tasks/generate_keypair.yaml)                   | Generates asymmetric key pair     |
| [generate_self_signed_cert](./tasks/generate_self_signed_cert.yaml) | Generates self-signed certificate |
| [generate_csr](./tasks/generate_csr.yaml)                           | Generates CSR                     |
| [generate_cert](./tasks/generate_cert.yaml)                         | Generates certificate from CSR    |

#### install

Installs the `openssl` binary on a machine (Linux and macOS supported):

```yaml
- name: Install openssl
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: install
```

#### generate_keypair

Generates an asymmetric key pair (private key and corresponding public key) without producing a certificate:

```yaml
- name: Generate an asymmetric key pair using openssl
  vars:
    openssl_private_key_path: /tmp/privKey.pem
    openssl_public_key_path: /tmp/pubKey.pem
    openssl_key_alg: EC
    openssl_key_opt: ec_paramgen_curve:P-256
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_keypair
```

#### generate_self_signed_cert

Generates a private key and produces a self-signed certificate:

```yaml
- name: Generate an ECDSA key with certificate using openssl
  vars:
    openssl_private_key_path: /tmp/privKey.pem
    openssl_cert_path: /tmp/pubKey.cert
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_self_signed_cert
```

#### generate_csr

Generates a Certificate Signing Request (CSR):

```yaml
- name: Generate a CSR using openssl
  vars:
    openssl_private_key_path: /tmp/privKey.pem
    openssl_csr_path: /tmp/csr.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_csr
```

#### generate_cert

Generates a certificate from a CSR using a CA:

```yaml
- name: Generate a certificate from CSR using openssl
  vars:
    openssl_csr_path: /tmp/csr.pem
    openssl_cert_path: /tmp/cert.pem
    openssl_ca_cert_path: /tmp/ca.crt
    openssl_ca_private_key_path: /tmp/ca.key
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_cert
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
