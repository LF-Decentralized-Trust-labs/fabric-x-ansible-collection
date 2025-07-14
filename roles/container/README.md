# hyperledger.fabricx.container

The role `hyperledger.fabricx.container` can be used to handle a container on a target node. The role allows to run a container with either `podman` or `docker`.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [install](#install)
  - [get_container_client](#get_container_client)
  - [start](#start)
  - [stop](#stop)
  - [rm](#rm)
  - [exec](#exec)
  - [fetch_logs](#fetch_logs)

## Prerequisites

The role requires either `podman` or `docker` to be installed on the targeted node.

## Tasks

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
    container_logs_dir: /tmp
    container_logs_file: my-container_logs.txt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: fetch_logs
```
