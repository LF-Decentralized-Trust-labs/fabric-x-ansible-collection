# hyperledger.fabricx.container

> Shared Docker and Podman lifecycle helpers for installing runtimes, managing containers, networks, registry logins, host-path volumes, and collected logs.

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

> Install a supported container client

Verifies the requested container runtime or auto-detects a host runtime, preferring Podman and then Docker.Installs the selected runtime on supported Linux hosts when it is missing and verifies that the client can run containers.

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

> Detect the available container client

Selects the container runtime used by generic lifecycle tasks.Uses `container_client` when provided, otherwise probes the host for Podman first and Docker second.

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

> Start a container with the selected client

Starts or updates a container through the selected Docker or Podman backend.Accepts image, command, environment, ports, volumes, network, resource limits, logging, retry, healthcheck, and readiness inputs.Stores runtime module output in `container_output` and can print captured process output when debug mode is enabled for foreground containers.

```yaml
- name: Start a container with the selected client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Selects the container image to start. Example: `ghcr.io/hyperledger/fabric-x/orderer:latest`.
    container_image: "ghcr.io/hyperledger/fabric-x/orderer:latest"
    # Overrides the image entrypoint. Example: `['/bin/sh', '-c']`.
    container_entrypoint: ['/bin/sh', '-c']
    # Supplies the command passed to the container runtime. Example: `orderer --config /etc/fabricx/orderer.yaml`.
    container_command: orderer --config /etc/fabricx/orderer.yaml
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
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
    # Publishes container ports when bridge networking is used. Example: `[7050:7050, 9443:9443]`.
    container_ports:[7050:7050, 9443:9443]
    # Limits container memory using runtime syntax such as `2g`. Example: `2g`.
    container_memory: "2g"
    # Limits CPU allocation for the container. Example: `2.0`.
    container_cpus: "2.0"
    # Mounts host paths or named volumes into the container. Example: `['/opt/fabricx/orderer/config:/etc/fabricx:ro']`.
    container_volumes:
      - /opt/fabricx/orderer/config:/etc/fabricx:ro
    # Applies runtime ulimit settings to the container. Example: `['nofile=65536:65536']`.
    container_ulimits:
      - nofile=65536:65536
    # Defines environment variables passed to the container process. Example: `{'FABRIC_LOGGING_SPEC': 'INFO', 'ORDERER_GENERAL_LISTENPORT': '7050'}`.
    container_env:
      FABRIC_LOGGING_SPEC: 'INFO'
      ORDERER_GENERAL_LISTENPORT: '7050'
    # Selects the runtime log driver.
    container_log_driver: json-file
    # Sets the maximum log file size.
    container_log_max_size: 1g
    # Limits the number of log lines shown in debug output.
    container_log_lines: 0
    # Enables debug output.
    container_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Defines the container healthcheck command. Example: `['CMD', 'curl', '-f', 'http://localhost:9443/healthz']`.
    container_healthcheck_test: ['CMD', 'curl', '-f', 'http://localhost:9443/healthz']
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
    # Provides the host used by readiness checks when `container_wait_until_running` is true. Example: `orderer-assembler-1.example.com`.
    actual_host: "orderer-assembler-1.example.com"
    # Provides the port probed by readiness checks. Example: `7050`.
    container_wait_port: 7050
    # Delays readiness checks after container start.
    container_wait_delay: 1
    # Sets the readiness check timeout.
    container_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: start
```

### stop

> Stop a container with the selected client

Stops the named container through the selected Docker or Podman backend.Uses `container_name` as the lifecycle target and resolves `container_client` before dispatching.

```yaml
- name: Stop a container with the selected client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: stop
```

### rm

> Remove a container with the selected client

Removes the named container through the selected Docker or Podman backend.Uses `container_name` as the lifecycle target and removes associated container volumes where the backend supports it.

```yaml
- name: Remove a container with the selected client
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: rm
```

### exec

> Execute a command in a container

Runs `container_command` inside an existing container through the selected Docker or Podman backend.Passes `container_env` to the command when provided and registers the backend execution result.

```yaml
- name: Execute a command in a container
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Supplies the command passed to the container runtime. Example: `orderer --config /etc/fabricx/orderer.yaml`.
    container_command: orderer --config /etc/fabricx/orderer.yaml
    # Defines environment variables passed to the container process. Example: `{'FABRIC_LOGGING_SPEC': 'INFO', 'ORDERER_GENERAL_LISTENPORT': '7050'}`.
    container_env:
      FABRIC_LOGGING_SPEC: 'INFO'
      ORDERER_GENERAL_LISTENPORT: '7050'
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: exec
```

