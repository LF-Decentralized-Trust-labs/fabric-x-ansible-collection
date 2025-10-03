# Hyperledger Fabric-X Ansible Collection Roles

This document lists all the roles that come together within the collection and that can be used to manage the Hyperledger Fabric-X components.

## Table of Contents <!-- omit in toc -->

- [How to use](#how-to-use)
- [Roles list](#roles-list)

## How to use

The roles within this repository can be used to handle the different components that are needed in order to boostrap a Fabric-X network.

They are structured in multiple tasks, each one devoted to a specific action. To perform an action, you can use the `ansible.builtin.include_role` functionality:

```yaml
- name: Generate the crypto material with cryptogen
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cryptogen
    tasks_from: start
```

The roles are interconnected each other, meaning that some roles play as base for other role functions (e.g. the [bin](./bin) or [container](./container) roles).

## Roles list

The roles that come within such collection are listed hereafter. Click on them to access their documentation:

- [`hyperledger.fabricx.armageddon`](./armageddon);
- [`hyperledger.fabricx.bin`](./bin);
- [`hyperledger.fabricx.committer`](./committer);
- [`hyperledger.fabricx.configtxgen`](./configtxgen);
- [`hyperledger.fabricx.container`](./container);
- [`hyperledger.fabricx.cryptogen`](./cryptogen);
- [`hyperledger.fabricx.fxconfig`](./fxconfig);
- [`hyperledger.fabricx.git`](./git);
- [`hyperledger.fabricx.grafana`](./grafana);
- [`hyperledger.fabricx.jaeger`](./jaeger);
- [`hyperledger.fabricx.loadgen`](./loadgen);
- [`hyperledger.fabricx.node_exporter`](./node_exporter);
- [`hyperledger.fabricx.openssl`](./openssl);
- [`hyperledger.fabricx.orderer`](./orderer);
- [`hyperledger.fabricx.package`](./package);
- [`hyperledger.fabricx.postgres`](./postgres);
- [`hyperledger.fabricx.postgres_exporter`](./postgres_exporter);
- [`hyperledger.fabricx.prometheus`](./prometheus);
- [`hyperledger.fabricx.tmux`](./tmux);
- [`hyperledger.fabricx.utils`](./utils);
- [`hyperledger.fabricx.yugabyte`](./yugabyte).
