# hyperledger.fabricx.orderer

The role `hyperledger.fabricx.orderer` can be used to run the Fabric-X `orderer` component.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate and/or transfer the crypto material needed to run a Fabric-X Orderer component. The task supports two modes to run:

- with `cryptogen` (see [hyperledger.fabricx.cryptogen](../cryptogen/README.md)): the crypto material generated on the control node with `cryptogen` is transferred to the remote node;
- with `fabric-ca` (see [hyperledger.fabricx.fabric_ca](../fabric_ca/README.md)): the crypto material is generated directly on the remote node querying the reference `fabric_ca` host.

```yaml
- name: Setup the crypto material for Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` allows to fetch the Fabric-X Orderer certificates on the control node. This operation is important for the generation of the genesis block on the control node, which will embed the certificates of the orderers.

```yaml
- name: Fetch the Fabric-X Orderer certificates
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for a Fabric-X Orderer:

```yaml
- name: Remove the Fabric-X Orderer crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` allows to transfer the configuration files for a Fabric-X Orderer on the remote node:

```yaml
- name: Transfer the Fabric-X Orderer configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Fabric-X Orderer configuration files on the remote node:

```yaml
- name: Remove the Fabric-X Orderer configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: config/rm
```

### start

The task `start` allows to start the Fabric-X Orderer either as binary or as container.

```yaml
- name: Start the Fabric-X Orderer
  vars:
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: start
```

### stop

The task `stop` allows to stop the Fabric-X Orderer running as binary or as container.

```yaml
- name: Stop the Fabric-X Orderer
  vars:
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Fabric-X Orderer running as binary or as container and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown the Fabric-X Orderer
  vars:
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Fabric-X Orderer running as binary or as container, remove all the artifacts (configuration files, binaries and all the runtime-generated artifacts).

```yaml
- name: Wipe the Fabric-X Orderer
  vars:
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Fabric-X Orderer components from the remote hosts to the control node.

```yaml
- name: Fetch the Fabric-X Orderer logs
  vars:
    orderer_use_bin: true # set to false or unset for container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Fabric-X Orderer components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: ping
```
