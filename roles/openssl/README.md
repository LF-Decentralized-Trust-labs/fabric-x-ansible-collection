# hyperledger.fabricx.openssl

The role `hyperledger.fabricx.openssl` can be used to run the `openssl` CLI utility.

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [install](#install)
  - [generate\_keypair](#generate_keypair)
  - [generate\_self\_signed\_cert](#generate_self_signed_cert)
  - [generate\_csr](#generate_csr)
  - [generate\_cert](#generate_cert)

## Variables

| Variable                     | Default                             | Description                                                          |
| ---------------------------- | ----------------------------------- | -------------------------------------------------------------------- |
| `openssl_remote_config_dir`  | `{{ remote_node_dir }}/openssl`     | Directory on the remote node where generated files are stored        |
| `openssl_clean_after_gen`    | `false`                             | Remove intermediate files (CSR, config) after certificate generation |
| `openssl_ca_cert_file`       | `ca.crt`                            | CA certificate file name                                             |
| `openssl_key_alg`            | `RSA`                               | Key algorithm (`RSA` or `EC`)                                        |
| `openssl_key_type`           | `rsa:4096`                          | Key type and size passed to `openssl genrsa` or `openssl ecparam`    |
| `openssl_cert_duration`      | `365`                               | Certificate validity in days                                         |
| `openssl_default_md`         | `sha256`                            | Message digest algorithm for the CSR                                 |
| `openssl_country`            | `US`                                | Distinguished Name country field                                     |
| `openssl_state`              | `California`                        | Distinguished Name state field                                       |
| `openssl_organization`       | `MyOrg Inc.`                        | Distinguished Name organization field                                |
| `openssl_common_name`        | `example.com`                       | Distinguished Name common name field                                 |
| `openssl_basic_constraints`  | `CA:false`                          | X.509 basic constraints extension                                    |
| `openssl_key_usage`          | `keyEncipherment, digitalSignature` | X.509 key usage extension                                            |
| `openssl_extended_key_usage` | `serverAuth, clientAuth`            | X.509 extended key usage extension                                   |
| `openssl_san_dns_entries`    | `[DNS:{{ ansible_host }}]`          | SAN DNS entries                                                      |
| `openssl_san_ip_entries`     | all host IPv4 addresses             | SAN IP entries                                                       |
| `openssl_san_entries`        | `san_dns_entries + san_ip_entries`  | Combined SAN entries                                                 |

## Tasks

### install

The `install` task allows to install the `openssl` binary utility on a machine (Linux and macOS supported).

```yaml
- name: Install openssl
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: install
```

### generate_keypair

The `generate_keypair` task allows to generate an asymmetric key pair (private key and corresponding public key) without producing a certificate:

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
