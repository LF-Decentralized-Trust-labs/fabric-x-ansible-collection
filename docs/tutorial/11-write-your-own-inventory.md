# 11. Write Your Own Inventory

The capstone. You have read the sample inventories, changed one, and switched families. Now build one from nothing: a minimal Fabric-X network of your own design, in your own directory, that the collection deploys with the same three commands as everything else.

> [!NOTE]
> Estimated time: 60 minutes. Builds on everything from [5. Read the Inventory](./05-read-the-inventory.md) onwards.

## Table of Contents <!-- omit in toc -->

- [What You Will Learn](#what-you-will-learn)
- [Keep Your Inventory Out of `examples/`](#keep-your-inventory-out-of-examples)
- [The Bundle Layout](#the-bundle-layout)
- [The Ten Authoring Rules](#the-ten-authoring-rules)
- [Step 1: The Environment File](#step-1-the-environment-file)
- [Step 2: Control-Node Paths](#step-2-control-node-paths)
- [Step 3: Organizations](#step-3-organizations)
- [Step 4: The Orderer Group](#step-4-the-orderer-group)
- [Step 5: The Committer](#step-5-the-committer)
- [Step 6: The Load Generator](#step-6-the-load-generator)
- [The Complete Inventory](#the-complete-inventory)
- [Deploy It](#deploy-it)
- [Where to Go From Here](#where-to-go-from-here)
- [Exercise](#exercise)
- [Next](#next)

## What You Will Learn

- Where a custom inventory should live, and why not in `examples/`.
- The non-obvious file that every inventory bundle needs and no documentation page spells out.
- How to build a minimal but complete Fabric-X topology from scratch.
- How to validate an inventory before deploying it.

## Keep Your Inventory Out of `examples/`

In [lesson 8](./08-change-the-topology.md) you copied a sample into `examples/inventory/local/` because it was convenient. For real work, do not.

`examples/inventory/` is the **maintained example catalog**. It is documented, referenced by `mkdocs.yml`, and covered by the repository's checks. Anything you put there will conflict on your next `git pull`, and it invites confusion about which inventories are yours.

Your inventory is an **operator bundle**: a self-contained directory you own, kept anywhere outside the example catalog. For this lesson:

```shell
mkdir -p my-network/group_vars/all
```

> [!TIP]
> The repository has an agent skill, `.agents/skills/creating-fabricx-inventories`, that walks a compatible AI assistant through this same process interactively — including auditing credentials into an Ansible Vault file, which this lesson does not cover. Worth knowing about once you move past a learning exercise.

## The Bundle Layout

Here is the layout, and one file in it is the thing people get wrong:

```text
my-network/
├── fabric-x-minimal.yaml          # the inventory
└── group_vars/
    └── all/
        ├── env.yaml               # connection model and target paths
        └── vars.yaml              # control-node paths and channel_id
```

The `group_vars/all/vars.yaml` file is the non-obvious one. Every sample family has it, and in each case it is a **symlink**:

```shell
ls -l examples/inventory/local/group_vars/all/
# env.yaml
# vars.yaml -> ../../../vars.yaml
```

That symlink is how `project_dir`, `out_dir`, `control_node_dir`, `cryptogen_artifacts_dir`, and `channel_id` reach the playbooks. Nothing else loads [`examples/inventory/vars.yaml`](../../examples/inventory/vars.yaml) — not `ansible.cfg`, not a `vars_files` entry. Ansible picks it up purely because it sits in `group_vars/all/` next to the inventory.

Omit it and your deployment fails on an undefined `out_dir` before it does anything useful. So create it first, either as a symlink:

```shell
ln -s ../../../examples/inventory/vars.yaml my-network/group_vars/all/vars.yaml
```

or as a copy you then own and can change:

```shell
cp examples/inventory/vars.yaml my-network/group_vars/all/vars.yaml
```

Copy it if you want your own `channel_id` or `out_dir`; symlink it if you want to track the repository's defaults.

## The Ten Authoring Rules

Before writing anything, here are the rules from the [Inventory Guide](../../examples/inventory/README.md), which are worth having in front of you:

1. **Hostnames stable and unique.** They become container names, certificate names, output directories, and `Makefile` targets.
2. **Keep the standard parent groups** unless you are replacing the playbook layer too.
3. **Set the dispatcher variable on every component host** — `orderer_component_type` or `committer_component_type`.
4. **Unique ports for colocated services.**
5. **Group variables for policy** — TLS, mTLS, runtime mode, shared organisation data.
6. **Host variables for facts** — RPC ports, metrics ports, shard IDs, database references.
7. **Reference services by inventory hostname**, never by ad hoc address.
8. **Define organisations consistently.** Fabric CA inventories need `fabric_ca_host` and enrollment data; `cryptogen` inventories still need names and domains.
9. **Preserve the family's path variables** — `remote_deploy_dir`, `remote_node_dir`, `remote_config_dir`, `remote_data_dir`.
10. **Run `make targets`** after adding, removing, or renaming hosts.

And the test to apply when you are done: pick any host and you should be able to say what service it runs, where it runs, which organisation owns it, how other services reach it, and where its files will be written.

## Step 1: The Environment File

Start with the environment, because it decides _where_ before you decide _what_. This is a local deployment, so copy the local family's model:

```yaml
# my-network/group_vars/all/env.yaml
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# =========================
# Ansible Connection
# =========================
ansible_connection: local
ansible_user: "{{ lookup('env', 'USER') }}"
ansible_host: "{{ lookup('env', 'LOCAL_ANSIBLE_HOST') or 'localhost' }}"
actual_host: "{{ ansible_host }}"

# =========================
# Remote Node Paths
# =========================
remote_deploy_dir: "{{ out_dir }}/my-network-deployment"
remote_node_dir: "{{ remote_deploy_dir }}/{{ inventory_hostname }}"
remote_config_dir: "{{ remote_node_dir }}/config"
remote_data_dir: "{{ remote_node_dir }}/data"
```

Only `remote_deploy_dir` differs from the shipped local file, so your deployment writes to its own directory and cannot collide with a sample deployment's state.

> [!NOTE]
> Every YAML file in this repository carries the Apache-2.0 license header, and CI enforces it on tracked `.yaml` files. Your own bundle is not part of the repository, but the header costs nothing and keeps the habit.

## Step 2: Control-Node Paths

As covered above:

```shell
cp examples/inventory/vars.yaml my-network/group_vars/all/vars.yaml
```

Leave the contents alone. In particular, **do not change `channel_id`**.

> [!WARNING]
> `channel_id: arma` looks like a name you get to pick. It is not. The channel name is currently hardcoded in the Fabric-X orderer — `config/generate/config_block_gen.go` and `common/tools/armageddon/cryptogen.go` both use the literal `"arma"`, and `node/ledger/assembler_ledger.go` carries the comment _"this will change when we'll support configurable channel name"_.
>
> So the variable exists, and the generated artifacts will faithfully use whatever you set — but the orderer will be looking for `arma`, and the deployment will not work. Keep it as it is until configurable channel names land upstream.

This is worth pausing on, because it generalises: an inventory variable existing does not mean every value of it is supported. The authoritative answer for any given variable is the role's `meta/argument_specs.yaml`, and — for anything that reaches a Fabric-X binary — the component's own source.

## Step 3: Organizations

Design decision time. The baseline sample uses five organisations — four owning an orderer group each, plus `Org1`. For a minimal network, use **two**: one that owns the ordering service and one that owns the committer and the client.

To keep the bundle small, skip Fabric CA and use `cryptogen`. That removes ten containers and, per [lesson 8](./08-change-the-topology.md), is the right choice for a learning exercise as long as you remember it is not a certificate lifecycle.

```yaml
all:
  vars:
    # cryptogen and the control-plane CLIs run as binaries on the control node
    cryptogen_use_bin: true
    armageddon_use_bin: true
    configtxgen_use_bin: true
    fxconfig_use_bin: true

    # =========================
    # Organizations
    # =========================
    organizations:
      orderer_org_1: &OrdererOrg1
        name: OrdererOrg1
        domain: ordererorg1.example.com
      org1: &Org1
        name: Org1
        domain: org1.example.com
```

Note the anchors. `&OrdererOrg1` and `&Org1` are defined once here and merged in with `<<:` wherever they are needed — rule 8.

## Step 4: The Orderer Group

One orderer group with the four required services. An ordering service needs all four component types; you cannot omit one.

> [!WARNING]
> **One orderer group is a teaching topology, not a viable one.** Fabric-X ordering is Byzantine-fault-tolerant, and the orderer derives its fault tolerance from the number of parties as `f = (n - 1) / 3`. With one party, `f = 0` — the network tolerates **no** faulty or unavailable orderer at all, and a single consenter going down stops ordering entirely.
>
> The minimum for real BFT is **4 orderer organisations** (`n = 4`, `f = 1`), which is exactly why every shipped sample uses four. Use one group here to keep the bundle small enough to read in one sitting, then scale to four before the inventory means anything — it is the first item in [Where to Go From Here](#where-to-go-from-here) for that reason.
>
> Note also that this is a _genesis-level_ property: the party set is encoded in the genesis block, so going from one group to four is `make teardown wipe` and a fresh ledger, not a restart. Plan for four early rather than discovering this later.

```yaml
    network:
      children:
        fabric_x:
          children:
            fabric_x_orderers:
              vars:
                orderer_use_tls: true
                orderer_use_mtls: true
                orderer_operations_mtls_clients:
                  - prometheus
              children:
                fabric_x_orderer_1:
                  vars:
                    organization:
                      <<: *OrdererOrg1
                      role: orderer
                    orderer_group: 1
                  hosts:
                    orderer-router-1:
                      orderer_component_type: router
                      orderer_rpc_port: 7050
                      orderer_operations_port: 7060
                    orderer-consenter-1:
                      orderer_component_type: consensus
                      orderer_rpc_port: 7051
                      orderer_operations_port: 7061
                    orderer-assembler-1:
                      orderer_component_type: assembler
                      orderer_rpc_port: 7052
                      orderer_operations_port: 7062
                    orderer-batcher-1:
                      orderer_component_type: batcher
                      orderer_shard_id: 1
                      orderer_rpc_port: 7053
                      orderer_operations_port: 7063
```

Compare against the sample and notice what is _missing_: no `fabric_ca_host`, and no `orderer:` enrollment block. Those are Fabric CA concepts, and this is a `cryptogen` inventory. The organisation still needs `name`, `domain`, and `role` so certificate material and channel configuration can be generated — rule 8 again.

## Step 5: The Committer

The committer needs all five services plus a database. None of them is optional: no coordinator means no work distribution, no sidecar means no block intake.

```yaml
            fabric_x_committers:
              children:
                fabric_x_committer:
                  vars:
                    committer_use_tls: true
                    committer_use_mtls: true
                    committer_monitoring_mtls_clients:
                      - prometheus
                    organization:
                      <<: *Org1
                      role: peer
                  hosts:
                    committer-db:
                      postgres_user: sc_user
                      postgres_password: sc_secret_pwd
                      postgres_db: sc_db
                      postgres_port: 5150
                      postgres_use_tls: true
                    committer-validator:
                      committer_component_type: validator
                      committer_rpc_port: 5100
                      committer_metrics_port: 5200
                      postgres_db_host: committer-db
                    committer-verifier:
                      committer_component_type: verifier
                      committer_rpc_port: 5110
                      committer_metrics_port: 5210
                    committer-coordinator:
                      committer_component_type: coordinator
                      committer_rpc_port: 5120
                      committer_metrics_port: 5220
                    committer-sidecar:
                      committer_component_type: sidecar
                      committer_rpc_port: 5130
                      committer_metrics_port: 5230
                    committer-query-service:
                      committer_component_type: query-service
                      committer_rpc_port: 5140
                      committer_metrics_port: 5240
                      postgres_db_host: committer-db
```

`postgres_db_host` appears on exactly two hosts — the validator that writes state and the query service that reads it — for the reason you worked out in the [lesson 5 exercise](./05-read-the-inventory.md#exercise). Rule 6 in action: a database reference is a per-instance fact, not a group policy.

> [!WARNING]
> `sc_user` / `sc_secret_pwd` are the sample credentials. For anything beyond a local exercise, protect them with Ansible Vault instead — encrypt `postgres_password` in place, or move it into a dedicated `group_vars/all/vault.yaml` and reference it as `{{ vault_committer_db_password }}`. Plaintext credentials in an inventory you might share are the most common way this collection gets misused. [Lesson 12](./12-using-ansible-vault-for-secrets.md) covers both techniques and when to reach for each.

## Step 6: The Load Generator

Finally, something to produce traffic — and, importantly, the host that declares the Fabric-X namespace.

```yaml
    load_generators:
      hosts:
        orderer-loadgen:
          organization:
            <<: *Org1
            role: peer
            users:
              - name: orderer-loadgen
                secret: orderer-loadgenPWD
            namespaces:
              - id: 0
                policy: threshold
          loadgen_use_tls: true
          loadgen_metrics_port: 12010
          loadgen_rpc_port: 12020
```

The `namespaces:` list is what `make init` will act on, exactly as in [lesson 9](./09-add-the-extras.md). Without it the network starts fine and has nowhere to write state.

Note that `load_generators` sits under `all.children`, **not** under `network`. That mirrors the samples: the load generator is a client, not part of the deployable network, which is why `make network teardown` leaves it alone.

There is no `monitoring` group at all in this bundle. That is a deliberate choice for a minimal inventory — but it has one consequence worth predicting rather than discovering: the `orderer_operations_mtls_clients: [prometheus]` and `committer_monitoring_mtls_clients: [prometheus]` lines now name a host that does not exist. They are harmless (the trust bundle simply has no such client to add), and leaving them in means adding monitoring later is a pure addition. Deciding this consciously is the difference between a minimal inventory and an incomplete one.

## The Complete Inventory

Assembled, `my-network/fabric-x-minimal.yaml` is the six steps in order:

```text
all:
  vars:                       # step 3: CLI binary flags + organizations
  children:
    network:
      children:
        fabric_x:
          children:
            fabric_x_orderers:      # step 4
              children:
                fabric_x_orderer_1:
            fabric_x_committers:    # step 5
              children:
                fabric_x_committer:
    load_generators:          # step 6
```

That is 4 orderer services, 5 committer services, 1 database, and 1 load generator — **11 hosts** instead of the baseline's forty-odd, running one orderer group instead of four and no CAs, Explorer, or monitoring.

Be clear-eyed about what that buys and costs. Eleven hosts is small enough to hold in your head, which is the entire point of the exercise. It is also a network with `f = 0` and centrally generated test certificates, so it is a **learning artifact and nothing more**.

## Deploy It

Validate before you deploy. Ansible will tell you about structural mistakes for free:

```shell
export ANSIBLE_INVENTORY=my-network/fabric-x-minimal.yaml

# does it parse, and is the group tree what you intended?
.venv/bin/ansible-inventory --graph

# are the resolved variables right, including out_dir from vars.yaml?
.venv/bin/ansible-inventory --host committer-validator
```

Check three things in that second output specifically. Remember from [lesson 5](./05-read-the-inventory.md#query-the-inventory-instead-of-reading-it) that `ansible-inventory` prints definitions rather than values, so you are checking that each key is **present**, not what it evaluates to:

| Look for                                             | Confirms                                     |
| ---------------------------------------------------- | -------------------------------------------- |
| `out_dir` and `channel_id` appear at all             | `group_vars/all/vars.yaml` is being loaded   |
| `remote_deploy_dir` mentions `my-network-deployment` | `env.yaml` is being loaded                   |
| `committer_component_type` is present                | the dispatcher variable survived inheritance |

If `out_dir` is absent, your `vars.yaml` symlink or copy is missing or in the wrong directory. That is the single most likely failure, and it is much easier to spot here than three minutes into `make setup`.

To confirm the paths actually evaluate the way you intended, ask the host rather than the inventory:

```shell
.venv/bin/ansible committer-validator -m ansible.builtin.debug -a "var=remote_config_dir"
```

That should print a path under `out/my-network-deployment/committer-validator/config`.

Then the same three commands as every other deployment:

```shell
make targets
make setup
make start
make init
make ping
```

## Where to Go From Here

Your minimal network is a baseline. Now apply the discipline from [lesson 8](./08-change-the-topology.md) and change one dimension at a time:

| Next change                                | What to add                                                                                                                  | Fresh ledger? |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------- |
| **Actual fault tolerance — do this first** | Orderer organisations 2, 3, and 4, each with its own `fabric_x_orderer_N` group of four services, to reach `n = 4` / `f = 1` | yes           |
| Real identity management                   | A `fabric_cas` group, `fabric_ca_host` per organisation, and enrollment blocks                                               | yes           |
| Observability                              | A `monitoring` group — and now those `prometheus` mTLS client lines start doing work                                         | no            |
| Block browsing                             | A `fabric_x_block_explorer` group, plus `block-explorer` in `committer_mtls_clients`                                         | no            |
| An Ethereum endpoint                       | A `fabric_x_evm` host in `Org1`, with a `users:` entry and its own namespace                                                 | no            |
| More ordering throughput                   | A second batcher shard per group                                                                                             | yes           |
| More committing throughput                 | More verifiers and validators                                                                                                | no            |
| Horizontal-scale storage                   | Swap `committer-db` for a `committer_dbs` YugabyteDB cluster                                                                 | yes           |
| Real machines                              | Change `env.yaml` to `ansible_connection: ssh` and set `ansible_host` per service                                            | yes           |

The first row is not optional for anything you intend to rely on. Everything below it is a genuine choice; a one-party ordering service is not.

Each one is a small, reviewable diff against a topology you already know works. That is the whole method.

## Exercise

> [!TIP]
> Build the bundle described above and get it running.
>
> 1. Create `my-network/` with the inventory, `env.yaml`, and `vars.yaml`.
> 2. Validate it with `ansible-inventory` **before** deploying, and confirm the three things in the table above.
> 3. Deploy it and confirm the ports are open.
> 4. Then extend it: add a **Block Explorer** so you can browse your own blocks. Work out for yourself which two hosts and which one line elsewhere in the inventory you need.

<details markdown="1">
<summary>Solution</summary>

Steps 1 to 3 are the lesson. The one that requires thought is step 4.

The Block Explorer needs **two hosts**, in a `fabric_x_block_explorer` group under `fabric_x`:

```yaml
fabric_x_block_explorer:
  hosts:
    block-explorer-db:
      postgres_user: block_explorer_user
      postgres_password: block_explorer_pwd
      postgres_db: explorer
      postgres_port: 18432
      postgres_use_tls: true
    block-explorer:
      block_explorer_port: 18080
      block_explorer_ui_port: 18000
      sidecar_host: committer-sidecar
      postgres_db_host: block-explorer-db
```

Its own database, separate from the committer's — the Explorer indexes blocks into its own store rather than reading the committer's state.

And the **one line elsewhere** is in the committer's group variables:

```yaml
fabric_x_committer:
  vars:
    committer_mtls_clients:
      - block-explorer # <-- add this
```

Without it the sidecar refuses the Explorer's gRPC block stream. This is the rule from [lesson 9](./09-add-the-extras.md): the client declares who it connects to (`sidecar_host`), and the server declares who it trusts (`committer_mtls_clients`). Both halves are inventory lines, and omitting the second produces a component that looks broken while being perfectly configured.

Note also what you did _not_ have to configure: the Explorer's own TLS mode. There is no `block_explorer_use_tls` — it is derived from the `committer_use_tls` and `committer_use_mtls` settings of the host named by `sidecar_host`. Your committer has both on, so the Explorer uses both automatically.

Applying it:

```shell
make targets
make setup
make fabric_x_committers restart        # the sidecar must reload its trust bundle
make fabric_x_block_explorer start
make fabric_x_block_explorer ping
```

Then open <http://localhost:18000> and look at the blocks your own inventory produced.

The committer restart is the part worth remembering: you changed `committer_mtls_clients`, which changes the sidecar's _trust bundle_, which is generated configuration. `make setup` re-rendered it, and the restart is what makes the sidecar read it.

</details>

## Next

| Previous                                       | Next                                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------------------ |
| [10. Go Beyond Local](./10-go-beyond-local.md) | [12. Using Ansible Vault for Secrets](./12-using-ansible-vault-for-secrets.md) |
