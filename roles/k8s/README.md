# hyperledger.fabricx.k8s

> Provides utility tasks for interacting with a Kubernetes cluster.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [namespace/create](#namespacecreate)
  - [registry/create_pull_secret](#registrycreate_pull_secret)
  - [fetch_logs](#fetch_logs)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### namespace/create

Ensure a Kubernetes namespace exists

Ensures the target Kubernetes namespace is present in the cluster.

Requires a valid kubeconfig on the control node and the kubernetes.core collection.

```yaml
- name: Ensure a Kubernetes namespace exists
  vars:
    # Specifies the Kubernetes namespace managed by the task. Example: `fabric-x`.
    k8s_namespace: "string"
    # Controls whether the namespace creation task applies the namespace resource. When `false`, the namespace creation task is skipped.
    k8s_create_namespace: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: namespace/create
```

### registry/create_pull_secret

Create a Kubernetes image pull secret

Creates or updates a Docker registry imagePullSecret in the target namespace.

Renders a kubernetes.io/dockerconfigjson secret from the configured registry credentials.

```yaml
- name: Create a Kubernetes image pull secret
  vars:
    # Specifies the Kubernetes namespace managed by the task. Example: `fabric-x`.
    k8s_namespace: "string"
    # Specifies the name of the Kubernetes Secret used for image pulls. Example: `regcred`.
    k8s_image_pull_secret: "string"
    # Specifies the container registry host recorded in the generated Docker config. Example: `icr.io`.
    k8s_container_registry: "string"
    # Specifies the username stored in the generated image pull secret. Example: `iamapikey`.
    k8s_container_registry_username: "string"
    # Specifies the password or token stored in the generated image pull secret. This value should be stored in an Ansible Vault.
    k8s_container_registry_password: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: registry/create_pull_secret
```

### fetch_logs

Fetch Kubernetes pod logs

Collects pod logs selected by label from the target namespace, writes them on the managed host, and fetches them back to the control node.

Log collection tolerates missing pods or missing log content and still attempts artifact retrieval.

```yaml
- name: Fetch Kubernetes pod logs
  vars:
    # Specifies the Kubernetes namespace managed by the task. Example: `fabric-x`.
    k8s_namespace: "string"
    # Specifies the label selectors passed to the Kubernetes log query. Example: `['app=fabric-x-orderer']`.
    k8s_pod_label_selectors: ["entry1", "entry2"]
    # Optionally specifies the container name to query from multi-container pods. When omitted, Kubernetes uses the default container.
    k8s_pod_container: "string"
    # Shared managed-host root directory used to derive the remote log path.
    remote_node_dir: "string"
    # Shared control-node artifact root used to derive the fetched log directory.
    fetched_artifacts_dir: "string"
    # Specifies the directory on the managed host where pod logs are written before transfer. The default derives from `remote_node_dir`.
    k8s_remote_logs_dir: "{{ remote_node_dir }}/logs"
    # Specifies the filename used for pod logs on the managed host.
    k8s_remote_logs_file: logs.txt
    # Specifies the directory on the control node where fetched pod logs are stored. The default derives from `fetched_artifacts_dir` and `inventory_hostname`.
    k8s_fetched_logs_dir: "{{ fetched_artifacts_dir }}/{{ inventory_hostname }}"
    # Specifies the filename used for the fetched log artifact on the control node.
    k8s_fetched_logs_file: logs.txt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.k8s
    tasks_from: fetch_logs
```
