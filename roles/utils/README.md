# hyperledger.fabricx.utils

> Provides utility functions for inventory management and port checking.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [generate_makefile_targets](#generate_makefile_targets)
  - [ping](#ping)
  - [select_one_host_per_k8s_namespace](#select_one_host_per_k8s_namespace)
  - [select_one_host_per_machine](#select_one_host_per_machine)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### generate_makefile_targets

Generate Makefile targets for inventory hosts

Generates a `target_hosts.mk` file with one Makefile target per inventory host in `groups['all']`.

The output path is `project_dir + '/target_hosts.mk'`, using the caller-provided `project_dir` variable.

```yaml
- name: Generate Makefile targets for inventory hosts
  vars:
    # Defines the project root directory used by utility entry points that write generated files. Example: `/path/to/hyperledger/fabricx`.
    project_dir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: generate_makefile_targets
```

### ping

Check whether TCP ports are reachable

Checks whether each port in `utils_ports_to_ping` is reachable on `actual_host` for the current host.

Failures are handled through a silent rescue block, so unreachable ports do not fail the play.

```yaml
- name: Check whether TCP ports are reachable
  vars:
    # Lists the TCP ports that the ping entry point probes on the current host. Example: `[9000, 9001]`.
    utils_ports_to_ping: [1000, 2000]
    # Sets the network address that the ping entry point probes for each port in `utils_ports_to_ping`. Example: `orderer-router-1.example.com`.
    actual_host: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: ping
```

### select_one_host_per_k8s_namespace

Create a group with one host per Kubernetes namespace

Creates the `k8s_namespaces` group with one selected inventory host per distinct Kubernetes namespace.

Only hosts with `k8s_image_pull_secret` defined participate, and the selection reads `k8s_namespace` from `hostvars` across `ansible_play_hosts`.

```yaml
- name: Create a group with one host per Kubernetes namespace
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_k8s_namespace
```

### select_one_host_per_machine

Create a group with one host per machine

Creates the `machines` group with one selected inventory host per distinct machine address.

The selection reads `actual_host` from `hostvars` across `ansible_play_hosts` to identify hosts that share the same machine.

```yaml
- name: Create a group with one host per machine
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_machine
```
