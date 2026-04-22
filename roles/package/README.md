
# hyperledger.fabricx.package

> Installs OS packages on target machines (apt / brew).


## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [install](#task-install)
  - [install_on_linux](#task-install_on_linux)
  - [install_on_macos](#task-install_on_macos)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

<a id="task-install"></a>

### install

Install a package for the current operating system


Installs a package by dispatching to the Linux or macOS entry point based on `ansible_facts.system`.

This entry point validates `package_name` and `package_service_name`.


```yaml
- name: Install a package for the current operating system
  vars:
    # Names the executable or package to install on the target host. Set this to the package identifier used by the host package manager.
    package_name: "string"
    # Names the Linux service to enable and start after installation.
    package_service_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install
```

<a id="task-install_on_linux"></a>

### install_on_linux

Install a package on Linux


Installs a package on Linux hosts after confirming the command is not already present and the package is available through the system package manager.

If a service name is provided, this entry point also enables and starts that service after installation.


```yaml
- name: Install a package on Linux
  vars:
    # Names the executable or package to install on the target host. Set this to the package identifier used by the host package manager.
    package_name: "string"
    # Names the Linux service to enable and start after installation.
    package_service_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_linux
```

<a id="task-install_on_macos"></a>

### install_on_macos

Install a package on macOS


Installs a package on macOS hosts with Homebrew after confirming the command is not already present.

This entry point assumes Homebrew is already installed on the target host.


```yaml
- name: Install a package on macOS
  vars:
    # Names the executable or package to install on the target host. Set this to the package identifier used by the host package manager.
    package_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.package
    tasks_from: install_on_macos
```


