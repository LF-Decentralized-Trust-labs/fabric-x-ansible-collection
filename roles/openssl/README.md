# hyperledger.fabricx.openssl

> Generates keys, CSRs, self-signed certificates, and CA-signed certificates with the `openssl` CLI.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [install](#install)
  - [generate_keypair](#generate_keypair)
  - [generate_self_signed_cert](#generate_self_signed_cert)
  - [generate_csr](#generate_csr)
  - [generate_cert](#generate_cert)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.openssl
```

## Tasks

### install

> Install the OpenSSL CLI

Install the `openssl` package on the target host by delegating to the package role.

```yaml
- name: Install the OpenSSL CLI
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: install
```

### generate_keypair

> Generate an asymmetric key pair

Generate a private key and the matching public key on the target host.The private key is written to `openssl_private_key_path` and the public key to `openssl_public_key_path`.The task is idempotent and skips regeneration when both output files already exist.

```yaml
- name: Generate an asymmetric key pair
  vars:
    # Path to the private key file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.key`.
    openssl_private_key_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.key"
    # Path to the public key file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.pub`.
    openssl_public_key_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.pub"
    # OpenSSL algorithm passed to `openssl genpkey`.
    openssl_key_alg: RSA
    # Optional key-generation option passed with `-pkeyopt`. Example: `rsa_keygen_bits:4096`.
    openssl_key_opt: "rsa_keygen_bits:4096"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_keypair
```

### generate_self_signed_cert

> Generate a self-signed certificate

Generate a private key and a self-signed X.509 certificate.The certificate is written to `openssl_cert_path` and remains valid for `openssl_cert_duration` days.The role renders a temporary OpenSSL config file beneath `openssl_remote_config_dir`, then copies the generated certificate to `openssl_ca_cert_file` in the certificate directory so the self-signed output can also act as a CA certificate.When `openssl_clean_after_gen` is true, the temporary configuration directory is removed after generation.

```yaml
- name: Generate a self-signed certificate
  vars:
    # Base directory for remote role state and temporary OpenSSL config files. Example: `/tmp/fabricx/openssl`.
    remote_node_dir: "/tmp/fabricx/openssl"
    # Inventory host address used in SAN defaults. Example: `peer0.org1.example.com`.
    actual_host: "peer0.org1.example.com"
    # Inventory host address used in SAN defaults. Example: `192.0.2.15`.
    ansible_host: "192.0.2.15"
    # Path to the private key file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.key`.
    openssl_private_key_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.key"
    # Path to the certificate file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.crt`.
    openssl_cert_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.crt"
    # Directory for the temporary OpenSSL config file. For example, `/tmp/fabricx/openssl`.
    openssl_remote_config_dir: "{{ remote_node_dir }}/openssl"
    # Remove the rendered OpenSSL config directory after generation.
    openssl_clean_after_gen: false
    # Filename used when copying the self-signed certificate as the CA certificate.
    openssl_ca_cert_file: ca.crt
    # Key type passed to `openssl req -newkey`.
    openssl_key_type: "rsa:4096"
    # Optional key-generation option passed with `-pkeyopt`. Example: `rsa_keygen_bits:4096`.
    openssl_key_opt: "rsa_keygen_bits:4096"
    # Number of days the generated certificate remains valid.
    openssl_cert_duration: 365
    # Message digest written into the generated OpenSSL request config.
    openssl_default_md: sha256
    # Country code written into the certificate subject.
    openssl_country: US
    # State or province written into the certificate subject.
    openssl_state: California
    # Optional locality or city written into the certificate subject. Example: `Zurich`.
    openssl_locality: "Zurich"
    # Organization name written into the certificate subject.
    openssl_organization: MyOrg Inc.
    # Optional organizational unit written into the certificate subject. Example: `Platform Engineering`.
    openssl_organizational_unit: "Platform Engineering"
    # Common Name written into the certificate subject.
    openssl_common_name: example.com
    # Basic constraints value written into the X.509 v3 extensions.
    openssl_basic_constraints: "CA:false"
    # Key usage written into the X.509 v3 extensions.
    openssl_key_usage: keyEncipherment, digitalSignature
    # Extended key usage written into the X.509 v3 extensions.
    openssl_extended_key_usage: serverAuth, clientAuth
    # Regex used to split SAN hosts into DNS and IP entries.
    openssl_san_ipv4_regex: "^[0-9]{1,3}(\\.[0-9]{1,3}){3}$"
    # Hosts used for SAN entries.
    openssl_san_hosts: >-
      {{
        [ansible_host, actual_host]
        | unique
        | list
      }}
    # DNS SAN entries generated from `openssl_san_hosts`.
    openssl_san_dns_entries: >-
      {{
        openssl_san_hosts
        | reject('match', openssl_san_ipv4_regex)
        | map('regex_replace', '^', 'DNS:')
        | list
      }}
    # IP SAN entries generated from `openssl_san_hosts` and `ansible_facts.all_ipv4_addresses`.
    openssl_san_ip_entries: >-
      {{
        (
          openssl_san_hosts | select('match', openssl_san_ipv4_regex) | list
          + (ansible_facts.all_ipv4_addresses | default([]))
        )
        | unique
        | map('regex_replace', '^', 'IP:')
        | list
      }}
    # Final SAN list assembled from DNS and IP SAN entries.
    openssl_san_entries: "{{ openssl_san_dns_entries + openssl_san_ip_entries }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_self_signed_cert
```

### generate_csr

> Generate a certificate signing request

Generate a private key and certificate signing request using a rendered OpenSSL config file.The private key is written to `openssl_private_key_path` and the CSR to `openssl_csr_path`.The role renders a temporary OpenSSL config file beneath `openssl_remote_config_dir` and, when `openssl_ext_file_path` is set, also renders an extension file for later signing.When `openssl_clean_after_gen` is true, the temporary configuration directory is removed after generation.

```yaml
- name: Generate a certificate signing request
  vars:
    # Base directory for remote role state and temporary OpenSSL config files. Example: `/tmp/fabricx/openssl`.
    remote_node_dir: "/tmp/fabricx/openssl"
    # Inventory host address used in SAN defaults. Example: `peer0.org1.example.com`.
    actual_host: "peer0.org1.example.com"
    # Inventory host address used in SAN defaults. Example: `192.0.2.15`.
    ansible_host: "192.0.2.15"
    # Path to the private key file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.key`.
    openssl_private_key_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.key"
    # Path to the CSR file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.csr`.
    openssl_csr_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.csr"
    # Directory for the temporary OpenSSL config file. For example, `/tmp/fabricx/openssl`.
    openssl_remote_config_dir: "{{ remote_node_dir }}/openssl"
    # Optional extension file path passed to `openssl x509 -extfile`. Example: `/var/hyperledger/fabricx/openssl/server.ext`.
    openssl_ext_file_path: "/var/hyperledger/fabricx/openssl/server.ext"
    # Remove the rendered OpenSSL config directory after generation.
    openssl_clean_after_gen: false
    # Key type passed to `openssl req -newkey`.
    openssl_key_type: "rsa:4096"
    # Optional key-generation option passed with `-pkeyopt`. Example: `rsa_keygen_bits:4096`.
    openssl_key_opt: "rsa_keygen_bits:4096"
    # Number of days the generated certificate remains valid.
    openssl_cert_duration: 365
    # Message digest written into the generated OpenSSL request config.
    openssl_default_md: sha256
    # Country code written into the certificate subject.
    openssl_country: US
    # State or province written into the certificate subject.
    openssl_state: California
    # Optional locality or city written into the certificate subject. Example: `Zurich`.
    openssl_locality: "Zurich"
    # Organization name written into the certificate subject.
    openssl_organization: MyOrg Inc.
    # Optional organizational unit written into the certificate subject. Example: `Platform Engineering`.
    openssl_organizational_unit: "Platform Engineering"
    # Common Name written into the certificate subject.
    openssl_common_name: example.com
    # Basic constraints value written into the X.509 v3 extensions.
    openssl_basic_constraints: "CA:false"
    # Key usage written into the X.509 v3 extensions.
    openssl_key_usage: keyEncipherment, digitalSignature
    # Extended key usage written into the X.509 v3 extensions.
    openssl_extended_key_usage: serverAuth, clientAuth
    # Regex used to split SAN hosts into DNS and IP entries.
    openssl_san_ipv4_regex: "^[0-9]{1,3}(\\.[0-9]{1,3}){3}$"
    # Hosts used for SAN entries.
    openssl_san_hosts: >-
      {{
        [ansible_host, actual_host]
        | unique
        | list
      }}
    # DNS SAN entries generated from `openssl_san_hosts`.
    openssl_san_dns_entries: >-
      {{
        openssl_san_hosts
        | reject('match', openssl_san_ipv4_regex)
        | map('regex_replace', '^', 'DNS:')
        | list
      }}
    # IP SAN entries generated from `openssl_san_hosts` and `ansible_facts.all_ipv4_addresses`.
    openssl_san_ip_entries: >-
      {{
        (
          openssl_san_hosts | select('match', openssl_san_ipv4_regex) | list
          + (ansible_facts.all_ipv4_addresses | default([]))
        )
        | unique
        | map('regex_replace', '^', 'IP:')
        | list
      }}
    # Final SAN list assembled from DNS and IP SAN entries.
    openssl_san_entries: "{{ openssl_san_dns_entries + openssl_san_ip_entries }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_csr
```

### generate_cert

> Sign a certificate from a CSR

Generate a certificate from an existing CSR using the provided CA certificate and private key.The signed certificate is written to `openssl_cert_path` and remains valid for `openssl_cert_duration` days.When `openssl_ext_file_path` is set, the role applies the rendered extension file while signing so the resulting certificate inherits the requested X.509 v3 extensions.

```yaml
- name: Sign a certificate from a CSR
  vars:
    # Path to the CA private key used to sign the certificate. Store this value in Ansible Vault. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/ca/ca.key`.
    openssl_ca_private_key_path: "/var/hyperledger/fabricx/crypto/org1.example.com/ca/ca.key"
    # Path to the CA certificate used to sign the certificate. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/ca/ca.crt`.
    openssl_ca_cert_path: "/var/hyperledger/fabricx/crypto/org1.example.com/ca/ca.crt"
    # Path to the CSR file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.csr`.
    openssl_csr_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.csr"
    # Path to the certificate file to create. Example: `/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.crt`.
    openssl_cert_path: "/var/hyperledger/fabricx/crypto/org1.example.com/tls/server.crt"
    # Number of days the generated certificate remains valid.
    openssl_cert_duration: 365
    # Optional extension file path passed to `openssl x509 -extfile`. Example: `/var/hyperledger/fabricx/openssl/server.ext`.
    openssl_ext_file_path: "/var/hyperledger/fabricx/openssl/server.ext"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_cert
```
