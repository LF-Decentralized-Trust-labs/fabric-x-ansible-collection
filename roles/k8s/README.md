# hyperledger.fabricx.k8s

> Provides utility tasks for interacting with a Kubernetes cluster.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Namespace](#namespace)
    - [namespace/create](#namespacecreate)
- [Variables](#variables)

## Prerequisites

- `kubernetes.core` collection to be installed
- A valid `kubeconfig` accessible from the control node

## Tasks

### Namespace

| Task                                              | Description              |
| ------------------------------------------------- | ------------------------ |
| [namespace/create](./tasks/namespace/create.yaml) | Ensures namespace exists |

#### namespace/create

Ensures a Kubernetes namespace exists. Idempotent — if the namespace already exists it is left unchanged.

```yaml
- name: Ensure Kubernetes namespace exists
  vars:
    k8s_namespace: fabric-x
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: namespace/create
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
