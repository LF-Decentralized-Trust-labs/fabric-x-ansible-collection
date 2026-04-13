# hyperledger.fabricx.go

> Provides tasks for building and installing Go binaries, and mapping Ansible facts to Go platform values (GOOS/GOARCH).

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Lifecycle](#lifecycle)
    - [install_go](#install_go)
    - [map_platform](#map_platform)
    - [build](#build)
    - [install](#install)
- [Variables](#variables)

## Prerequisites

- `go` installed on the controller node
- C compiler (when `go_cgo_enabled: true`)

## Tasks

### Lifecycle

| Task                                      | Description                       |
| ----------------------------------------- | --------------------------------- |
| [install_go](./tasks/install_go.yaml)     | Installs Go runtime               |
| [map_platform](./tasks/map_platform.yaml) | Maps Ansible facts to GOOS/GOARCH |
| [build](./tasks/build.yaml)               | Builds Go binary                  |
| [install](./tasks/install.yaml)           | Installs Go binary                |

#### install_go

Installs the Go runtime on the targeted node. Idempotent — if Go is already installed, the task is a no-op.

```yaml
- name: Install Go
  vars:
    go_version: "1.23.0"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: install_go
```

#### map_platform

Maps Ansible facts (`ansible_facts.system`, `ansible_facts.architecture`) from a remote host to Go's `GOOS` and `GOARCH` values.

```yaml
- name: Map platform for target host
  vars:
    go_host_to_map: target-host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: map_platform
```

#### build

Builds a Go binary from source:

```yaml
- name: Build Go binary
  vars:
    go_source_code_path: /path/to/source
    go_output_name: my-binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: build
```

#### install

Installs a Go binary using `go install`:

```yaml
- name: Install Go binary
  vars:
    go_package: github.com/example/my-binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: install
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
