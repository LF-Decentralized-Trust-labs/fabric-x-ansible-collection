# hyperledger.fabricx.container

> Handles container lifecycle management (supports `podman` and `docker`).

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [install](#install)
  - [get_container_client](#get_container_client)
  - [start](#start)
  - [stop](#stop)
  - [rm](#rm)
  - [exec](#exec)
  - [fetch_logs](#fetch_logs)
  - [registry/login](#registrylogin)
  - [network/create](#networkcreate)
  - [network/rm](#networkrm)
  - [volume/create](#volumecreate)
  - [volume/rm](#volumerm)
  - [docker/install](#dockerinstall)
  - [docker/start](#dockerstart)
  - [docker/stop](#dockerstop)
  - [docker/rm](#dockerrm)
  - [docker/exec](#dockerexec)
  - [docker/registry/login](#dockerregistrylogin)
  - [docker/network/create](#dockernetworkcreate)
  - [docker/network/rm](#dockernetworkrm)
  - [docker/volume/create](#dockervolumecreate)
  - [docker/volume/rm](#dockervolumerm)
  - [podman/install](#podmaninstall)
  - [podman/start](#podmanstart)
  - [podman/stop](#podmanstop)
  - [podman/rm](#podmanrm)
  - [podman/exec](#podmanexec)
  - [podman/registry/login](#podmanregistrylogin)
  - [podman/network/create](#podmannetworkcreate)
  - [podman/network/rm](#podmannetworkrm)
  - [podman/volume/create](#podmanvolumecreate)
  - [podman/volume/rm](#podmanvolumerm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.container
```

## Tasks

### install

Install a supported container client

Detects an available container client and installs Docker or Podman on Linux when needed.

```yaml
- name: Install a supported container client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: install
```

### get_container_client

Detect the available container client

Chooses the requested container client or auto-detects one from the current host.

```yaml
- name: Detect the available container client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: get_container_client
```

### start

Start a container with the selected client

Logs the command in debug mode, resolves the container client, and delegates startup to the matching backend task file.

```yaml
- name: Start a container with the selected client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role.
    container_name: "string"
    # Selects the container image to start.
    container_image: "string"
    # Overrides the image entrypoint.
    container_entrypoint: "string"
    # Supplies the command passed to the container runtime.
    container_command: "string"
    # Sets the hostname inside the container.
    container_hostname: "{{ container_name | default(inventory_hostname) }}"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Runs the container as the detected host user when set to `true`.
    container_run_as_host_user: false
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
    # Controls the container network mode.
    container_network_mode: "{{ 'bridge' if (container_on_mac or (container_network is defined)) else 'host' }}"
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
    # Publishes container ports when bridge networking is used.
    container_ports: ["entry1", "entry2"]
    # Limits container memory using runtime syntax such as `2g`.
    container_memory: "string"
    # Limits CPU allocation for the container.
    container_cpus: "string"
    # Mounts host paths or named volumes into the container.
    container_volumes: ["entry1", "entry2"]
    # Applies runtime ulimit settings to the container.
    container_ulimits: ["entry1", "entry2"]
    # Defines environment variables passed to the container process.
    container_env: {}
    # Selects the runtime log driver.
    container_log_driver: json-file
    # Sets the maximum log file size.
    container_log_max_size: 1g
    # Limits the number of log lines shown in debug output.
    container_log_lines: 0
    # Enables debug output.
    container_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Defines the container healthcheck command.
    container_healthcheck_test: "string"
    # Sets the interval between healthcheck runs.
    container_healthcheck_interval: 30s
    # Removes the container automatically when it exits.
    container_autoremove: false
    # Ignores runtime errors from container start operations.
    container_ignore_errors: false
    # Runs the container in detached mode when set to `true`.
    container_run_detach_mode: true
    # Provides an optional until condition for container start retries.
    container_run_until: "string"
    # Sets the delay between container start retries.
    container_run_delay: 0
    # Sets the number of container start retries.
    container_run_retries: 0
    # Waits for readiness checks after container start when set to `true`.
    container_wait_until_running: false
    # Provides the host used by readiness checks when `container_wait_until_running` is true.
    actual_host: "string"
    # Provides the port probed by readiness checks.
    container_wait_port: 1000
    # Delays readiness checks after container start.
    container_wait_delay: 1
    # Sets the readiness check timeout.
    container_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: start
```

### stop

Stop a container with the selected client

Resolves the active container client and delegates container shutdown to the matching backend task file.

```yaml
- name: Stop a container with the selected client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role.
    container_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: stop
```

### rm

Remove a container with the selected client

Resolves the active container client and delegates container removal to the matching backend task file.

```yaml
- name: Remove a container with the selected client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role.
    container_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: rm
```

### exec

Execute a command in a container

Resolves the active container client and delegates command execution to the matching backend task file.

```yaml
- name: Execute a command in a container
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role.
    container_name: "string"
    # Supplies the command passed to the container runtime.
    container_command: "string"
    # Defines environment variables passed to the container process.
    container_env: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: exec
```

### fetch_logs

Fetch container logs from the remote host

Resolves the active container client, writes logs on the remote node, and fetches them to the control host.

```yaml
- name: Fetch container logs from the remote host
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role.
    container_name: "string"
    # Sets the remote directory used to stage collected container logs.
    container_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Sets the filename used for collected container logs.
    container_remote_logs_file: logs.txt
    # Sets the local destination for fetched container logs.
    container_fetched_logs_dir: "{{ fetched_artifacts_dir }}/{{ container_name }}"
    # Sets the filename used for fetched container logs.
    container_fetched_logs_file: logs.txt
    # Provides the base remote artifact directory for collected logs.
    remote_node_dir: "string"
    # Provides the base local artifact directory for fetched logs.
    fetched_artifacts_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: fetch_logs
```

### registry/login

Log in to a container registry

Resolves the active container client and delegates registry login to the matching backend task file.

```yaml
- name: Log in to a container registry
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container registry for login operations.
    container_registry: "string"
    # Provides the registry username.
    container_registry_username: "string"
    # Provides the registry password.
    container_registry_password: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: registry/login
```

### network/create

Create a container network

Resolves the active container client and delegates network creation to the matching backend task file.

```yaml
- name: Create a container network
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
    # Selects the network driver used when creating a container network.
    container_network_driver: bridge
    # Marks Docker networks as attachable. Podman networks are always attachable.
    container_network_attachable: true
    # Marks the container network as internal when set to `true`.
    container_network_internal: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: network/create
```

### network/rm

Remove a container network

Resolves the active container client and delegates network removal to the matching backend task file.

```yaml
- name: Remove a container network
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: network/rm
```

### volume/create

Create a container volume

Resolves the active container client and delegates volume creation to the matching backend task file.

```yaml
- name: Create a container volume
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role.
    container_name: "string"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
    # Names the file system path used for a container volume.
    container_volume_path: "string"
    # Sets the file mode applied to a container volume path.
    container_volume_mode: "string"
    # Selects the file system state for a container volume path.
    container_volume_type: "string"
    # Provides the uid applied to a container volume path.
    container_volume_uid: "string"
    # Provides the gid applied to a container volume path.
    container_volume_gid: "string"
    # Applies recursive permission changes when set to `true`.
    recurse: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/create
```

### volume/rm

Remove a container volume

Resolves the active container client and delegates volume removal to the matching backend task file.

```yaml
- name: Remove a container volume
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
    # Names the file system path used for a container volume.
    container_volume_path: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/rm
```

### docker/install

Install Docker on the target host

Installs Docker on Linux, enables the service, and runs a hello-world container to verify the client.

```yaml
- name: Install Docker on the target host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/install
```

### docker/start

Start a container with Docker

Starts a Docker container with the requested runtime options and optionally waits for health or port readiness.

```yaml
- name: Start a container with Docker
  vars:
    # Names the container managed by the role.
    container_name: "string"
    # Selects the container image to start.
    container_image: "string"
    # Overrides the image entrypoint.
    container_entrypoint: "string"
    # Supplies the command passed to the container runtime.
    container_command: "string"
    # Sets the hostname inside the container.
    container_hostname: "{{ container_name | default(inventory_hostname) }}"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Runs the container as the detected host user when set to `true`.
    container_run_as_host_user: false
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
    # Controls the container network mode.
    container_network_mode: "{{ 'bridge' if (container_on_mac or (container_network is defined)) else 'host' }}"
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
    # Publishes container ports when bridge networking is used.
    container_ports: ["entry1", "entry2"]
    # Limits container memory using runtime syntax such as `2g`.
    container_memory: "string"
    # Limits CPU allocation for the container.
    container_cpus: "string"
    # Mounts host paths or named volumes into the container.
    container_volumes: ["entry1", "entry2"]
    # Applies runtime ulimit settings to the container.
    container_ulimits: ["entry1", "entry2"]
    # Defines environment variables passed to the container process.
    container_env: {}
    # Selects the runtime log driver.
    container_log_driver: json-file
    # Sets the maximum log file size.
    container_log_max_size: 1g
    # Limits the number of log lines shown in debug output.
    container_log_lines: 0
    # Enables debug output.
    container_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Defines the container healthcheck command.
    container_healthcheck_test: "string"
    # Sets the interval between healthcheck runs.
    container_healthcheck_interval: 30s
    # Removes the container automatically when it exits.
    container_autoremove: false
    # Ignores runtime errors from container start operations.
    container_ignore_errors: false
    # Runs the container in detached mode when set to `true`.
    container_run_detach_mode: true
    # Provides an optional until condition for container start retries.
    container_run_until: "string"
    # Sets the delay between container start retries.
    container_run_delay: 0
    # Sets the number of container start retries.
    container_run_retries: 0
    # Waits for readiness checks after container start when set to `true`.
    container_wait_until_running: false
    # Provides the host used by readiness checks when `container_wait_until_running` is true.
    actual_host: "string"
    # Provides the port probed by readiness checks.
    container_wait_port: 1000
    # Delays readiness checks after container start.
    container_wait_delay: 1
    # Sets the readiness check timeout.
    container_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/start
```

### docker/stop

Stop a container with Docker

Stops a Docker container when it exists.

```yaml
- name: Stop a container with Docker
  vars:
    # Names the container managed by the role.
    container_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/stop
```

### docker/rm

Remove a container with Docker

Removes a Docker container and its volumes.

```yaml
- name: Remove a container with Docker
  vars:
    # Names the container managed by the role.
    container_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/rm
```

### docker/exec

Execute a command in a Docker container

Runs a command inside a Docker container.

```yaml
- name: Execute a command in a Docker container
  vars:
    # Names the container managed by the role.
    container_name: "string"
    # Supplies the command passed to the container runtime.
    container_command: "string"
    # Defines environment variables passed to the container process.
    container_env: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/exec
```

### docker/registry/login

Log in to a registry with Docker

Logs Docker in to the requested container registry.

```yaml
- name: Log in to a registry with Docker
  vars:
    # Names the container registry for login operations.
    container_registry: "string"
    # Provides the registry username.
    container_registry_username: "string"
    # Provides the registry password.
    container_registry_password: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/registry/login
```

### docker/network/create

Create a Docker network

Creates a Docker network with the requested driver and flags.

```yaml
- name: Create a Docker network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
    # Selects the network driver used when creating a container network.
    container_network_driver: bridge
    # Marks Docker networks as attachable. Podman networks are always attachable.
    container_network_attachable: true
    # Marks the container network as internal when set to `true`.
    container_network_internal: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/network/create
```

### docker/network/rm

Remove a Docker network

Removes a Docker network.

```yaml
- name: Remove a Docker network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/network/rm
```

### docker/volume/create

Create a Docker volume

Creates a Docker volume and adjusts ownership when needed.

```yaml
- name: Create a Docker volume
  vars:
    # Names the container managed by the role.
    container_name: "string"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Names the file system path used for a container volume.
    container_volume_path: "string"
    # Sets the file mode applied to a container volume path.
    container_volume_mode: "string"
    # Selects the file system state for a container volume path.
    container_volume_type: "string"
    # Provides the uid applied to a container volume path.
    container_volume_uid: "string"
    # Provides the gid applied to a container volume path.
    container_volume_gid: "string"
    # Applies recursive permission changes when set to `true`.
    recurse: false
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/volume/create
```

### docker/volume/rm

Remove a Docker volume

Removes a Docker volume path.

```yaml
- name: Remove a Docker volume
  vars:
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
    # Names the file system path used for a container volume.
    container_volume_path: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/volume/rm
```

### podman/install

Install Podman on the target host

Installs Podman and verifies that the binary is available.

```yaml
- name: Install Podman on the target host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/install
```

### podman/start

Start a container with Podman

Starts a Podman container with the requested runtime options and optionally waits for health or port readiness.

```yaml
- name: Start a container with Podman
  vars:
    # Names the container managed by the role.
    container_name: "string"
    # Selects the container image to start.
    container_image: "string"
    # Overrides the image entrypoint.
    container_entrypoint: "string"
    # Supplies the command passed to the container runtime.
    container_command: "string"
    # Sets the hostname inside the container.
    container_hostname: "{{ container_name | default(inventory_hostname) }}"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Runs the container as the detected host user when set to `true`.
    container_run_as_host_user: false
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
    # Controls the container network mode.
    container_network_mode: "{{ 'bridge' if (container_on_mac or (container_network is defined)) else 'host' }}"
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
    # Publishes container ports when bridge networking is used.
    container_ports: ["entry1", "entry2"]
    # Limits container memory using runtime syntax such as `2g`.
    container_memory: "string"
    # Limits CPU allocation for the container.
    container_cpus: "string"
    # Mounts host paths or named volumes into the container.
    container_volumes: ["entry1", "entry2"]
    # Applies runtime ulimit settings to the container.
    container_ulimits: ["entry1", "entry2"]
    # Defines environment variables passed to the container process.
    container_env: {}
    # Selects the runtime log driver.
    container_log_driver: json-file
    # Sets the maximum log file size.
    container_log_max_size: 1g
    # Limits the number of log lines shown in debug output.
    container_log_lines: 0
    # Enables debug output.
    container_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Defines the container healthcheck command.
    container_healthcheck_test: "string"
    # Sets the interval between healthcheck runs.
    container_healthcheck_interval: 30s
    # Removes the container automatically when it exits.
    container_autoremove: false
    # Ignores runtime errors from container start operations.
    container_ignore_errors: false
    # Runs the container in detached mode when set to `true`.
    container_run_detach_mode: true
    # Provides an optional until condition for container start retries.
    container_run_until: "string"
    # Sets the delay between container start retries.
    container_run_delay: 0
    # Sets the number of container start retries.
    container_run_retries: 0
    # Waits for readiness checks after container start when set to `true`.
    container_wait_until_running: false
    # Provides the host used by readiness checks when `container_wait_until_running` is true.
    actual_host: "string"
    # Provides the port probed by readiness checks.
    container_wait_port: 1000
    # Delays readiness checks after container start.
    container_wait_delay: 1
    # Sets the readiness check timeout.
    container_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/start
```

### podman/stop

Stop a container with Podman

Stops a Podman container when it exists.

```yaml
- name: Stop a container with Podman
  vars:
    # Names the container managed by the role.
    container_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/stop
```

### podman/rm

Remove a container with Podman

Removes a Podman container and its volumes.

```yaml
- name: Remove a container with Podman
  vars:
    # Names the container managed by the role.
    container_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/rm
```

### podman/exec

Execute a command in a Podman container

Runs a command inside a Podman container.

```yaml
- name: Execute a command in a Podman container
  vars:
    # Names the container managed by the role.
    container_name: "string"
    # Supplies the command passed to the container runtime.
    container_command: "string"
    # Defines environment variables passed to the container process.
    container_env: {}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/exec
```

### podman/registry/login

Log in to a registry with Podman

Logs Podman in to the requested container registry.

```yaml
- name: Log in to a registry with Podman
  vars:
    # Names the container registry for login operations.
    container_registry: "string"
    # Provides the registry username.
    container_registry_username: "string"
    # Provides the registry password.
    container_registry_password: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/registry/login
```

### podman/network/create

Create a Podman network

Creates a Podman network with the requested driver.

```yaml
- name: Create a Podman network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
    # Selects the network driver used when creating a container network.
    container_network_driver: bridge
    # Marks the container network as internal when set to `true`.
    container_network_internal: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/network/create
```

### podman/network/rm

Remove a Podman network

Removes a Podman network.

```yaml
- name: Remove a Podman network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected.
    container_network: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/network/rm
```

### podman/volume/create

Create a Podman volume

Creates a Podman volume and adjusts ownership when needed.

```yaml
- name: Create a Podman volume
  vars:
    # Names the container managed by the role.
    container_name: "string"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Names the file system path used for a container volume.
    container_volume_path: "string"
    # Sets the file mode applied to a container volume path.
    container_volume_mode: "string"
    # Selects the file system state for a container volume path.
    container_volume_type: "string"
    # Provides the uid applied to a container volume path.
    container_volume_uid: "string"
    # Provides the gid applied to a container volume path.
    container_volume_gid: "string"
    # Applies recursive permission changes when set to `true`.
    recurse: false
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/volume/create
```

### podman/volume/rm

Remove a Podman volume

Removes a Podman volume path.

```yaml
- name: Remove a Podman volume
  vars:
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
    # Names the file system path used for a container volume.
    container_volume_path: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/volume/rm
```
