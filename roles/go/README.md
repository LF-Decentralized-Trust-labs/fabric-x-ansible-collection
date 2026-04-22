
# hyperledger.fabricx.go

> Provides tasks for building and installing Go binaries, and mapping Ansible facts to Go platform values (GOOS/GOARCH).


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [install_go](#task-install_go)
  - [map_platform](#task-map_platform)
  - [build](#task-build)
  - [install](#task-install)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-install_go"></a>

### install_go

Install the Go toolchain on the target host


Installs the Go runtime when it is not already present on the target host.

This entry point maps the target platform before downloading the matching Go archive.


```yaml
- name: Install the Go toolchain on the target host
  vars:
    # Specifies the Go release version to install.
    go_version: 1.25.8
    # Download URL for the Go archive. The default derives from `go_version`, `go_os`, and `go_arch`.
    go_download_url: "https://go.dev/dl/go{{ go_version }}.{{ go_os }}-{{ go_arch }}.tar.gz"
    # Sets the base directory where the Go distribution is extracted.
    go_install_dir: /usr/local
    # Selects the host whose facts are mapped into `go_os` and `go_arch`. The default derives from `inventory_hostname`.
    go_host_to_map: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: install_go
```

<a id="task-map_platform"></a>

### map_platform

Map Ansible host facts to GOOS and GOARCH values


Reads host facts and derives the Go platform identifiers used for cross-compilation and downloads.

This entry point sets `go_os` and `go_arch` facts for later tasks in the role.


```yaml
- name: Map Ansible host facts to GOOS and GOARCH values
  vars:
    # Selects the host whose facts are mapped into `go_os` and `go_arch`. The default derives from `inventory_hostname`.
    go_host_to_map: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: map_platform
```

<a id="task-build"></a>

### build

Build a Go binary from source


Runs `go build` for the selected source package and output name.

This entry point can cross-compile by mapping host facts and optionally enabling CGO.


```yaml
- name: Build a Go binary from source
  vars:
    # Sets the output path passed to `go build -o`.
    go_output_name: "string"
    # Defines the base directory containing the Go source tree to build.
    go_source_code_path: "string"
    # Appends a package subdirectory under `go_source_code_path` before invoking `go build`. The default is blank, which builds from the source root.
    go_source_code_package: ""
    # Selects the host whose facts are mapped into `go_os` and `go_arch`. The default derives from `inventory_hostname`.
    go_host_to_map: "{{ inventory_hostname }}"
    # Enables CGO for build and install commands. A compatible C compiler is required when this is `true`.
    go_cgo_enabled: false
    # Provides optional Go build tags passed to the Go command. The list is joined with commas before execution.
    go_tags: ["entry1", "entry2"]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: build
```

<a id="task-install"></a>

### install

Install a Go package with go install


Runs `go install` for the requested package using the mapped target platform values.

This entry point can place the installed binary in a custom output directory and optionally enable CGO.


```yaml
- name: Install a Go package with go install
  vars:
    # Specifies the Go package or module path passed to `go install`.
    go_package: "string"
    # Sets the directory exported as `GOBIN` for installed binaries. The default derives from `GOBIN` when set, otherwise from `GOPATH`.
    go_output_dir: "{{ lookup('env', 'GOBIN') | default(lookup('env', 'GOPATH') + '/bin', true) }}"
    # Selects the host whose facts are mapped into `go_os` and `go_arch`. The default derives from `inventory_hostname`.
    go_host_to_map: "{{ inventory_hostname }}"
    # Enables CGO for build and install commands. A compatible C compiler is required when this is `true`.
    go_cgo_enabled: false
    # Provides optional Go build tags passed to the Go command. The list is joined with commas before execution.
    go_tags: ["entry1", "entry2"]
  ansible.builtin.include_role:
    name: hyperledger.fabricx.go
    tasks_from: install
```


