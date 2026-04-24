# hyperledger.fabricx.k8s

> Provides Kubernetes helper tasks for namespaces, image pull secrets, and pod log retrieval.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [namespace/create](#namespacecreate)
  - [registry/create\_pull\_secret](#registrycreate_pull_secret)
  - [fetch\_logs](#fetch_logs)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.k8s
```

## Tasks

### namespace/create

> Ensure a Kubernetes namespace exists

Creates or updates the named Kubernetes namespace resource in the target cluster. Uses the control-node kubeconfig and the kubernetes.core collection to apply a Namespace object named by `k8s_namespace`. Skips the task when `k8s_create_namespace` is false.

```yaml
- name: Ensure a Kubernetes namespace exists
  vars:
    # Specifies the Kubernetes namespace targeted by the task. Example: `fabric-x`.
    k8s_namespace: "fabric-x"
    # Controls whether the namespace creation task applies the namespace resource. When `false`, the namespace creation task is skipped.
    k8s_create_namespace: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: namespace/create
```

### registry/create_pull_secret

> Create a Kubernetes image pull secret

Creates or updates a `kubernetes.io/dockerconfigjson` Secret named by `k8s_image_pull_secret` in the target namespace. Renders the secret from the configured registry host, username, and password for image pulls. Requires the namespace to exist and a valid kubeconfig on the control node.

```yaml
- name: Create a Kubernetes image pull secret
  vars:
    # Specifies the Kubernetes namespace targeted by the task. Example: `fabric-x`.
    k8s_namespace: "fabric-x"
    # Specifies the Kubernetes Secret name used for image pulls. Example: `regcred`.
    k8s_image_pull_secret: "regcred"
    # Specifies the container registry host recorded in the generated Docker config. Example: `icr.io`.
    k8s_container_registry: "icr.io"
    # Specifies the registry username stored in the generated image pull secret. Example: `iamapikey`.
    k8s_container_registry_username: "iamapikey"
    # Specifies the registry password or token stored in the generated image pull secret. Store this value in an Ansible Vault. Example: `my_private_cr_password`.
    k8s_container_registry_password: "my_private_cr_password"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: registry/create_pull_secret
```

### fetch_logs

> Fetch Kubernetes pod logs

Collects pod logs from the target namespace for pods matched by `k8s_pod_label_selectors`. Optionally narrows collection to `k8s_pod_container` when the selected pods expose multiple containers. Writes the collected logs to `k8s_remote_logs_dir`/`k8s_remote_logs_file` on the managed host and fetches them to `k8s_fetched_logs_dir`/`k8s_fetched_logs_file` on the control node. Continues even when no pod logs are returned so artifact retrieval still happens.

```yaml
- name: Fetch Kubernetes pod logs
  vars:
    # Specifies the Kubernetes namespace targeted by the task. Example: `fabric-x`.
    k8s_namespace: "fabric-x"
    # Specifies the Kubernetes label selectors used to select pods for log collection. Example: `['app=fabric-x-orderer', 'component=assembler']`.
    k8s_pod_label_selectors:
      - "app=fabric-x-orderer"
      - "component=assembler"
    # Optionally specifies the container name to query from multi-container pods. Example: `orderer`. When omitted, Kubernetes uses the default container.
    k8s_pod_container: "orderer"
    # Shared managed-host root directory for the remote log path. Example: `/var/tmp/fabricx`.
    remote_node_dir: "/var/tmp/fabricx"
    # Shared control-node artifact root for the fetched log directory. Example: `artifacts`.
    fetched_artifacts_dir: "artifacts"
    # Specifies the directory on the managed host where pod logs are written before transfer.
    k8s_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Specifies the filename used for pod logs on the managed host.
    k8s_remote_logs_file: logs.txt
    # Specifies the directory on the control node where fetched pod logs are stored.
    k8s_fetched_logs_dir: "{{ fetched_artifacts_dir }}/{{ inventory_hostname }}"
    # Specifies the filename used for the fetched log artifact on the control node.
    k8s_fetched_logs_file: logs.txt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: fetch_logs
```
