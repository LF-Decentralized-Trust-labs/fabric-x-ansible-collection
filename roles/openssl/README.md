# hyperledger.fabricx.openssl

The role `hyperledger.fabricx.openssl` can be used to run the `openssl` CLI utility.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [install](#install)
  - [generate_ecdsa_key](#generate_ecdsa_key)

## Tasks

### install

The `install` task allows to install the `openssl` binary utility on a machine (Linux and macOS supported).

```yaml
- name: Install openssl
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: install
```

### generate_ecdsa_key

The `generate_ecdsa_key` task allows to generate an ECDSA private key and its corresponding self-signed certificate.

```yaml
- name: Generate an ECDSA key with certificate using openssl
  vars:
    openssl_ecdsa_curve: prime256v1
    openssl_private_key_path: /tmp/privKey.pem
    openssl_csr_path: /tmp/cert.csr
    openssl_cert_path: /tmp/pubKey.cert
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_ecdsa_key
```
