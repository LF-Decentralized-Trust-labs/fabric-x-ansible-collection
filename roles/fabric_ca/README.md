# hyperledger.fabricx.fabric_ca

The role `hyperledger.fabricx.fabric_ca` can be used to run an Hyperledger Fabric CA server and set it up using a Fabric CA client.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [server/config/transfer](#serverconfigtransfer)
  - [server/start](#serverstart)
  - [server/config/fetch_crypto_material](#serverconfigfetch_crypto_material)
  - [server/stop](#serverstop)
  - [server/teardown](#serverteardown)
  - [server/wipe](#serverwipe)
  - [server/ping](#serverping)
  - [server/fetch_logs](#serverfetch_logs)
  - [client/register](#clientregister)
  - [client/enroll](#clientenroll)
  - [client/reenroll](#clientreenroll)
  - [client/identity_list](#clientidentity_list)
  - [client/revoke](#clientrevoke)
  - [client/gencrl](#clientgencrl)

## Prerequisites

The role requires:

- `go` to be installed (only if you plan to use binaries with `fabric_ca_server_use_bin: true` or `fabric_ca_client_use_bin: true`).

## Tasks

### server/config/transfer

The task `server/config/transfer` generates the configuration file for a Fabric CA server:

```yaml
- name: Transfer the Fabric CA server configuration file
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/transfer
```

### server/start

The task `server/start` starts a Fabric CA server (either as container or as binary if the `fabric_ca_use_bin` variable is set):

```yaml
- name: Start a Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/start
```

### server/config/fetch_crypto_material

The task `server/config/fetch_crypto_material` fetches on the control node the certificates of a Fabric CA server that need to be used to build the genesis block:

```yaml
- name: Fetch the Fabric CA server crypto material
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/fetch_crypto_material
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

The task `server/teardown` tears down a Fabric CA server:

```yaml
- name: Stop a Fabric CA server
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
    fabric_ca_tls_certfile: /tmp/fabric_ca_orderer_org1/ca-cert.pem
    fabric_ca_host: fabric_ca_orderer_org1
    fabric_ca_msp_dir: /tmp/fabric_ca_orderer_org1/admin/msp
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
    fabric_ca_host: fabric_ca_orderer_org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric_ca_orderer_org1
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
    fabric_ca_host: fabric_ca_orderer_org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric_ca_orderer_org1
    fabric_ca_msp_dir: /tmp/orderer-router-1/msp
    fabric_ca_tls_certfile: /tmp/orderer-router-1/ca-cert.pem
    fabric_ca_csr_hosts:
      - orderer-router-1
    fabric_ca_identity:
      name: orderer-router-1
      secret: orderer-router-1-PWD
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/re-enroll
```

### client/identity_list

The task `client/identity_list` lists all the identities registered in a Fabric CA server.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Find all registered identities in "fabric_ca_orderer_org1" Fabric CA server
  vars:
    fabric_ca_host: fabric_ca_orderer_org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric_ca_orderer_org1
    fabric_ca_msp_dir: /tmp/fabric_ca_orderer_org1/admin/msp
    fabric_ca_tls_certfile: /tmp/fabric_ca_orderer_org1/ca-cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/identity_list
```

### client/revoke

The task `client/revoke` revokes an identity previously enrolled in a Fabric CA server.

It uses the `fabric-ca-client` CLI utility (either as container or as binary by setting the variable `fabric_ca_client_use_bin: true`):

```yaml
- name: Find all registered identities in "fabric_ca_orderer_org1" Fabric CA server
  vars:
    fabric_ca_host: fabric_ca_orderer_org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric_ca_orderer_org1
    fabric_ca_msp_dir: /tmp/fabric_ca_orderer_org1/admin/msp
    fabric_ca_tls_certfile: /tmp/fabric_ca_orderer_org1/ca-cert.pem
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
- name: Find all registered identities in "fabric_ca_orderer_org1" Fabric CA server
  vars:
    fabric_ca_host: fabric_ca_orderer_org1
    fabric_ca_use_tls: true
    fabric_ca_name: fabric_ca_orderer_org1
    fabric_ca_msp_dir: /tmp/fabric_ca_orderer_org1/admin/msp
    fabric_ca_tls_certfile: /tmp/fabric_ca_orderer_org1/ca-cert.pem
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/gencrl
```
