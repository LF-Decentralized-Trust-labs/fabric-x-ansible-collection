# hyperledger.fabricx.package

> Installs OS packages on target machines (apt / brew).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [Lifecycle](#lifecycle)
    - [install](#install)
    - [install_on_linux](#install_on_linux)
    - [install_on_macos](#install_on_macos)
- [Variables](#variables)

## Tasks

### Lifecycle

| Task                                              | Description               |
| ------------------------------------------------- | ------------------------- |
| [install](./tasks/install.yaml)                   | Installs package          |
| [install_on_linux](./tasks/install_on_linux.yaml) | Installs package on Linux |
| [install_on_macos](./tasks/install_on_macos.yaml) | Installs package on macOS |

#### install

Installs a package on the target machine:

```yaml
- name: Install tmux
  vars:
    package_name: tmux
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install
```

#### install_on_linux

Installs a package on a Linux machine and, optionally, starts it as a daemon if needed (through the `package_service_name` flag):

```yaml
- name: Install chrony on Linux
  vars:
    package_name: chrony
    package_service_name: chronyd # optional
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_linux
```

#### install_on_macos

Installs a package on macOS (requires `brew`):

```yaml
- name: Install chronyc on macOS
  vars:
    package_name: chronyc
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_macos
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
