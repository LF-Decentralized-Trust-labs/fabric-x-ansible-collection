# hyperledger.fabricx.package

The role `hyperledger.fabricx.package` can be used to install a package on a machine.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [install](#install)
  - [install_on_linux](#install_on_linux)
  - [install_on_macos](#install_on_macos)

## Tasks

### install

The task `install` allows to install a package on the target machine:

```yaml
- name: Install tmux
  vars:
    package_name: tmux
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install
```

### install_on_linux

The task `install_on_linux` allows to install a package on a Linux machine and, optionally, to start it also as daemon if needed (through the `package_has_service` flag):

```yaml
- name: Install chrony on Linux
  vars:
    package_name: chrony
    package_has_service: true # optional
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_linux
```

### install_on_macos

The task `install_on_macos` allows to install a package on macOS (it requires `brew`):

```yaml
- name: Install chronyc on macOS
  vars:
    package_name: chronyc
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_macos
```
