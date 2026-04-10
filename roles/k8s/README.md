# hyperledger.fabricx.k8s

The role `hyperledger.fabricx.k8s` provides utility tasks for interacting with a Kubernetes cluster. It is used as a shared helper by other roles that deploy resources to Kubernetes (e.g. `orderer`, `postgres`).

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Variables](#variables)
- [Tasks](#tasks)
  - [namespace/create](#namespacecreate)

## Prerequisites

The role requires:

- `kubernetes.core` collection to be installed;
- A valid `kubeconfig` accessible from the control node.

## Variables

| Variable        | Default | Description                              |
| --------------- | ------- | ---------------------------------------- |
| `k8s_namespace` | —       | Name of the Kubernetes namespace to use. |

## Tasks

### namespace/create

The task `namespace/create` ensures a Kubernetes namespace exists. It is idempotent — if the namespace already exists it is left unchanged.

```yaml
- name: Ensure Kubernetes namespace exists
  vars:
    k8s_namespace: fabric-x
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: namespace/create
```
