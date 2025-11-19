# Hyperledger Fabric-X Deployment Samples

This folder contains sample inspirational inventories and playbooks to deploy different Hyperledger Fabric-X networks on a single node.

## Table of Contents <!-- omit in toc -->

- [Inventories](#inventories)
  - [Define the inventory to run](#define-the-inventory-to-run)
    - [Use `ansible.cfg`](#use-ansiblecfg)
    - [Set via env](#set-via-env)
  - [fabric-x.yaml](#fabric-xyaml)
  - [fabric-x-yugabyte.yaml](#fabric-x-yugabyteyaml)
  - [fabric-x-bin.yaml](#fabric-x-binyaml)
  - [fabric-x-cryptogen.yaml](#fabric-x-cryptogenyaml)
  - [fabric-x-distributed.yaml](#fabric-x-distributedyaml)
- [Playbooks](#playbooks)
- [How to replicate an horizontally scalable microservice](#how-to-replicate-an-horizontally-scalable-microservice)
- [How to run a microservice on a different machine](#how-to-run-a-microservice-on-a-different-machine)

## Inventories

There are currently 4 different [inventories](./inventory/) that can be used.

The microservices indicated as _horizontally scalable_ can be replicated. To understand how to replicate them, look at [this section](#how-to-replicate-an-horizontally-scalable-microservice).

### Define the inventory to run

To decide the inventory to run, you can:

#### Use `ansible.cfg`

Set the inventory in the [ansible.cfg](./ansible.cfg) file directly:

```ini
inventory = <path_to_the_inventory>
```

#### Set via env

Set the inventory as env variable:

```shell
export ANSIBLE_INVENTORY=<path_to_the_inventory>
```

### fabric-x.yaml

The [fabric-x.yaml](./inventory/fabric-x.yaml) inventory represents the following network scenario:

![fabric-x-inventory](./images/fabric-x.drawio.png)

It bootstraps a network with:

- 5 **Hyperledger Fabric CAs** containers;
- 4 **Hyperledger Fabric-X Orderers**, each one made by:
  - 1 consenter container;
  - 1 assembler container;
  - 1 batcher container (_horizontally scalable_);
  - 1 router container;
- 1 **Hyperledger Fabric-X Committer**, made by:
  - 1 validator container (_horizontally scalable_);
  - 1 verifier container (_horizontally scalable_);
  - 1 coordinator container;
  - 1 sidecar container;
  - 1 query service container;
  - 1 PostgreSQL container;
- 1 **Hyperledger Fabric-X Loadgen** binary;
- 1 **Grafana** container;
- 1 **Prometheus** container.

### fabric-x-yugabyte.yaml

The [fabric-x-yugabyte.yaml](./inventory/fabric-x-yugabyte.yaml) inventory represents the following network scenario:

![fabric-x-yugabyte-inventory](./images/fabric-x-yugabyte.drawio.png)

It bootstraps a network with:

- 5 **Hyperledger Fabric CAs** containers;
- 4 **Hyperledger Fabric-X Orderers**, each one made by:
  - 1 consenter container;
  - 1 assembler container;
  - 1 batcher container (_horizontally scalable_);
  - 1 router container;
- 1 **Hyperledger Fabric-X Committer**, made by:
  - 1 validator container (_horizontally scalable_);
  - 1 verifier container (_horizontally scalable_);
  - 1 coordinator container;
  - 1 sidecar container;
  - 1 query service container;
  - 1 **YugabyteDB** container (_horizontally scalable_);
- 1 **Hyperledger Fabric-X Loadgen** binary;
- 1 **Grafana** container;
- 1 **Prometheus** container.

### fabric-x-bin.yaml

The [fabric-x-bin.yaml](./inventory/fabric-x-bin.yaml) inventory represents the following network scenario:

![fabric-x-bin-inventory](./images/fabric-x-bin.drawio.png)

It bootstraps a network with:

- 5 **Hyperledger Fabric CAs** binaries;
- 4 **Hyperledger Fabric-X Orderers**, each one made by:
  - 1 consenter binary;
  - 1 assembler binary;
  - 1 batcher binary (_horizontally scalable_);
  - 1 router binary;
- 1 **Hyperledger Fabric-X Committer**, made by:
  - 1 validator binary (_horizontally scalable_);
  - 1 verifier binary (_horizontally scalable_);
  - 1 coordinator binary;
  - 1 sidecar binary;
  - 1 query service binary;
  - 1 PostgreSQL container;
- 1 **Hyperledger Fabric-X Loadgen** binary;
- 1 **Grafana** container;
- 1 **Prometheus** container.

### fabric-x-cryptogen.yaml

The [fabric-x-cryptogen.yaml](./inventory/fabric-x-cryptogen.yaml) inventory represents the following network scenario:

![fabric-x-cryptogen-inventory](./images/fabric-x-cryptogen.drawio.png)

It bootstraps a network with:

- 4 **Hyperledger Fabric-X Orderers**, each one made by:
  - 1 consenter container;
  - 1 assembler container;
  - 1 batcher container (_horizontally scalable_);
  - 1 router container;
- 1 **Hyperledger Fabric-X Committer**, made by:
  - 1 validator container (_horizontally scalable_);
  - 1 verifier container (_horizontally scalable_);
  - 1 coordinator container;
  - 1 sidecar container;
  - 1 query service container;
  - 1 PostgreSQL container;
- 1 **Hyperledger Fabric-X Loadgen** binary;
- 1 **Grafana** container;
- 1 **Prometheus** container.

The absence of the Fabric CAs is due to the fact that the crypto material is generated on the control node using `cryptogen`. As stated within the inventory itself, this deployment is not meant for Production.

### fabric-x-distributed.yaml

The [fabric-x-distributed.yaml](./inventory/fabric-x-distributed.yaml) inventory represents the following network scenario:

![fabric-x-distributed-inventory](./images/fabric-x-distributed.drawio.png)

It bootstraps a network with:

- 4 **Hyperledger Fabric-X Orderers**, each one made by:
  - 1 consenter container;
  - 1 assembler container;
  - 2 batcher containers (_horizontally scalable_);
  - 1 router container;
- 1 **Hyperledger Fabric-X Committer**, made by:
  - 1 coordinator container;
  - 1 sidecar container;
  - 1 query service container;
  - 7 validator containers (_horizontally scalable_);
  - 7 verifier containers (_horizontally scalable_);
  - 3 Yugabyte master containers (_horizontally scalable_);
  - 7 Yugabyte tablet containers (_horizontally scalable_);
- 2 **Hyperledger Fabric-X Loadgen** binaries;
- 1 **Grafana** container;
- 1 **Prometheus** container.

The absence of the Fabric CAs is due to the fact that the crypto material is generated on the control node using `cryptogen`. Thus, this deployment is not meant for Production, but for performance evaluation only.

## Playbooks

We have crafted some [playbooks](./playbooks/) that work with the groups indicated in the stated-above inventories. They make use of the playbooks coming with the collection itself.

You can either run a playbook directly using `ansible-playbook` or use the `Makefile` targets as stated in the [README.md](../README.md#1-generate-the-artifacts).

## How to replicate an horizontally scalable microservice

Replicating an horizontally scalable microservice using this collection is straightforward. All you need to do is add new entries into the reference inventory.

Let's make an example. Assume we want to add a new batcher for the `fabric_x_orderer_1` node, all you need to do is add a new `batcher` host within the node:

```yaml
# ...
fabric_x_orderer_1:
  # ...
  hosts:
    # batcher already present
    orderer-batcher-1:
      orderer_shard_id: 1
      orderer_component_type: batcher
      orderer_rpc_port: 7051
    # additional batcher
    orderer-batcher-2:
      orderer_shard_id: 2 # <- each batcher in the same node must have a unique shard ID
      orderer_component_type: batcher # <- define the orderer component type to "batcher"
      orderer_rpc_port: 7061 # <- make sure to assign a port not taken by others
```

This approach can be extended for all the other components marked as _horizontally scalable_.

## How to run a microservice on a different machine

All the inventories that are indicated in this repository run on a single machine. This is useful to quickly run a network and test its functionalities, but to achieve better performance each microservice can be run on a separate machine.

To do it, you must first switch from `ansible_connection: local` to `ansible_connection: ssh`:

```yaml
all:
  vars:
    # set the connection to ssh and make sure you can ssh from the control node to the target machines
    ansible_connection: ssh
```

Once you have done this, assign to each host the machine where to run it through the `ansible_host` variable.

Let's make an example. Assume we want to distribute the `fabric_x_orderer_1` node microservices over 4 different machines on the cloud, all you need to set is the following:

```yaml
# ...
fabric_x_orderer_1:
  # ...
  hosts:
    orderer-router-1:
      ansible_host: myremotemachine1.cloud.com # <- 1st machine on the cloud
      orderer_component_type: router
      orderer_rpc_port: 7050
    orderer-batcher-1:
      ansible_host: myremotemachine2.cloud.com # <- 2nd machine on the cloud
      orderer_shard_id: 1
      orderer_component_type: batcher
      orderer_rpc_port: 7051
    orderer-consenter-1:
      ansible_host: myremotemachine3.cloud.com # <- 3rd machine on the cloud
      orderer_component_type: consenter
      orderer_rpc_port: 7052
    orderer-assembler-1:
      ansible_host: myremotemachine4.cloud.com # <- 4th machine on the cloud
      orderer_component_type: assembler
      orderer_rpc_port: 7053
```

This approach is valid for all the microservices within the inventory.
