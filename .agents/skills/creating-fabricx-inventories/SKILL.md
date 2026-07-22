---
name: creating-fabricx-inventories
description: Use when creating, adapting, or reviewing a custom Hyperledger Fabric-X Ansible inventory for local, Kubernetes, OpenShift, or distributed deployment, including topology, crypto, database, TLS, host placement, ports, or encrypted inventory secrets.
compatibility: Requires repository access, Ansible tooling, and an interactive terminal for Ansible Vault secret entry.
---

# Creating Fabric-X Inventories

Create a **user-owned operator bundle**, not a contribution to the maintained
example catalog. The completed bundle contains:

- a main inventory;
- `group_vars/all/env.yaml`;
- encrypted `group_vars/all/vault.yaml`; and
- an operator README that records the selected baseline, decisions, validation,
  and remaining operator actions.

Do not create the final bundle until its topology summary is confirmed.

## Required workflow

1. **Choose the output safely.** Ask for a user-owned output path. Check whether
   it exists and do not overwrite any file without explicit confirmation. Keep
   all generated files outside `examples/inventory/`.
2. **Read before adapting.** Read the repository `AGENTS.md`,
   `examples/inventory/README.md`, and the selected maintained inventory with
   its `group_vars/all/env.yaml`. When selecting the baseline, consult the
   [inventory decision reference](references/inventory-decisions.md).
3. **Ask progressive decisions.** Ask exactly one unresolved topology question
   at a time. Do not infer a production topology from a sample or begin writing
   while decisions are unresolved. Work through, in this order:
   1. deployment family and supported runtime (local, Kubernetes, OpenShift, or
      distributed);
   2. crypto source (Fabric CA or test-only cryptogen), TLS, and mTLS;
   3. organizations, domains, and component scale;
   4. physical target/namespace, storage, and externally reachable addresses;
   5. database backend and optional services;
   6. placement of every logical service, including colocations; and
   7. ports, NodePorts, and orderer batcher shard IDs.

   Skip a question only when the operator already answered it unambiguously.
   For distributed targets, obtain the actual SSH-target map and port plan;
   unique logical hostnames alone do not prevent collisions.

4. **Inspect interfaces before variables.** Before copying or introducing a
   role variable, read the relevant `roles/<role>/meta/argument_specs.yaml`.
   Inspect `orderer` and `committer` for Fabric-X components; also inspect the
   selected crypto, database, and runtime roles (for example `fabric_ca`,
   `cryptogen`, `postgres`, `yugabyte`, `k8s`, or `openshift`). Use only the
   selected role's supported deployment mode and variables.
5. **Summarize and confirm.** Present the intended source sample, runtime,
   crypto and security posture, organizations, component/target map, database,
   externally exposed addresses, and complete port/shard plan. Obtain explicit
   confirmation before generating files.
6. **Audit credentials before generating.** Audit the selected inventory and
   its environment file for every credential or secret. Before writing the
   operator bundle, replace each copied plaintext credential with a
   `{{ vault_* }}` variable reference in the inventory or environment file.
   Record only the resulting Vault variable names in the operator README; do
   not copy example credential values, even known sample values.
7. **Generate by adapting, not inventing.** Copy the selected inventory's
   group structure and environment contract into the user-owned bundle only
   after the credential audit and replacements are complete, then make only
   the confirmed changes. Preserve comments that identify operator actions and
   record deviations in the operator README.
8. **Create secrets only in Vault.** Require an interactive terminal before
   creating `group_vars/all/vault.yaml`. The assistant must never request,
   receive, echo, log, place in a command, or temporarily store a Vault
   password or credential value. Create the encrypted file with:

   ```sh
   ansible-vault create "$OUTPUT/group_vars/all/vault.yaml"
   ```

   The operator enters the Vault password and every audited credential value
   solely in the interactive editor. The main inventory and environment file
   retain only their `{{ vault_* }}` references. Document secret **variable
   names** only, never values. If an interactive terminal is unavailable, stop
   the Vault step and provide this command for the operator to run later; do
   not create a plaintext substitute or ask for secrets in chat.

9. **Parse and review without deployment.** Run these safe checks, with an
   interactive Vault prompt where an encrypted vault exists:

   ```sh
   ansible-inventory -i "$OUTPUT/inventory.yaml" --list --ask-vault-pass >/dev/null
   ansible-inventory -i "$OUTPUT/inventory.yaml" --graph --ask-vault-pass
   ```

   If no vault-referenced value is needed to parse the inventory, omit
   `--ask-vault-pass`. Never provide a password through command-line arguments,
   environment variables, files, or chat. Review the bundle paths and
   diff/status to confirm that `examples/inventory/`, its documentation, and
   `mkdocs.yml` are unchanged. Report validation outcomes and remaining manual
   operator actions.

## Inventory contracts to preserve

- Keep the standard groups from the selected sample unless the operator
  explicitly confirms an intentional replacement: `network`, `fabric_cas`
  (when Fabric CA is used), `fabric_x`, `fabric_x_orderers`,
  `fabric_x_committers`, `fabric_x_committer`, `load_generators`, and
  `monitoring`.
- Every Fabric-X component host uses its dispatcher variable:
  `orderer_component_type` for orderers and `committer_component_type` for
  committers. Preserve the selected sample's component hierarchy and parent
  group membership.
- Keep logical inventory hostnames unique. Resolve every host reference to an
  inventory hostname, including Fabric CA/database hosts and cross-component
  references. Keep organization name, domain, role, crypto source, and service
  ownership consistent throughout the topology.
- Check every port and exposed NodePort for uniqueness on its **physical
  target** or cluster exposure scope. For a batcher replica, check that
  `orderer_shard_id` is unique within its intended orderer group, not globally.
- Preserve runtime environment variables from the selected family, including
  its target connection model and paths such as `remote_deploy_dir`,
  `remote_node_dir`, `remote_config_dir`, and `remote_data_dir` where
  applicable.
- Check cross-role dependencies: Fabric CA or cryptogen artifacts exist before
  orderer/committer configuration; the committer backend agrees with its
  PostgreSQL or YugabyteDB hosts; the coordinator can resolve assembler hosts;
  Kubernetes resources agree on namespace, storage, and externally reachable
  NodePort address; and optional explorer/monitoring references resolve to the
  owning inventory hosts.

## Non-negotiable safety boundaries

- Never edit `examples/inventory/`, inventory documentation, or `mkdocs.yml`
  for an operator artifact. Do not register it as a maintained example.
- Never handle plaintext credentials or replace encrypted Vault data with an
  unencrypted file.
- Do not run deployment or lifecycle targets, including `make start`,
  `make stop`, `make teardown`, `make wipe`, or other target actions that
  create, alter, or remove network resources.
- Do not run `make lint` unless the user directly requests it.

## Completion report

State the output path, source sample(s), confirmed topology, files created,
Vault interaction status without secret values, commands and results, catalog
exclusion review, and remaining operator actions. If a required decision,
interactive Vault terminal, or safe parse prerequisite is unavailable, report
that blocker rather than guessing or deploying.
