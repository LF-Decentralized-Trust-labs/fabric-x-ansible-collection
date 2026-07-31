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
  - [get\_admin\_password](#get_admin_password)
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
  - [configure](#configure)
  - [configure/organization](#configureorganization)
  - [configure/collection\_sync](#configurecollection_sync)
  - [configure/credentials](#configurecredentials)
  - [configure/project](#configureproject)
  - [configure/inventories](#configureinventories)
  - [configure/job\_templates](#configurejob_templates)

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

### get_admin_password

> Retrieve and decode the AWX admin password Secret

```yaml
- name: Retrieve and decode the AWX admin password Secret
  vars:
    # Kubernetes namespace for AWX resources
    k8s_namespace: "string"
    # Name of the Secret holding the AWX admin password.
    awx_admin_password_secret_name: awx-admin-password
    # Readiness polling retry count while waiting for the admin password Secret.
    awx_admin_password_retries: "{{ awx_k8s_ready_retries }}"
    # Readiness polling delay in seconds while waiting for the admin password Secret.
    awx_admin_password_delay: "{{ awx_k8s_ready_delay }}"
    # Wait for the `password` key to appear in the Secret, not just for the Secret to exist. Disabled during restore, where a missing `password` key is a legitimate outcome handled by a fallback reset rather than a wait condition.
    awx_admin_password_require_password: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: get_admin_password
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

### configure

> Populate a running AWX with the Fabric-X examples project, inventories, and job templates

```yaml
- name: Populate a running AWX with the Fabric-X examples project, inventories, and job templates
  vars:
    # AWX/Controller username used to authenticate configuration requests.
    awx_config_controller_username: admin
    # Validate TLS certificates when talking to the AWX/Controller API. Left disabled by default because the AWX Operator's default web certificate is self-signed.
    awx_config_validate_certs: false
    # Enable the `AWX_COLLECTIONS_ENABLED`/`AWX_ROLES_ENABLED` instance settings and attach `awx_config_galaxy_credential_names` to the organization, so the project's `collections/requirements.yml` actually gets installed on sync. Off by default: `AWX_COLLECTIONS_ENABLED`/`AWX_ROLES_ENABLED` are AWX instance-wide settings, not scoped to this organization, so enabling this affects every project on the AWX instance, not just this one.
    awx_config_enable_collection_sync: false
    # Credential objects created before the project and job templates. Each item is passed to `awx.awx.credential` (`name`, `credential_type`, optional `organization`, optional `inputs`). Use this for Source Control tokens (private/enterprise repositories) and container-registry credentials. Machine/SSH credentials used to reach target hosts are intentionally out of scope: create those manually in the AWX UI so private key material is never read or transmitted by this role.
    awx_config_credentials:
      - name: "GHE Fabric-X Token"
        credential_type: "Source Control"
        inputs:
          username: "svc-fabricx"
          password: "REPLACE_WITH_VAULTED_TOKEN"
    # Inventories created from the AWX project, one per `examples/inventory` family. Each item is passed to `awx.awx.inventory` and `awx.awx.inventory_source` (`name`, optional `description`, `source_path`, optional `credential` name of a machine/SSH credential created manually in the AWX UI). This list is not discovered automatically; it is kept in sync by hand with `examples/inventory`. Add, rename, or remove an entry here when a family is added, renamed, or removed there.
    awx_config_inventories:
      - name: Fabric-X - local
        source_path: examples/inventory/local/fabric-x.yaml
      - name: Fabric-X - k8s
        source_path: examples/inventory/k8s/fabric-x.yaml
      - name: Fabric-X - openshift
        source_path: examples/inventory/openshift/fabric-x.yaml
      - name: Fabric-X - distributed
        source_path: examples/inventory/distributed/fabric-x.yaml
    # Job templates created for the numbered example playbooks under `examples/playbooks/`. Each item is passed to `awx.awx.job_template` (`name`, `playbook`, optional `inventory`, optional `extra_vars`, optional `credentials`). `ask_inventory_on_launch` and `ask_variables_on_launch` are always enabled so operators can pick a different example family or override `extra_vars` such as `target_hosts` at launch time, mirroring the `TARGET_HOSTS` override supported by the repository Makefile. This list is not discovered automatically; it is kept in sync by hand with `examples/playbooks`. Add, rename, or remove an entry here when a numbered playbook is added, renamed, or removed there.
    awx_config_job_templates:
      - name: Fabric-X - Binaries
        playbook: examples/playbooks/10-binaries.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Generate Crypto
        playbook: examples/playbooks/20-generate-crypto.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Build Genesis Block
        playbook: examples/playbooks/21-build-genesis-block.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Configs
        playbook: examples/playbooks/30-configs.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Start
        playbook: examples/playbooks/40-start.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Init
        playbook: examples/playbooks/41-init.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Stop
        playbook: examples/playbooks/50-stop.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Teardown
        playbook: examples/playbooks/60-teardown.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Ping
        playbook: examples/playbooks/70-ping.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Get Metrics
        playbook: examples/playbooks/93-get-metrics.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Fetch Crypto
        playbook: examples/playbooks/95-fetch-crypto.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Fetch Logs
        playbook: examples/playbooks/96-fetch-logs.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Wipe
        playbook: examples/playbooks/100-wipe.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Hard Wipe
        playbook: examples/playbooks/110-hard-wipe.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Run Command
        playbook: examples/playbooks/999-run-command.yaml
        inventory: Fabric-X - k8s
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: configure
```

### configure/organization

> Ensure the AWX organization exists

```yaml
- name: Ensure the AWX organization exists
  vars:
    # Name of the AWX organization that owns the Fabric-X examples project, credentials, inventories, and job templates.
    awx_config_organization_name: Fabric-X
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: configure/organization
```

### configure/collection_sync

> Enable AWX collection/role syncing and attach Galaxy credentials to the organization

```yaml
- name: Enable AWX collection/role syncing and attach Galaxy credentials to the organization
  vars:
    # Name of the AWX organization that owns the Fabric-X examples project, credentials, inventories, and job templates.
    awx_config_organization_name: Fabric-X
    # Names of existing Galaxy-type credentials to attach to the organization so it can install collections/roles from them. Only used when `awx_config_enable_collection_sync` is enabled. Defaults to the built-in `Ansible Galaxy` credential AWX ships pointing at `galaxy.ansible.com`.
    awx_config_galaxy_credential_names:
      - Ansible Galaxy
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: configure/collection_sync
```

### configure/credentials

> Ensure AWX credentials exist

```yaml
- name: Ensure AWX credentials exist
  vars:
    # Credential objects created before the project and job templates. Each item is passed to `awx.awx.credential` (`name`, `credential_type`, optional `organization`, optional `inputs`). Use this for Source Control tokens (private/enterprise repositories) and container-registry credentials. Machine/SSH credentials used to reach target hosts are intentionally out of scope: create those manually in the AWX UI so private key material is never read or transmitted by this role.
    awx_config_credentials:
      - name: "GHE Fabric-X Token"
        credential_type: "Source Control"
        inputs:
          username: "svc-fabricx"
          password: "REPLACE_WITH_VAULTED_TOKEN"
    # Name of the AWX organization that owns the Fabric-X examples project, credentials, inventories, and job templates.
    awx_config_organization_name: Fabric-X
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: configure/credentials
```

### configure/project

> Ensure the AWX Fabric-X examples project exists

```yaml
- name: Ensure the AWX Fabric-X examples project exists
  vars:
    # Name of the AWX organization that owns the Fabric-X examples project, credentials, inventories, and job templates.
    awx_config_organization_name: Fabric-X
    # Name of the AWX project synced from `awx_config_project_scm_url`.
    awx_config_project_name: Fabric-X Examples
    # SCM type used for the AWX project.
    awx_config_project_scm_type: git
    # Git URL of the repository synced into the AWX project. Point this at an internal/enterprise mirror (for example a github.ibm.com repository) together with `awx_config_project_scm_credential` when the public repository is not reachable from AWX.
    awx_config_project_scm_url: "https://github.com/LF-Decentralized-Trust-labs/fabric-x-ansible-collection.git"
    # Git branch, tag, or commit synced into the AWX project.
    awx_config_project_scm_branch: main
    # Name of a Source Control credential (see `awx_config_credentials`) to attach to the project. Required for private or enterprise repositories such as github.ibm.com; leave unset for the public repository.
    awx_config_project_scm_credential: "string"
    # Refresh the project from its SCM source before launching a job that uses it.
    awx_config_project_scm_update_on_launch: true
    # Wait for the project's initial SCM sync to finish before creating inventories and job templates against it.
    awx_config_project_wait: true
    # Seconds to wait for the project's initial SCM sync (see `awx_config_project_wait`).
    awx_config_project_wait_timeout: 120
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: configure/project
```

### configure/inventories

> Ensure AWX inventories and their SCM inventory sources exist

```yaml
- name: Ensure AWX inventories and their SCM inventory sources exist
  vars:
    # Name of the AWX organization that owns the Fabric-X examples project, credentials, inventories, and job templates.
    awx_config_organization_name: Fabric-X
    # Name of the AWX project synced from `awx_config_project_scm_url`.
    awx_config_project_name: Fabric-X Examples
    # Inventories created from the AWX project, one per `examples/inventory` family. Each item is passed to `awx.awx.inventory` and `awx.awx.inventory_source` (`name`, optional `description`, `source_path`, optional `credential` name of a machine/SSH credential created manually in the AWX UI). This list is not discovered automatically; it is kept in sync by hand with `examples/inventory`. Add, rename, or remove an entry here when a family is added, renamed, or removed there.
    awx_config_inventories:
      - name: Fabric-X - local
        source_path: examples/inventory/local/fabric-x.yaml
      - name: Fabric-X - k8s
        source_path: examples/inventory/k8s/fabric-x.yaml
      - name: Fabric-X - openshift
        source_path: examples/inventory/openshift/fabric-x.yaml
      - name: Fabric-X - distributed
        source_path: examples/inventory/distributed/fabric-x.yaml
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: configure/inventories
```

### configure/job_templates

> Ensure AWX job templates for the numbered example playbooks exist

```yaml
- name: Ensure AWX job templates for the numbered example playbooks exist
  vars:
    # Name of the AWX organization that owns the Fabric-X examples project, credentials, inventories, and job templates.
    awx_config_organization_name: Fabric-X
    # Name of the AWX project synced from `awx_config_project_scm_url`.
    awx_config_project_name: Fabric-X Examples
    # Job templates created for the numbered example playbooks under `examples/playbooks/`. Each item is passed to `awx.awx.job_template` (`name`, `playbook`, optional `inventory`, optional `extra_vars`, optional `credentials`). `ask_inventory_on_launch` and `ask_variables_on_launch` are always enabled so operators can pick a different example family or override `extra_vars` such as `target_hosts` at launch time, mirroring the `TARGET_HOSTS` override supported by the repository Makefile. This list is not discovered automatically; it is kept in sync by hand with `examples/playbooks`. Add, rename, or remove an entry here when a numbered playbook is added, renamed, or removed there.
    awx_config_job_templates:
      - name: Fabric-X - Binaries
        playbook: examples/playbooks/10-binaries.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Generate Crypto
        playbook: examples/playbooks/20-generate-crypto.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Build Genesis Block
        playbook: examples/playbooks/21-build-genesis-block.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Configs
        playbook: examples/playbooks/30-configs.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Start
        playbook: examples/playbooks/40-start.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Init
        playbook: examples/playbooks/41-init.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Stop
        playbook: examples/playbooks/50-stop.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Teardown
        playbook: examples/playbooks/60-teardown.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Ping
        playbook: examples/playbooks/70-ping.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Get Metrics
        playbook: examples/playbooks/93-get-metrics.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Fetch Crypto
        playbook: examples/playbooks/95-fetch-crypto.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Fetch Logs
        playbook: examples/playbooks/96-fetch-logs.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Wipe
        playbook: examples/playbooks/100-wipe.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Hard Wipe
        playbook: examples/playbooks/110-hard-wipe.yaml
        inventory: Fabric-X - k8s
      - name: Fabric-X - Run Command
        playbook: examples/playbooks/999-run-command.yaml
        inventory: Fabric-X - k8s
  ansible.builtin.include_role:
    name: hyperledger.fabricx.awx
    tasks_from: configure/job_templates
```
