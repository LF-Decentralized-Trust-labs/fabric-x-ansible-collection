# AGENTS.md — AI Agent Guide for `hyperledger.fabricx`

`hyperledger.fabricx` is an Ansible collection that automates deployment and lifecycle management of **Hyperledger Fabric-X** networks.
Namespace/name: `hyperledger.fabricx`. Authoritative version and deps: [`galaxy.yml`](galaxy.yml).

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
3. **Lint** — run `make lint` before committing (`ansible-lint` over roles, playbooks, examples).
4. **Idempotency** — all tasks must be idempotent; use `creates:`, `changed_when:`, or appropriate modules.
5. **Task names** — every `ansible.builtin.*` task must have a `name:` field.
6. **Code order** — first `name:` field, then `vars:` (if needed), FQDN name of task and finally `when:` (if needed). For blocks: `name:`, then `when:`, then `block:`.
7. **Defaults** — role variables with defaults go in `roles/<role>/defaults/main.yaml`; never hard-code values in tasks unless they are truly constant.
8. **Templates** — Jinja2 templates go in `roles/<role>/templates/` with `.j2` extension.

---

## Working in isolation

For large or multi-file changes, create a git worktree under `.worktrees/` rather than editing the main checkout directly. If you are unsure whether a change qualifies, ask before starting.

```shell
git worktree add .worktrees/<3-4-word-slug> -b worktree/<3-4-word-slug>
```

Do **not** remove the worktree when done — leave cleanup to the user.

---

## Architecture

### Always read the role README first

Before modifying any role, read `roles/<role>/README.md`. It is the authoritative reference for that role: available tasks, variables, and which deployment modes (binary / container / k8s) it supports. Deployment mode support varies per role — do not assume.

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
├── defaults/main.yaml          # all role variables and defaults
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

| Dependency                                         | Detail                                                                                                                                                                                                          |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `committer` → `postgres`                           | Started when `postgres_port` is defined in inventory                                                                                                                                                            |
| `committer` → `yugabyte`                           | Started when `yugabyte_component_type` is defined in inventory                                                                                                                                                  |
| `committer` ↔ `orderer`                            | Coordinator receives the assembler host list at startup                                                                                                                                                         |
| `fxconfig` → `committer`, `orderer`                | Generates configs consumed by both; for k8s deployments also runs namespace creation                                                                                                                            |
| `cryptogen` / `fabric_ca` → `orderer`, `committer` | Crypto artifacts must exist before either can be configured or started                                                                                                                                          |
| `armageddon` / `configtxgen` → crypto              | Genesis block generation depends on crypto output                                                                                                                                                               |
| `k8s` role → k8s deployments                       | Namespace setup is a prerequisite for any k8s-mode deployment                                                                                                                                                   |
| Monitoring                                         | `prometheus` scrapes `committer`, `orderer`, `loadgen`, `yugabyte`; `postgres_exporter` scrapes postgres; `node_exporter` on all nodes; `grafana` for dashboards; `elasticsearch`/`jaeger` for logs and tracing |

---

## Role reference

| Role                | Component managed                                                         |
| ------------------- | ------------------------------------------------------------------------- |
| `armageddon`        | Genesis block builder (armageddon CLI)                                    |
| `bin`               | Generic binary build/install helpers                                      |
| `committer`         | Fabric-X Committer (validator/verifier/coordinator/sidecar/query-service) |
| `configtxgen`       | configtxgen CLI wrapper                                                   |
| `container`         | Generic container helpers (start/stop/rm)                                 |
| `cryptogen`         | Crypto material generation                                                |
| `elasticsearch`     | Elasticsearch log backend                                                 |
| `fabric_ca`         | Fabric CA server and client                                               |
| `fxconfig`          | fxconfig configuration tool                                               |
| `git`               | Git clone helper                                                          |
| `go`                | Go binary build, install, and platform-mapping helpers                    |
| `grafana`           | Grafana dashboard                                                         |
| `idemixgen`         | idemixgen CLI wrapper                                                     |
| `jaeger`            | Jaeger tracing backend                                                    |
| `k8s`               | Shared Kubernetes helper (used by roles that deploy to k8s)               |
| `loadgen`           | Load generator                                                            |
| `node_exporter`     | Prometheus Node Exporter                                                  |
| `openssl`           | OpenSSL certificate helpers                                               |
| `orderer`           | Fabric-X Orderer (consenter/batcher/assembler/router)                     |
| `package`           | OS package installation (apt / brew)                                      |
| `postgres`          | PostgreSQL database                                                       |
| `postgres_exporter` | Prometheus Postgres Exporter                                              |
| `prometheus`        | Prometheus monitoring                                                     |
| `tmux`              | tmux session helpers                                                      |
| `utils`             | Miscellaneous utility tasks                                               |
| `yugabyte`          | YugabyteDB                                                                |

---

## Essential commands

```shell
make lint                  # validate before committing
make start / stop / teardown / wipe   # lifecycle
make install-deps          # set up control node (venv + python + ansible deps)
make help                  # full command reference
```

## Modifying a role or playbook

1. If the modification introduces new tasks under `tasks/`, `tasks/config/` or `tasks/crypto`, update the role README.
2. If the modification introduces new variables, put them in `defaults/main.yaml` only if it makes sense that such variables can have multiple values.
3. Run `make lint` and fix any issues before committing.

---

## Adding a role or playbook (rare)

1. Create `roles/<new_role>/README.md`, `defaults/main.yaml`, and at least one task file.
2. Add the Apache-2.0 license header to every file created.
3. Register the role in [`roles/README.md`](roles/README.md) (alphabetical order).
4. Add playbooks under `playbooks/<new_role>/` following existing patterns.
5. Run `make lint` and fix any issues before committing.

> **WARNING**: Never run `make install` when the repo is cloned directly into the Ansible collections path — it overwrites the live checkout with a built artifact.
