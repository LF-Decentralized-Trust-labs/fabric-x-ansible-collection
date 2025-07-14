# hyperledger.fabricx.orderer

The role `hyperledger.fabricx.orderer` can be used to run the Fabric-X `orderer` component.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)

## Tasks

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
