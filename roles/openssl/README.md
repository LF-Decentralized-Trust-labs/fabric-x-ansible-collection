# hyperledger.fabricx.openssl

> Runs the `openssl` CLI utility for certificate and key generation.

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

Install the OpenSSL CLI

Install the `openssl` package on the target host by delegating to the package role.

```yaml
- name: Install the OpenSSL CLI
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: install
```

### generate_keypair

Generate an asymmetric key pair

Generate a private key and the matching public key on the target host.

```yaml
- name: Generate an asymmetric key pair
  vars:
    # Path to the private key file to create.
    openssl_private_key_path: "string"
    # Path to the public key file to create.
    openssl_public_key_path: "string"
    # OpenSSL algorithm passed to `openssl genpkey`.
    openssl_key_alg: RSA
    # Optional key-generation option passed with `-pkeyopt`.
    openssl_key_opt: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_keypair
```

### generate_self_signed_cert

Generate a self-signed certificate

Generate a private key and a self-signed X.509 certificate.

The role also renders a temporary OpenSSL config file and copies the certificate to the CA filename.

```yaml
- name: Generate a self-signed certificate
  vars:
    # Base directory for remote role state. The default for `openssl_remote_config_dir` derives from this value.
    remote_node_dir: "string"
    # Inventory host address used in SAN defaults.
    actual_host: "string"
    # Inventory host address used in SAN defaults.
    ansible_host: "string"
    # Path to the private key file to create.
    openssl_private_key_path: "string"
    # Path to the certificate file to create.
    openssl_cert_path: "string"
    # Directory for the temporary OpenSSL config file. The default derives from `remote_node_dir`.
    openssl_remote_config_dir: "{{ remote_node_dir }}/openssl"
    # Remove the rendered OpenSSL config directory after generation.
    openssl_clean_after_gen: false
    # Filename used when copying the self-signed certificate as the CA certificate.
    openssl_ca_cert_file: ca.crt
    # Key type passed to `openssl req -newkey`.
    openssl_key_type: "rsa:4096"
    # Optional key-generation option passed with `-pkeyopt`.
    openssl_key_opt: "string"
    # Number of days the generated certificate remains valid.
    openssl_cert_duration: 365
    # Message digest written into the generated OpenSSL request config.
    openssl_default_md: sha256
    # Country code written into the certificate subject.
    openssl_country: US
    # State or province written into the certificate subject.
    openssl_state: California
    # Optional locality or city written into the certificate subject.
    openssl_locality: "string"
    # Organization name written into the certificate subject.
    openssl_organization: MyOrg Inc.
    # Optional organizational unit written into the certificate subject.
    openssl_organizational_unit: "string"
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
    # Hosts used to derive SAN entries. The default derives from `ansible_host` and `actual_host`.
    openssl_san_hosts: >-
      {{
        [ansible_host, actual_host]
        | unique
        | list
      }}
    # DNS SAN entries derived from `openssl_san_hosts`. The default also uses `openssl_san_ipv4_regex`.
    openssl_san_dns_entries: >-
      {{
        openssl_san_hosts
        | reject('match', openssl_san_ipv4_regex)
        | map('regex_replace', '^', 'DNS:')
        | list
      }}
    # IP SAN entries derived from `openssl_san_hosts`. The default also uses `openssl_san_ipv4_regex` and `ansible_facts.all_ipv4_addresses`.
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
    # Final SAN list derived from `openssl_san_dns_entries` and `openssl_san_ip_entries`.
    openssl_san_entries: "{{ openssl_san_dns_entries + openssl_san_ip_entries }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_self_signed_cert
```

### generate_csr

Generate a certificate signing request

Generate a private key and a certificate signing request using a rendered OpenSSL config file.

```yaml
- name: Generate a certificate signing request
  vars:
    # Base directory for remote role state. The default for `openssl_remote_config_dir` derives from this value.
    remote_node_dir: "string"
    # Inventory host address used in SAN defaults.
    actual_host: "string"
    # Inventory host address used in SAN defaults.
    ansible_host: "string"
    # Path to the private key file to create.
    openssl_private_key_path: "string"
    # Path to the CSR file to create.
    openssl_csr_path: "string"
    # Directory for the temporary OpenSSL config file. The default derives from `remote_node_dir`.
    openssl_remote_config_dir: "{{ remote_node_dir }}/openssl"
    # Optional extension file path passed to `openssl x509 -extfile`.
    openssl_ext_file_path: "string"
    # Remove the rendered OpenSSL config directory after generation.
    openssl_clean_after_gen: false
    # Key type passed to `openssl req -newkey`.
    openssl_key_type: "rsa:4096"
    # Optional key-generation option passed with `-pkeyopt`.
    openssl_key_opt: "string"
    # Number of days the generated certificate remains valid.
    openssl_cert_duration: 365
    # Message digest written into the generated OpenSSL request config.
    openssl_default_md: sha256
    # Country code written into the certificate subject.
    openssl_country: US
    # State or province written into the certificate subject.
    openssl_state: California
    # Optional locality or city written into the certificate subject.
    openssl_locality: "string"
    # Organization name written into the certificate subject.
    openssl_organization: MyOrg Inc.
    # Optional organizational unit written into the certificate subject.
    openssl_organizational_unit: "string"
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
    # Hosts used to derive SAN entries. The default derives from `ansible_host` and `actual_host`.
    openssl_san_hosts: >-
      {{
        [ansible_host, actual_host]
        | unique
        | list
      }}
    # DNS SAN entries derived from `openssl_san_hosts`. The default also uses `openssl_san_ipv4_regex`.
    openssl_san_dns_entries: >-
      {{
        openssl_san_hosts
        | reject('match', openssl_san_ipv4_regex)
        | map('regex_replace', '^', 'DNS:')
        | list
      }}
    # IP SAN entries derived from `openssl_san_hosts`. The default also uses `openssl_san_ipv4_regex` and `ansible_facts.all_ipv4_addresses`.
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
    # Final SAN list derived from `openssl_san_dns_entries` and `openssl_san_ip_entries`.
    openssl_san_entries: "{{ openssl_san_dns_entries + openssl_san_ip_entries }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_csr
```

### generate_cert

Sign a certificate from a CSR

Generate a certificate from an existing CSR using the provided CA certificate and private key.

```yaml
- name: Sign a certificate from a CSR
  vars:
    # Path to the CA private key used to sign the certificate. Store this value in Ansible Vault.
    openssl_ca_private_key_path: "string"
    # Path to the CA certificate used to sign the certificate.
    openssl_ca_cert_path: "string"
    # Path to the CSR file to create.
    openssl_csr_path: "string"
    # Path to the certificate file to create.
    openssl_cert_path: "string"
    # Number of days the generated certificate remains valid.
    openssl_cert_duration: 365
    # Optional extension file path passed to `openssl x509 -extfile`.
    openssl_ext_file_path: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openssl
    tasks_from: generate_cert
```