### fetch_logs

> Fetch container logs from the remote host

Collects logs from the named container with the selected runtime client.Writes the log file under `container_remote_logs_dir` on the managed node, then fetches it to `container_fetched_logs_dir` on the control host.

```yaml
- name: Fetch container logs from the remote host
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Sets the remote directory used to stage collected container logs.
    container_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Sets the filename used for collected container logs.
    container_remote_logs_file: logs.txt
    # Sets the local destination for fetched container logs.
    container_fetched_logs_dir: "{{ fetched_artifacts_dir }}/{{ container_name }}"
    # Sets the filename used for fetched container logs.
    container_fetched_logs_file: logs.txt
    # Provides the base remote artifact directory for collected logs. Example: `/var/hyperledger/fabricx/orderer-assembler-1`.
    remote_node_dir: "/var/hyperledger/fabricx/orderer-assembler-1"
    # Provides the base local artifact directory for fetched logs. Example: `/tmp/fabricx/fetched-logs`.
    fetched_artifacts_dir: "/tmp/fabricx/fetched-logs"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: fetch_logs
```

### registry/login

> Log in to a container registry

Authenticates the selected Docker or Podman backend to `container_registry`.Uses the supplied username and password placeholders without changing registry credentials elsewhere.

```yaml
- name: Log in to a container registry
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container registry for login operations. Example: `ghcr.io`.
    container_registry: "ghcr.io"
    # Provides the registry username. Example: `iamapikey`.
    container_registry_username: "iamapikey"
    # Provides the registry password. Example: `{{ vault_container_registry_password }}`.
    container_registry_password: "{{ vault_container_registry_password }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: registry/login
```

### network/create

> Create a container network

Creates the named network through the selected Docker or Podman backend.Uses driver, attachable, and internal-network inputs where the selected runtime supports them.

```yaml
- name: Create a container network
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
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

> Remove a container network

Removes the named network through the selected Docker or Podman backend.Uses `container_network` as the lifecycle target after resolving `container_client`.

```yaml
- name: Remove a container network
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: network/rm
```

### volume/create

> Create a container volume

Creates or updates a host path used as a container volume through the selected Docker or Podman backend.Applies path state, mode, ownership, and optional recursive permission inputs, using runtime-specific helpers when rootless ownership changes are needed.

```yaml
- name: Create a container volume
  vars:
    # Selects the container client to verify or use. Leave it empty to auto-detect `podman` first and then `docker`.
    container_client: "{{ lookup('env', 'CONTAINER_CLIENT') or '' }}"
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
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
    # Names the file system path used for a container volume. Example: `/var/hyperledger/fabricx/orderer/data`.
    container_volume_path: "/var/hyperledger/fabricx/orderer/data"
    # Sets the file mode applied to a container volume path. Example: `0750`.
    container_volume_mode: "0750"
    # Selects the file system state for a container volume path. Example: `bind`.
    container_volume_type: "bind"
    # Provides the uid applied to a container volume path. Example: `1000`.
    container_volume_uid: 1000
    # Provides the gid applied to a container volume path. Example: `1000`.
    container_volume_gid: 1000
    # Applies recursive permission changes when set to `true`. Example: `true`.
    recurse: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/create
```

### volume/rm

> Remove a container volume

Removes the host path used as a container volume through the selected Docker or Podman backend.Uses `container_volume_path` as the lifecycle target after resolving `container_client`.

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
    # Names the file system path used for a container volume. Example: `/var/hyperledger/fabricx/orderer/data`.
    container_volume_path: "/var/hyperledger/fabricx/orderer/data"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: volume/rm
```

### docker/install

> Install Docker on the target host

Installs the Docker runtime on supported Linux hosts.Enables the Docker service and runs a hello-world container to verify that the client and daemon can launch containers.

```yaml
- name: Install Docker on the target host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/install
```

### docker/start

> Start a container with Docker

Starts or updates a Docker container with the requested image, command, environment, ports, volumes, network, resource limits, and log settings.Supports rootless Docker adjustments, optional healthcheck state, retry controls, port readiness checks, and foreground output capture in `container_output`.

