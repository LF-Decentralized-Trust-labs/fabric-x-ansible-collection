# hyperledger.fabricx.utils

> Provides inventory grouping helpers, Makefile target generation, and TCP reachability checks.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [generate\_makefile\_targets](#generate_makefile_targets)
  - [ping](#ping)
  - [select\_one\_host\_per\_k8s\_namespace](#select_one_host_per_k8s_namespace)
  - [select\_one\_host\_per\_machine](#select_one_host_per_machine)
  - [benchmark\_volume](#benchmark_volume)

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

Creates the inventory dispatch group in Makefile form by writing one phony target per host in `groups['all']`. The generated targets are named after inventory hosts and route commands to a single host through `TARGET_HOSTS`, which is written to `project_dir/target_hosts.mk`.

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

Checks each port in `utils_ports_to_ping` against `actual_host` to verify whether the host is reachable on the requested network endpoints. Unreachable ports are handled through a silent rescue block, so this entry point reports reachability without failing the play.

```yaml
- name: Check whether TCP ports are reachable
  vars:
    # Lists the TCP ports that the ping entry point probes for reachability on the current host. Example: `[7051, 9443]`.
    utils_ports_to_ping:
      - 7051
      - 9443
    # Real machine host. Example: `myvpc.cloud.ibm.com`.
    actual_host: "myvpc.cloud.ibm.com"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: ping
```

### select_one_host_per_k8s_namespace

> Create a group with one host per Kubernetes namespace

Creates the `k8s_namespaces` inventory group with one selected host per distinct Kubernetes namespace. Only hosts with `k8s_image_pull_secret` defined participate, and the selection reads `k8s_namespace` from `hostvars` across `ansible_play_hosts`.

```yaml
- name: Create a group with one host per Kubernetes namespace
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_k8s_namespace
```

### select_one_host_per_machine

> Create a group with one host per machine

Creates the `machines` inventory group with one selected host per distinct machine address. The selection reads `actual_host` from `hostvars` across `ansible_play_hosts` to identify hosts that share the same machine.

```yaml
- name: Create a group with one host per machine
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: select_one_host_per_machine
```

### benchmark_volume

> Run SSD performance benchmark on remote hosts

Copies `ssd_benchmark.sh` to the remote host and executes it to measure sequential write/read throughput, random 4K IOPS, and I/O latency. Evaluates whether the machine meets the minimum sequential write threshold of `1 GB/s` required for high-performance Fabric-X operations. Prints a warning if the measured sequential write speed falls below the threshold but does not fail the play.

```yaml
- name: Run SSD performance benchmark on remote hosts
  vars:
    # Remote directory where the benchmark script is copied before execution. Example: `/tmp`.
    utils_benchmark_remote_dir: /tmp
    # Directory on the remote host where benchmark test files are created during the run. The directory is cleaned up automatically after the benchmark completes. Example: `/tmp/ssd_benchmark_test`.
    utils_benchmark_test_dir: /tmp/ssd_benchmark_test
    # Total data size used by fio random I/O tests. Example: `1G`.
    utils_benchmark_test_size: 1G
    # Block size used for random I/O tests. Example: `4k`.
    utils_benchmark_block_size: 4k
  ansible.builtin.include_role:
    name: hyperledger.fabricx.utils
    tasks_from: benchmark_volume
```
