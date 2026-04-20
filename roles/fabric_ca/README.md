# hyperledger.fabricx.fabric_ca

> Runs a Hyperledger Fabric CA server and client for certificate management across binary, container, and Kubernetes deployments.

<!-- @depends_on: hyperledger.fabricx.openssl -->

## Table of Contents <!-- omit in toc -->

- [Depends On](#depends-on)
- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Server Crypto](#server-crypto)
    - [server/crypto/setup](#servercryptosetup)
    - [server/crypto/x509/setup](#servercryptox509setup)
    - [server/crypto/idemix/setup](#servercryptoidemixsetup)
    - [server/crypto/fetch](#servercryptofetch)
  - [Server Config](#server-config)
    - [server/config/transfer](#serverconfigtransfer)
  - [Server Lifecycle](#server-lifecycle)
    - [server/start](#serverstart)
    - [server/stop](#serverstop)
    - [server/teardown](#serverteardown)
    - [server/wipe](#serverwipe)
    - [server/ping](#serverping)
    - [server/fetch_logs](#serverfetch_logs)
  - [Client Tasks](#client-tasks)
    - [client/register](#clientregister)
    - [client/enroll](#clientenroll)
    - [client/reenroll](#clientreenroll)
    - [client/identity_list](#clientidentity_list)
    - [client/revoke](#clientrevoke)
    - [client/gencrl](#clientgencrl)
- [Variables](#variables)

## Depends On

| Role                                                  | Reason                                  |
| ----------------------------------------------------- | --------------------------------------- |
| [`hyperledger.fabricx.openssl`](../openssl/README.md) | Used for CSR and certificate generation |

## Prerequisites

- `go` to be installed (when using binary mode)
- `postgres_db_host` to be defined for the Fabric CA server; SQLite is no longer supported
- a reachable Kubernetes cluster with `kubernetes.core` configured (when using k8s mode)

## Tasks

### Server Crypto

| Task                                                                  | Description                                   |
| --------------------------------------------------------------------- | --------------------------------------------- |
| [server/crypto/setup](./tasks/server/crypto/setup.yaml)               | Pre-generates x509 and Idemix crypto material |
| [server/crypto/x509/setup](./tasks/server/crypto/x509/setup.yaml)     | Pre-generates Fabric CA x509 material         |
| [server/crypto/idemix/setup](./tasks/server/crypto/idemix/setup.yaml) | Pre-generates Idemix crypto material          |
| [server/crypto/fetch](./tasks/server/crypto/fetch.yaml)               | Fetches CA certificates                       |

#### server/crypto/setup

Pre-generates x509 and Idemix crypto material for a Fabric CA server. It is an orchestrator over `server/crypto/x509/setup` and `server/crypto/idemix/setup`:

```yaml
- name: Setup the Fabric CA server crypto material
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/setup
```

#### server/crypto/x509/setup

Pre-generates Fabric CA x509 material:

```yaml
- name: Setup the Fabric CA server x509 crypto material
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/x509/setup
```

#### server/crypto/idemix/setup

Pre-generates Idemix crypto material:

```yaml
- name: Setup the Fabric CA server Idemix crypto material
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/idemix/setup
```

#### server/crypto/fetch

Fetches CA certificates:

```yaml
- name: Fetch the Fabric CA certificates
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/crypto/fetch
```

### Server Config

| Task                                                          | Description                       |
| ------------------------------------------------------------- | --------------------------------- |
| [server/config/transfer](./tasks/server/config/transfer.yaml) | Transfers CA server configuration |

#### server/config/transfer

Transfers CA server configuration:

```yaml
- name: Transfer the Fabric CA server configuration
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/config/transfer
```

### Server Lifecycle

| Task                                                | Description                |
| --------------------------------------------------- | -------------------------- |
| [server/start](./tasks/server/start.yaml)           | Starts the CA server       |
| [server/stop](./tasks/server/stop.yaml)             | Stops the CA server        |
| [server/teardown](./tasks/server/teardown.yaml)     | Removes CA server runtime  |
| [server/wipe](./tasks/server/wipe.yaml)             | Removes CA server data     |
| [server/ping](./tasks/server/ping.yaml)             | Health check for CA server |
| [server/fetch_logs](./tasks/server/fetch_logs.yaml) | Collects CA server logs    |

#### server/start

Starts the CA server:

```yaml
- name: Start the Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/start
```

#### server/stop

Stops the CA server:

```yaml
- name: Stop the Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/stop
```

#### server/teardown

Removes CA server runtime:

```yaml
- name: Teardown the Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/teardown
```

#### server/wipe

Removes CA server data:

```yaml
- name: Wipe the Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/wipe
```

#### server/ping

Health check for CA server:

```yaml
- name: Ping the Fabric CA server
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/ping
```

#### server/fetch_logs

Collects CA server logs:

```yaml
- name: Fetch the Fabric CA server logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: server/fetch_logs
```

### Client Tasks

| Task                   | File                                                                 | Description            |
| ---------------------- | -------------------------------------------------------------------- | ---------------------- |
| `client/register`      | [tasks/client/register.yaml](./tasks/client/register.yaml)           | Registers an identity  |
| `client/enroll`        | [tasks/client/enroll.yaml](./tasks/client/enroll.yaml)               | Enrolls an identity    |
| `client/reenroll`      | [tasks/client/reenroll.yaml](./tasks/client/reenroll.yaml)           | Re-enrolls an identity |
| `client/identity_list` | [tasks/client/identity_list.yaml](./tasks/client/identity_list.yaml) | Lists identities       |
| `client/revoke`        | [tasks/client/revoke.yaml](./tasks/client/revoke.yaml)               | Revokes an identity    |
| `client/gencrl`        | [tasks/client/gencrl.yaml](./tasks/client/gencrl.yaml)               | Generates CRL          |

Client operations automatically resolve the effective Fabric CA connection port and use the NodePort value whenever `fabric_ca_server_k8s_use_node_port: true` is enabled on the referenced CA host.

#### client/register

Registers an identity:

```yaml
- name: Register an identity
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/register
```

#### client/enroll

Enrolls an identity:

```yaml
- name: Enroll an identity
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/enroll
```

#### client/reenroll

Re-enrolls an identity:

```yaml
- name: Re-enroll an identity
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/reenroll
```

#### client/identity_list

Lists identities:

```yaml
- name: List identities
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/identity_list
```

#### client/revoke

Revokes an identity:

```yaml
- name: Revoke an identity
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/revoke
```

#### client/gencrl

Generates CRL:

```yaml
- name: Generate CRL
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fabric_ca
    tasks_from: client/gencrl
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
