# hyperledger.fabricx.container

> Handles container lifecycle management (supports `podman` and `docker`).

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Registry](#registry)
    - [registry/login](#registrylogin)
  - [Network](#network)
    - [network/create](#networkcreate)
    - [network/rm](#networkrm)
  - [Volume](#volume)
    - [volume/create](#volumecreate)
    - [volume/rm](#volumerm)
  - [Lifecycle](#lifecycle)
    - [install](#install)
    - [get_container_client](#get_container_client)
    - [start](#start)
    - [stop](#stop)
    - [rm](#rm)
    - [exec](#exec)
    - [fetch_logs](#fetch_logs)
- [Variables](#variables)

## Prerequisites

- `podman` or `docker` installed on the targeted node

## Tasks

### Registry

| Task                                          | Description                    |
| --------------------------------------------- | ------------------------------ |
| [registry/login](./tasks/registry/login.yaml) | Logs into a container registry |

#### registry/login

Logs a container engine within a certain Container Registry:

```yaml
- name: Log the container engine within container registry
  vars:
    container_registry: icr.io
    container_registry_username: iamapikey
    container_registry_password: my_api_key
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: registry/login
```

### Network

| Task                                          | Description                 |
| --------------------------------------------- | --------------------------- |
| [network/create](./tasks/network/create.yaml) | Creates a container network |
| [network/rm](./tasks/network/rm.yaml)         | Removes a container network |

#### network/create

Creates a container network:

```yaml
- name: Create a container network
  vars:
    container_network_name: my-network
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: network/create
```

#### network/rm

Removes a container network:

```yaml
- name: Remove a container network
  vars:
    container_network_name: my-network
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: network/rm
```

### Volume

| Task                                        | Description                |
| ------------------------------------------- | -------------------------- |
| [volume/create](./tasks/volume/create.yaml) | Creates a container volume |
| [volume/rm](./tasks/volume/rm.yaml)         | Removes a container volume |

#### volume/create

Creates a container volume:

```yaml
- name: Create a container volume
  vars:
    container_volume_name: my-volume
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/create
```

#### volume/rm

Removes a container volume:

```yaml
- name: Remove a container volume
  vars:
    container_volume_name: my-volume
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/rm
```

### Lifecycle

| Task                                                      | Description                        |
| --------------------------------------------------------- | ---------------------------------- |
| [install](./tasks/install.yaml)                           | Installs container engine          |
| [get_container_client](./tasks/get_container_client.yaml) | Detects available container client |
| [start](./tasks/start.yaml)                               | Starts a container                 |
| [stop](./tasks/stop.yaml)                                 | Stops a container                  |
| [rm](./tasks/rm.yaml)                                     | Removes a container                |
| [exec](./tasks/exec.yaml)                                 | Executes command in container      |
| [fetch_logs](./tasks/fetch_logs.yaml)                     | Collects container logs            |

#### install

Installs the container engine:

```yaml
- name: Install container engine
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: install
```

#### get_container_client

Detects available container client:

```yaml
- name: Get container client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: get_container_client
```

#### start

Starts a container:

```yaml
- name: Start a container
  vars:
    container_name: my-container
    container_image: my-image
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: start
```

#### stop

Stops a container:

```yaml
- name: Stop a container
  vars:
    container_name: my-container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: stop
```

#### rm

Removes a container:

```yaml
- name: Remove a container
  vars:
    container_name: my-container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: rm
```

#### exec

Executes a command in a container:

```yaml
- name: Execute command in container
  vars:
    container_name: my-container
    container_command: echo hello
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: exec
```

#### fetch_logs

Collects container logs:

```yaml
- name: Fetch container logs
  vars:
    container_name: my-container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: fetch_logs
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
