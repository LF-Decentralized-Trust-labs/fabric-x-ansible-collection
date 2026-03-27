# hyperledger.fabricx.container

The role `hyperledger.fabricx.container` can be used to handle a container on a target node. The role allows to run a container with either `podman` or `docker`.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [registry/login](#registrylogin)
  - [network/create](#networkcreate)
  - [network/rm](#networkrm)
  - [volume/create](#volumecreate)
  - [volume/rm](#volumerm)
  - [install](#install)
  - [get\_container\_client](#get_container_client)
  - [start](#start)
  - [stop](#stop)
  - [rm](#rm)
  - [exec](#exec)
  - [fetch\_logs](#fetch_logs)

## Prerequisites

The role requires either `podman` or `docker` to be installed on the targeted node.

## Variables

| Variable                         | Default                                              | Description                                                                      |
| -------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| `container_client`               | `$CONTAINER_CLIENT` or auto-detected                 | Container engine to use (`podman` or `docker`)                                   |
| `container_run_detach_mode`      | `true`                                               | Run the container in detached mode                                               |
| `container_healthcheck_interval` | `30s`                                                | Container healthcheck interval                                                   |
| `container_autoremove`           | `false`                                              | Automatically remove the container when it stops                                 |
| `container_ignore_errors`        | `false`                                              | Ignore errors when running the container                                         |
| `container_host_uid`             | `{{ ansible_facts.user_uid }}`                       | UID of the host user                                                             |
| `container_host_gid`             | `{{ ansible_facts.user_gid }}`                       | GID of the host user                                                             |
| `container_host_user`            | `uid:gid`                                            | Host user identity passed to the container                                       |
| `container_host_user_is_root`    | derived                                              | Whether the host user is root                                                    |
| `container_run_as_host_user`     | `false`                                              | Run the container as the host user                                               |
| `container_fetched_logs_dir`     | `{{ fetched_artifacts_dir }}/{{ container_name }}`   | Directory on the controller where logs are fetched                               |
| `container_fetched_logs_file`    | `logs.txt`                                           | Fetched log file name                                                            |
| `container_remote_logs_dir`      | `{{ remote_node_dir }}/logs`                         | Logs directory on the remote node                                                |
| `container_remote_logs_file`     | `logs.txt`                                           | Log file name on the remote node                                                 |
| `container_debug`                | `$DEBUG` or `false`                                  | Enable debug mode                                                                |
| `container_log_driver`           | `json-file`                                          | Container log driver                                                             |
| `container_log_max_size`         | `1g`                                                 | Maximum log file size                                                            |
| `container_log_lines`            | `0`                                                  | Number of log lines to tail (0 = all)                                            |
| `container_on_mac`               | derived                                              | Whether the host is running macOS                                                |
| `container_network_mode`         | `host` (Linux) or `bridge` (macOS)                   | Container network mode                                                           |
| `container_network_driver`       | `bridge`                                             | Network driver                                                                   |
| `container_network_attachable`   | `true`                                               | Make the network attachable (docker-only; podman networks are always attachable) |
| `container_network_internal`     | `false`                                              | Create an internal (isolated) network                                            |
| `container_hostname`             | `{{ container_name }}` or `{{ inventory_hostname }}` | Container hostname                                                               |
| `container_run_until`            | `null`                                               | Ansible `until` condition to retry the run                                       |
| `container_run_delay`            | `0`                                                  | Delay in seconds between retries                                                 |
| `container_run_retries`          | `0`                                                  | Number of retries                                                                |
| `container_wait_until_running`   | `false`                                              | Wait for the container to be running after start                                 |
| `container_wait_delay`           | `1`                                                  | Delay in seconds between wait checks                                             |
| `container_wait_timeout`         | `60`                                                 | Timeout in seconds for the wait                                                  |

## Tasks

### registry/login

The task `registry/login` allows to login a container engine within a certain Container Registry:

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

### network/create

The task `network/create` allows to create a container network:

```yaml
- name: Create the container network "fabric-x"
  vars:
    container_network: fabric-x
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: network/create
```

### network/rm

The task `network/rm` removes a container network:

```yaml
- name: Remove the container network "fabric-x"
  vars:
    container_network: fabric-x
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: network/rm
```

### volume/create

The task `volume/create` creates a container volume with the necessary permissions. It is useful when the container engine runs as `rootless` and cannot create volumes with specific `uid:gid`:

```yaml
- name: Create Postgres DB data volume
  vars:
    container_volume_path: /tmp/data
    container_volume_mode: "0o750"
    container_volume_uid: "999" # a rootless user could not create normally a folder with uid=999, but this task allows to create anyway
    container_volume_gid: "999" # a rootless user could not create normally a folder with uid=999, but this task allows to create anyway
    container_volume_type: directory
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/create
```

### volume/rm

The task `volume/rm` removes a container volume. It is useful when the container volumes has been created with special permissions and a `rootless` user could not normally delete it (incurring in `Permission Denied`):

```yaml
- name: Delete Postgres DB data volume
  vars:
    container_volume_path: /tmp/data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/rm
```

### install

The task `install` allows to install either `podman` or `docker` on the machine.

**NOTE**: only Linux is currently supported, and most specifically only RHEL/Fedora and Ubuntu distributions.

```yaml
- name: Install the container engine
  vars:
    container_client: "podman" # or docker
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: install
```

In case no `container_client` is indicated, the task installs `podman` by default.

### get_container_client

The task `get_container_client` returns the container client to use to handle the containers. It automatically detects which client is installed on the machine and sets the `container_client` fact accordingly.

```yaml
- name: Get the container client
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: get_container_client
```

### start

The task `start` command allows to start a container given a specific image. The [task](./tasks/start.yaml) comes with multiple options to fine-tune how to run the container.

```yaml
- name: Start the container named "my-container" with the "docker.io/library/busybox" image
  vars:
    container_name: my-container
    container_image: docker.io/library/busybox
    container_command: echo "Hello World"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: start
```

### stop

The task `stop` allows to stop a container given its name.

```yaml
- name: Stop the container named  "my-container"
  vars:
    container_name: my-container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: stop
```

### rm

The task `rm` allows to remove a container given its image.

```yaml
- name: Stop the container named "my-container"
  vars:
    container_name: my-container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: rm
```

### exec

The task `exec` allows to run a command within the chosen container.

```yaml
- name: Exec a command in my-container
  vars:
    container_name: my-container
    container_command: echo "Hello World"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: exec
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs of a container on the control node.

```yaml
- name: Fetch the logs from my-container container
  vars:
    container_name: my-container
    container_fetched_logs_dir: /tmp
    container_fetched_logs_file: my-container_logs.txt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: fetch_logs
```
