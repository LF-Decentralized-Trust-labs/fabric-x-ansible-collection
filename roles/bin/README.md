# hyperledger.fabricx.bin

> Handles binary build, installation, and lifecycle management on target nodes.

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

Build a Go binary for each target platform

Clones the source repository, groups target hosts by platform, and builds one binary per unique operating system and architecture combination.

This entry point validates only variables owned by the bin role and does not redeclare git or go role inputs passed through internal includes.

```yaml
- name: Build a Go binary for each target platform
  vars:
    # Sets the base directory on the control node used to derive `bin_control_source_code_dir` and `bin_control_dir`. Required when relying on the defaults of those options and `bin_build_on_control_node` is true.
    control_node_dir: "string"
    # Sets the base directory on the managed host used to derive `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Required when relying on the defaults of those options.
    remote_node_dir: "string"
    # Controls whether source code is cloned and binaries are built on the control node instead of on the managed host.
    bin_build_on_control_node: false
    # Sets the target operating system used when deriving platform-specific build output paths. The default derives from `ansible_facts.system`.
    bin_target_os: "{{ ansible_facts.system }}"
    # Sets the target CPU architecture used when deriving platform-specific build output paths. The default derives from `ansible_facts.architecture`.
    bin_target_arch: "{{ ansible_facts.architecture }}"
    # Sets the output binary name. Example: `sample-go`. The default derives from `inventory_hostname`.
    bin_name: "{{ inventory_hostname }}"
    # Defines the source code directory on the control node when builds run locally. The default derives from `control_node_dir`.
    bin_control_source_code_dir: "{{ control_node_dir }}/code"
    # Defines the platform-specific output directory on the control node for built or installed binaries. The default derives from `control_node_dir`, `bin_target_os`, and `bin_target_arch`.
    bin_control_dir: "{{ control_node_dir }}/bin/{{ bin_target_os }}/{{ bin_target_arch }}"
    # Defines the source code directory used when invoking the go build role after cloning. The default derives from `bin_control_source_code_dir`, `bin_build_on_control_node`, and `bin_remote_source_code_dir`.
    bin_source_code_dir: "{{ bin_control_source_code_dir if bin_build_on_control_node else bin_remote_source_code_dir }}"
    # Defines the source code directory on the managed host when builds do not run on the control node. The default derives from `remote_node_dir`.
    bin_remote_source_code_dir: "{{ remote_node_dir }}/code"
    # Sets the directory where built binaries are written for each target platform. The default derives from `bin_control_dir`, `bin_build_on_control_node`, and `bin_remote_dir`.
    bin_dir: "{{ bin_control_dir if bin_build_on_control_node else bin_remote_dir }}"
    # Lists the hosts whose facts are used to determine the operating system and architecture combinations that must be built. The default derives from `inventory_hostname`.
    bin_hosts: ['{{ inventory_hostname }}']
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/build
```

### go/install

Install a Go binary for each target platform

Groups target hosts by platform and invokes the go install entry point once per unique operating system and architecture combination.

This entry point validates only bin role inputs and does not redeclare go role variables forwarded internally.

```yaml
- name: Install a Go binary for each target platform
  vars:
    # Sets the base directory on the control node used to derive `bin_control_source_code_dir` and `bin_control_dir`. Required when relying on the defaults of those options and `bin_build_on_control_node` is true.
    control_node_dir: "string"
    # Sets the base directory on the managed host used to derive `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Required when relying on the defaults of those options.
    remote_node_dir: "string"
    # Controls whether source code is cloned and binaries are built on the control node instead of on the managed host.
    bin_build_on_control_node: false
    # Sets the target operating system used when deriving platform-specific build output paths. The default derives from `ansible_facts.system`.
    bin_target_os: "{{ ansible_facts.system }}"
    # Sets the target CPU architecture used when deriving platform-specific build output paths. The default derives from `ansible_facts.architecture`.
    bin_target_arch: "{{ ansible_facts.architecture }}"
    # Defines the platform-specific output directory on the control node for built or installed binaries. The default derives from `control_node_dir`, `bin_target_os`, and `bin_target_arch`.
    bin_control_dir: "{{ control_node_dir }}/bin/{{ bin_target_os }}/{{ bin_target_arch }}"
    # Sets the directory where built binaries are written for each target platform. The default derives from `bin_control_dir`, `bin_build_on_control_node`, and `bin_remote_dir`.
    bin_dir: "{{ bin_control_dir if bin_build_on_control_node else bin_remote_dir }}"
    # Lists the hosts whose facts are used to determine the operating system and architecture combinations that must be built. The default derives from `inventory_hostname`.
    bin_hosts: ['{{ inventory_hostname }}']
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/install
```

### map_platform_to_host

Map hosts to unique platform keys

Builds the `bin_platforms` fact by grouping target hosts that share the same operating system and architecture values.

Host facts for each listed host must already be available before this entry point runs.

```yaml
- name: Map hosts to unique platform keys
  vars:
    # Lists the hosts whose facts are used to determine the operating system and architecture combinations that must be built. The default derives from `inventory_hostname`.
    bin_hosts: ['{{ inventory_hostname }}']
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: map_platform_to_host
```

### transfer

Copy a binary to the managed host

Ensures the target binary directory exists on the managed host and copies the selected binary into it.

The source binary must already exist at the resolved local or control-node path before this entry point runs.

```yaml
- name: Copy a binary to the managed host
  vars:
    # Sets the base directory on the control node used to derive `bin_control_source_code_dir` and `bin_control_dir`. Required when relying on the defaults of those options and `bin_build_on_control_node` is true.
    control_node_dir: "string"
    # Sets the base directory on the managed host used to derive `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Required when relying on the defaults of those options.
    remote_node_dir: "string"
    # Controls whether source code is cloned and binaries are built on the control node instead of on the managed host.
    bin_build_on_control_node: false
    # Sets the target operating system used when deriving platform-specific build output paths. The default derives from `ansible_facts.system`.
    bin_target_os: "{{ ansible_facts.system }}"
    # Sets the target CPU architecture used when deriving platform-specific build output paths. The default derives from `ansible_facts.architecture`.
    bin_target_arch: "{{ ansible_facts.architecture }}"
    # Defines the platform-specific output directory on the control node for built or installed binaries. The default derives from `control_node_dir`, `bin_target_os`, and `bin_target_arch`.
    bin_control_dir: "{{ control_node_dir }}/bin/{{ bin_target_os }}/{{ bin_target_arch }}"
    # Sets the output binary name. Example: `sample-go`. The default derives from `inventory_hostname`.
    bin_name: "{{ inventory_hostname }}"
    # Sets the directory where built binaries are written for each target platform. The default derives from `bin_control_dir`, `bin_build_on_control_node`, and `bin_remote_dir`.
    bin_dir: "{{ bin_control_dir if bin_build_on_control_node else bin_remote_dir }}"
    # Sets the directory that is prefixed to `bin_command` when constructing the executable path. The default derives from `remote_node_dir`.
    bin_remote_dir: "{{ remote_node_dir }}/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: transfer
