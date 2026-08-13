# AGENTS.md — AI Agent Guide for `hyperledger.fabricx`

`hyperledger.fabricx` is an Ansible collection that automates deployment and lifecycle management of **Hyperledger Fabric-X** networks.
Namespace/name: `hyperledger.fabricx`. Authoritative version and deps: [`galaxy.yml`](galaxy.yml).

## Project-local Agent Skills

[`.agents/skills/`](.agents/skills/) is the source of truth for project-local Agent Skills. Compatible agents discover their metadata from this trusted repository checkout and load the applicable `SKILL.md` on demand:

- `creating-fabricx-inventories`: load when creating, adapting, or reviewing a custom operator-owned Fabric-X inventory.
- `validating-fabricx-changes`: load when checking, validating, reviewing, or preparing repository changes.

---

## Rules — follow before every commit

1. **License header** — every YAML, shell, and Jinja2 file must begin with:

   ```yaml
   #
   # Copyright IBM Corp. All Rights Reserved.
   #
   # SPDX-License-Identifier: Apache-2.0
   #
   ```

   CI enforces this via `scripts/check_license_header.sh`.

2. **No trailing spaces** in `.j2` files — enforced by `scripts/check_trailing_spaces.sh`.
3. **Idempotency** — all tasks must be idempotent; use `creates:`, `changed_when:`, or appropriate modules.
4. **Task names** — every `ansible.builtin.*` task must have a `name:` field.
5. **Code order** — first `name:` field, then `vars:` (if needed), FQDN name of task and finally `when:` (if needed). For blocks: `name:`, then `when:`, then `block:`.
6. **Templates** — Jinja2 templates go in `roles/<role>/templates/` with `.j2` extension.

---

## Working in isolation

Use git worktrees under `.worktrees/` only for multi-agent jobs (i.e. with subagents). For single-agent work, edit the main checkout directly.

```shell
git worktree add .worktrees/<3-4-word-slug> -b worktree/<3-4-word-slug>
```

Do **not** remove the worktree when done — leave cleanup to the user.

---

## Architecture

### Always read the role argument_specs.yaml first

Before modifying any role, read `roles/<role>/meta/argument_specs.yaml`. It is the authoritative reference for that role: available tasks, variables, and which deployment modes (binary / container / k8s) it supports. Deployment mode support varies per role — do not assume.

### Dispatch pattern

Roles that manage multiple sub-components (e.g. `orderer`: consenter/batcher/assembler/router; `committer`: validator/verifier/coordinator/sidecar/query-service) use a dispatcher: the top-level task file reads `<role>_component_type` and delegates to the matching sub-component directory:

```yaml
ansible.builtin.include_role:
  name: hyperledger.fabricx.<role>
  tasks_from: <sub_component>/start # e.g. coordinator/start, assembler/bin/install
```

### Role layout

```text
roles/<role>/
├── defaults/main.yaml          # auto-generated from meta/argument_specs.yaml
├── meta/argument_specs.yaml    # single source of truth for variables and docs
├── tasks/
│   ├── start.yaml              # top-level dispatcher (reads *_component_type)
│   ├── <sub_component>/
│   │   ├── bin/
│   │   ├── container/
│   │   └── k8s/
└── templates/                  # *.j2 Jinja2 templates
```

---

## Cross-role dependencies

These connections are not visible from within a single role:

| Dependency                                         | Detail                                                                                                                                                                                                                                                |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `committer` → `postgres`                           | Started when `postgres_port` is defined in inventory                                                                                                                                                                                                  |
| `committer` → `yugabyte`                           | Started when `yugabyte_component_type` is defined in inventory                                                                                                                                                                                        |
| `committer` ↔ `orderer`                            | Coordinator receives the assembler host list at startup                                                                                                                                                                                               |
| `fxconfig` → `committer`, `orderer`                | Generates configs consumed by both; for k8s deployments also runs namespace creation                                                                                                                                                                  |
| `block_explorer` → `committer` (sidecar)           | Streams blocks over gRPC from the host named by `sidecar_host`; TLS/mTLS mode is derived from that host's `committer_use_tls`/`committer_use_mtls`, not a local flag                                                                                  |
| `block_explorer` → `postgres`                      | Reads/writes indexed blocks via the host named by `postgres_db_host`                                                                                                                                                                                  |
| `cryptogen` / `fabric_ca` → `orderer`, `committer` | Crypto artifacts must exist before either can be configured or started                                                                                                                                                                                |
| `armageddon` / `configtxgen` → crypto              | Genesis block generation depends on crypto output                                                                                                                                                                                                     |
| `k8s` role → k8s deployments                       | Namespace setup is a prerequisite for any k8s-mode deployment                                                                                                                                                                                         |
| Monitoring                                         | `prometheus` scrapes `committer`, `orderer`, `loadgen`, `yugabyte`; `postgres_exporter` scrapes postgres; `node_exporter` on all nodes; `cadvisor` scrapes container metrics; `grafana` for dashboards; `elasticsearch`/`jaeger` for logs and tracing |

