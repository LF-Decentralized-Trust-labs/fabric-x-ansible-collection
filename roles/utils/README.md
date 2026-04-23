# hyperledger.fabricx.utils

> Provides inventory grouping helpers, Makefile target generation, and TCP reachability checks.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [generate_makefile_targets](#generate_makefile_targets)
  - [ping](#ping)
  - [select_one_host_per_k8s_namespace](#select_one_host_per_k8s_namespace)
  - [select_one_host_per_machine](#select_one_host_per_machine)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.utils
```

## Tasks

### generate_makefile_targets

> Generate Makefile targets for inventory hosts

Creates the inventory dispatch group in Makefile form by writing one phony target per host in `groups['all']`.The generated targets are named after inventory hosts and route commands to a single host through `TARGET_HOSTS`, which is written to `project_dir/target_hosts.mk`.

```yaml
- name: Generate Makefile targets for inventory hosts
  vars:
    # Defines the project root directory used by utility entry points that generate Makefile targets, which writes `target_hosts.mk` to `project_dir/target_hosts.mk`. Example: `/path/to/hyperledger/fabricx`.
    project_dir: "/path/to/hyperledger/fabricx"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: generate_makefile_targets
```

### ping

> Check whether TCP ports are reachable

Checks each port in `utils_ports_to_ping` against `actual_host` to verify whether the host is reachable on the requested network endpoints.Unreachable ports are handled through a silent rescue block, so this entry point reports reachability without failing the play.

```yaml
- name: Check whether TCP ports are reachable
  vars:
    # Lists the TCP ports that the ping entry point probes for reachability on the current host. Example: `[7051, 9443]`.
    utils_ports_to_ping:
      - 7051
      - 9443
    # Sets the inventory host address that the ping entry point probes for each port in `utils_ports_to_ping`. Example: `orderer-router-1.example.com`.
    actual_host: "orderer-router-1.example.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: ping
```

### select_one_host_per_k8s_namespace

> Create a group with one host per Kubernetes namespace

Creates the `k8s_namespaces` inventory group with one selected host per distinct Kubernetes namespace.Only hosts with `k8s_image_pull_secret` defined participate, and the selection reads `k8s_namespace` from `hostvars` across `ansible_play_hosts`.

```yaml
- name: Create a group with one host per Kubernetes namespace
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_k8s_namespace
```

### select_one_host_per_machine

> Create a group with one host per machine

Creates the `machines` inventory group with one selected host per distinct machine address.The selection reads `actual_host` from `hostvars` across `ansible_play_hosts` to identify hosts that share the same machine.

```yaml
- name: Create a group with one host per machine
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_machine
```
