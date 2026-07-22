# Inventory Baselines and Topology Decisions

Read this reference only when selecting a maintained baseline or checking a
custom inventory topology. Examples are adaptation sources, not destinations:
write operator bundles outside `examples/inventory/` and do not update its
documentation or `mkdocs.yml`.

## Select the closest baseline

| Need                                              | Closest maintained inventory                                                                                    | Also inspect                                                                                                                                |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Local containers, Fabric CA, PostgreSQL, TLS/mTLS | `examples/inventory/local/fabric-x.yaml`                                                                        | `examples/inventory/local/group_vars/all/env.yaml`                                                                                          |
| Local containers with YugabyteDB                  | `examples/inventory/local/fabric-x-yugabyte.yaml`                                                               | `examples/inventory/local/group_vars/all/env.yaml`                                                                                          |
| Local, test-only centrally generated crypto       | `examples/inventory/local/fabric-x-cryptogen.yaml`                                                              | `examples/inventory/local/group_vars/all/env.yaml`                                                                                          |
| Local Fabric-X binaries                           | `examples/inventory/local/fabric-x-bin.yaml`                                                                    | `examples/inventory/local/group_vars/all/env.yaml` and `roles/orderer/meta/argument_specs.yaml`, `roles/committer/meta/argument_specs.yaml` |
| Kubernetes, Fabric CA, PostgreSQL                 | `examples/inventory/k8s/fabric-x.yaml`                                                                          | `examples/inventory/k8s/group_vars/all/env.yaml`                                                                                            |
| Kubernetes with YugabyteDB                        | `examples/inventory/k8s/fabric-x-yugabyte.yaml`                                                                 | `examples/inventory/k8s/group_vars/all/env.yaml`                                                                                            |
| Kubernetes with test-only cryptogen               | `examples/inventory/k8s/fabric-x-cryptogen.yaml`                                                                | `examples/inventory/k8s/group_vars/all/env.yaml`                                                                                            |
| Kubernetes cryptogen and YugabyteDB               | Reconcile `examples/inventory/k8s/fabric-x-cryptogen.yaml` with `examples/inventory/k8s/fabric-x-yugabyte.yaml` | Their shared `examples/inventory/k8s/group_vars/all/env.yaml` and relevant role specifications before combining variables                   |
| OpenShift with Fabric CA and PostgreSQL           | `examples/inventory/openshift/fabric-x.yaml`                                                                    | `examples/inventory/openshift/group_vars/all/env.yaml`                                                                                      |
| OpenShift with test-only cryptogen                | `examples/inventory/openshift/fabric-x-cryptogen.yaml`                                                          | `examples/inventory/openshift/group_vars/all/env.yaml`                                                                                      |
| Distributed SSH performance topology              | `examples/inventory/distributed/fabric-x.yaml`                                                                  | `examples/inventory/distributed/group_vars/all/env.yaml`                                                                                    |

For local and Kubernetes samples, select the `no-mtls` or `no-tls` variant only
when the operator expressly chooses that security posture. No TLS is a local
debugging baseline, not a production starting point. Cryptogen is test-only;
choose a Fabric CA baseline for a production certificate lifecycle.

The distributed sample has placeholder machines and is not ready to run as-is.
Obtain real SSH targets, connection details, remote paths, and a colocated-port
plan before adapting it.

## Group and component contract

Retain the selected sample's hierarchy. The normal contract is:

```text
network
├── fabric_cas                       # Fabric CA inventories only
├── fabric_x
│   ├── fabric_x_orderers
│   │   └── fabric_x_orderer_<n>
│   └── fabric_x_committers
│       └── fabric_x_committer
├── load_generators
└── monitoring
```

- An orderer group contains router, consensus, assembler, and batcher hosts;
  every host has `orderer_component_type`. Batcher replicas have a unique
  `orderer_shard_id` **within that orderer group**.
- A committer group contains the selected validator, verifier, coordinator,
  sidecar, query-service, and database hosts; every committer service host has
  `committer_component_type`.
- `fabric_cas` contains Fabric CA servers and their database hosts when Fabric
  CA creates identities. Cryptogen samples omit those CA services but still
  require consistent organization names and domains.
- A logical host can share a physical SSH target or local machine with another
  logical host. Check RPC, operations, metrics, database, and any exposed
  ports against all services on that target. In Kubernetes, check NodePorts
  against the cluster exposure scope.
- Keep references as inventory hostnames: for example database hosts, Fabric
  CA hosts, and component discovery references. Do not replace them with
  untracked ad hoc addresses.

## Required source inspection

Always read `AGENTS.md`, `examples/inventory/README.md`, the baseline inventory,
and its environment file. Then read the applicable specifications before using
variables:

| Topology element               | Required specifications                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------ |
| Orderer or committer component | `roles/orderer/meta/argument_specs.yaml`, `roles/committer/meta/argument_specs.yaml` |
| Fabric CA crypto               | `roles/fabric_ca/meta/argument_specs.yaml`                                           |
| Cryptogen test crypto          | `roles/cryptogen/meta/argument_specs.yaml`                                           |
| PostgreSQL backend             | `roles/postgres/meta/argument_specs.yaml`                                            |
| YugabyteDB backend             | `roles/yugabyte/meta/argument_specs.yaml`                                            |
| Kubernetes runtime             | `roles/k8s/meta/argument_specs.yaml` plus affected component specifications          |
| OpenShift runtime              | `roles/openshift/meta/argument_specs.yaml` plus affected component specifications    |

This inspection confirms deployment-mode support and prevents copying a
variable that the selected role does not accept.

## Safe validation of an operator bundle

Validation must parse or inspect only; it must not deploy or invoke lifecycle
Make targets. From the repository checkout, use the custom inventory path and
ask Ansible to prompt interactively when an encrypted vault is present:

```sh
ansible-inventory -i "$OUTPUT/inventory.yaml" --list --ask-vault-pass >/dev/null
ansible-inventory -i "$OUTPUT/inventory.yaml" --graph --ask-vault-pass
```

If the inventory has no vault-referenced values needed for parsing, omit
`--ask-vault-pass`. Never provide a password through command-line arguments,
environment variables, files, or chat. Inspect the generated path set and, when
working in a checkout, review `git status --short` and `git diff --check` to
confirm no maintained catalog path or `mkdocs.yml` changed.