---

## Role reference

| Role                | Component managed                                                          |
| ------------------- | -------------------------------------------------------------------------- |
| `armageddon`        | Genesis block builder (armageddon CLI)                                     |
| `bin`               | Generic binary build/install helpers                                       |
| `block_explorer`    | Fabric-X Block Explorer server + Next.js UI (streams blocks from sidecar)  |
| `cadvisor`          | cAdvisor container metrics exporter                                        |
| `committer`         | Fabric-X Committer (validator/verifier/coordinator/sidecar/query-service)  |
| `configtxgen`       | configtxgen CLI wrapper                                                    |
| `container`         | Generic container helpers (start/stop/rm)                                  |
| `cryptogen`         | Crypto material generation                                                 |
| `elasticsearch`     | Elasticsearch log backend                                                  |
| `fabric_ca`         | Fabric CA server and client                                                |
| `fxconfig`          | fxconfig configuration tool                                                |
| `git`               | Git clone helper                                                           |
| `go`                | Go binary build, install, and platform-mapping helpers                     |
| `grafana`           | Grafana dashboard                                                          |
| `idemixgen`         | idemixgen CLI wrapper                                                      |
| `jaeger`            | Jaeger tracing backend                                                     |
| `k8s`               | Shared Kubernetes helper (used by roles that deploy to k8s)                |
| `loadgen`           | Load generator                                                             |
| `node_exporter`     | Prometheus Node Exporter                                                   |
| `openssl`           | OpenSSL certificate helpers                                                |
| `orderer`           | Fabric-X Orderer (consenter/batcher/assembler/router)                      |
| `package`           | OS package installation (apt / brew)                                       |
| `postgres`          | PostgreSQL database                                                        |
| `postgres_exporter` | Prometheus Postgres Exporter                                               |
| `prometheus`        | Prometheus monitoring                                                      |
| `tmux`              | tmux session helpers                                                       |
| `utils`             | Miscellaneous utility tasks                                                |
| `yugabyte`          | YugabyteDB                                                                 |

---

## Essential commands

```shell
make lint                  # full validation; run only when the user explicitly asks
make start / stop / teardown / wipe   # lifecycle
make install-deps          # set up control node (venv + python + ansible deps)
make help                  # full command reference
```

Agents must use the Makefile targets for repository checks. Do not rewrite or bypass the project check scripts (for example, with ad hoc Python replacements) unless the user explicitly asks for that.

`make lint` is very time consuming. Do not run it unless the user explicitly asks you to run `make lint`.

## Modifying a role

1. Role variables and documentation are managed exclusively through [`roles/<role>/meta/argument_specs.yaml`](roles/). Both `defaults/main.yaml` and `README.md` are auto-generated — never edit them directly.
2. When you change `argument_specs.yaml`, use these Makefile checks in order:

   ```shell
   make check-argument-specs
   make check-trailing-spaces
   make check-license-header
   ```

3. Run `make lint` only if the user explicitly asks for it.
4. Only when all checks pass, regenerate the docs:

   ```shell
   make generate-roles-docs
   ```

## Adding a role (rare)

1. Create `roles/<new_role>/meta/argument_specs.yaml` with role options and entrypoints.
2. Create the task files under `roles/<new_role>/tasks/`.
3. Add the Apache-2.0 license header to every file created.
4. Run `make generate-roles-docs` to generate `defaults/main.yaml` and `README.md`.
5. Register the role in [`roles/README.md`](roles/README.md) (alphabetical order).
6. Add playbooks under `playbooks/<new_role>/` following existing patterns.
7. Run `make lint` and fix any issues before committing.

## Adding a new inventory

When a new inventory is added under [`examples/inventory/`](examples/inventory/), write a corresponding doc under [`examples/inventory/docs/`](examples/inventory/docs/) following the structure of existing docs (e.g. [`examples/inventory/docs/local/fabric-x.md`](examples/inventory/docs/local/fabric-x.md)). Then register the new doc in [`mkdocs.yml`](mkdocs.yml) under the `nav.Inventories` section, in the appropriate deployment-type group.

## Modifying a playbook

When a playbook under [`playbooks/`](playbooks/) is modified, update the corresponding `README.md` in the same directory. These READMEs are **not** auto-generated.

> **WARNING**: Never run `make install` when the repo is cloned directly into the Ansible collections path — it overwrites the live checkout with a built artifact.
