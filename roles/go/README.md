# hyperledger.fabricx.go

> Provides tasks for installing Go, mapping Ansible facts to GOOS and GOARCH, and building or installing Go binaries with cross-compilation support.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [install_go](#install_go)
  - [map_platform](#map_platform)
  - [build](#build)
  - [install](#install)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.go
```

## Tasks

### install_go

> Install the Go toolchain on the target host

Installs the Go runtime when it is not already present on the target host. Maps the selected host to `GOOS` and `GOARCH` before downloading the matching Go archive. Example: `Linux x86_64 -> GOOS=linux, GOARCH=amd64`. Extracts the archive into `go_install_dir` and leaves the Go binaries ready for PATH updates.

```yaml
- name: Install the Go toolchain on the target host
  vars:
    # Specifies the Go release version to install.
    go_version: 1.25.8
    # Sets the base directory where the Go distribution is extracted.
    go_install_dir: /usr/local
    # Selects the host whose facts are mapped into `go_os` and `go_arch`.
    go_host_to_map: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: install_go
```

### map_platform

> Map Ansible host facts to GOOS and GOARCH values

Reads host facts and derives the Go platform identifiers used for cross-compilation and downloads. Example: `Linux x86_64 -> GOOS=linux, GOARCH=amd64`. This entry point sets `go_os` and `go_arch` facts for later tasks in the role.

```yaml
- name: Map Ansible host facts to GOOS and GOARCH values
  vars:
    # Selects the host whose facts are mapped into `go_os` and `go_arch`.
    go_host_to_map: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: map_platform
```

### build

> Build a Go binary from source

Runs `go build` for the selected source tree and output name. Uses `GOOS`, `GOARCH`, `CGO_ENABLED`, and optional build tags to support cross-compilation. Example: `macOS arm64 building a Linux amd64 binary with GOOS=linux and GOARCH=amd64`. This entry point can also set `CC` when CGO is enabled for Linux targets from macOS.

```yaml
- name: Build a Go binary from source
  vars:
    # Sets the output path passed to `go build -o`. Example: `/opt/fabricx/bin/fxconfig`.
    go_output_name: "/opt/fabricx/bin/fxconfig"
    # Defines the base directory containing the Go source tree or module to build. Example: `/opt/fabricx/tools/fxconfig`.
    go_source_code_path: "/opt/fabricx/tools/fxconfig"
    # Appends a package subdirectory under `go_source_code_path` before invoking `go build`. Example: `cmd/fxconfig`.
    go_source_code_package: ""
    # Selects the host whose facts are mapped into `go_os` and `go_arch`.
    go_host_to_map: "{{ inventory_hostname }}"
    # Enables CGO for build and install commands. A compatible C compiler is required when this is `true`.
    go_cgo_enabled: false
    # Provides optional Go build tags passed to the Go command. Example: `['netgo', 'osusergo']`. The list is joined with commas before execution.
    go_tags:
      - netgo
      - osusergo
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: build
```

### install

> Install a Go package with go install

Runs `go install` for the requested package or module path using the mapped target platform values. Exports `GOBIN` to place installed binaries in `go_output_dir` and can optionally enable CGO. Example: `go install github.com/hyperledger/fabric-x/tools/fxconfig@v0.0.12 with GOOS=linux and GOARCH=amd64`. This entry point also supports build tags and the same platform mapping used by `go build`.

```yaml
- name: Install a Go package with go install
  vars:
    # Specifies the Go package or module path passed to `go install`. Example: `github.com/hyperledger/fabric-x/tools/fxconfig@v0.0.12`.
    go_package: "github.com/hyperledger/fabric-x/tools/fxconfig@v0.0.12"
    # Sets the directory exported as `GOBIN` for installed binaries.
    go_output_dir: "{{ lookup('env', 'GOBIN') | default(lookup('env', 'GOPATH') + '/bin', true) }}"
    # Selects the host whose facts are mapped into `go_os` and `go_arch`.
    go_host_to_map: "{{ inventory_hostname }}"
    # Enables CGO for build and install commands. A compatible C compiler is required when this is `true`.
    go_cgo_enabled: false
    # Provides optional Go build tags passed to the Go command. Example: `['netgo', 'osusergo']`. The list is joined with commas before execution.
    go_tags:
      - netgo
      - osusergo
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: install
```
