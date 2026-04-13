# hyperledger.fabricx.utils

> Provides utility functions for inventory management and port checking.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [Lifecycle](#lifecycle)
    - [generate_makefile_targets](#generate_makefile_targets)
    - [ping](#ping)
    - [select_one_host_per_machine](#select_one_host_per_machine)
- [Variables](#variables)

## Tasks

### Lifecycle

| Task                                                                    | Description                |
| ----------------------------------------------------------------------- | -------------------------- |
| [generate_makefile_targets](./tasks/generate_makefile_targets.yaml)     | Generates Makefile targets |
| [ping](./tasks/ping.yaml)                                               | Checks port availability   |
| [select_one_host_per_machine](./tasks/select_one_host_per_machine.yaml) | Creates machines group     |

#### generate_makefile_targets

Generates Makefile targets for all individual hosts in the inventory. The generated targets are written to `target_hosts.mk` in the project root directory.

```yaml
- name: Generate Makefile targets for all inventory hosts
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: generate_makefile_targets
```

This is typically invoked via the Makefile:

```bash
make targets
```

After generation, you can target individual hosts:

```bash
make orderer-router-1 start
make committer-validator stop
```

#### ping

Checks whether a set of ports on a given machine is open:

```yaml
- name: Check that the port 9000 and 9001 are open
  vars:
    utils_ports_to_ping:
      - 9000
      - 9001
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: ping
```

#### select_one_host_per_machine

Creates a group named `machines` that will contain exactly a single host per machine. It can be useful when you need to perform some operations that would collide and generate errors if run concurrently on the same machine (e.g. when 2 hosts are located on the same machine).

```yaml
- name: Set the group "machines"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_machine
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
