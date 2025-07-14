# hyperledger.fabricx.utils

The role `hyperledger.fabricx.utils` can be used to run utility functions.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [ping](#ping)

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
