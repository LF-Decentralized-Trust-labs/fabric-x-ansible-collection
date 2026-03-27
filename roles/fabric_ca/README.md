# hyperledger.fabricx.fabric_ca

The role `hyperledger.fabricx.fabric_ca` can be used to run an Hyperledger Fabric CA server and set it up using a Fabric CA client.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [server/config/transfer](#serverconfigtransfer)
  - [server/crypto/fetch](#servercryptofetch)
  - [server/start](#serverstart)
  - [server/stop](#serverstop)
  - [server/teardown](#serverteardown)
  - [server/wipe](#serverwipe)
  - [server/ping](#serverping)
  - [server/fetch\_logs](#serverfetch_logs)
  - [client/register](#clientregister)
  - [client/enroll](#clientenroll)
  - [client/reenroll](#clientreenroll)
  - [client/identity\_list](#clientidentity_list)
  - [client/revoke](#clientrevoke)
  - [client/gencrl](#clientgencrl)

## Prerequisites

The role requires:

- `go` to be installed (only if you plan to use binaries with `fabric_ca_server_use_bin: true` or `fabric_ca_client_use_bin: true`).

## Variables

| Variable                                  | Default                                                   | Description                                                                        |
| ----------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `fabric_ca_registry_endpoint`             | `$FABRIC_CA_REGISTRY_ENDPOINT` or `docker.io/hyperledger` | Container registry endpoint                                                        |
| `fabric_ca_image_name`                    | `fabric-ca`                                               | Container image name                                                               |
| `fabric_ca_image_tag`                     | `1.5.15`                                                  | Container image tag                                                                |
| `fabric_ca_image`                         | `{{ registry }}/{{ name }}:{{ tag }}`                     | Full container image reference                                                     |
| `fabric_ca_container_name`                | `{{ inventory_hostname }}`                                | Name given to the container                                                        |
| `fabric_ca_git_uri`                       | `https://github.com/hyperledger/fabric-ca.git`            | Git repository used to build the binaries                                          |
| `fabric_ca_git_commit`                    | `v1.5.15`                                                 | Git ref (tag or commit) to check out                                               |
| `fabric_ca_server_source_code_package`    | `cmd/fabric-ca-server`                                    | Go source package path for the server binary                                       |
| `fabric_ca_server_bin_package`            | `github.com/hyperledger/fabric-ca/cmd/fabric-ca-server`   | Fully-qualified Go package for `go install` (server)                               |
| `fabric_ca_server_bin_name`               | `fabric-ca-server`                                        | Name of the server binary                                                          |
| `fabric_ca_server_use_bin`                | `false`                                                   | Set to `true` to run the CA server as a native binary                              |
| `fabric_ca_client_source_code_package`    | `cmd/fabric-ca-client`                                    | Go source package path for the client binary                                       |
| `fabric_ca_client_bin_package`            | `github.com/hyperledger/fabric-ca/cmd/fabric-ca-client`   | Fully-qualified Go package for `go install` (client)                               |
| `fabric_ca_client_bin_name`               | `fabric-ca-client`                                        | Name of the client binary                                                          |
| `fabric_ca_client_use_bin`                | `false`                                                   | Set to `true` to run the CA client as a native binary                              |
| `fabric_ca_server_remote_config_dir`      | `{{ remote_config_dir }}`                                 | Configuration directory on the remote node                                         |
| `fabric_ca_server_remote_data_dir`        | `{{ remote_data_dir }}`                                   | Data directory on the remote node                                                  |
| `fabric_ca_server_container_config_dir`   | `/config`                                                 | Server configuration directory inside the container                                |
| `fabric_ca_client_container_config_dir`   | `/config`                                                 | Client configuration directory inside the container                                |
| `fabric_ca_server_container_data_dir`     | `/data`                                                   | Server data directory inside the container                                         |
| `fabric_ca_server_config_dir`             | auto-selected                                             | Active config directory (remote or container, based on `fabric_ca_server_use_bin`) |
| `fabric_ca_server_data_dir`               | auto-selected                                             | Active data directory (remote or container, based on `fabric_ca_server_use_bin`)   |
| `fabric_ca_log_level`                     | `INFO`                                                    | Log level                                                                          |
| `fabric_ca_use_tls`                       | `false`                                                   | Enable TLS                                                                         |
| `fabric_ca_scheme`                        | `https` or `http`                                         | URL scheme derived from `fabric_ca_use_tls`                                        |
| `fabric_ca_enable_nodeous`                | `true`                                                    | Enable NodeOUs in the MSP configuration                                            |
| `fabric_ca_tls_root_cert`                 | `{{ fabric_ca_server_remote_config_dir }}/ca-cert.pem`    | Path to the CA TLS root certificate                                                |
| `fabric_ca_name`                          | `{{ inventory_hostname }}`                                | Name of the CA                                                                     |
| `fabric_ca_csr_cn`                        | `{{ fabric_ca_name }}`                                    | Common Name (CN) for the CA CSR                                                    |
| `fabric_ca_csr_hosts`                     | `[ansible_host, inventory_hostname]`                      | SAN hosts for the CA CSR                                                           |
| `fabric_ca_csr_expiry`                    | `131400h`                                                 | Certificate expiry (15 years)                                                      |
| `fabric_ca_cryptogenize_tls_ca_cert_file` | `ca.crt`                                                  | TLS CA certificate file name (cryptogenize mode)                                   |
| `fabric_ca_cryptogenize_tls_cert_file`    | `server.crt`                                              | TLS server certificate file name (cryptogenize mode)                               |
| `fabric_ca_cryptogenize_tls_key_file`     | `server.key`                                              | TLS server key file name (cryptogenize mode)                                       |

## Tasks

### server/config/transfer

The task `server/config/transfer` generates the configuration file for a Fabric CA server:

```yaml
- name: Transfer the Fabric CA server configuration file
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/transfer
```

### server/crypto/fetch

The task `server/crypto/fetch` fetches on the control node the certificates of a Fabric CA server that need to be used to build the genesis block:

```yaml
- name: Fetch the Fabric CA server crypto material
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/fetch
```

### server/start

The task `server/start` starts a Fabric CA server (either as container or as binary if the `fabric_ca_use_bin` variable is set):

```yaml
- name: Start a Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/start
```

### server/stop

The task `server/stop` stops a Fabric CA server:

```yaml
- name: Stop a Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/stop
```

### server/teardown

The task `server/teardown` tears down a Fabric CA server and removes all the artifacts generated during runtime:

```yaml
- name: Teardown a Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/teardown
```

### server/wipe

The task `server/wipe` wipes a Fabric CA server removing all the data generated at runtime as well as any configuration file:

```yaml
- name: Wipe a Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/wipe
```

### server/ping

The task `server/ping` pings a Fabric CA server to check if is up and running:

```yaml
- name: Ping a Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/ping
```

### server/fetch_logs

The task `server/fetch_logs` fetches the logs of a Fabric CA server:

```yaml
- name: Fetch the logs of a Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/fetch_logs
```

### client/register

The task `client/register` registers an identity within a Fabric CA server.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Register the "orderer-router-1" user
  vars:
    fabric_ca_tls_certfile: /tmp/fabric-ca-orderer-org1/ca-cert.pem
    fabric_ca_host: fabric-ca-orderer-org1
    fabric_ca_msp_dir: /tmp/fabric-ca-orderer-org1/admin/msp
    fabric_ca_identity:
      name: orderer-router-1
      secret: orderer-router-1-PWD
      type: orderer
      attrs:
        hf.GenCRL: "true:ecert"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/register
```

### client/enroll

The task `client/enroll` enrolls a registered identity and generates its MSP crypto material.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Enroll the "orderer-router-1" user
  vars:
    fabric_ca_host: fabric-ca-orderer-org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric-ca-orderer-org1
    fabric_ca_msp_dir: /tmp/orderer-router-1/msp
    fabric_ca_tls_certfile: /tmp/orderer-router-1/ca-cert.pem
    fabric_ca_csr_hosts:
      - orderer-router-1
    fabric_ca_identity:
      name: orderer-router-1
      secret: orderer-router-1-PWD
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/enroll
```

### client/reenroll

The task `client/reenroll` re-enrolls a registered identity and generates new MSP crypto material.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Re-enroll the "orderer-router-1" user
  vars:
    fabric_ca_host: fabric-ca-orderer-org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric-ca-orderer-org1
    fabric_ca_msp_dir: /tmp/orderer-router-1/msp
    fabric_ca_tls_certfile: /tmp/orderer-router-1/ca-cert.pem
    fabric_ca_csr_hosts:
      - orderer-router-1
    fabric_ca_identity:
      name: orderer-router-1
      secret: orderer-router-1-PWD
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/reenroll
```

### client/identity_list

The task `client/identity_list` lists all the identities registered in a Fabric CA server.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Find all registered identities in "fabric-ca-orderer-org1" Fabric CA server
  vars:
    fabric_ca_host: fabric-ca-orderer-org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric-ca-orderer-org1
    fabric_ca_msp_dir: /tmp/fabric-ca-orderer-org1/admin/msp
    fabric_ca_tls_certfile: /tmp/fabric-ca-orderer-org1/ca-cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/identity_list
```

### client/revoke

The task `client/revoke` revokes an identity previously enrolled in a Fabric CA server.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Find all registered identities in "fabric-ca-orderer-org1" Fabric CA server
  vars:
    fabric_ca_host: fabric-ca-orderer-org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric-ca-orderer-org1
    fabric_ca_msp_dir: /tmp/fabric-ca-orderer-org1/admin/msp
    fabric_ca_tls_certfile: /tmp/fabric-ca-orderer-org1/ca-cert.pem
    fabric_ca_identity:
      name: orderer-router-1
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/revoke
```

### client/gencrl

The task `client/gencrl` generates the Certificate Revocation List for a given Fabric CA server. **NOTE** that only users registered with the `hf.GenCRL: true` attribute are allowed to generate such list.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Find all registered identities in "fabric-ca-orderer-org1" Fabric CA server
  vars:
    fabric_ca_host: fabric-ca-orderer-org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric-ca-orderer-org1
    fabric_ca_msp_dir: /tmp/fabric-ca-orderer-org1/admin/msp
    fabric_ca_tls_certfile: /tmp/fabric-ca-orderer-org1/ca-cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/gencrl
```
