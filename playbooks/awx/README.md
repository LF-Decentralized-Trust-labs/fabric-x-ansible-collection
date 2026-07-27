# AWX Playbooks

The `awx` playbooks operate AWX through the same lifecycle used by the rest of this collection. AWX has no `stop` operation: an AWX Operator deployment cannot be meaningfully paused in place, so use `teardown` instead.

## Table of Contents <!-- omit in toc -->

- [Operational model](#operational-model)
- [Playbooks flow](#playbooks-flow)
- [start.yaml](#startyaml)
- [configure.yaml](#configureyaml)
- [teardown.yaml](#teardownyaml)
- [wipe.yaml](#wipeyaml)
- [backup.yaml](#backupyaml)
- [restore.yaml](#restoreyaml)
- [Accessing AWX](#accessing-awx)
- [Observing AWX](#observing-awx)

## Operational model

AWX is managed by the AWX Operator. This role installs and removes the AWX Operator as part of the AWX lifecycle on both Kubernetes and OpenShift — OpenShift support builds directly on top of the Kubernetes flow and additionally publishes an OpenShift route through `hyperledger.fabricx.openshift`. Installing the operator requires the ability to create cluster-scoped resources (CRDs, ClusterRoles, ClusterRoleBindings) in the target cluster.

The generated role README ([`roles/awx/README.md`](../../roles/awx/README.md)) documents all role variables. This playbook README explains how to operate the deployed AWX instance.

`start`, `configure`, `teardown`, and `wipe` are also folded into the same numbered wrappers under [`examples/playbooks/`](../../examples/README.md) that operate the rest of the collection, so `make start`, `make teardown`, and `make wipe` drive AWX alongside everything else in one command. This works because every component's play targets `"{{ target_hosts | default('<its own group>') }}:&<its own group>"` (AWX's own group being `awx`) — when an inventory has no `awx` group, that play simply matches zero hosts and is skipped, so bundling AWX in is harmless even against inventories that don't deploy it. `backup` and `restore` are maintenance operations without a wrapper; invoke them directly via `ansible-playbook` as shown below.

## Playbooks flow

```mermaid
flowchart LR
  START[start] --> CONFIGURE[configure]
  START --> BACKUP[backup]
  BACKUP --> RESTORE[restore]
  START --> TEARDOWN[teardown]
  TEARDOWN --> WIPE[wipe]
```

## start.yaml

[`start.yaml`](./start.yaml) starts AWX on Kubernetes or OpenShift based on inventory variables:

- `awx_use_k8s: true` uses Kubernetes resources.
- `awx_use_openshift: true` uses Kubernetes resources and publishes an OpenShift route.

```shell
ansible-playbook hyperledger.fabricx.awx.start --extra-vars '{"target_hosts": "awx"}'
```

Or, from the repository root, via [`examples/playbooks/40-start.yaml`](../../examples/playbooks/40-start.yaml):

```shell
make start
```

Properties:

- Target hosts: `awx` by default.
- For Kubernetes, define `awx_k8s_node_port` in the inventory to expose the AWX service outside the cluster.
- After a successful start, the playbook computes AWX's effective address (`tasks_from: effective_address`) and prints the URL, username, and password. The URL is derived automatically, in priority order, from the OpenShift route (`awx_openshift_route`), the Kubernetes NodePort (`awx_k8s_node_port`), or the ClusterIP port (`awx_port`) — no inventory variable needs to be set for the URL itself.

## configure.yaml

[`configure.yaml`](./configure.yaml) populates a running AWX instance so the [`examples`](../../examples/README.md) playbooks and inventories can be run from the AWX UI without any manual setup: an organization, a Git SCM project synced from this collection's repository, one inventory per `examples/inventory` family, and one job template per numbered playbook under `examples/playbooks`.

```shell
ansible-playbook hyperledger.fabricx.awx.configure --extra-vars '{"target_hosts": "awx"}'
```

Or, from the repository root, via [`examples/playbooks/40-start.yaml`](../../examples/playbooks/40-start.yaml), which imports `configure` right after `start`:

```shell
make start
```

Properties:

- Target hosts: `awx` by default. Runs after `start` on the same inventory, since it authenticates using the same admin-password Secret and computed effective address.
- Idempotent: reconciles the organization, project, inventories, and job templates through the `awx.awx` collection modules — running it again after AWX or the underlying data changes settles back to the same state instead of erroring or duplicating objects.
- The project defaults to the public collection repository (`awx_config_project_scm_url`) on the `main` branch (`awx_config_project_scm_branch`). To point at an internal/enterprise mirror instead (for example a `github.ibm.com` repository), override `awx_config_project_scm_url`/`awx_config_project_scm_branch` and add a matching `Source Control` credential entry to `awx_config_credentials`, then reference its name in `awx_config_project_scm_credential`.
- `awx_config_credentials` only covers non-machine secrets such as Source Control tokens and container-registry credentials — supply their values via vaulted vars, never commit them. Machine/SSH credentials used to reach target hosts (for example the `distributed` example family) are intentionally left out of scope: create those manually in the AWX UI so private key material is never read from disk or transmitted by this role.
- Job templates prompt for inventory and extra vars on launch (`ask_inventory_on_launch`, `ask_variables_on_launch`), mirroring the `TARGET_HOSTS`/`target_hosts` override supported by the repository `Makefile`.
- The AWX project needs `hyperledger.fabricx` (and its own dependencies) installed as collections to resolve the `hyperledger.fabricx.*` FQCN used by the `examples/playbooks` wrappers. This repository ships a [`collections/requirements.yml`](../../collections/requirements.yml) at its root for that purpose, which AWX installs automatically on every project sync; update its URL if the project points at a mirror instead of the public repository.
- That automatic install only happens if the AWX instance actually allows it. If a project sync log shows *"Collection and role syncing disabled. Check the `AWX_ROLES_ENABLED` and `AWX_COLLECTIONS_ENABLED` settings and Galaxy credentials on the project's organization."*, set `awx_config_enable_collection_sync: true` to have `configure` enable those two instance settings and attach `awx_config_galaxy_credential_names` (default: the built-in `Ansible Galaxy` credential) to the organization. This is off by default because `AWX_COLLECTIONS_ENABLED`/`AWX_ROLES_ENABLED` are instance-wide settings that affect every project on the AWX instance, not just this organization's.

## teardown.yaml

[`teardown.yaml`](./teardown.yaml) removes the AWX custom resource, its residual namespaced workloads (Deployments, StatefulSets, Jobs, Services), and the PostgreSQL/backup persistent volume claims — the next `start` reconciles a fresh database.

```shell
ansible-playbook hyperledger.fabricx.awx.teardown --extra-vars '{"target_hosts": "awx"}'
```

Or, from the repository root, via [`examples/playbooks/60-teardown.yaml`](../../examples/playbooks/60-teardown.yaml):

```shell
make teardown
```

Properties:

- Target hosts: `awx` by default.
- Never removes the namespace itself, since it may be shared with other components.
- The AWX Operator and its cluster-scoped resources are preserved (removed only by `wipe`).
- Secrets and ConfigMaps are preserved across teardown: the AWX Operator reuses the existing `<name>-secret-key` and `<name>-admin-password` Secrets on the next `start` instead of regenerating them — losing them would rotate the database encryption key and reset the admin password on every teardown/start cycle.
- One exception: `<name>-<deployment_type>-configmap` (for example `awx-awx-configmap`) is owned by the AWX custom resource via a Kubernetes owner reference, so it is garbage-collected automatically when the custom resource is deleted. This is expected and harmless: the Operator regenerates it from the AWX spec on the next `start`, and unlike the Secrets above it carries no state.

## wipe.yaml

[`wipe.yaml`](./wipe.yaml) runs the `teardown` tasks and then additionally removes AWX Secrets, ConfigMaps, the AWX Operator, its CRDs, and the rendered operator kustomization artifacts — on both Kubernetes and OpenShift, since this role manages the operator on both platforms.

```shell
ansible-playbook hyperledger.fabricx.awx.wipe --extra-vars '{"target_hosts": "awx"}'
```

Or, from the repository root, via [`examples/playbooks/100-wipe.yaml`](../../examples/playbooks/100-wipe.yaml):

```shell
make wipe
```

Properties:

- Target hosts: `awx` by default.
- Preserves the namespace, since it may be shared with other components.

## backup.yaml

[`backup.yaml`](./backup.yaml) creates an `AWXBackup` resource and waits until it reaches a terminal status. On success, it reports the backup PVC and backup directory reported by the operator.

```shell
ansible-playbook hyperledger.fabricx.awx.backup --extra-vars '{"target_hosts": "awx"}'
```

Properties:

- Target hosts: `awx` by default.
- The AWX Operator already provisions the backup persistent volume — `awx_postgres_fix_pvc_permissions` does not create or resize it. It exists because some storage provisioners (for example `local-path-provisioner`, or plain `hostPath` PVs) don't reliably apply `fsGroup`/security-context ownership on mount, so a volume ends up owned by root while the backup pod runs as UID 26 and fails to start. Default is `false`; on managed clusters `fsGroup` is normally honored and it isn't needed.

## restore.yaml

[`restore.yaml`](./restore.yaml) validates the backup, removes the target AWX resource and target PostgreSQL PVC, creates an `AWXRestore` resource, waits for the restored deployment, and computes the restored URL and admin credentials.

```shell
ansible-playbook hyperledger.fabricx.awx.restore --extra-vars '{"target_hosts": "awx"}'
```

Properties:

- Target hosts: `awx` by default.
- Set `awx_restore_name` to the same value as the source instance to restore in place and reuse the existing NodePort/route without a service port conflict.
- After a successful restore, the playbook prints the restored admin URL and password to task output.
- `awx_new_admin_credential` is only used as a fallback if the restored instance's admin-password Secret is missing a password. It has no default; supply a vaulted or otherwise secret-managed value.

## Accessing AWX

The default AWX username is `admin`. The `start` and `restore` playbooks print the admin URL and password to task output.

If you need to retrieve the password separately, read it from the AWX admin password secret.

For Kubernetes:

```shell
kubectl -n <namespace> get secret awx-admin-password -o jsonpath='{.data.password}' | base64 --decode; echo
```

For OpenShift:

```shell
oc -n <namespace> get secret awx-admin-password -o jsonpath='{.data.password}' | base64 --decode; echo
```

For restored instances, the secret name follows the restored AWX resource name:

```shell
<awx_restore_name>-admin-password
```

## Observing AWX

Use the AWX custom resource, pods, services, PVCs, and routes to understand whether the operator has reconciled the deployment.

For Kubernetes:

```shell
kubectl -n <namespace> get awx,pods,pvc,svc
kubectl -n <namespace> logs deploy/awx-operator-controller-manager -c awx-manager --tail=200
```

For OpenShift:

```shell
oc -n <namespace> get awx,pods,pvc,svc,route
oc -n <namespace> get route awx
oc -n <namespace> logs deploy/awx-operator-controller-manager -c awx-manager --tail=200
```