```

### start

Start a binary process

Builds the runtime command, optionally redirects logs, and starts the binary either in tmux or directly in the shell.

Set `bin_command` to the executable command to run. Set `bin_wait_port` only when `bin_wait_until_running` is true.

```yaml
- name: Start a binary process
  vars:
    # Sets the base directory on the managed host used to derive `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Required when relying on the defaults of those options.
    remote_node_dir: "string"
    # Defines the command to execute, relative to `bin_remote_dir` when that directory is set. Example: `myservice --config /etc/myservice/config.yaml`.
    bin_command: "string"
    # Provides environment variables prefixed onto the command line before the binary is started.
    bin_env: {}
    # Sets the directory that is prefixed to `bin_command` when constructing the executable path. The default derives from `remote_node_dir`.
    bin_remote_dir: "{{ remote_node_dir }}/bin"
    # Controls whether stdout and stderr are redirected to a log file on the managed host.
    bin_collect_logs: true
    # Sets the directory used for redirected log output when `bin_collect_logs` is enabled. The default derives from `remote_node_dir`.
    bin_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Sets the log file name used when `bin_collect_logs` is enabled.
    bin_remote_logs_file: logs.txt
    # Controls whether the assembled command and direct-run output are printed for debugging. The default derives from the `DEBUG` environment variable.
    bin_debug: "{{ lookup('env', 'DEBUG') | bool | default(false) }}"
    # Controls whether the binary is started in a tmux session instead of through a direct shell invocation.
    bin_run_with_tmux: true
    # Sets the output binary name. Example: `sample-go`. The default derives from `inventory_hostname`.
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
    bin_wait_port: 1000
    # Sets the initial delay in seconds before checking `bin_wait_port`.
    bin_wait_delay: 1
    # Sets the maximum wait time in seconds for `bin_wait_port` to become reachable.
    bin_wait_timeout: 60
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: start
```

### stop

Stop a tmux-managed binary process

Stops the tmux session associated with the binary when tmux-based execution is enabled.

When tmux execution is disabled this entry point performs no action.

```yaml
- name: Stop a tmux-managed binary process
  vars:
    # Sets the output binary name. Example: `sample-go`. The default derives from `inventory_hostname`.
    bin_name: "{{ inventory_hostname }}"
    # Controls whether the binary is started in a tmux session instead of through a direct shell invocation.
    bin_run_with_tmux: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: stop
```

### rm

Remove a binary from the managed host

Deletes the binary file from the managed host.

```yaml
- name: Remove a binary from the managed host
  vars:
    # Sets the directory that is prefixed to `bin_command` when constructing the executable path. The default derives from `remote_node_dir`.
    bin_remote_dir: "{{ remote_node_dir }}/bin"
    # Sets the output binary name. Example: `sample-go`. The default derives from `inventory_hostname`.
    bin_name: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: rm
```

### fetch_logs

Fetch binary log output

Copies the binary log file from the managed host to the control node without failing when the file is absent.

```yaml
- name: Fetch binary log output
  vars:
    # Sets the local directory used to derive `bin_fetched_logs_dir`. Required when relying on the default of that option.
    fetched_artifacts_dir: "string"
    # Sets the base directory on the managed host used to derive `bin_remote_source_code_dir`, `bin_remote_dir`, and `bin_remote_logs_dir`. Required when relying on the defaults of those options.
    remote_node_dir: "string"
    # Sets the output binary name. Example: `sample-go`. The default derives from `inventory_hostname`.
    bin_name: "{{ inventory_hostname }}"
    # Sets the directory used for redirected log output when `bin_collect_logs` is enabled. The default derives from `remote_node_dir`.
    bin_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Sets the log file name used when `bin_collect_logs` is enabled.
    bin_remote_logs_file: logs.txt
    # Sets the destination directory on the control node where the fetched log file is stored. The default derives from `fetched_artifacts_dir` and `bin_name`.
    bin_fetched_logs_dir: "{{ fetched_artifacts_dir }}/{{ bin_name }}"
    # Sets the destination file name used for the fetched log output.
    bin_fetched_logs_file: logs.txt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: fetch_logs
```
