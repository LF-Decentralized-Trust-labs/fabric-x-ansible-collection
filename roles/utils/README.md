# hyperledger.fabricx.utils

The role `hyperledger.fabricx.utils` can be used to run utility functions.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [ping](#ping)
  - [select_one_host_per_machine](#select_one_host_per_machine)

## Tasks

### ping

The task `ping` can be used to check whether a set of ports on a given machine is open:

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

### select_one_host_per_machine

The task `select_one_host_per_machine` can be used to create a group named `machines` that will contain exactly a single host per machine. It can be useful when you need to perform some operations that would collide and generate errors if run concurrently on the same machine (e.g. when 2 hosts are located on the same machine).

```yaml
- name: Set the group "machines"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_machine
```
