# hyperledger.fabricx.bin

The role `hyperledger.fabricx.bin` can be used to handle a binary run on a target node.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [go](#go)
    - [build](#build)
    - [install](#install)
  - [map\_platform\_to\_host](#map_platform_to_host)
  - [transfer](#transfer)
  - [start](#start)
  - [stop](#stop)
  - [rm](#rm)
  - [fetch\_logs](#fetch_logs)

## Prerequisites

The role requires:

- `tmux` to run binaries in a tmux session;
- `go` to build/install binaries;
- `rsync` to transfer binaries from the control node to the target node.

## Variables

| Variable                      | Default                                                                | Description                                                                            |
| ----------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `bin_build_on_control_node`   | `false`                                                                | Build the binary on the control node instead of the remote node                        |
| `bin_target_os`               | `{{ ansible_facts.system }}`                                           | Target OS for cross-compilation                                                        |
| `bin_target_arch`             | `{{ ansible_facts.architecture }}`                                     | Target architecture for cross-compilation                                              |
| `bin_name`                    | `{{ inventory_hostname }}`                                             | Name of the binary                                                                     |
| `bin_control_source_code_dir` | `{{ control_node_dir }}/code`                                          | Source code directory on the control node                                              |
| `bin_control_dir`             | `{{ control_node_dir }}/bin/{{ bin_target_os }}/{{ bin_target_arch }}` | Binary output directory on the control node                                            |
| `bin_remote_source_code_dir`  | `{{ remote_node_dir }}/code`                                           | Source code directory on the remote node                                               |
| `bin_remote_dir`              | `{{ remote_node_dir }}/bin`                                            | Binary directory on the remote node                                                    |
| `bin_source_code_dir`         | auto-selected                                                          | Active source code directory (control or remote, based on `bin_build_on_control_node`) |
| `bin_dir`                     | auto-selected                                                          | Active binary directory (control or remote, based on `bin_build_on_control_node`)      |
| `bin_hosts`                   | `[inventory_hostname]`                                                 | List of hosts to build the binary for                                                  |
| `bin_remote_logs_dir`         | `{{ remote_node_dir }}/logs`                                           | Logs directory on the remote node                                                      |
| `bin_remote_logs_file`        | `logs.txt`                                                             | Log file name on the remote node                                                       |
| `bin_fetched_logs_dir`        | `{{ fetched_artifacts_dir }}/{{ bin_name }}`                           | Directory on the controller where logs are fetched                                     |
| `bin_fetched_logs_file`       | `logs.txt`                                                             | Fetched log file name                                                                  |
| `bin_collect_logs`            | `true`                                                                 | Whether to collect logs                                                                |
| `bin_debug`                   | `$DEBUG` or `false`                                                    | Enable debug mode                                                                      |
| `bin_env`                     | `{}`                                                                   | Extra environment variables passed to the binary                                       |
| `bin_run_with_tmux`           | `true`                                                                 | Run the binary inside a tmux session                                                   |
| `bin_chdir`                   | `null`                                                                 | Working directory for the binary                                                       |
| `bin_ignore_errors`           | `false`                                                                | Ignore errors when running the binary                                                  |
| `bin_run_until`               | `null`                                                                 | Ansible `until` condition to retry the run                                             |
| `bin_run_delay`               | `0`                                                                    | Delay in seconds between retries                                                       |
| `bin_run_retries`             | `0`                                                                    | Number of retries                                                                      |
| `bin_wait_until_running`      | `false`                                                                | Wait for the binary to be running after start                                          |
| `bin_wait_delay`              | `1`                                                                    | Delay in seconds between wait checks                                                   |
| `bin_wait_timeout`            | `60`                                                                   | Timeout in seconds for the wait                                                        |

## Tasks

### go

The tasks in the [`go`](./tasks/go) section are thin wrappers that orchestrate cloning, platform detection, and cross-compilation by delegating to the [`hyperledger.fabricx.go`](../go/README.md) role.

#### build

The task `build` clones the source code of a `go` binary, detects the target platform for each host in `bin_hosts`, and builds a cross-compiled binary for each unique platform via `hyperledger.fabricx.go`:

```yaml
- name: Build the sample-go binary
  vars:
    # Git vars
    git_hub_url: github.com
    git_repo: "sample/sample-go"
    git_commit: "v1.0.0"
    # Bin vars
    bin_name: sample-go
    bin_hosts: "{{ groups['orderers'] }}"
    bin_source_code_dir: /tmp/sample-go/src
    bin_dir: /usr/local/bin
    # Go vars
    go_source_code_package: "cmd/sample-go"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/build
```

**Note**: The `git_hub_url` and `git_repo` are separated to allow the git role to internally handle URL construction with either HTTPS or SSH protocols. The `git_repo` should not include the domain (e.g., `sample/sample-go` instead of `github.com/sample/sample-go`).

#### install

The task `install` detects the target platform for each host in `bin_hosts` and installs a go binary with the `go install` paradigm via `hyperledger.fabricx.go`:

```yaml
- name: Install the sample-go binary
  vars:
    go_package: github.com/example/sample-go/cmd
    bin_hosts: "{{ groups['orderers'] }}"
    bin_dir: /usr/local/bin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/install
```

### map_platform_to_host

The task `map_platform_to_host` builds a dictionary of unique OS/architecture platform combinations from a list of hosts. It deduplicates platforms so that cross-compilation is performed only once per unique platform rather than once per host instance.

```yaml
- name: Build the unique platform map for the target hosts
  vars:
    bin_hosts: "{{ groups['orderers'] }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: map_platform_to_host
```

After execution, the `bin_platforms` fact contains a dictionary keyed by `<os>:<arch>` strings, each holding the OS, architecture, and the list of hosts sharing that platform.

### transfer

The task `transfer` allows to transfer a binary from the control node to the remote nodes.

```yaml
- name: Transfer the sample-go binary to the remote hosts
  vars:
    bin_name: sample-go
    bin_dir: /usr/local/bin
    bin_remote_dir: /usr/local/bin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: transfer
```

### start

The task `start` allows to start a binary within a **tmux** session.

```yaml
- name: Start the sample-go binary
  vars:
    bin_name: sample-go
    bin_command: /usr/local/bin/sample-go start
    bin_wait_until_running: true
    bin_wait_port: 9010
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: start
```

### stop

The task `stop` allows to stop a binary by killing the associated **tmux** session.

```yaml
- name: Stop the sample-go binary
  vars:
    bin_name: sample-go
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: stop
```

### rm

The task `rm` allows to remove the binary from the filesystem.

```yaml
- name: Remove the sample-go binary
  vars:
    bin_name: sample-go
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: rm
```

### fetch_logs

The task `fetch_logs` allows to collect the logs generated by a binary.

```yaml
- name: Fetch the logs from the sample-go binary
  vars:
    bin_name: sample-go
    bin_fetched_logs_dir: /tmp/
    bin_fetched_logs_file: sample-go_logs.txt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: fetch_logs
```
