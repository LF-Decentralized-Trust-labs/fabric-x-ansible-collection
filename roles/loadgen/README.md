# hyperledger.fabricx.loadgen

The role `hyperledger.fabricx.loadgen` can be used to run a Load generator to test the throughput of the system.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [crypto/transfer](#cryptotransfer)
  - [crypto/fetch](#cryptofetch)
  - [config/transfer](#configtransfer)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)
  - [get_metrics](#get_metrics)
  - [limit_rate](#limit_rate)

## Tasks

### crypto/transfer

The task `crypto/transfer` allows to generate and/or transfer the crypto material needed to run a Fabric-X Loadgen component. The task supports two modes to run:

- with `cryptogen` (when `organization.fabric_ca_host` is not set): the crypto material must be generated with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)) on the control node and is transferred to the remote node;
- with `fabric-ca`: in this case the crypto material is generated directly on the remote node.

```yaml
- name: Setup the crypto material for Fabric-X Loadgen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/transfer
```

### crypto/fetch

The task `crypto/fetch` allows to fetch the Fabric-X Loadgen certificates on the control node. This operation is important for the generation of the genesis block on the control node in case the Loadgen user is set as **Meta Namespace Admin** (with the `meta_namespace_admin` flag).

```yaml
- name: Fetch the Fabric-X Loadgen certificates
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: crypto/fetch
```

### config/transfer

The task `config/transfer` allows to transfer the configuration files for a Fabric-X Loadgen on the remote node:

```yaml
- name: Transfer the Fabric-X Loadgen configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: config/transfer
```

### start

The task `start` allows to start the Fabric-X Load Generator either as binary or as container.

```yaml
- name: Start the Fabric-X Load Generator
  vars:
    loadgen_use_bin: true # set to false or unset for container
    loadgen_web_port: 6997
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: start
```

### stop

The task `stop` allows to stop the Fabric-X Load Generator running as binary or as container.

```yaml
- name: Stop the Fabric-X Load Generator
  vars:
    loadgen_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Fabric-X Load Generator running as binary or as container and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown the Fabric-X Load Generator
  vars:
    loadgen_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Fabric-X Load Generator running as binary or as container, remove all the artifacts (configuration files, binaries and all the runtime-generated artifacts).

```yaml
- name: Wipe the Fabric-X Load Generator
  vars:
    loadgen_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Fabric-X Load Generator components from the remote hosts to the control node.

```yaml
- name: Fetch the Fabric-X Load Generator logs
  vars:
    loadgen_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Fabric-X Load Generator components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Fabric-X Load Generator
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: ping
```

### get_metrics

The task `get_metrics` allows to fetch the metrics from the Fabric-X Load Generator components and print them on stdout.

```yaml
- name: Fetch the Fabric-X Load Generator metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: get_metrics
```

### limit_rate

The task `limit_rate` allows to limit the load generator throughput at runtime to a specified value.

```yaml
- name: Set the upper TPS limit for the Fabric-X Load Generator
  vars:
    loadgen_limit_rate: 2000 # limit to 2000 TPS
  ansible.builtin.include_role:
    name: hyperledger.fabricx.loadgen
    tasks_from: limit_rate
```
