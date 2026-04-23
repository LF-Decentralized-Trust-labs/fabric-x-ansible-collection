# hyperledger.fabricx.bin

> Provides shared helpers for building, installing, transferring, starting, stopping, and collecting logs for Fabric-X binaries. The role supports both control-node and managed-host execution paths and groups hosts by platform before invoking the Go helpers.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [go/build](#gobuild)
  - [go/install](#goinstall)
  - [map_platform_to_host](#map_platform_to_host)
  - [transfer](#transfer)
  - [start](#start)
  - [stop](#stop)
  - [rm](#rm)
  - [fetch_logs](#fetch_logs)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.bin
```

## Tasks

### go/build

> Build a Go binary for each target platform

Clones the source repository, groups target hosts by platform, and builds one binary per unique operating system and architecture combination.When `bin_build_on_control_node` is true, cloning and compilation happen on the control node; otherwise they run on the managed host.The resulting binaries are written under `bin_dir` using `bin_name`, and this entry point only validates bin role inputs before delegating to the git and go roles.

```yaml
- name: Build a Go binary for each target platform
  vars:
    # Sets the base directory on the control node for `bin_control_source_code_dir` and `bin_control_dir`. Example: `/opt/fabricx/control`.
    control_node_dir: "/opt/fabricx/control"
    # Sets the base directory on the managed host for `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Example: `/var/lib/fabricx`.
    remote_node_dir: "/var/lib/fabricx"
    # Controls whether source code is cloned and binaries are built on the control node instead of on the managed host.
    bin_build_on_control_node: false
    # Sets the target operating system used when deriving platform-specific build output paths.
    bin_target_os: "{{ ansible_facts.system }}"
    # Sets the target CPU architecture used when deriving platform-specific build output paths.
    bin_target_arch: "{{ ansible_facts.architecture }}"
    # Sets the output binary name. Example: `sample-go`.
    bin_name: "{{ inventory_hostname }}"
    # Defines the source code directory on the control node when builds run locally.
    bin_control_source_code_dir: "{{ control_node_dir }}/code"
    # Defines the platform-specific output directory on the control node for built or installed binaries.
    bin_control_dir: "{{ control_node_dir }}/bin/{{ bin_target_os }}/{{ bin_target_arch }}"
    # Defines the source code directory used when invoking the go build role after cloning.
    bin_source_code_dir: "{{ bin_control_source_code_dir if bin_build_on_control_node else bin_remote_source_code_dir }}"
    # Defines the source code directory on the managed host when builds do not run on the control node.
    bin_remote_source_code_dir: "{{ remote_node_dir }}/code"
    # Sets the directory where built binaries are written for each target platform.
    bin_dir: "{{ bin_control_dir if bin_build_on_control_node else bin_remote_dir }}"
    # Lists the hosts whose facts are used to determine the operating system and architecture combinations that must be built.
    bin_hosts:
      - "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/build
```

### go/install

> Install a Go binary for each target platform

Groups target hosts by platform and invokes the go install entry point once per unique operating system and architecture combination.The installed binaries are placed under `bin_dir`, and the role reuses gathered host facts to avoid repeating work for hosts that share the same platform.This entry point validates only bin role inputs and forwards the platform-specific context to the go role.

```yaml
- name: Install a Go binary for each target platform
  vars:
    # Sets the base directory on the control node for `bin_control_source_code_dir` and `bin_control_dir`. Example: `/opt/fabricx/control`.
    control_node_dir: "/opt/fabricx/control"
    # Sets the base directory on the managed host for `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Example: `/var/lib/fabricx`.
    remote_node_dir: "/var/lib/fabricx"
    # Controls whether source code is cloned and binaries are built on the control node instead of on the managed host.
    bin_build_on_control_node: false
    # Sets the target operating system used when deriving platform-specific build output paths.
    bin_target_os: "{{ ansible_facts.system }}"
    # Sets the target CPU architecture used when deriving platform-specific build output paths.
    bin_target_arch: "{{ ansible_facts.architecture }}"
    # Defines the platform-specific output directory on the control node for built or installed binaries.
    bin_control_dir: "{{ control_node_dir }}/bin/{{ bin_target_os }}/{{ bin_target_arch }}"
    # Sets the directory where built binaries are written for each target platform.
    bin_dir: "{{ bin_control_dir if bin_build_on_control_node else bin_remote_dir }}"
    # Lists the hosts whose facts are used to determine the operating system and architecture combinations that must be built.
    bin_hosts:
      - "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/install
```

### map_platform_to_host

> Map hosts to unique platform keys

Builds the `bin_platforms` fact by grouping target hosts that share the same operating system and architecture values.The resulting fact maps each platform key to its OS, architecture, and host list, and host facts for every target must already be available before this entry point runs.

```yaml
- name: Map hosts to unique platform keys
  vars:
    # Lists the hosts whose facts are used to determine the operating system and architecture combinations that must be built.
    bin_hosts:
      - "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: map_platform_to_host
```

### transfer

> Copy a binary to the managed host

Ensures the target binary directory exists on the managed host and copies the selected binary into it.The source binary is read from `bin_dir`/`bin_name` and written to `bin_remote_dir`/`bin_name`, so the built artifact must already exist before this entry point runs.

```yaml
- name: Copy a binary to the managed host
  vars:
    # Sets the base directory on the control node for `bin_control_source_code_dir` and `bin_control_dir`. Example: `/opt/fabricx/control`.
    control_node_dir: "/opt/fabricx/control"
    # Sets the base directory on the managed host for `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Example: `/var/lib/fabricx`.
    remote_node_dir: "/var/lib/fabricx"
    # Controls whether source code is cloned and binaries are built on the control node instead of on the managed host.
    bin_build_on_control_node: false
    # Sets the target operating system used when deriving platform-specific build output paths.
    bin_target_os: "{{ ansible_facts.system }}"
    # Sets the target CPU architecture used when deriving platform-specific build output paths.
    bin_target_arch: "{{ ansible_facts.architecture }}"
    # Defines the platform-specific output directory on the control node for built or installed binaries.
    bin_control_dir: "{{ control_node_dir }}/bin/{{ bin_target_os }}/{{ bin_target_arch }}"
    # Sets the output binary name. Example: `sample-go`.
    bin_name: "{{ inventory_hostname }}"
    # Sets the directory where built binaries are written for each target platform.
    bin_dir: "{{ bin_control_dir if bin_build_on_control_node else bin_remote_dir }}"
    # Sets the directory that is prefixed to `bin_command` when constructing the executable path.
    bin_remote_dir: "{{ remote_node_dir }}/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: transfer
```

### start

> Start a binary process

Builds the runtime command, optionally redirects logs, and starts the binary either in tmux or directly in the shell.When logging is enabled the role writes to `bin_remote_logs_dir`/`bin_remote_logs_file`, and readiness checks wait on `bin_wait_port` only when `bin_wait_until_running` is true.Set `bin_command` to the executable command to run, and use `bin_chdir` when the process must start from a specific working directory.

```yaml
- name: Start a binary process
  vars:
    # Sets the base directory on the managed host for `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Example: `/var/lib/fabricx`.
    remote_node_dir: "/var/lib/fabricx"
    # Defines the command to execute, relative to `bin_remote_dir` when that directory is set. Example: `orderer --config /etc/fabricx/orderer.yaml`.
    bin_command: "orderer --config /etc/fabricx/orderer.yaml"
    # Provides environment variables prefixed onto the command line before the binary is started.
    bin_env: {}
    # Sets the directory that is prefixed to `bin_command` when constructing the executable path.
    bin_remote_dir: "{{ remote_node_dir }}/bin"
    # Controls whether stdout and stderr are redirected to a log file on the managed host.
    bin_collect_logs: true
    # Sets the directory used for redirected log output when `bin_collect_logs` is enabled.
    bin_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Sets the log file name used when `bin_collect_logs` is enabled.
    bin_remote_logs_file: logs.txt
    # Controls whether the assembled command and direct-run output are printed for debugging.
    bin_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Controls whether the binary is started in a tmux session instead of through a direct shell invocation.
    bin_run_with_tmux: true
    # Sets the output binary name. Example: `sample-go`.
    bin_name: "{{ inventory_hostname }}"
    # Sets the working directory used for tmux and direct shell execution when a specific directory is required.
    bin_chdir: "string"
    # Defines the until expression used for retrying direct shell execution when `bin_run_with_tmux` is false.
    bin_run_until: "string"
    # Sets how many times direct shell execution is retried when `bin_run_until` is defined.
    bin_run_retries: 0
    # Sets the delay in seconds between retries for direct shell execution.
    bin_run_delay: 0
    # Controls whether failures from direct shell execution are ignored when `bin_run_with_tmux` is false.
    bin_ignore_errors: false
    # Controls whether the role waits for a TCP port to become reachable after the process starts.
    bin_wait_until_running: false
    # Sets the TCP port checked by the wait step when `bin_wait_until_running` is true. Example: `7050`.
    bin_wait_port: 7050
    # Sets the initial delay in seconds before checking `bin_wait_port`.
    bin_wait_delay: 1
    # Sets the maximum wait time in seconds for `bin_wait_port` to become reachable.
    bin_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: start
```

### stop

> Stop a tmux-managed binary process

Stops the tmux session associated with the binary when tmux-based execution is enabled.When tmux execution is disabled this entry point performs no action, so direct-shell starts are left untouched.

```yaml
- name: Stop a tmux-managed binary process
  vars:
    # Sets the output binary name. Example: `sample-go`.
    bin_name: "{{ inventory_hostname }}"
    # Controls whether the binary is started in a tmux session instead of through a direct shell invocation.
    bin_run_with_tmux: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: stop
```

### rm

> Remove a binary from the managed host

Deletes the binary file from the managed host at `bin_remote_dir`/`bin_name`.

```yaml
- name: Remove a binary from the managed host
  vars:
    # Sets the directory that is prefixed to `bin_command` when constructing the executable path.
    bin_remote_dir: "{{ remote_node_dir }}/bin"
    # Sets the output binary name. Example: `sample-go`.
    bin_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: rm
```

### fetch_logs

> Fetch binary log output

Copies the binary log file from the managed host to the control node without failing when the file is absent.The fetched file is stored under `bin_fetched_logs_dir`/`bin_fetched_logs_file`, making it easy to collect logs from repeated runs.

```yaml
- name: Fetch binary log output
  vars:
    # Sets the local directory for `bin_fetched_logs_dir`. Example: `/tmp/fabricx/artifacts`.
    fetched_artifacts_dir: "/tmp/fabricx/artifacts"
    # Sets the base directory on the managed host for `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Example: `/var/lib/fabricx`.
    remote_node_dir: "/var/lib/fabricx"
    # Sets the output binary name. Example: `sample-go`.
    bin_name: "{{ inventory_hostname }}"
    # Sets the directory used for redirected log output when `bin_collect_logs` is enabled.
    bin_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Sets the log file name used when `bin_collect_logs` is enabled.
    bin_remote_logs_file: logs.txt
    # Sets the destination directory on the control node where the fetched log file is stored.
    bin_fetched_logs_dir: "{{ fetched_artifacts_dir }}/{{ bin_name }}"
    # Sets the destination file name used for the fetched log output.
    bin_fetched_logs_file: logs.txt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: fetch_logs
```
