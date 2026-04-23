# hyperledger.fabricx.package

> Shared package installer that dispatches to Linux package managers or Homebrew on macOS.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [install](#install)
  - [install_on_linux](#install_on_linux)
  - [install_on_macos](#install_on_macos)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.package
```

## Tasks

### install

> Dispatch package installation for the current operating system

Shared entry point that dispatches to the Linux or macOS installer based on `ansible_facts.system`.Use this entry point when the target host may be either Linux or macOS and you want the role to choose the correct package manager path.This entry point validates `package_name` and `package_service_name`.

```yaml
- name: Dispatch package installation for the current operating system
  vars:
    # Names the executable or package to install on the target host. Set this to the package identifier used by the host package manager. Example: `postgresql-client` on a Debian/Ubuntu host or `postgresql@16` with Homebrew on macOS.
    package_name: "string"
    # Names the Linux service to enable and start after installation. Example: `postgresql`.
    package_service_name: "postgresql"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install
```

### install_on_linux

> Install a package on Linux

Installs a package on Linux hosts after confirming the command is not already present and the package is available through the system package manager.Uses the host package manager to install the requested package identifier and then enables and starts the matching service when `package_service_name` is provided.

```yaml
- name: Install a package on Linux
  vars:
    # Names the executable or package to install on the target host. Set this to the package identifier used by the host package manager. Example: `postgresql-client` on a Debian/Ubuntu host or `postgresql@16` with Homebrew on macOS.
    package_name: "string"
    # Names the Linux service to enable and start after installation. Example: `postgresql`.
    package_service_name: "postgresql"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_linux
```

### install_on_macos

> Install a package on macOS

Installs a package on macOS hosts with Homebrew after confirming the command is not already present.Uses Homebrew to install the requested formula or cask and assumes Homebrew is already installed on the target host.

```yaml
- name: Install a package on macOS
  vars:
    # Names the executable or package to install on the target host. Set this to the package identifier used by the host package manager. Example: `postgresql-client` on a Debian/Ubuntu host or `postgresql@16` with Homebrew on macOS.
    package_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_macos
```
