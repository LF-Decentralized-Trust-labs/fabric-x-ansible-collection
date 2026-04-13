# hyperledger.fabricx.bin

> Handles binary build, installation, and lifecycle management on target nodes.

<!-- @depends_on: hyperledger.fabricx.go, hyperledger.fabricx.git, hyperledger.fabricx.tmux -->

## Table of Contents <!-- omit in toc -->

- [Depends On](#depends-on)
- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Go Tasks](#go-tasks)
    - [go/build](#gobuild)
    - [go/install](#goinstall)
  - [Lifecycle](#lifecycle)
    - [map_platform_to_host](#map_platform_to_host)
    - [transfer](#transfer)
    - [start](#start)
    - [stop](#stop)
    - [rm](#rm)
    - [fetch_logs](#fetch_logs)
- [Variables](#variables)

## Depends On

| Role                                            | Reason                        |
| ----------------------------------------------- | ----------------------------- |
| [`hyperledger.fabricx.go`](../go/README.md)     | Builds Go binaries            |
| [`hyperledger.fabricx.git`](../git/README.md)   | Clones source code            |
| [`hyperledger.fabricx.tmux`](../tmux/README.md) | Runs binaries in tmux session |

## Prerequisites

- `go` to build/install binaries
- `rsync` to transfer binaries from control node to target node

## Tasks

### Go Tasks

| Task                                  | Description                                     |
| ------------------------------------- | ----------------------------------------------- |
| [go/build](./tasks/go/build.yaml)     | Clones source, detects platform, cross-compiles |
| [go/install](./tasks/go/install.yaml) | Installs binary to target directory             |

#### go/build

Clones the source code of a `go` binary, detects the target platform for each host in `bin_hosts`, and builds a cross-compiled binary for each unique platform via `hyperledger.fabricx.go`:

```yaml
- name: Build the sample-go binary
  vars:
    git_uri: "https://github.com/sample/sample-go.git"
    bin_name: sample-go
    bin_hosts: "{{ groups['orderers'] }}"
    bin_source_code_dir: /tmp/sample-go/src
    bin_dir: /usr/local/bin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/build
```

#### go/install

Installs a Go binary to the target directory:

```yaml
- name: Install the sample-go binary
  vars:
    bin_name: sample-go
    bin_hosts: "{{ groups['orderers'] }}"
    bin_dir: /usr/local/bin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: go/install
```

### Lifecycle

| Task                                                      | Description                              |
| --------------------------------------------------------- | ---------------------------------------- |
| [map_platform_to_host](./tasks/map_platform_to_host.yaml) | Maps Ansible facts to Go platform values |
| [transfer](./tasks/transfer.yaml)                         | Transfers binary to target node          |
| [start](./tasks/start.yaml)                               | Starts the binary                        |
| [stop](./tasks/stop.yaml)                                 | Stops the binary                         |
| [rm](./tasks/rm.yaml)                                     | Removes the binary                       |
| [fetch_logs](./tasks/fetch_logs.yaml)                     | Collects logs                            |

#### map_platform_to_host

Maps Ansible facts (`ansible_facts.system`, `ansible_facts.architecture`) from a remote host to Go's `GOOS` and `GOARCH` values:

```yaml
- name: Map platform for target host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: map_platform_to_host
```

#### transfer

Transfers the binary to the target node:

```yaml
- name: Transfer the binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: transfer
```

#### start

Starts the binary:

```yaml
- name: Start the binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: start
```

#### stop

Stops the binary:

```yaml
- name: Stop the binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: stop
```

#### rm

Removes the binary:

```yaml
- name: Remove the binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: rm
```

#### fetch_logs

Collects logs from the binary:

```yaml
- name: Fetch binary logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.bin
    tasks_from: fetch_logs
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
