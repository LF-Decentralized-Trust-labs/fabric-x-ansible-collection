# hyperledger.fabricx.committer

The role `hyperledger.fabricx.committer` can be used to run the Fabric-X `committer` components (i.e. `validator`, `verifier`, `coordinator` and `sidecar`).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)
  - [get_metrics](#get_metrics)

## Tasks

### start

The task `start` allows to Start Hyperledger Fabric-X Committer either as binary or as container.

```yaml
- name: Start Hyperledger Fabric-X Committer
  vars:
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: start
```

### stop

The task `stop` allows to stop the Fabric-X Committer running as binary or as container.

```yaml
- name: Stop the Fabric-X Committer
  vars:
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Fabric-X Committer running as binary or as container and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown the Fabric-X Committer
  vars:
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Fabric-X Committer running as binary or as container, remove all the artifacts (configuration files, binaries and all the runtime-generated artifacts).

```yaml
- name: Wipe the Fabric-X Committer
  vars:
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Fabric-X Committer components from the remote hosts to the control node.

```yaml
- name: Fetch the Fabric-X Committer logs
  vars:
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Fabric-X Committer components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Fabric-X Committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: ping
```

### get_metrics

The task `get_metrics` allows to fetch the metrics from the Fabric-X Committer components and print them on stdout.

```yaml
- name: Fetch the Fabric-X Committer metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: get_metrics
```
