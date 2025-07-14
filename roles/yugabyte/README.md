# hyperledger.fabricx.yugabyte

The role `hyperledger.fabricx.yugabyte` can be used to run a `yugabyte` distributed DB cluster.

It supports 2 types of deployments:

- **standalone**: a minimal Yugabyte cluster is deployed on the same machine through a single container (1 master, 1 tablet => replication factor = 1). This deployment strategy is used whenever a Yugabyte host does not specify its cluster role (`master` or `tablet`);
- **distributed**: the Yugabyte cluster nodes are deployed according to the `yugabyte_component_type` value that has been assigned (`master` or `tablet`).

The role allows to run YugabyteDB as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)

## Tasks

### install_prereqs

The task `install_prereqs` allows to install the needed Yugabyte prerequisites on the remote hosts. Specifically, it installs and enable `chrony`.

```yaml
- name: Install the Yugabyte DB prerequisites
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: install_prereqs
```

### start

The task `start` allows to start the Yugabyte DB Cluster.

```yaml
- name: Start the Yugabyte DB Cluster
  vars:
    # ports for the Yugabyte cluster master
    yugabyte_master_rpc_bind_port: 7100
    yugabyte_master_webserver_port: 7000
    # ports for the Yugabyte cluster tablet
    yugabyte_tablet_pgsql_bind_port: 5432
    yugabyte_tablet_rpc_bind_port: 9100
    yugabyte_tablet_webserver_port: 9000
    yugabyte_tablet_redis_web_port: 11000
    yugabyte_tablet_cql_web_port: 12000
    yugabyte_tablet_pgsql_web_port: 13000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: start
```

### stop

The task `stop` allows to stop the Yugabyte DB Cluster.

```yaml
- name: Stop the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down the Yugabyte DB Cluster and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down the Yugabyte DB Cluster, remove all the artifacts (configuration files and all the runtime-generated artifacts).

```yaml
- name: Wipe the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from the Yugabyte DB Cluster components from the remote hosts to the control node.

```yaml
- name: Fetch the Yugabyte DB Cluster logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping the Yugabyte DB Cluster components on their opened ports. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the Yugabyte DB Cluster
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: ping
```

### get_metrics

The task `get_metrics` allows to fetch the Yugabyte DB metrics.

```yaml
- name: Fetch the Yugabyte DB Cluster metrics
  ansible.builtin.include_role:
    name: hyperledger.fabricx.yugabyte
    tasks_from: get_metrics
```
