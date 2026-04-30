# hyperledger.fabricx.fabric_ca

> Manages Hyperledger Fabric CA server and client certificate workflows, including X.509 and Idemix crypto, enrollment, registration, logs, configuration, and binary, container, or Kubernetes runtimes.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [client/enroll](#clientenroll)
  - [client/register](#clientregister)
  - [client/reenroll](#clientreenroll)
  - [client/identity\_list](#clientidentity_list)
  - [client/revoke](#clientrevoke)
  - [client/gencrl](#clientgencrl)
  - [client/effective\_address](#clienteffective_address)
  - [client/cryptogenize](#clientcryptogenize)
  - [client/bin/build](#clientbinbuild)
  - [client/bin/install](#clientbininstall)
  - [client/bin/transfer](#clientbintransfer)
  - [client/bin/rm](#clientbinrm)
  - [client/bin/enroll](#clientbinenroll)
  - [client/bin/register](#clientbinregister)
  - [client/bin/reenroll](#clientbinreenroll)
  - [client/bin/identity\_list](#clientbinidentity_list)
  - [client/bin/revoke](#clientbinrevoke)
  - [client/bin/gencrl](#clientbingencrl)
  - [client/container/enroll](#clientcontainerenroll)
  - [client/container/register](#clientcontainerregister)
  - [client/container/reenroll](#clientcontainerreenroll)
  - [client/container/identity\_list](#clientcontaineridentity_list)
  - [client/container/revoke](#clientcontainerrevoke)
  - [client/container/gencrl](#clientcontainergencrl)
  - [server/start](#serverstart)
  - [server/stop](#serverstop)
  - [server/teardown](#serverteardown)
  - [server/wipe](#serverwipe)
  - [server/ping](#serverping)
  - [server/fetch\_logs](#serverfetch_logs)
  - [server/bin/build](#serverbinbuild)
  - [server/bin/install](#serverbininstall)
  - [server/bin/start](#serverbinstart)
  - [server/bin/stop](#serverbinstop)
  - [server/bin/fetch\_logs](#serverbinfetch_logs)
  - [server/bin/rm](#serverbinrm)
  - [server/bin/transfer](#serverbintransfer)
  - [server/container/start](#servercontainerstart)
  - [server/container/stop](#servercontainerstop)
  - [server/container/fetch\_logs](#servercontainerfetch_logs)
  - [server/container/rm](#servercontainerrm)
  - [server/k8s/start](#serverk8sstart)
  - [server/k8s/ping](#serverk8sping)
  - [server/k8s/fetch\_logs](#serverk8sfetch_logs)
  - [server/k8s/rm](#serverk8srm)
  - [server/k8s/config/transfer](#serverk8sconfigtransfer)
  - [server/k8s/config/rm](#serverk8sconfigrm)
  - [server/k8s/crypto/transfer](#serverk8scryptotransfer)
  - [server/k8s/crypto/rm](#serverk8scryptorm)
  - [server/crypto/setup](#servercryptosetup)
  - [server/crypto/x509/setup](#servercryptox509setup)
  - [server/crypto/idemix/setup](#servercryptoidemixsetup)
  - [server/crypto/fetch](#servercryptofetch)
  - [server/crypto/rm](#servercryptorm)
  - [server/config/transfer](#serverconfigtransfer)
  - [server/config/rm](#serverconfigrm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.fabric_ca
```

## Tasks

### client/enroll

> Dispatch client enrollment

Dispatches client enrollment to the binary or transient-container implementation. Creates MSP or Idemix material for the requested identity under `fabric_ca_msp_dir`, using TLS profile settings when requested.

```yaml
- name: Dispatch client enrollment
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/enroll
```

### client/register

> Dispatch client registration

Dispatches identity registration to the binary or transient-container implementation. Registers a new Fabric CA identity such as a peer, orderer, admin, or client using an already enrolled registrar MSP.

```yaml
- name: Dispatch client registration
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/register
```

### client/reenroll

> Dispatch client reenrollment

Dispatches reenrollment to the binary or transient-container implementation. Refreshes the enrolled identity certificates in `fabric_ca_msp_dir`, including TLS certificates when `fabric_ca_enrollment_profile` is `tls`.

```yaml
- name: Dispatch client reenrollment
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/reenroll
```

### client/identity_list

> Dispatch client identity listing

Dispatches Fabric CA identity listing to the binary or transient-container implementation. Uses the enrolled registrar MSP to query identities registered on the target Fabric CA server.

```yaml
- name: Dispatch client identity listing
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/identity_list
```

### client/revoke

> Dispatch client revocation

Dispatches identity revocation to the binary or transient-container implementation. Revokes the configured identity on the target Fabric CA server using the registrar MSP.

```yaml
- name: Dispatch client revocation
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/revoke
```

### client/gencrl

> Dispatch client CRL generation

Dispatches certificate revocation list generation to the binary or transient-container implementation. Fetches the CRL from the target Fabric CA server using the enrolled registrar MSP.

```yaml
- name: Dispatch client CRL generation
  vars:
    # Uses the binary client flow instead of the container flow.
    fabric_ca_client_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/gencrl
```

### client/effective_address

> Resolve the Fabric CA connection address

Resolves the effective Fabric CA host, port, and URL scheme used by client operations. The referenced host must define `actual_host` and the Fabric CA server port settings; when it enables NodePort, the client uses `fabric_ca_server_k8s_node_port` instead of `fabric_ca_port`.

```yaml
- name: Resolve the Fabric CA connection address
  vars:
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/effective_address
```

### client/cryptogenize

> Normalize enrolled MSP output

Copies enrolled client MSP and TLS material into cryptogen-compatible filenames. Produces normalized files such as `ca.crt`, `server.crt`, and `server.key` for consumers that expect cryptogen layout.

```yaml
- name: Normalize enrolled MSP output
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Sets an optional enrollment profile such as `tls`. Example: `tls`.
    fabric_ca_enrollment_profile: "tls"
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

### client/bin/build

> Build the Fabric CA client binary

Builds the Fabric CA client binary from the configured Fabric CA Git source revision. Produces the local `fabric-ca-client` artifact later transferred to managed hosts.

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

### client/bin/install

> Install the Fabric CA client binary

Installs the Fabric CA client binary directly on the managed host with Go tooling. Uses the configured repository, source package, and revision without changing client enrollment data.

```yaml
- name: Install the Fabric CA client binary
  vars:
    # Sets the client Go package path.
    fabric_ca_client_bin_package: "{{ fabric_ca_git_hub_url }}/{{ fabric_ca_git_repo }}/{{ fabric_ca_client_source_code_package }}"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
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

### client/bin/transfer

> Transfer the Fabric CA client binary

Copies the previously built Fabric CA client binary to the managed host. Prepares the binary runtime path used by client enrollment, registration, revocation, and CRL tasks.

```yaml
- name: Transfer the Fabric CA client binary
  vars:
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/transfer
```

### client/bin/rm

> Remove the Fabric CA client binary

Removes the Fabric CA client binary from the managed host. Leaves enrolled MSP, TLS, and Idemix artifacts untouched.

```yaml
- name: Remove the Fabric CA client binary
  vars:
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/rm
```

### client/bin/enroll

> Enroll an identity with the client binary

Enrolls an identity with the locally installed Fabric CA client binary. Writes X.509 MSP, TLS, or Idemix enrollment artifacts under `fabric_ca_msp_dir` depending on enrollment type and profile.

```yaml
- name: Enroll an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Selects the enrollment type.
    fabric_ca_enrollment_type: bccsp
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets the Idemix enrollment profile.
    fabric_ca_idemix_enrollment_profile: idemix
    # Sets an optional enrollment profile such as `tls`. Example: `tls`.
    fabric_ca_enrollment_profile: "tls"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Sets the CSR SAN host list.
    fabric_ca_csr_hosts:
      - "{{ ansible_host }}"
      - "{{ actual_host }}"
      - "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/enroll
```

### client/bin/register

> Register an identity with the client binary

Registers a new identity with the locally installed Fabric CA client binary. Uses the registrar MSP in `fabric_ca_msp_dir` to create the configured enrollment ID, secret, type, and affiliation on the target server.

```yaml
- name: Register an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/register
```

### client/bin/reenroll

> Reenroll an identity with the client binary

Reenrolls an existing identity with the locally installed Fabric CA client binary. Refreshes certificate material in `fabric_ca_msp_dir`, preserving the selected CA name, CSR hosts, TLS settings, and enrollment profile.

```yaml
- name: Reenroll an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets an optional enrollment profile such as `tls`. Example: `tls`.
    fabric_ca_enrollment_profile: "tls"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Sets the CSR SAN host list.
    fabric_ca_csr_hosts:
      - "{{ ansible_host }}"
      - "{{ actual_host }}"
      - "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/reenroll
```

### client/bin/identity_list

> List Fabric CA identities with the client binary

Lists identities registered in the target Fabric CA server with the locally installed client binary. Uses the enrolled registrar MSP and effective server address to report identities without changing server state.

```yaml
- name: List Fabric CA identities with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/identity_list
```

### client/bin/revoke

> Revoke an identity with the client binary

Revokes an enrolled identity with the locally installed Fabric CA client binary. Uses the registrar MSP to revoke the configured enrollment ID on the target server while leaving local files for cleanup by separate tasks.

```yaml
- name: Revoke an identity with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/revoke
```

### client/bin/gencrl

> Generate a CRL with the client binary

Generates a certificate revocation list from the target Fabric CA server with the locally installed client binary. Uses the registrar MSP and effective address to retrieve current revocation data without changing runtime resources.

```yaml
- name: Generate a CRL with the client binary
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the client binary name.
    fabric_ca_client_bin_name: fabric-ca-client
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/bin/gencrl
```

### client/container/enroll

> Enroll an identity with the client container

Enrolls an identity with a transient Fabric CA client container. Mounts the local MSP/config path into the container and writes X.509, TLS, or Idemix artifacts under `fabric_ca_msp_dir`.

```yaml
- name: Enroll an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Selects the enrollment type.
    fabric_ca_enrollment_type: bccsp
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the Fabric CA image.
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
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets the Idemix enrollment profile.
    fabric_ca_idemix_enrollment_profile: idemix
    # Sets an optional enrollment profile such as `tls`. Example: `tls`.
    fabric_ca_enrollment_profile: "tls"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Sets the CSR SAN host list.
    fabric_ca_csr_hosts:
      - "{{ ansible_host }}"
      - "{{ actual_host }}"
      - "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/enroll
```

### client/container/register

> Register an identity with the client container

Registers a new identity with a transient Fabric CA client container. Uses the mounted registrar MSP to create the configured enrollment ID, secret, type, and affiliation on the target server.

```yaml
- name: Register an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the Fabric CA image.
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
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/register
```

### client/container/reenroll

> Reenroll an identity with the client container

Reenrolls an existing identity with a transient Fabric CA client container. Refreshes mounted MSP or TLS certificate material while preserving the selected CA name and CSR host settings.

```yaml
- name: Reenroll an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the Fabric CA image.
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
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Sets an optional enrollment profile such as `tls`. Example: `tls`.
    fabric_ca_enrollment_profile: "tls"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Sets the CSR SAN host list.
    fabric_ca_csr_hosts:
      - "{{ ansible_host }}"
      - "{{ actual_host }}"
      - "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/reenroll
```

### client/container/identity_list

> List Fabric CA identities with the client container

Lists identities registered in the target Fabric CA server with a transient client container. Mounts the registrar MSP read-only for query-style behavior and does not change server runtime resources.

```yaml
- name: List Fabric CA identities with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the Fabric CA image.
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
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/identity_list
```

### client/container/revoke

> Revoke an identity with the client container

Revokes an enrolled identity with a transient Fabric CA client container. Uses the mounted registrar MSP to revoke the configured enrollment ID on the target server.

```yaml
- name: Revoke an identity with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Supplies the identity used by Fabric CA client operations. Store secrets in Ansible Vault. Example: `peer0.org1.example.com`.
    fabric_ca_identity:peer0.org1.example.com
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the Fabric CA image.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/revoke
```

### client/container/gencrl

> Generate a CRL with the client container

Generates a certificate revocation list from the target Fabric CA server with a transient client container. Mounts the registrar MSP and retrieves revocation data without installing client binaries on the host.

```yaml
- name: Generate a CRL with the client container
  vars:
    # Sets the MSP directory used by Fabric CA client flows and MSP normalization. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp`.
    fabric_ca_msp_dir: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Names the inventory host that provides the target Fabric CA server. Example: `ca-org1`.
    fabric_ca_host: "ca-org1"
    # Sets the Fabric CA image.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the in-container client config root.
    fabric_ca_client_container_config_dir: /config
    # Sets the client URL scheme.
    fabric_ca_scheme: "{{ 'https' if fabric_ca_use_tls else 'http' }}"
    # Sets the CA name.
    fabric_ca_name: "{{ inventory_hostname }}"
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the TLS root certificate file used by Fabric CA client flows when TLS is enabled. Example: `/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`.
    fabric_ca_tls_certfile: "/tmp/fabricx/crypto-config/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/container/gencrl
```

### server/start

> Dispatch server startup

Dispatches Fabric CA server startup to the binary, container, or Kubernetes runtime. Starts the server after config and crypto artifacts have been prepared by the corresponding config and crypto tasks.

```yaml
- name: Dispatch server startup
  vars:
    # Uses the container server flow.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/start
```

### server/stop

> Dispatch server stop

Dispatches Fabric CA server stop to the binary or container runtime. Stops local runtime processes while leaving configuration, crypto, and fetched artifacts in place.

```yaml
- name: Dispatch server stop
  vars:
    # Uses the container server flow.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/stop
```

### server/teardown

> Dispatch server teardown

Dispatches Fabric CA server runtime removal across binary, container, or Kubernetes deployments. Removes runtime resources while preserving role-managed configuration and crypto unless dedicated cleanup tasks are invoked.

```yaml
- name: Dispatch server teardown
  vars:
    # Uses the container server flow.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/teardown
```

### server/wipe

> Wipe all server assets

Removes Fabric CA server runtime resources, binaries, configuration, and Kubernetes crypto resources. Use for full role cleanup when local and Kubernetes artifacts should be removed together.

```yaml
- name: Wipe all server assets
  vars:
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/wipe
```

### server/ping

> Check server ports

Checks that the Fabric CA API and operations endpoints are reachable. Uses direct host ports for local runtimes and delegates to the NodePort ping task for Kubernetes NodePort exposure.

```yaml
- name: Check server ports
  vars:
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
    # Sets the Fabric CA API port. Example: `7054`.
    fabric_ca_port: 7054
    # Sets the Fabric CA operations port. Example: `9443`.
    fabric_ca_operations_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/ping
```

### server/fetch_logs

> Dispatch server log collection

Dispatches Fabric CA server log collection for binary, container, or Kubernetes deployments. Collects runtime logs without changing server process, pod, configuration, or crypto state.

```yaml
- name: Dispatch server log collection
  vars:
    # Uses the container server flow.
    fabric_ca_server_use_container: "{{ (not fabric_ca_server_use_bin) and (not fabric_ca_server_use_k8s) }}"
    # Uses the binary server flow instead of container or Kubernetes.
    fabric_ca_server_use_bin: false
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/fetch_logs
```

### server/bin/build

> Build the Fabric CA server binary

Builds the Fabric CA server binary from the configured Fabric CA Git source revision. Produces the local `fabric-ca-server` artifact later transferred to managed hosts.

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

### server/bin/install

> Install the Fabric CA server binary

Installs the Fabric CA server binary directly on the managed host with Go tooling. Uses the configured repository, source package, and revision without rendering server configuration.

```yaml
- name: Install the Fabric CA server binary
  vars:
    # Sets the server Go package path.
    fabric_ca_server_bin_package: "{{ fabric_ca_git_hub_url }}/{{ fabric_ca_git_repo }}/{{ fabric_ca_server_source_code_package }}"
    # Sets the server binary name.
    fabric_ca_server_bin_name: fabric-ca-server
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

### server/bin/start

> Start the Fabric CA server binary

Starts the Fabric CA server as a managed local binary process. Reads the rendered server config and crypto from `fabric_ca_server_remote_config_dir` and exposes the configured API port.

```yaml
- name: Start the Fabric CA server binary
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Sets the Fabric CA API port. Example: `7054`.
    fabric_ca_port: 7054
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/start
```

### server/bin/stop

> Stop the Fabric CA server binary

Stops the managed Fabric CA server binary process. Leaves binaries, rendered configuration, logs, and crypto material available for restart or collection.

```yaml
- name: Stop the Fabric CA server binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/stop
```

### server/bin/fetch_logs

> Fetch server binary logs

Collects logs for the managed Fabric CA server binary process. Fetches runtime output for diagnosis without stopping the server or modifying artifacts.

```yaml
- name: Fetch server binary logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/fetch_logs
```

### server/bin/rm

> Remove the Fabric CA server binary

Removes the Fabric CA server binary from the managed host. Does not remove rendered configuration, crypto material, or fetched log artifacts.

```yaml
- name: Remove the Fabric CA server binary
  vars:
    # Sets the server binary name.
    fabric_ca_server_bin_name: fabric-ca-server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/rm
```

### server/bin/transfer

> Transfer the Fabric CA server binary

Copies the previously built Fabric CA server binary to the managed host. Prepares the binary runtime while leaving server configuration and crypto generation to separate tasks.

```yaml
- name: Transfer the Fabric CA server binary
  vars:
    # Sets the server binary name.
    fabric_ca_server_bin_name: fabric-ca-server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/bin/transfer
```

### server/container/start

> Start the Fabric CA server container

Starts the Fabric CA server as a managed container. Mounts rendered configuration and crypto into the container and publishes the configured API and operations ports.

```yaml
- name: Start the Fabric CA server container
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Sets the in-container Fabric CA config root.
    fabric_ca_server_container_config_dir: /config
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
    # Sets the Fabric CA image.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the Fabric CA API port. Example: `7054`.
    fabric_ca_port: 7054
    # Sets the Fabric CA operations port. Example: `9443`.
    fabric_ca_operations_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/start
```

### server/container/stop

> Stop the Fabric CA server container

Stops the managed Fabric CA server container. Keeps the container definition, mounted configuration, and crypto artifacts available for restart.

```yaml
- name: Stop the Fabric CA server container
  vars:
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/stop
```

### server/container/fetch_logs

> Fetch server container logs

Collects logs for the managed Fabric CA server container. Reads container runtime output without changing container, image, configuration, or crypto state.

```yaml
- name: Fetch server container logs
  vars:
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/fetch_logs
```

### server/container/rm

> Remove the Fabric CA server container

Removes the managed Fabric CA server container. Leaves remote configuration directories and generated crypto files for explicit cleanup tasks.

```yaml
- name: Remove the Fabric CA server container
  vars:
    # Sets the container name used for the Fabric CA server runtime.
    fabric_ca_container_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/container/rm
```

### server/k8s/start

> Start the Fabric CA server on Kubernetes

Creates Fabric CA Kubernetes runtime resources for the server. Uses the ConfigMap and Secret produced by transfer tasks, configures API and operations Services, and optionally exposes NodePorts.

```yaml
- name: Start the Fabric CA server on Kubernetes
  vars:
    # Sets the Kubernetes deployment wait timeout.
    fabric_ca_server_k8s_wait_timeout: 120
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Sets the Fabric CA image.
    fabric_ca_image: "{{ fabric_ca_registry_endpoint }}/{{ fabric_ca_image_name }}:{{ fabric_ca_image_tag }}"
    # Sets the registry endpoint used to resolve the Fabric CA image.
    fabric_ca_registry_endpoint: "{{ lookup('env', 'FABRIC_CA_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Sets the Fabric CA image name.
    fabric_ca_image_name: fabric-ca
    # Sets the Fabric CA image tag.
    fabric_ca_image_tag: 1.5.15
    # Sets the in-container Fabric CA config root.
    fabric_ca_server_container_config_dir: /config
    # Sets the Fabric CA API port. Example: `7054`.
    fabric_ca_port: 7054
    # Sets the Fabric CA operations port. Example: `9443`.
    fabric_ca_operations_port: 9443
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
    # Names the PostgreSQL host defined elsewhere in inventory. Example: `postgres0.example.com`.
    postgres_db_host: "postgres0.example.com"
    # Provides the Kubernetes namespace from the shared inventory. Example: `fabricx`.
    k8s_namespace: "fabricx"
    # Provides an optional Kubernetes image pull secret from shared inventory. Example: `registry-pull-secret`.
    k8s_image_pull_secret: "registry-pull-secret"
    # Kubernetes NodePort value used by the external API Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30054`.
    fabric_ca_server_k8s_node_port: 30054
    # Kubernetes NodePort value used by the external operations Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30943`.
    fabric_ca_server_k8s_operations_node_port: 30943
    # Set to `true` to create a LoadBalancer Service entry that exposes the API port externally. When undefined or `false`, the API port is not included in the LoadBalancer Service.
    fabric_ca_server_k8s_loadbalancer_expose_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the operations port externally. When undefined or `false`, the operations port is not included in the LoadBalancer Service.
    fabric_ca_server_k8s_loadbalancer_expose_operations_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/start
```

### server/k8s/ping

> Check Fabric CA node ports

Probes configured Kubernetes NodePort values and LoadBalancer-exposed service ports for external reachability.

```yaml
- name: Check Fabric CA node ports
  vars:
    # Kubernetes NodePort value used by the external API Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30054`.
    fabric_ca_server_k8s_node_port: 30054
    # Kubernetes NodePort value used by the external operations Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30943`.
    fabric_ca_server_k8s_operations_node_port: 30943
    # Set to `true` to create a LoadBalancer Service entry that exposes the API port externally. When undefined or `false`, the API port is not included in the LoadBalancer Service.
    fabric_ca_server_k8s_loadbalancer_expose_port: false
    # Set to `true` to create a LoadBalancer Service entry that exposes the operations port externally. When undefined or `false`, the operations port is not included in the LoadBalancer Service.
    fabric_ca_server_k8s_loadbalancer_expose_operations_port: false
    # Sets the Fabric CA API port. Example: `7054`.
    fabric_ca_port: 7054
    # Sets the Fabric CA operations port. Example: `9443`.
    fabric_ca_operations_port: 9443
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/ping
```

### server/k8s/fetch_logs

> Fetch server pod logs

Collects pod logs for the Fabric CA Kubernetes deployment. Fetches runtime output from the server pod in `k8s_namespace` without changing cluster resources.

```yaml
- name: Fetch server pod logs
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/fetch_logs
```

### server/k8s/rm

> Remove server Kubernetes runtime resources

Deletes the Fabric CA Kubernetes runtime resources. Removes Deployment and Service objects while leaving ConfigMap and Secret cleanup to their dedicated tasks.

```yaml
- name: Remove server Kubernetes runtime resources
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Provides the Kubernetes namespace from the shared inventory. Example: `fabricx`.
    k8s_namespace: "fabricx"
    # Kubernetes NodePort value used by the external API Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30054`.
    fabric_ca_server_k8s_node_port: 30054
    # Set to `true` to create a LoadBalancer Service entry that exposes the API port externally. When undefined or `false`, the API port is not included in the LoadBalancer Service.
    fabric_ca_server_k8s_loadbalancer_expose_port: false
    # Kubernetes NodePort value used by the external operations Service port. Defining this variable enables the NodePort Service; the value is set as the static `nodePort` in the Service spec. Example: `30943`.
    fabric_ca_server_k8s_operations_node_port: 30943
    # Set to `true` to create a LoadBalancer Service entry that exposes the operations port externally. When undefined or `false`, the operations port is not included in the LoadBalancer Service.
    fabric_ca_server_k8s_loadbalancer_expose_operations_port: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/rm
```

### server/k8s/config/transfer

> Transfer server config to a ConfigMap

Creates or updates the Fabric CA Kubernetes ConfigMap from rendered server configuration. Publishes config files into `k8s_namespace` for consumption by the Kubernetes server runtime.

```yaml
- name: Transfer server config to a ConfigMap
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Names the PostgreSQL host defined elsewhere in inventory. Example: `postgres0.example.com`.
    postgres_db_host: "postgres0.example.com"
    # Provides the Kubernetes namespace from the shared inventory. Example: `fabricx`.
    k8s_namespace: "fabricx"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/config/transfer
```

### server/k8s/config/rm

> Remove the server ConfigMap

Deletes the Fabric CA Kubernetes ConfigMap. Removes Kubernetes config resources while leaving runtime and crypto Secret cleanup to separate tasks.

```yaml
- name: Remove the server ConfigMap
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Provides the Kubernetes namespace from the shared inventory. Example: `fabricx`.
    k8s_namespace: "fabricx"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/config/rm
```

### server/k8s/crypto/transfer

> Transfer server crypto to a Secret

Creates or updates the Fabric CA Kubernetes Secret containing server crypto material. Transfers CA and optional TLS keypairs from the remote config directory into `k8s_namespace`.

```yaml
- name: Transfer server crypto to a Secret
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
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
    # Provides the Kubernetes namespace from the shared inventory. Example: `fabricx`.
    k8s_namespace: "fabricx"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/crypto/transfer
```

### server/k8s/crypto/rm

> Remove the server Secret

Deletes the Fabric CA Kubernetes Secret. Removes server CA and TLS key material from Kubernetes while leaving local files untouched.

```yaml
- name: Remove the server Secret
  vars:
    # Sets the Kubernetes resource name for the Fabric CA server and its Service resources.
    fabric_ca_server_k8s_resource_name: "{{ inventory_hostname }}"
    # Provides the Kubernetes namespace from the shared inventory. Example: `fabricx`.
    k8s_namespace: "fabricx"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/k8s/crypto/rm
```

### server/crypto/setup

> Generate server crypto material

Generates X.509 and Idemix crypto material for the Fabric CA server. Coordinates the role's root CA, TLS, and Idemix issuer artifact generation before runtime start or Kubernetes transfer.

```yaml
- name: Generate server crypto material
  vars:
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/setup
```

### server/crypto/x509/setup

> Generate server x509 crypto

Generates the Fabric CA root CA and TLS keypairs. Writes private keys and certificates into `fabric_ca_server_remote_config_dir` using the configured common name, SAN hosts, organization domain, and curve.

```yaml
- name: Generate server x509 crypto
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
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
    # Sets the CSR common name.
    fabric_ca_csr_cn: "{{ fabric_ca_name }}"
    # Sets the CSR SAN host list.
    fabric_ca_csr_hosts:
      - "{{ ansible_host }}"
      - "{{ actual_host }}"
      - "{{ inventory_hostname }}"
    # Matches IPv4 SAN entries while splitting Fabric CA CSR hosts into IP and DNS names. Example: `^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$`
    openssl_san_ipv4_regex: "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
    # Provides the organization metadata defined elsewhere in inventory; `domain` is required. Example: `org1.example.com`.
    organization:org1.example.com
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/x509/setup
```

### server/crypto/idemix/setup

> Generate server Idemix crypto

Generates the Fabric CA Idemix issuer keys. Stages Idemix issuer artifacts in the transient output directory and places them where the server configuration expects them.

```yaml
- name: Generate server Idemix crypto
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Sets the transient Idemix output directory.
    fabric_ca_server_idemixgen_output_dir: "{{ fabric_ca_server_remote_config_dir }}/idemixgen-artifacts"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/idemix/setup
```

### server/crypto/fetch

> Fetch server certificates

Fetches the Fabric CA server certificate material. Copies CA certificates from the managed host into `fetched_artifacts_dir` for cross-role trust distribution.

```yaml
- name: Fetch server certificates
  vars:
    # Provides the organization metadata defined elsewhere in inventory; `domain` is required. Example: `org1.example.com`.
    organization:org1.example.com
    # Provides the shared local artifacts root used by this role. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/fetched-artifacts"
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Sets the server CA certificate filename.
    fabric_ca_server_ca_cert_file: ca-cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/fetch
```

### server/crypto/rm

> Remove server Secret

Deletes Kubernetes crypto resources for the Fabric CA server when Kubernetes mode is enabled. Leaves local X.509 and Idemix files to the config cleanup path unless the broader wipe flow is used.

```yaml
- name: Remove server Secret
  vars:
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/rm
```

### server/config/transfer

> Render and transfer server config

Renders and transfers the Fabric CA server configuration. Includes bootstrap admin, CA name, TLS, CSR, operations, PostgreSQL, and registry settings, and copies the PostgreSQL TLS CA certificate when needed.

```yaml
- name: Render and transfer server config
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Sets the Fabric CA API port. Example: `7054`.
    fabric_ca_port: 7054
    # Sets the server log level.
    fabric_ca_log_level: INFO
    # Enables TLS for server and client connections.
    fabric_ca_use_tls: false
    # Sets the server config directory.
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
    # Supplies the bootstrap administrator rendered into the server registry section; `name` and `secret` are required. Store the secret in Ansible Vault. Example: `admin`.
    fabric_ca_admin:admin
    # Sets the CSR common name.
    fabric_ca_csr_cn: "{{ fabric_ca_name }}"
    # Sets the CSR SAN host list.
    fabric_ca_csr_hosts:
      - "{{ ansible_host }}"
      - "{{ actual_host }}"
      - "{{ inventory_hostname }}"
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
    # Sets the CSR expiry.
    fabric_ca_csr_expiry: 131400h
    # Provides the organization metadata defined elsewhere in inventory; `domain` is required. Example: `org1.example.com`.
    organization:org1.example.com
    # Names the PostgreSQL host defined elsewhere in inventory. Example: `postgres0.example.com`.
    postgres_db_host: "postgres0.example.com"
    # Provides the shared local artifacts root used by this role. Example: `/tmp/fabricx/fetched-artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/fetched-artifacts"
    # Sets the Fabric CA operations port. Example: `9443`.
    fabric_ca_operations_port: 9443
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/transfer
```

### server/config/rm

> Remove server config resources

Deletes Fabric CA server configuration resources. Removes local or Kubernetes config artifacts according to runtime mode while leaving fetched artifacts untouched.

```yaml
- name: Remove server config resources
  vars:
    # Sets the remote Fabric CA config root.
    fabric_ca_server_remote_config_dir: "{{ remote_config_dir }}"
    # Provides the shared remote configuration root used by this role. Example: `/var/hyperledger/fabricx/fabric-ca/ca-org1/config`.
    remote_config_dir: "/var/hyperledger/fabricx/fabric-ca/ca-org1/config"
    # Uses the Kubernetes server flow instead of the local runtimes.
    fabric_ca_server_use_k8s: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/rm
```
