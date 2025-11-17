# hyperledger.fabricx.openssl

The role `hyperledger.fabricx.openssl` can be used to run the `openssl` CLI utility.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [install](#install)
  - [generate_key](#generate_self_signed_cert)

## Tasks

### install

The `install` task allows to install the `openssl` binary utility on a machine (Linux and macOS supported).

```yaml
- name: Install openssl
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: install
```

### generate_self_signed_cert

The `generate_self_signed_cert` task allows to generate a private key and its corresponding certificate.

```yaml
- name: Generate an ECDSA key with certificate using openssl
  vars:
    openssl_private_key_path: /tmp/privKey.pem
    openssl_cert_path: /tmp/pubKey.cert
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_self_signed_cert
```