```yaml
- name: Start a container with Docker
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Selects the container image to start. Example: `ghcr.io/hyperledger/fabric-x/orderer:latest`.
    container_image: "ghcr.io/hyperledger/fabric-x/orderer:latest"
    # Overrides the image entrypoint. Example: `['/bin/sh', '-c']`.
    container_entrypoint: ['/bin/sh', '-c']
    # Supplies the command passed to the container runtime. Example: `orderer --config /etc/fabricx/orderer.yaml`.
    container_command: orderer --config /etc/fabricx/orderer.yaml
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
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
    # Publishes container ports when bridge networking is used. Example: `[7050:7050, 9443:9443]`.
    container_ports:[7050:7050, 9443:9443]
    # Limits container memory using runtime syntax such as `2g`. Example: `2g`.
    container_memory: "2g"
    # Limits CPU allocation for the container. Example: `2.0`.
    container_cpus: "2.0"
    # Mounts host paths or named volumes into the container. Example: `['/opt/fabricx/orderer/config:/etc/fabricx:ro']`.
    container_volumes:
      - /opt/fabricx/orderer/config:/etc/fabricx:ro
    # Applies runtime ulimit settings to the container. Example: `['nofile=65536:65536']`.
    container_ulimits:
      - nofile=65536:65536
    # Defines environment variables passed to the container process. Example: `{'FABRIC_LOGGING_SPEC': 'INFO', 'ORDERER_GENERAL_LISTENPORT': '7050'}`.
    container_env:
      FABRIC_LOGGING_SPEC: 'INFO'
      ORDERER_GENERAL_LISTENPORT: '7050'
    # Selects the runtime log driver.
    container_log_driver: json-file
    # Sets the maximum log file size.
    container_log_max_size: 1g
    # Limits the number of log lines shown in debug output.
    container_log_lines: 0
    # Enables debug output.
    container_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Defines the container healthcheck command. Example: `['CMD', 'curl', '-f', 'http://localhost:9443/healthz']`.
    container_healthcheck_test: ['CMD', 'curl', '-f', 'http://localhost:9443/healthz']
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
    # Provides the host used by readiness checks when `container_wait_until_running` is true. Example: `orderer-assembler-1.example.com`.
    actual_host: "orderer-assembler-1.example.com"
    # Provides the port probed by readiness checks. Example: `7050`.
    container_wait_port: 7050
    # Delays readiness checks after container start.
    container_wait_delay: 1
    # Sets the readiness check timeout.
    container_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/start
```

### docker/stop

> Stop a container with Docker

Stops the named Docker container when it exists.Uses `container_name` as the lifecycle target.

```yaml
- name: Stop a container with Docker
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/stop
```

### docker/rm

> Remove a container with Docker

Removes the named Docker container and its attached anonymous volumes.Uses `container_name` as the lifecycle target.

```yaml
- name: Remove a container with Docker
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/rm
```

### docker/exec

> Execute a command in a Docker container

Runs `container_command` inside an existing Docker container.Passes `container_env` when provided and registers the Docker exec result.

```yaml
- name: Execute a command in a Docker container
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Supplies the command passed to the container runtime. Example: `orderer --config /etc/fabricx/orderer.yaml`.
    container_command: orderer --config /etc/fabricx/orderer.yaml
    # Defines environment variables passed to the container process. Example: `{'FABRIC_LOGGING_SPEC': 'INFO', 'ORDERER_GENERAL_LISTENPORT': '7050'}`.
    container_env:
      FABRIC_LOGGING_SPEC: 'INFO'
      ORDERER_GENERAL_LISTENPORT: '7050'
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/exec
```

### docker/registry/login

> Log in to a registry with Docker

Logs the Docker client in to `container_registry`.Uses the supplied username and password for image pull access.

```yaml
- name: Log in to a registry with Docker
  vars:
    # Names the container registry for login operations. Example: `ghcr.io`.
    container_registry: "ghcr.io"
    # Provides the registry username. Example: `iamapikey`.
    container_registry_username: "iamapikey"
    # Provides the registry password. Example: `{{ vault_container_registry_password }}`.
    container_registry_password: "{{ vault_container_registry_password }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/registry/login
```

### docker/network/create

> Create a Docker network

Creates the named Docker network with the requested driver, attachable flag, and internal flag.Provides the network artifact used by bridge-mode containers.

