# hyperledger.fabricx.committer

The role `hyperledger.fabricx.committer` can be used to run the Fabric-X `committer` components (i.e. `validator`, `verifier`, `coordinator`, `sidecar` and `query-service`).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [config/transfer](#configtransfer)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)
  - [get_metrics](#get_metrics)

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate and/or transfer the crypto material needed to run a Fabric-X Committer component. The task supports two modes:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Setup the crypto material for Fabric-X Committer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` allows to fetch the Fabric-X Committer TLS certificate on the control node. This operation is important for sharing the TLS CA certificate with clients that need to establish a trusted connection to the committer.

```yaml
- name: Fetch the Fabric-X Committer TLS certificate
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the TLS crypto material generated for a Fabric-X Committer component:

```yaml
- name: Remove the Fabric-X Committer crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` allows to transfer the configuration files for a Fabric-X Committer component on the remote node. The component type is determined by the `committer_component_type` variable (`validator`, `verifier`, `coordinator`, `sidecar`, or `query-service`):

```yaml
- name: Transfer the Fabric-X Committer configuration files
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: config/transfer
```

### start

The task `start` allows to start Hyperledger Fabric-X Committer either as binary or as container. The sub-component to start is determined by the `committer_component_type` variable (`validator`, `verifier`, `coordinator`, `sidecar`, or `query-service`):

```yaml
- name: Start Hyperledger Fabric-X Committer
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: start
```

### stop

The task `stop` allows to stop the Fabric-X Committer running as binary or as container. The sub-component to stop is determined by the `committer_component_type` variable:

```yaml
- name: Stop the Fabric-X Committer
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Fabric-X Committer running as binary or as container and remove all the artifacts being generated during runtime. The sub-component to teardown is determined by the `committer_component_type` variable:

```yaml
- name: Teardown the Fabric-X Committer
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Fabric-X Committer running as binary or as container, remove all the artifacts (configuration files, binaries and all the runtime-generated artifacts). The sub-component to wipe is determined by the `committer_component_type` variable:

```yaml
- name: Wipe the Fabric-X Committer
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Fabric-X Committer components from the remote hosts to the control node. The sub-component whose logs are fetched is determined by the `committer_component_type` variable:

```yaml
- name: Fetch the Fabric-X Committer logs
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
    committer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.committer
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Fabric-X Committer components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable. The sub-component to ping is determined by the `committer_component_type` variable:

```yaml
- name: Ping the Fabric-X Committer
  vars:
    committer_component_type: validator # or verifier, coordinator, sidecar, query-service
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
