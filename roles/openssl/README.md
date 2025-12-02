# hyperledger.fabricx.openssl

The role `hyperledger.fabricx.openssl` can be used to run the `openssl` CLI utility.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [install](#install)
  - [generate_self_signed_cert](#generate_self_signed_cert)
  - [generate_csr](#generate_csr)
  - [generate_cert](#generate_cert)

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

The `generate_self_signed_cert` task allows to generate a private key and produce a self-signed certificate:

```yaml
- name: Generate an ECDSA key with certificate using openssl
  vars:
    openssl_private_key_path: /tmp/privKey.pem
    openssl_cert_path: /tmp/pubKey.cert
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_self_signed_cert
```

### generate_csr

The `generate_csr` task allows to generate a CSR (Certificate Signing Request) that can be used to request for a certificate:

```yaml
- name: Generate a Certificate Signing Request (CSR) using openssl
  vars:
    openssl_private_key_path: /tmp/privKey.pem
    openssl_csr_path: /tmp/tls.csr
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_csr
```

### generate_cert

The `generate_cert` task allows to generate a certificate from a CSR (Certificate Signing Request):

```yaml
- name: Generate a Certificate Signing Request (CSR) using openssl
  vars:
    openssl_ca_private_key_path: /tmp/ca/tls_key.pem
    openssl_ca_cert_path: /tmp/ca/tls_cert.pem
    openssl_cert_path: /tmp/tls_cert.pem
    openssl_csr_path: /tmp/tls.csr
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_cert
```
