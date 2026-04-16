# hyperledger.fabricx.k8s

> Provides utility tasks for interacting with a Kubernetes cluster.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Tasks](#tasks)
  - [Namespace](#namespace)
    - [namespace/create](#namespacecreate)
  - [Registry](#registry)
    - [registry/create_pull_secret](#registrycreate_pull_secret)
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

### Registry

| Task                                                                    | Description                                                                                   |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [registry/create_pull_secret](./tasks/registry/create_pull_secret.yaml) | Creates an `imagePullSecret` of type `kubernetes.io/dockerconfigjson` in the target namespace |

#### registry/create_pull_secret

Creates a Kubernetes Secret for pulling images from a private registry. Idempotent - if the secret already exists it is updated in place.

Requires `k8s_image_pull_secret` to be set on the host, which is used as the secret name.

```yaml
- name: Create imagePullSecret
  vars:
    k8s_image_pull_secret: regcred
    k8s_container_registry: icr.io
    k8s_container_registry_username: iamapikey
    k8s_container_registry_password: my_api_key
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: registry/create_pull_secret
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
