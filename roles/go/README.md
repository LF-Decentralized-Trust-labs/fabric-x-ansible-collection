# hyperledger.fabricx.go

The role `hyperledger.fabricx.go` provides tasks for building and installing Go binaries, as well as mapping platform information from Ansible facts to Go's GOOS and GOARCH values.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [map_platform](#map_platform)
  - [build](#build)
  - [install](#install)

## Prerequisites

The role requires:

- `go` to be installed on the controller node.
- When `go_cgo_enabled` is `true`, a C compiler must be available for cross-compilation.

## Variables

The following variables can be used to customize the role:

| Variable              | Description                                   | Default                       |
| --------------------- | --------------------------------------------- | ----------------------------- |
| `go_cgo_enabled`      | Enable CGO for cross-compilation              | `false`                       |
| `go_output_dir`       | Output directory for binaries                 | `bin_dir` or `/usr/local/bin` |
| `go_source_code_path` | Path to source code (build task)              | `""`                          |
| `go_output_name`      | Name of output binary (build task)            | `""`                          |
| `go_package`          | Go package to install (install task)          | `""`                          |
| `go_host_to_map`      | Host to map platform from (map_platform task) | `""`                          |
| `go_os`               | Mapped GOOS value (set by map_platform)       | `""`                          |
| `go_arch`             | Mapped GOARCH value (set by map_platform)     | `""`                          |

## Tasks

### map_platform

The task `map_platform` maps Ansible facts (`ansible_facts.system` and `ansible_facts.architecture`) from a remote host to Go's `GOOS` and `GOARCH` values.

This task accepts a `go_host_to_map` variable containing the hostname of a remote host. It reads the Ansible facts from that host and maps them to the appropriate Go platform values.

**GOOS Mapping:**

| Ansible `system` | GOOS    |
| ---------------- | ------- |
| Linux            | linux   |
| Darwin           | darwin  |
| Windows          | windows |
| FreeBSD          | freebsd |
| OpenBSD          | openbsd |
| NetBSD           | netbsd  |

**GOARCH Mapping:**

| Ansible `architecture` | GOARCH  |
| ---------------------- | ------- |
| x86_64                 | amd64   |
| x86                    | 386     |
| aarch64                | arm64   |
| armv7l                 | arm     |
| armv6l                 | arm     |
| ppc64le                | ppc64le |
| ppc64                  | ppc64   |
| s390x                  | s390x   |
| riscv64                | riscv64 |
| loong64                | loong64 |

```yaml
- name: Map platform for host
  vars:
    go_host_to_map: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: map_platform
```

### build

The task `build` compiles a Go binary from source code.

Required variables:

- `go_source_code_path`: Path to the source code directory
- `go_output_name`: Name of the output binary

Optional variables:

- `go_os`: Target operating system (defaults to local OS)
- `go_arch`: Target architecture (defaults to local architecture)
- `go_cgo_enabled`: Enable CGO (defaults to false)

```yaml
- name: Build a Go binary
  vars:
    go_source_code_path: "/path/to/source"
    go_output_name: "mybinary"
    go_os: "linux"
    go_arch: "amd64"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: build
```

### install

The task `install` installs a Go binary package using `go install`.

Required variables:

- `go_package`: Full Go package path (e.g., `github.com/user/repo/cmd/tool`)

Optional variables:

- `go_output_dir`: Output directory for the binary
- `go_os`: Target operating system
- `go_arch`: Target architecture
- `go_cgo_enabled`: Enable CGO

```yaml
- name: Install a Go package
  vars:
    go_package: "github.com/hyperledger/fabric-x-committer/cmd/loadgen"
    go_output_dir: "/usr/local/bin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: install
```
