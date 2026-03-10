# AGENTS.md — AI Agent Guide for `hyperledger.fabricx`

This document describes the structure, conventions, and workflows of the `hyperledger.fabricx` Ansible collection so that AI coding agents can contribute to it effectively.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Layout](#repository-layout)
- [Roles](#roles)
- [Playbooks](#playbooks)
- [Inventory & Variables](#inventory--variables)
- [Makefile Entrypoints](#makefile-entrypoints)
- [CI Pipelines](#ci-pipelines)
- [Code Conventions](#code-conventions)
- [How to Add a New Role](#how-to-add-a-new-role)
- [How to Add a New Playbook](#how-to-add-a-new-playbook)
- [Dependencies](#dependencies)

---

## Project Overview

`hyperledger.fabricx` (version `0.5.9`) is an Ansible collection that automates the deployment and lifecycle management of **Hyperledger Fabric-X** networks. Fabric-X is an extension of Hyperledger Fabric targeted at regulated digital asset use-cases.

- **Namespace / name**: `hyperledger.fabricx`
- **License**: Apache-2.0
- **Galaxy metadata**: [`galaxy.yml`](galaxy.yml)
- **Repository**: <https://github.com/LF-Decentralized-Trust-labs/fabric-x-ansible-collection>

---

## Repository Layout

```text
.
├── galaxy.yml                  # Collection metadata (version, authors, deps)
├── Makefile                    # Top-level developer entrypoints
├── target_hosts.mk             # Predefined host-group shortcuts for make
├── requirements.txt            # Python/pip dependencies (ansible-lint, etc.)
├── requirements.yml            # Ansible collection dependencies
├── .ansible-lint               # ansible-lint configuration
├── ci/                         # CI helper shell scripts
│   ├── check_license_header.sh
│   ├── check_trailing_spaces.sh
│   └── run_ci_test.sh
├── .github/workflows/          # GitHub Actions workflows
│   ├── lint.yaml
│   ├── test.yaml
│   └── publish.yaml
├── examples/                   # Sample inventories, playbooks, images
│   ├── ansible.cfg
│   ├── inventory/
│   │   ├── local/              # Single-machine inventories
│   │   └── distributed/        # Multi-node inventories
│   └── playbooks/              # Numbered orchestration playbooks
├── playbooks/                  # Collection-level reusable playbooks
│   ├── artifacts/
│   ├── committer/
│   ├── fabric_ca_client/
│   ├── fabric_ca_server/
│   ├── fxconfig/
│   ├── loadgen/
│   ├── monitoring/
│   ├── orderer/
│   └── yugabyte/
├── roles/                      # Ansible roles (one per component)
│   ├── README.md
│   └── <role_name>/
│       ├── README.md
│       ├── defaults/main.yaml
│       ├── tasks/
│       └── templates/
└── meta/
    └── runtime.yml             # Minimum ansible-core version requirement
```

---

## Roles

Every Fabric-X component is managed by a dedicated role under `roles/`.
Roles are referenced as `hyperledger.fabricx.<role_name>`.

| Role                | Component managed                         |
| ------------------- | ----------------------------------------- |
| `armageddon`        | Genesis block builder (armageddon CLI)    |
| `bin`               | Generic binary build/install helpers      |
| `committer`         | Fabric-X Committer node                   |
| `configtxgen`       | configtxgen CLI wrapper                   |
| `container`         | Generic container helpers (start/stop/rm) |
| `cryptogen`         | Crypto material generation                |
| `elasticsearch`     | Elasticsearch log backend                 |
| `fabric_ca_client`  | Fabric CA client binary                   |
| `fabric_ca_server`  | Fabric CA server                          |
| `fxconfig`          | fxconfig configuration tool               |
| `git`               | Git clone helper                          |
| `grafana`           | Grafana dashboard                         |
| `jaeger`            | Jaeger tracing backend                    |
| `loadgen`           | Load generator                            |
| `node_exporter`     | Prometheus Node Exporter                  |
| `openssl`           | OpenSSL certificate helpers               |
| `orderer`           | Fabric-X Orderer (consenter + router)     |
| `package`           | OS package installation (apt / brew)      |
| `postgres`          | PostgreSQL database                       |
| `postgres_exporter` | Prometheus Postgres Exporter              |
| `prometheus`        | Prometheus monitoring                     |
| `tmux`              | tmux session helpers                      |
| `utils`             | Miscellaneous utility tasks               |
| `yugabyte`          | YugabyteDB                                |

### Role internal structure

Each role follows this directory convention:

```text
roles/<role>/
├── README.md             # Role-level documentation (mandatory)
├── defaults/
│   └── main.yaml         # Default variable values
├── tasks/
│   ├── start.yaml        # Start the component
│   ├── stop.yaml         # Stop without wiping data
│   ├── teardown.yaml     # Stop and remove data
│   ├── wipe.yaml         # Remove config artifacts / binaries
│   ├── ping.yaml         # Health / port check
│   ├── fetch_logs.yaml   # Pull logs to controller
│   ├── get_metrics.yaml  # Scrape metrics
│   ├── generate_crypto.yaml
│   ├── transfer_configs.yaml
│   ├── bin/              # Binary-mode sub-tasks
│   │   ├── build.yaml
│   │   ├── install.yaml
│   │   ├── transfer.yaml
│   ├── container/        # Container-mode sub-tasks
│   └── config/           # Config generation sub-tasks
└── templates/            # Jinja2 templates (*.j2)
```

Not every role implements every task — only those relevant to its component.

### Using a role task from a playbook

```yaml
- name: Start Fabric-X Orderer
  ansible.builtin.include_role:
    name: hyperledger.fabricx.orderer
    tasks_from: start
```

---

## Playbooks

### Collection playbooks (`playbooks/`)

Reusable playbooks organised by component. They are designed to be called by the example orchestration playbooks or directly by users. Each playbook accepts a `target_hosts` extra variable that restricts execution to a subset of the inventory.

### Example orchestration playbooks (`examples/playbooks/`)

Numbered sequencing playbooks that wire the collection playbooks together for a full lifecycle run:

| File                          | Purpose                           |
| ----------------------------- | --------------------------------- |
| `10-run-command.yaml`         | Run an arbitrary shell command    |
| `20-generate-crypto.yaml`     | Generate crypto material          |
| `21-build-genesis-block.yaml` | Build the genesis block           |
| `30-binaries.yaml`            | Build/transfer component binaries |
| `40-transfer-configs.yaml`    | Push configs to remote nodes      |
| `60-start.yaml`               | Start all components              |
| `70-stop.yaml`                | Stop all components               |
| `80-teardown.yaml`            | Teardown (stop + delete data)     |
| `90-ping.yaml`                | Port health check                 |
| `93-get-metrics.yaml`         | Metrics collection                |
| `96-fetch-logs.yaml`          | Fetch remote logs                 |
| `100-wipe.yaml`               | Wipe configs/bins from remotes    |
| `110-hard-wipe.yaml`          | Wipe deploy folder from remotes   |

---

## Inventory & Variables

Sample inventories live under `examples/inventory/`:

| Inventory                       | Description                         |
| ------------------------------- | ----------------------------------- |
| `local/fabric-x.yaml`           | Default containerised local network |
| `local/fabric-x-yugabyte.yaml`  | Local network with YugabyteDB       |
| `local/fabric-x-bin.yaml`       | Local network using native binaries |
| `local/fabric-x-cryptogen.yaml` | Crypto generated with cryptogen CLI |
| `local/fabric-x-no-tls.yaml`    | No TLS variant                      |
| `local/fabric-x-no-mtls.yaml`   | No mTLS variant                     |
| `distributed/fabric-x.yaml`     | Multi-node distributed network      |

### Predefined host groups (`target_hosts.mk`)

| Group                | Targets                                           |
| -------------------- | ------------------------------------------------- |
| `fabric_cas`         | Fabric CA servers                                 |
| `fabric_x`           | All Fabric-X network nodes (orderers + committer) |
| `fabric_x_orderers`  | All orderer nodes                                 |
| `fabric_x_committer` | Committer components                              |
| `load_generators`    | Load generator instances                          |
| `monitoring`         | Monitoring stack (Grafana, Prometheus, etc.)      |

Pass a group to any make target using prefix syntax:

```shell
make fabric_x_orderers start
```

This sets `TARGET_HOSTS=fabric_x_orderers` for the underlying playbook call.

---

## Makefile Entrypoints

Run `make help` to see all commands. The most important ones are:

| Command                 | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `install`               | Build and install the collection locally         |
| `lint`                  | Run `ansible-lint`                               |
| `check-license-header`  | Verify license headers on all files              |
| `check-trailing-spaces` | Check for trailing spaces in `.j2` files         |
| `install-prerequisites` | Install prerequisites on remote hosts            |
| `setup`                 | `build` + `transfer` (full artifact pipeline)    |
| `build`                 | `build-artifacts` + `binaries`                   |
| `build-artifacts`       | `generate-crypto` + `genesis-block`              |
| `generate-crypto`       | Generate crypto material on controller           |
| `genesis-block`         | Build genesis block                              |
| `binaries`              | Build/install binaries on controller or remotes  |
| `transfer`              | `transfer-configs`                               |
| `transfer-configs`      | Push config artifacts to remotes                 |
| `start`                 | Start targeted components                        |
| `stop`                  | Stop targeted components (keep data)             |
| `restart`               | `teardown` + `start`                             |
| `teardown`              | Stop + delete data                               |
| `wipe`                  | Remove configs/bins from remotes                 |
| `hard-wipe`             | Remove deploy folder from remotes                |
| `clean`                 | Remove local `out/` directory                    |
| `ping`                  | Check that component ports are open              |
| `get-metrics`           | Collect metrics from components                  |
| `fetch-logs`            | Pull logs from remote hosts                      |
| `limit-rate`            | Adjust load-generator TPS (`LIMIT=<n>`)          |
| `login-cr`              | Log into a container registry                    |
| `run-command`           | Run arbitrary command on remotes (`COMMAND="…"`) |

---

## CI Pipelines

### Lint (`.github/workflows/lint.yaml`)

Runs on every push/PR to `main`:

1. `make install lint check-trailing-spaces` — installs the collection, then runs `ansible-lint` on `roles/`, `playbooks/`, and `examples/`.
1. `make check-trailing-spaces` — checks that no trailing spaces are left within `.j2` templates.
1. `make check-license-header` — verifies Apache-2.0 license headers.

### Tests (`.github/workflows/test.yaml`)

Matrix job that tests six inventories in parallel on every push/PR to `main`:

- `fabric-x`, `fabric-x-yugabyte`, `fabric-x-bin`, `fabric-x-cryptogen`, `fabric-x-no-tls`, `fabric-x-no-mtls`.

Each job runs `ci/run_ci_test.sh` with `CONTAINER_CLIENT=docker`.

### Publish (`.github/workflows/publish.yaml`)

Publishes the collection to Ansible Galaxy on release.

---

## Code Conventions

1. **License header** — Every YAML, shell, and Jinja2 file **must** begin with:

   ```yaml
   #
   # Copyright IBM Corp. All Rights Reserved.
   #
   # SPDX-License-Identifier: Apache-2.0
   #
   ```

   The CI `check-license-header` step enforces this.

2. **No trailing spaces** — Jinja2 (`.j2`) template files must not have trailing whitespace. The CI `check-trailing-spaces` step enforces this.

3. **YAML formatting** — Follow `ansible-lint` rules. Run `make lint` before opening a PR.

4. **Task naming** — Every `ansible.builtin.*` task must have a descriptive `name:` field.

5. **Idempotency** — All tasks must be idempotent. Use `creates:`, `changed_when:`, or appropriate Ansible modules.

6. **Defaults** — Role variables with sensible defaults belong in `roles/<role>/defaults/main.yaml`. Do not hard-code values in tasks.

7. **Templates** — Jinja2 templates go in `roles/<role>/templates/` and use the `.j2` extension.

8. **Sub-task files** — Group related sub-tasks into subdirectories (`bin/`, `container/`, `config/`, `crypto/`) rather than cramming everything into the top-level `tasks/` directory.

9. **Binary vs container mode** — Most components support both a native-binary mode and a container mode. Keep these implementations separate under `tasks/bin/` and `tasks/container/` respectively, with a dispatcher at the top-level task file.

---

## How to Add a New Role

1. Create the directory structure under `roles/<new_role>/`:

   ```text
   roles/<new_role>/
   ├── README.md
   ├── defaults/main.yaml
   └── tasks/
       └── start.yaml   # (add other tasks as needed)
   ```

2. Add the Apache-2.0 license header to **every** file you create.

3. Register the new role in [`roles/README.md`](roles/README.md) (alphabetical order in the roles list).

4. Add any sample playbooks under `playbooks/<new_role>/` following the same patterns as existing component playbooks.

5. Run `make lint` and fix any reported issues before committing.

---

## How to Add a New Playbook

1. Create the YAML file under `playbooks/<component>/` with the Apache-2.0 header.

1. Use `ansible.builtin.include_role` to delegate to the relevant role task:

   ```yaml
   - name: <Human-readable description>
     hosts: "{{ target_hosts | default('all') }}"
     gather_facts: false
     tasks:
       - name: <Action description>
         ansible.builtin.include_role:
           name: hyperledger.fabricx.<role>
           tasks_from: <task_file_stem>
   ```

1. If the playbook should be user-facing, add a numbered wrapper in `examples/playbooks/` and a corresponding `make` target in [`Makefile`](Makefile).

---

## Dependencies

### Ansible collections (`requirements.yml`)

| Collection          | Minimum version |
| ------------------- | --------------- |
| `ansible.posix`     | 1.6.2           |
| `community.general` | 10.3.0          |
| `community.docker`  | 4.3.1           |
| `containers.podman` | 1.16.2          |

Install with:

```shell
ansible-galaxy collection install -r requirements.yml
```

### Python packages (`requirements.txt`)

Install with:

```shell
pip install -r requirements.txt
```

### Controller node prerequisites

| Tool                 | Minimum version |
| -------------------- | --------------- |
| Python               | any recent 3.x  |
| Ansible              | 2.16            |
| Podman **or** Docker | latest stable   |
| Go                   | latest stable   |

### Remote node prerequisites

Install automatically via:

```shell
make install-prerequisites
```

> **Note**: The remote user must have passwordless `sudo` access.
