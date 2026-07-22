# hyperledger.fabricx.awx

> Deploy and manage AWX on Kubernetes and OpenShift

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [data/rm](#datarm)
  - [crypto/rm](#cryptorm)
  - [config/rm](#configrm)
  - [k8s/start](#k8sstart)
  - [effective\_address](#effective_address)
  - [k8s/rm](#k8srm)
  - [k8s/data/rm](#k8sdatarm)
  - [k8s/crypto/rm](#k8scryptorm)
  - [k8s/config/rm](#k8sconfigrm)
  - [k8s/resources/fix\_backup\_pvc](#k8sresourcesfix_backup_pvc)
  - [openshift/start](#openshiftstart)
  - [openshift/rm](#openshiftrm)
  - [openshift/fix\_postgres\_pvc](#openshiftfix_postgres_pvc)
  - [backup](#backup)
  - [restore](#restore)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.awx
```

## Tasks

### start

> Start AWX

```yaml
- name: Start AWX
  vars:
    # Deploy AWX on Kubernetes
    awx_use_k8s: false
    # Deploy AWX on OpenShift
    awx_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: start
```

### teardown

> Teardown AWX

```yaml
- name: Teardown AWX
  vars:
    # Deploy AWX on Kubernetes
    awx_use_k8s: false
    # Deploy AWX on OpenShift
    awx_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: teardown
```

### wipe

> Wipe AWX

```yaml
- name: Wipe AWX
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: wipe
```

### data/rm

> Remove AWX persistent volume claims

```yaml
- name: Remove AWX persistent volume claims
  vars:
    # Deploy AWX on Kubernetes
    awx_use_k8s: false
    # Deploy AWX on OpenShift
    awx_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: data/rm
```

### crypto/rm

> Remove AWX Secrets

```yaml
- name: Remove AWX Secrets
  vars:
    # Deploy AWX on Kubernetes
    awx_use_k8s: false
    # Deploy AWX on OpenShift
    awx_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: crypto/rm
```

### config/rm

> Remove AWX ConfigMaps and Operator

```yaml
- name: Remove AWX ConfigMaps and Operator
  vars:
    # Deploy AWX on Kubernetes
    awx_use_k8s: false
    # Deploy AWX on OpenShift
    awx_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: config/rm
```

### k8s/start

> Start AWX on Kubernetes

```yaml
- name: Start AWX on Kubernetes
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Kubernetes storage class for AWX persistent volumes
    k8s_storage_class: "string"
    # Directory for rendered remote configuration artifacts
    remote_config_dir: "string"
    # Directory used to render the AWX operator kustomization
    awx_k8s_operator_kustomize_dir: "{{ remote_config_dir }}/awx-operator"
    # Timeout in seconds for Kubernetes resource apply operations
    awx_k8s_wait_timeout: 300
    # Kubernetes NodePort for AWX external access
    awx_k8s_node_port: 1000
    # Readiness polling retry count
    awx_k8s_ready_retries: 60
    # Readiness polling delay in seconds
    awx_k8s_ready_delay: 10
    # AWX Operator version Git ref
    awx_operator_version: 2.19.1
    # Replacement image repository for the AWX Operator kube-rbac-proxy sidecar
    awx_kube_rbac_proxy_image: quay.io/brancz/kube-rbac-proxy
    # Replacement image tag for the AWX Operator kube-rbac-proxy sidecar
    awx_kube_rbac_proxy_version: v0.15.0
    # Size of the PostgreSQL persistent volume
    awx_postgres_size: 8Gi
    # Size of the projects persistent volume
    awx_projects_size: 1Gi
    # Security context settings applied to the AWX Operator-managed PostgreSQL container (not the pod).
    awx_postgres_security_context_settings:
      allowPrivilegeEscalation: False
      capabilities:
        drop:
          - "ALL"
      seccompProfile:
        type: "RuntimeDefault"
    # Enable ownership workarounds for storage backends that don't apply correct PVC permissions on mount. Triggers the AWX Operator's own init-container-based fix (postgres_data_volume_init) for the PostgreSQL PVC, and this role's own pre-create-and-chown fix for the AWXBackup PVC (the Operator has no equivalent lever for that one).
    awx_postgres_fix_pvc_permissions: false
    # Optional Kubernetes container resource requests and limits, applied identically to both the AWX web and task pods.
    k8s_resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "1000m"
    # Deploy AWX on OpenShift
    awx_use_openshift: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: k8s/start
```

### effective_address

> Compute the effective AWX web address

```yaml
- name: Compute the effective AWX web address
  vars:
    # Inventory host whose AWX effective address should be computed
    awx_host: "{{ inventory_hostname }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: effective_address
```

### k8s/rm

> Remove AWX Kubernetes resources

```yaml
- name: Remove AWX Kubernetes resources
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Timeout in seconds for Kubernetes resource apply operations
    awx_k8s_wait_timeout: 300
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: k8s/rm
```

### k8s/data/rm

> Remove AWX persistent volume claims

```yaml
- name: Remove AWX persistent volume claims
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Name of the PVC used by AWXBackup when pre-creating the backup volume
    awx_backup_pvc_name: awx-backup-claim
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: k8s/data/rm
```

### k8s/crypto/rm

> Remove AWX Secrets

```yaml
- name: Remove AWX Secrets
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: k8s/crypto/rm
```

### k8s/config/rm

> Remove AWX ConfigMaps and Operator

```yaml
- name: Remove AWX ConfigMaps and Operator
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Directory for rendered remote configuration artifacts
    remote_config_dir: "string"
    # Directory used to render the AWX operator kustomization
    awx_k8s_operator_kustomize_dir: "{{ remote_config_dir }}/awx-operator"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: k8s/config/rm
```

### k8s/resources/fix_backup_pvc

> Fix AWXBackup PVC ownership

```yaml
- name: Fix AWXBackup PVC ownership
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Kubernetes storage class for AWX persistent volumes
    k8s_storage_class: "string"
    # Timeout in seconds for Kubernetes resource apply operations
    awx_k8s_wait_timeout: 300
    # Readiness polling retry count
    awx_k8s_ready_retries: 60
    # Readiness polling delay in seconds
    awx_k8s_ready_delay: 10
    # Name of the PVC used by AWXBackup when pre-creating the backup volume
    awx_backup_pvc_name: awx-backup-claim
    # Size of the AWXBackup PVC when pre-creating the backup volume
    awx_backup_pvc_size: 8Gi
    # Container image used by AWX PVC permissions fix pods
    awx_pvc_permissions_image: "quay.io/sclorg/postgresql-15-c9s:latest"
    # User ID expected to own the AWX PostgreSQL data directory
    awx_postgres_run_as_user: 26
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: k8s/resources/fix_backup_pvc
```

### openshift/start

> Start AWX on OpenShift

```yaml
- name: Start AWX on OpenShift
  vars:
    # Expose AWX routes with TLS
    awx_use_tls: true
    # OpenShift route host for AWX
    awx_openshift_route: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: openshift/start
```

### openshift/rm

> Remove AWX OpenShift resources

```yaml
- name: Remove AWX OpenShift resources
  vars:
    # OpenShift route host for AWX
    awx_openshift_route: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: openshift/rm
```

### openshift/fix_postgres_pvc

> Fix AWX PostgreSQL PVC ownership on OpenShift

```yaml
- name: Fix AWX PostgreSQL PVC ownership on OpenShift
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Timeout in seconds for Kubernetes resource apply operations
    awx_k8s_wait_timeout: 300
    # Readiness polling retry count
    awx_k8s_ready_retries: 60
    # Readiness polling delay in seconds
    awx_k8s_ready_delay: 10
    # Container image used by AWX PVC permissions fix pods
    awx_pvc_permissions_image: "quay.io/sclorg/postgresql-15-c9s:latest"
    # User ID expected to own the AWX PostgreSQL data directory
    awx_postgres_run_as_user: 26
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: openshift/fix_postgres_pvc
```

### backup

> Backup AWX instance

```yaml
- name: Backup AWX instance
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Name of AWX backup
    awx_backup_name: awx-backup
    # Enable ownership workarounds for storage backends that don't apply correct PVC permissions on mount. Triggers the AWX Operator's own init-container-based fix (postgres_data_volume_init) for the PostgreSQL PVC, and this role's own pre-create-and-chown fix for the AWXBackup PVC (the Operator has no equivalent lever for that one).
    awx_postgres_fix_pvc_permissions: false
    # Name of the PVC used by AWXBackup when pre-creating the backup volume
    awx_backup_pvc_name: awx-backup-claim
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: backup
```

### restore

> Restore AWX instance

```yaml
- name: Restore AWX instance
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Deploy AWX on OpenShift
    awx_use_openshift: false
    # Expose AWX routes with TLS
    awx_use_tls: true
    # Name of AWX backup
    awx_backup_name: awx-backup
    # Name of AWX restore instance
    awx_restore_name: awx-restore
    # OpenShift route host for the restored AWX instance
    awx_restore_openshift_route: "string"
    # New admin credential for AWX restore, used only as a fallback if the restored instance's admin-password Secret is missing a password. Has no default; supply a vaulted or otherwise secret-managed value. Only required when that fallback path is actually reached.
    awx_new_admin_credential: "string"
    # Timeout in seconds for Kubernetes resource apply operations
    awx_k8s_wait_timeout: 300
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: restore
```