```yaml
- name: Create a Docker network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
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

> Remove a Docker network

Removes the named Docker network.Uses `container_network` as the lifecycle target.

```yaml
- name: Remove a Docker network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/network/rm
```

### docker/volume/create

> Create a Docker volume

Creates or updates a host path used as a Docker volume.Applies state, mode, ownership, and recursive permission inputs, using a short-lived helper container for rootless ownership or mode changes when needed.

```yaml
- name: Create a Docker volume
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Names the file system path used for a container volume. Example: `/var/hyperledger/fabricx/orderer/data`.
    container_volume_path: "/var/hyperledger/fabricx/orderer/data"
    # Sets the file mode applied to a container volume path. Example: `0750`.
    container_volume_mode: "0750"
    # Selects the file system state for a container volume path. Example: `bind`.
    container_volume_type: "bind"
    # Provides the uid applied to a container volume path. Example: `1000`.
    container_volume_uid: 1000
    # Provides the gid applied to a container volume path. Example: `1000`.
    container_volume_gid: 1000
    # Applies recursive permission changes when set to `true`. Example: `true`.
    recurse: true
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/volume/create
```

### docker/volume/rm

> Remove a Docker volume

Removes the host path used as a Docker volume.Uses `container_volume_path` as the lifecycle target.

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
    # Names the file system path used for a container volume. Example: `/var/hyperledger/fabricx/orderer/data`.
    container_volume_path: "/var/hyperledger/fabricx/orderer/data"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: docker/volume/rm
```

### podman/install

> Install Podman on the target host

Installs the Podman runtime on supported hosts.Verifies that the Podman client is available for subsequent container lifecycle tasks.

```yaml
- name: Install Podman on the target host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/install
```

### podman/start

> Start a container with Podman

Starts or updates a Podman container with the requested image, command, environment, ports, volumes, network, resource limits, and log settings.Supports keep-id user namespace handling, optional healthcheck polling, retry controls, port readiness checks, and foreground output capture in `container_output`.

```yaml
- name: Start a container with Podman
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Selects the container image to start. Example: `ghcr.io/hyperledger/fabric-x/orderer:latest`.
    container_image: "ghcr.io/hyperledger/fabric-x/orderer:latest"
    # Overrides the image entrypoint. Example: `['/bin/sh', '-c']`.
    container_entrypoint: ['/bin/sh', '-c']
    # Supplies the command passed to the container runtime. Example: `orderer --config /etc/fabricx/orderer.yaml`.
    container_command: orderer --config /etc/fabricx/orderer.yaml
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
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
    # Publishes container ports when bridge networking is used. Example: `[7050:7050, 9443:9443]`.
    container_ports:[7050:7050, 9443:9443]
    # Limits container memory using runtime syntax such as `2g`. Example: `2g`.
    container_memory: "2g"
    # Limits CPU allocation for the container. Example: `2.0`.
    container_cpus: "2.0"
    # Mounts host paths or named volumes into the container. Example: `['/opt/fabricx/orderer/config:/etc/fabricx:ro']`.
    container_volumes:
      - /opt/fabricx/orderer/config:/etc/fabricx:ro
    # Applies runtime ulimit settings to the container. Example: `['nofile=65536:65536']`.
    container_ulimits:
      - nofile=65536:65536
    # Defines environment variables passed to the container process. Example: `{'FABRIC_LOGGING_SPEC': 'INFO', 'ORDERER_GENERAL_LISTENPORT': '7050'}`.
    container_env:
      FABRIC_LOGGING_SPEC: 'INFO'
      ORDERER_GENERAL_LISTENPORT: '7050'
    # Selects the runtime log driver.
    container_log_driver: json-file
    # Sets the maximum log file size.
    container_log_max_size: 1g
    # Limits the number of log lines shown in debug output.
    container_log_lines: 0
    # Enables debug output.
    container_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Defines the container healthcheck command. Example: `['CMD', 'curl', '-f', 'http://localhost:9443/healthz']`.
    container_healthcheck_test: ['CMD', 'curl', '-f', 'http://localhost:9443/healthz']
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
    # Provides the host used by readiness checks when `container_wait_until_running` is true. Example: `orderer-assembler-1.example.com`.
    actual_host: "orderer-assembler-1.example.com"
    # Provides the port probed by readiness checks. Example: `7050`.
    container_wait_port: 7050
    # Delays readiness checks after container start.
    container_wait_delay: 1
    # Sets the readiness check timeout.
    container_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/start
```

### podman/stop

> Stop a container with Podman

