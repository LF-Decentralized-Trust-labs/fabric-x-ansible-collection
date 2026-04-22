
# hyperledger.fabricx.fabric_ca

> Runs a Hyperledger Fabric CA server and client for certificate management across binary, container, and Kubernetes deployments.


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [client/enroll](#task-client-enroll)
  - [client/register](#task-client-register)
  - [client/reenroll](#task-client-reenroll)
  - [client/identity_list](#task-client-identity_list)
  - [client/revoke](#task-client-revoke)
  - [client/gencrl](#task-client-gencrl)
  - [client/effective_address](#task-client-effective_address)
  - [client/cryptogenize](#task-client-cryptogenize)
  - [client/bin/build](#task-client-bin-build)
  - [client/bin/install](#task-client-bin-install)
  - [client/bin/transfer](#task-client-bin-transfer)
  - [client/bin/rm](#task-client-bin-rm)
  - [client/bin/enroll](#task-client-bin-enroll)
  - [client/bin/register](#task-client-bin-register)
  - [client/bin/reenroll](#task-client-bin-reenroll)
  - [client/bin/identity_list](#task-client-bin-identity_list)
  - [client/bin/revoke](#task-client-bin-revoke)
  - [client/bin/gencrl](#task-client-bin-gencrl)
  - [client/container/enroll](#task-client-container-enroll)
  - [client/container/register](#task-client-container-register)
  - [client/container/reenroll](#task-client-container-reenroll)
  - [client/container/identity_list](#task-client-container-identity_list)
  - [client/container/revoke](#task-client-container-revoke)
  - [client/container/gencrl](#task-client-container-gencrl)
  - [server/start](#task-server-start)
  - [server/stop](#task-server-stop)
  - [server/teardown](#task-server-teardown)
  - [server/wipe](#task-server-wipe)
  - [server/ping](#task-server-ping)
  - [server/fetch_logs](#task-server-fetch_logs)
  - [server/bin/build](#task-server-bin-build)
  - [server/bin/install](#task-server-bin-install)
  - [server/bin/start](#task-server-bin-start)
  - [server/bin/stop](#task-server-bin-stop)
  - [server/bin/fetch_logs](#task-server-bin-fetch_logs)
  - [server/bin/rm](#task-server-bin-rm)
  - [server/bin/transfer](#task-server-bin-transfer)
  - [server/container/start](#task-server-container-start)
  - [server/container/stop](#task-server-container-stop)
  - [server/container/fetch_logs](#task-server-container-fetch_logs)
  - [server/container/rm](#task-server-container-rm)
  - [server/k8s/start](#task-server-k8s-start)
  - [k8s/server/ping](#task-k8s-server-ping)
  - [server/k8s/fetch_logs](#task-server-k8s-fetch_logs)
  - [server/k8s/rm](#task-server-k8s-rm)
  - [server/k8s/config/transfer](#task-server-k8s-config-transfer)
  - [server/k8s/config/rm](#task-server-k8s-config-rm)
  - [server/k8s/crypto/transfer](#task-server-k8s-crypto-transfer)
  - [server/k8s/crypto/rm](#task-server-k8s-crypto-rm)
  - [server/crypto/setup](#task-server-crypto-setup)
  - [server/crypto/x509/setup](#task-server-crypto-x509-setup)
  - [server/crypto/idemix/setup](#task-server-crypto-idemix-setup)
  - [server/crypto/fetch](#task-server-crypto-fetch)
  - [server/crypto/rm](#task-server-crypto-rm)
  - [server/config/transfer](#task-server-config-transfer)
  - [server/config/rm](#task-server-config-rm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-client-enroll"></a>

### client/enroll

Dispatch client enrollment


Selects the client enrollment implementation.


```yaml
- name: Dispatch client enrollment
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/enroll
```

<a id="task-client-register"></a>

### client/register

Dispatch client registration


Selects the client registration implementation.


```yaml
- name: Dispatch client registration
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/register
```

<a id="task-client-reenroll"></a>

### client/reenroll

Dispatch client reenrollment


Selects the client reenrollment implementation.


```yaml
- name: Dispatch client reenrollment
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/reenroll
```

<a id="task-client-identity_list"></a>

### client/identity_list

Dispatch client identity listing


Selects the client identity listing implementation.


```yaml
- name: Dispatch client identity listing
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/identity_list
```

<a id="task-client-revoke"></a>

### client/revoke

Dispatch client revocation


Selects the client revocation implementation.


```yaml
- name: Dispatch client revocation
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/revoke
```

<a id="task-client-gencrl"></a>

### client/gencrl

Dispatch client CRL generation


Selects the client CRL generation implementation.


```yaml
- name: Dispatch client CRL generation
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/gencrl
```

<a id="task-client-effective_address"></a>

### client/effective_address

Resolve the Fabric CA connection address


Resolves the effective Fabric CA host and port for client operations.

The referenced host must define `actual_host` and the Fabric CA server port settings; when it enables NodePort, the client uses `fabric_ca_server_k8s_port_node_port` instead of `fabric_ca_port`.


```yaml
- name: Resolve the Fabric CA connection address
  vars:
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/effective_address
```

<a id="task-client-cryptogenize"></a>

### client/cryptogenize

Normalize enrolled MSP output


Copies enrolled client material into cryptogen-compatible filenames.


```yaml
- name: Normalize enrolled MSP output
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Sets an optional enrollment profile such as `tls`.
    fabric_ca_enrollment_profile: "string"
    # Sets the normalized TLS CA certificate filename.
    fabric_ca_cryptogenize_tls_ca_cert_file: ca.crt
    # Sets the normalized TLS certificate filename.
    fabric_ca_cryptogenize_tls_cert_file: server.crt
    # Sets the normalized TLS private key filename.
    fabric_ca_cryptogenize_tls_key_file: server.key
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/cryptogenize
```

<a id="task-client-bin-build"></a>

### client/bin/build

Build the Fabric CA client binary


Builds the Fabric CA client binary from source.


```yaml
- name: Build the Fabric CA client binary
  vars:
    # Sets the Git host used for Fabric CA source lookups.
    fabric_ca_git_hub_url: github.com
    # Sets the Fabric CA source repository.
    fabric_ca_git_repo: hyperledger/fabric-ca
    # Pins the Fabric CA source revision.
    fabric_ca_git_commit: v1.5.15
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the Go package path used to build the client binary.
    fabric_ca_client_source_code_package: cmd/fabric-ca-client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/build
```

<a id="task-client-bin-install"></a>

### client/bin/install

Install the Fabric CA client binary


Installs the Fabric CA client binary.


```yaml
- name: Install the Fabric CA client binary
  vars:
    # Sets the client Go package path; the default derives from `fabric_ca_git_hub_url`, `fabric_ca_git_repo`, and `fabric_ca_client_source_code_package`.
    fabric_ca_client_bin_package: "{{ fabric_ca_git_hub_url }}/{{ fabric_ca_git_repo }}/{{ fabric_ca_client_source_code_package }}"
    # Sets the Git host used for Fabric CA source lookups.
    fabric_ca_git_hub_url: github.com
    # Sets the Fabric CA source repository.
    fabric_ca_git_repo: hyperledger/fabric-ca
    # Sets the Go package path used to build the client binary.
    fabric_ca_client_source_code_package: cmd/fabric-ca-client
    # Pins the Fabric CA source revision.
    fabric_ca_git_commit: v1.5.15
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/install
```

<a id="task-client-bin-transfer"></a>

### client/bin/transfer

Transfer the Fabric CA client binary


Copies the built Fabric CA client binary to the managed host.


```yaml
- name: Transfer the Fabric CA client binary
  vars:
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/transfer
```

<a id="task-client-bin-rm"></a>

### client/bin/rm

Remove the Fabric CA client binary


Removes the Fabric CA client binary from the managed host.


```yaml
- name: Remove the Fabric CA client binary
  vars:
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/rm
```

<a id="task-client-bin-enroll"></a>

### client/bin/enroll

Enroll an identity with the client binary


Enrolls an identity with the locally installed client binary.


```yaml
- name: Enroll an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Selects the enrollment type.
    fabric_ca_enrollment_type: bccsp
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets the Idemix enrollment profile.
    fabric_ca_idemix_enrollment_profile: idemix
    # Sets an optional enrollment profile such as `tls`.
    fabric_ca_enrollment_profile: "string"
    # Provides the resolved host address used in computed defaults such as `fabric_ca_csr_hosts` and in client effective-address resolution.
    actual_host: "string"
    # Sets the CSR SAN host list; the default derives from `actual_host`, `ansible_host`, and `inventory_hostname`.
    fabric_ca_csr_hosts: ["entry1", "entry2"]
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/enroll
```

<a id="task-client-bin-register"></a>

### client/bin/register

Register an identity with the client binary


Registers a new identity with the locally installed client binary.


```yaml
- name: Register an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/register
```

<a id="task-client-bin-reenroll"></a>

### client/bin/reenroll

Reenroll an identity with the client binary


Reenrolls an existing identity with the locally installed client binary.


```yaml
- name: Reenroll an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets an optional enrollment profile such as `tls`.
    fabric_ca_enrollment_profile: "string"
    # Provides the resolved host address used in computed defaults such as `fabric_ca_csr_hosts` and in client effective-address resolution.
    actual_host: "string"
    # Sets the CSR SAN host list; the default derives from `actual_host`, `ansible_host`, and `inventory_hostname`.
    fabric_ca_csr_hosts: ["entry1", "entry2"]
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/reenroll
```

<a id="task-client-bin-identity_list"></a>

### client/bin/identity_list

List Fabric CA identities with the client binary


Lists identities registered in the target Fabric CA server with the locally installed client binary.


```yaml
- name: List Fabric CA identities with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/identity_list
```

<a id="task-client-bin-revoke"></a>

### client/bin/revoke

Revoke an identity with the client binary


Revokes an enrolled identity with the locally installed client binary.


```yaml
- name: Revoke an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/revoke
```

<a id="task-client-bin-gencrl"></a>

### client/bin/gencrl

Generate a CRL with the client binary


Generates a certificate revocation list from the target Fabric CA server with the locally installed client binary.


```yaml
- name: Generate a CRL with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/gencrl
```

<a id="task-client-container-enroll"></a>

### client/container/enroll

Enroll an identity with the client container


Enrolls an identity with a transient container.


```yaml
- name: Enroll an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Selects the enrollment type.
    fabric_ca_enrollment_type: bccsp
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets the Idemix enrollment profile.
    fabric_ca_idemix_enrollment_profile: idemix
    # Sets an optional enrollment profile such as `tls`.
    fabric_ca_enrollment_profile: "string"
    # Provides the resolved host address used in computed defaults such as `fabric_ca_csr_hosts` and in client effective-address resolution.
    actual_host: "string"
    # Sets the CSR SAN host list; the default derives from `actual_host`, `ansible_host`, and `inventory_hostname`.
    fabric_ca_csr_hosts: ["entry1", "entry2"]
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/enroll
```

<a id="task-client-container-register"></a>

### client/container/register

Register an identity with the client container


Registers a new identity with a transient container.


```yaml
- name: Register an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/register
```

<a id="task-client-container-reenroll"></a>

### client/container/reenroll

Reenroll an identity with the client container


Reenrolls an existing identity with a transient container.


```yaml
- name: Reenroll an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets an optional enrollment profile such as `tls`.
    fabric_ca_enrollment_profile: "string"
    # Provides the resolved host address used in computed defaults such as `fabric_ca_csr_hosts` and in client effective-address resolution.
    actual_host: "string"
    # Sets the CSR SAN host list; the default derives from `actual_host`, `ansible_host`, and `inventory_hostname`.
    fabric_ca_csr_hosts: ["entry1", "entry2"]
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/reenroll
```

<a id="task-client-container-identity_list"></a>

### client/container/identity_list

List Fabric CA identities with the client container


Lists identities registered in the target Fabric CA server with a transient container.


```yaml
- name: List Fabric CA identities with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/identity_list
```

<a id="task-client-container-revoke"></a>

### client/container/revoke

Revoke an identity with the client container


Revokes an enrolled identity with a transient container.


```yaml
- name: Revoke an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault.
    fabric_ca_identity: {}
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/revoke
```

<a id="task-client-container-gencrl"></a>

### client/container/gencrl

Generate a CRL with the client container


Generates a certificate revocation list from the target Fabric CA server with a transient container.


```yaml
- name: Generate a CRL with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization.
    fabric_ca_msp_dir: "string"
    # Names the inventory host that provides the target Fabric CA server.
    fabric_ca_host: "string"
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme; the default derives from `fabric_ca_use_tls`.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled.
    fabric_ca_tls_certfile: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/gencrl
```

<a id="task-server-start"></a>

### server/start

Dispatch server startup


Selects the server runtime to start.


```yaml
- name: Dispatch server startup
  vars:
    # Uses the container server flow; the default derives from `fabric_ca_server_use_bin` and `fabric_ca_server_use_k8s`.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/start
```

<a id="task-server-stop"></a>

### server/stop

Dispatch server stop


Selects the server runtime to stop.


```yaml
- name: Dispatch server stop
  vars:
    # Uses the container server flow; the default derives from `fabric_ca_server_use_bin` and `fabric_ca_server_use_k8s`.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/stop
```

<a id="task-server-teardown"></a>

### server/teardown

Dispatch server teardown


Selects the server runtime resources to remove.


```yaml
- name: Dispatch server teardown
  vars:
    # Uses the container server flow; the default derives from `fabric_ca_server_use_bin` and `fabric_ca_server_use_k8s`.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/teardown
```

<a id="task-server-wipe"></a>

### server/wipe

Wipe all server assets


Removes the server runtime, binaries, configuration, and Kubernetes crypto.


```yaml
- name: Wipe all server assets
  vars:
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/wipe
```

<a id="task-server-ping"></a>

### server/ping

Check server ports


Checks that the Fabric CA API and operations ports are reachable.


```yaml
- name: Check server ports
  vars:
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
    # Sets the Fabric CA API port.
    fabric_ca_port: 1000
    # Sets the Fabric CA operations port.
    fabric_ca_operations_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/ping
```

<a id="task-server-fetch_logs"></a>

### server/fetch_logs

Dispatch server log collection


Selects the server runtime logs to collect.


```yaml
- name: Dispatch server log collection
  vars:
    # Uses the container server flow; the default derives from `fabric_ca_server_use_bin` and `fabric_ca_server_use_k8s`.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/fetch_logs
```

<a id="task-server-bin-build"></a>

### server/bin/build

Build the Fabric CA server binary


Builds the Fabric CA server binary from source.


```yaml
- name: Build the Fabric CA server binary
  vars:
    # Sets the Git host used for Fabric CA source lookups.
    fabric_ca_git_hub_url: github.com
    # Sets the Fabric CA source repository.
    fabric_ca_git_repo: hyperledger/fabric-ca
    # Pins the Fabric CA source revision.
    fabric_ca_git_commit: v1.5.15
    # Sets the server binary name.
    fabric_ca_server_bin_name: fabric-ca-server
    # Sets the Go package path used to build the server binary.
    fabric_ca_server_source_code_package: cmd/fabric-ca-server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/build
```

<a id="task-server-bin-install"></a>

### server/bin/install

Install the Fabric CA server binary


Installs the Fabric CA server binary.


```yaml
- name: Install the Fabric CA server binary
  vars:
    # Sets the server Go package path; the default derives from `fabric_ca_git_hub_url`, `fabric_ca_git_repo`, and `fabric_ca_server_source_code_package`.
    fabric_ca_server_bin_package: "{{ fabric_ca_git_hub_url }}/{{ fabric_ca_git_repo }}/{{ fabric_ca_server_source_code_package }}"
    # Sets the Git host used for Fabric CA source lookups.
    fabric_ca_git_hub_url: github.com
    # Sets the Fabric CA source repository.
    fabric_ca_git_repo: hyperledger/fabric-ca
    # Sets the Go package path used to build the server binary.
    fabric_ca_server_source_code_package: cmd/fabric-ca-server
    # Pins the Fabric CA source revision.
    fabric_ca_git_commit: v1.5.15
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/install
```

<a id="task-server-bin-start"></a>

### server/bin/start

Start the Fabric CA server binary


Starts the Fabric CA server as a managed local binary process.


```yaml
- name: Start the Fabric CA server binary
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Sets the Fabric CA API port.
    fabric_ca_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/start
```

<a id="task-server-bin-stop"></a>

### server/bin/stop

Stop the Fabric CA server binary


Stops the managed Fabric CA server binary process.


```yaml
- name: Stop the Fabric CA server binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/stop
```

<a id="task-server-bin-fetch_logs"></a>

### server/bin/fetch_logs

Fetch server binary logs


Collects logs for the managed Fabric CA server binary process.


```yaml
- name: Fetch server binary logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/fetch_logs
```

<a id="task-server-bin-rm"></a>

### server/bin/rm

Remove the Fabric CA server binary


Removes the Fabric CA server binary from the managed host.


```yaml
- name: Remove the Fabric CA server binary
  vars:
    # Sets the server binary name.
    fabric_ca_server_bin_name: fabric-ca-server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/rm
```

<a id="task-server-bin-transfer"></a>

### server/bin/transfer

Transfer the Fabric CA server binary


Copies the built Fabric CA server binary to the managed host.


```yaml
- name: Transfer the Fabric CA server binary
  vars:
    # Sets the server binary name.
    fabric_ca_server_bin_name: fabric-ca-server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/transfer
```

<a id="task-server-container-start"></a>

### server/container/start

Start the Fabric CA server container


Starts the Fabric CA server as a managed container.


```yaml
- name: Start the Fabric CA server container
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Sets the in-container Fabric CA config root.
    fabric_ca_server_container_config_dir: /config
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the Fabric CA API port.
    fabric_ca_port: 1000
    # Sets the Fabric CA operations port.
    fabric_ca_operations_port: 1000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/start
```

<a id="task-server-container-stop"></a>

### server/container/stop

Stop the Fabric CA server container


Stops the managed Fabric CA server container.


```yaml
- name: Stop the Fabric CA server container
  vars:
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/stop
```

<a id="task-server-container-fetch_logs"></a>

### server/container/fetch_logs

Fetch server container logs


Collects logs for the managed Fabric CA server container.


```yaml
- name: Fetch server container logs
  vars:
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/fetch_logs
```

<a id="task-server-container-rm"></a>

### server/container/rm

Remove the Fabric CA server container


Removes the managed Fabric CA server container.


```yaml
- name: Remove the Fabric CA server container
  vars:
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/rm
```

<a id="task-server-k8s-start"></a>

### server/k8s/start

Start the Fabric CA server on Kubernetes


Creates the Fabric CA resources on Kubernetes.


```yaml
- name: Start the Fabric CA server on Kubernetes
  vars:
    # Sets the Kubernetes deployment wait timeout.
    fabric_ca_server_k8s_wait_timeout: 120
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Enables the optional Kubernetes NodePort Service for the Fabric CA server; client address resolution uses the node-port mapping on the referenced server host.
    fabric_ca_server_k8s_use_node_port: false
    # Sets the Fabric CA image; the default derives from `fabric_ca_registry_endpoint`, `fabric_ca_image_name`, and `fabric_ca_image_tag`.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the in-container Fabric CA config root.
    fabric_ca_server_container_config_dir: /config
    # Sets the Fabric CA API port.
    fabric_ca_port: 1000
    # Sets the Fabric CA operations port.
    fabric_ca_operations_port: 1000
    # Sets the pod fsGroup for the Fabric CA deployment.
    fabric_ca_server_k8s_fs_group: 0
    # Sets the server CA private key filename.
    fabric_ca_server_ca_private_key_file: ca-key.pem
    # Sets the server CA certificate filename.
    fabric_ca_server_ca_cert_file: ca-cert.pem
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the server TLS private key filename.
    fabric_ca_server_tls_private_key_file: tls-key.pem
    # Sets the server TLS certificate filename.
    fabric_ca_server_tls_cert_file: tls-cert.pem
    # Names the PostgreSQL host defined elsewhere in inventory.
    postgres_db_host: "string"
    # Provides the Kubernetes namespace from the shared inventory.
    k8s_namespace: "string"
    # Provides an optional Kubernetes image pull secret from shared inventory.
    k8s_image_pull_secret: "string"
    # Sets the Kubernetes NodePort for the API port; the default derives from `fabric_ca_port` and is used when NodePort exposure is enabled.
    fabric_ca_server_k8s_port_node_port: "{{ fabric_ca_port }}"
    # Sets the Kubernetes NodePort for the operations port; the default derives from `fabric_ca_operations_port` and is used when NodePort exposure is enabled.
    fabric_ca_server_k8s_operations_node_port: "{{ fabric_ca_operations_port }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/start
```

<a id="task-k8s-server-ping"></a>

### k8s/server/ping

Check Fabric CA node ports


Checks that the Fabric CA API and operations NodePorts are reachable when Kubernetes NodePort exposure is enabled.


```yaml
- name: Check Fabric CA node ports
  vars:
    # Enables the optional Kubernetes NodePort Service for the Fabric CA server; client address resolution uses the node-port mapping on the referenced server host.
    fabric_ca_server_k8s_use_node_port: false
    # Sets the Kubernetes NodePort for the API port; the default derives from `fabric_ca_port` and is used when NodePort exposure is enabled.
    fabric_ca_server_k8s_port_node_port: "{{ fabric_ca_port }}"
    # Sets the Kubernetes NodePort for the operations port; the default derives from `fabric_ca_operations_port` and is used when NodePort exposure is enabled.
    fabric_ca_server_k8s_operations_node_port: "{{ fabric_ca_operations_port }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: k8s/server/ping
```

<a id="task-server-k8s-fetch_logs"></a>

### server/k8s/fetch_logs

Fetch server pod logs


Collects pod logs for the Fabric CA Kubernetes deployment.


```yaml
- name: Fetch server pod logs
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/fetch_logs
```

<a id="task-server-k8s-rm"></a>

### server/k8s/rm

Remove server Kubernetes runtime resources


Deletes the Fabric CA Kubernetes runtime resources.


```yaml
- name: Remove server Kubernetes runtime resources
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Provides the Kubernetes namespace from the shared inventory.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/rm
```

<a id="task-server-k8s-config-transfer"></a>

### server/k8s/config/transfer

Transfer server config to a ConfigMap


Creates or updates the Fabric CA Kubernetes ConfigMap.


```yaml
- name: Transfer server config to a ConfigMap
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Names the PostgreSQL host defined elsewhere in inventory.
    postgres_db_host: "string"
    # Provides the Kubernetes namespace from the shared inventory.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/config/transfer
```

<a id="task-server-k8s-config-rm"></a>

### server/k8s/config/rm

Remove the server ConfigMap


Deletes the Fabric CA Kubernetes ConfigMap.


```yaml
- name: Remove the server ConfigMap
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Provides the Kubernetes namespace from the shared inventory.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/config/rm
```

<a id="task-server-k8s-crypto-transfer"></a>

### server/k8s/crypto/transfer

Transfer server crypto to a Secret


Creates or updates the Fabric CA Kubernetes Secret.


```yaml
- name: Transfer server crypto to a Secret
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the server CA private key filename.
    fabric_ca_server_ca_private_key_file: ca-key.pem
    # Sets the server CA certificate filename.
    fabric_ca_server_ca_cert_file: ca-cert.pem
    # Sets the server TLS private key filename.
    fabric_ca_server_tls_private_key_file: tls-key.pem
    # Sets the server TLS certificate filename.
    fabric_ca_server_tls_cert_file: tls-cert.pem
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Provides the Kubernetes namespace from the shared inventory.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/crypto/transfer
```

<a id="task-server-k8s-crypto-rm"></a>

### server/k8s/crypto/rm

Remove the server Secret


Deletes the Fabric CA Kubernetes Secret.


```yaml
- name: Remove the server Secret
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Provides the Kubernetes namespace from the shared inventory.
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/crypto/rm
```

<a id="task-server-crypto-setup"></a>

### server/crypto/setup

Generate server crypto material


Generates x509 and Idemix crypto material for the Fabric CA server.


```yaml
- name: Generate server crypto material
  vars:
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/setup
```

<a id="task-server-crypto-x509-setup"></a>

### server/crypto/x509/setup

Generate server x509 crypto


Generates the Fabric CA root CA and TLS keypairs.


```yaml
- name: Generate server x509 crypto
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Provides the resolved host address used in computed defaults such as `fabric_ca_csr_hosts` and in client effective-address resolution.
    actual_host: "string"
    # Sets the server CA private key filename.
    fabric_ca_server_ca_private_key_file: ca-key.pem
    # Sets the server CA certificate filename.
    fabric_ca_server_ca_cert_file: ca-cert.pem
    # Sets the server TLS private key filename.
    fabric_ca_server_tls_private_key_file: tls-key.pem
    # Sets the server TLS certificate filename.
    fabric_ca_server_tls_cert_file: tls-cert.pem
    # Sets the curve used for Fabric CA server key generation.
    fabric_ca_server_openssl_curve: P-256
    # Sets the CSR common name; the default derives from `fabric_ca_name`.
    fabric_ca_csr_cn: "{{ fabric_ca_name }}"
    # Sets the CSR SAN host list; the default derives from `actual_host`, `ansible_host`, and `inventory_hostname`.
    fabric_ca_csr_hosts: ["entry1", "entry2"]
    # Provides the organization metadata defined elsewhere in inventory; `domain` is required.
    organization: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/x509/setup
```

<a id="task-server-crypto-idemix-setup"></a>

### server/crypto/idemix/setup

Generate server Idemix crypto


Generates the Fabric CA Idemix issuer keys.


```yaml
- name: Generate server Idemix crypto
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Sets the transient Idemix output directory; the default derives from `fabric_ca_server_remote_config_dir`.
    fabric_ca_server_idemixgen_output_dir: "{{ fabric_ca_server_remote_config_dir }}/idemixgen-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/idemix/setup
```

<a id="task-server-crypto-fetch"></a>

### server/crypto/fetch

Fetch server certificates


Fetches the Fabric CA server certificate material.


```yaml
- name: Fetch server certificates
  vars:
    # Provides the organization metadata defined elsewhere in inventory; `domain` is required.
    organization: {}
    # Provides the shared local artifacts root used by this role.
    fetched_artifacts_dir: "string"
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Sets the server CA certificate filename.
    fabric_ca_server_ca_cert_file: ca-cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/fetch
```

<a id="task-server-crypto-rm"></a>

### server/crypto/rm

Remove server Secret


Deletes the Kubernetes Secret that stores the Fabric CA server crypto material.


```yaml
- name: Remove server Secret
  vars:
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/rm
```

<a id="task-server-config-transfer"></a>

### server/config/transfer

Render and transfer server config


Renders the Fabric CA server configuration and copies the PostgreSQL TLS CA certificate when needed.


```yaml
- name: Render and transfer server config
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Sets the Fabric CA API port.
    fabric_ca_port: 1000
    # Sets the server log level.
    fabric_ca_log_level: INFO
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the server config directory; the default derives from `fabric_ca_server_remote_config_dir`, `fabric_ca_server_use_bin`, and `fabric_ca_server_container_config_dir`.
    fabric_ca_server_config_dir: "{{ fabric_ca_server_remote_config_dir if fabric_ca_server_use_bin else fabric_ca_server_container_config_dir }}"
    # Sets the in-container Fabric CA config root.
    fabric_ca_server_container_config_dir: /config
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
    # Sets the server TLS certificate filename.
    fabric_ca_server_tls_cert_file: tls-cert.pem
    # Sets the server TLS private key filename.
    fabric_ca_server_tls_private_key_file: tls-key.pem
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets the server CA private key filename.
    fabric_ca_server_ca_private_key_file: ca-key.pem
    # Sets the server CA certificate filename.
    fabric_ca_server_ca_cert_file: ca-cert.pem
    # Supplies the bootstrap administrator rendered into the server registry section; `name` and `secret` are required. Store the secret in Ansible Vault.
    fabric_ca_admin: {}
    # Sets the CSR common name; the default derives from `fabric_ca_name`.
    fabric_ca_csr_cn: "{{ fabric_ca_name }}"
    # Sets the CSR SAN host list; the default derives from `actual_host`, `ansible_host`, and `inventory_hostname`.
    fabric_ca_csr_hosts: ["entry1", "entry2"]
    # Provides the resolved host address used in computed defaults such as `fabric_ca_csr_hosts` and in client effective-address resolution.
    actual_host: "string"
    # Sets the CSR expiry.
    fabric_ca_csr_expiry: 131400h
    # Provides the organization metadata defined elsewhere in inventory; `domain` is required.
    organization: {}
    # Names the PostgreSQL host defined elsewhere in inventory.
    postgres_db_host: "string"
    # Provides the shared local artifacts root used by this role.
    fetched_artifacts_dir: "string"
    # Sets the Fabric CA operations port.
    fabric_ca_operations_port: 1000
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/transfer
```

<a id="task-server-config-rm"></a>

### server/config/rm

Remove server config resources


Deletes the Fabric CA server configuration resources.


```yaml
- name: Remove server config resources
  vars:
    # Sets the remote Fabric CA config root; the default derives from `remote_config_dir`.
    fabric_ca_server_remote_config_dir: "string"
    # Provides the shared remote configuration root used by this role.
    remote_config_dir: "string"
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/rm
```