Stops the named Podman container when it exists.Uses `container_name` as the lifecycle target.

```yaml
- name: Stop a container with Podman
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/stop
```

### podman/rm

> Remove a container with Podman

Removes the named Podman container and its attached anonymous volumes.Uses `container_name` as the lifecycle target.

```yaml
- name: Remove a container with Podman
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/rm
```

### podman/exec

> Execute a command in a Podman container

Runs `container_command` inside an existing Podman container.Passes `container_env` when provided and registers the Podman exec result.

```yaml
- name: Execute a command in a Podman container
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Supplies the command passed to the container runtime. Example: `orderer --config /etc/fabricx/orderer.yaml`.
    container_command: orderer --config /etc/fabricx/orderer.yaml
    # Defines environment variables passed to the container process. Example: `{'FABRIC_LOGGING_SPEC': 'INFO', 'ORDERER_GENERAL_LISTENPORT': '7050'}`.
    container_env:
      FABRIC_LOGGING_SPEC: 'INFO'
      ORDERER_GENERAL_LISTENPORT: '7050'
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/exec
```

### podman/registry/login

> Log in to a registry with Podman

Logs the Podman client in to `container_registry`.Uses the supplied username and password for image pull access.

```yaml
- name: Log in to a registry with Podman
  vars:
    # Names the container registry for login operations. Example: `ghcr.io`.
    container_registry: "ghcr.io"
    # Provides the registry username. Example: `iamapikey`.
    container_registry_username: "iamapikey"
    # Provides the registry password. Example: `{{ vault_container_registry_password }}`.
    container_registry_password: "{{ vault_container_registry_password }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/registry/login
```

### podman/network/create

> Create a Podman network

Creates the named Podman network with the requested driver and internal flag.Provides the network artifact used by bridge-mode containers.

```yaml
- name: Create a Podman network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
    # Selects the network driver used when creating a container network.
    container_network_driver: bridge
    # Marks the container network as internal when set to `true`.
    container_network_internal: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/network/create
```

### podman/network/rm

> Remove a Podman network

Removes the named Podman network.Uses `container_network` as the lifecycle target.

```yaml
- name: Remove a Podman network
  vars:
    # Names the bridge network attached to the container when bridge mode is selected. Example: `fabricx-net`.
    container_network: "fabricx-net"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/network/rm
```

### podman/volume/create

> Create a Podman volume

Creates or updates a host path used as a Podman volume.Applies state, mode, ownership, and recursive permission inputs, using `podman unshare` for rootless ownership or mode changes when needed.

```yaml
- name: Create a Podman volume
  vars:
    # Names the container managed by the role. Example: `fabricx-orderer-assembler-1`.
    container_name: "fabricx-orderer-assembler-1"
    # Provides the host uid used to build `container_host_user`.
    container_host_uid: "{{ ansible_facts.user_uid }}"
    # Provides the host gid used to build `container_host_user`.
    container_host_gid: "{{ ansible_facts.user_gid }}"
    # Builds the host uid:gid pair used for rootless container execution.
    container_host_user: "{{ container_host_uid }}:{{ container_host_gid }}"
    # Reports whether `container_host_user` resolves to `0:0`.
    container_host_user_is_root: "{{ container_host_user == '0:0' }}"
    # Names the file system path used for a container volume. Example: `/var/hyperledger/fabricx/orderer/data`.
    container_volume_path: "/var/hyperledger/fabricx/orderer/data"
    # Sets the file mode applied to a container volume path. Example: `0750`.
    container_volume_mode: "0750"
    # Selects the file system state for a container volume path. Example: `bind`.
    container_volume_type: "bind"
    # Provides the uid applied to a container volume path. Example: `1000`.
    container_volume_uid: 1000
    # Provides the gid applied to a container volume path. Example: `1000`.
    container_volume_gid: 1000
    # Applies recursive permission changes when set to `true`. Example: `true`.
    recurse: true
    # Marks whether the target host is macOS.
    container_on_mac: "{{ ansible_facts.os_family == 'Darwin' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/volume/create
```

### podman/volume/rm

> Remove a Podman volume

Removes the host path used as a Podman volume.Uses `container_volume_path` as the lifecycle target.

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
    # Names the file system path used for a container volume. Example: `/var/hyperledger/fabricx/orderer/data`.
    container_volume_path: "/var/hyperledger/fabricx/orderer/data"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.container
    tasks_from: podman/volume/rm
```
