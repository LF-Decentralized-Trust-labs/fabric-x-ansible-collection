# Project Agent Skills Design

## Purpose

Add two repository-local skills that help agents work safely and effectively with `hyperledger.fabricx`:

1. `creating-fabricx-inventories` guides an operator through creating a valid custom deployment inventory.
2. `validating-fabricx-changes` selects and runs the project checks applicable to an agent's changes.

These skills are project tooling, not generated inventories themselves. They must follow the Agent Skills standard and be committed under `.agents/skills/`, allowing compatible agents to discover them from a trusted checkout without Pi-specific configuration.

## Architecture

Use two focused skills:

```text
.agents/skills/
├── creating-fabricx-inventories/
│   ├── SKILL.md
│   └── references/
│       ├── inventory-decisions.md
│       └── validation.md
└── validating-fabricx-changes/
    └── SKILL.md
```

The skills have separate triggering conditions and responsibilities. Inventory creation may invoke or follow the validation skill during its final verification phase. Project files remain authoritative; bundled references should organize project-specific decision guidance without copying entire role specifications or example inventories.

Each skill directory name must match its frontmatter `name`. Frontmatter must comply with the Agent Skills specification, including a lowercase hyphenated name and a focused description of the circumstances in which the skill should be loaded.

## Inventory-Creation Skill

### Scope

The first version supports all maintained inventory families and choices represented by the repository:

- local, Kubernetes, OpenShift, and distributed environments;
- container and binary runtimes where the applicable roles support them;
- Fabric CA and cryptogen crypto workflows;
- PostgreSQL and YugabyteDB persistence;
- TLS with mTLS, TLS without mTLS, and no TLS for local debugging;
- custom component scale and physical host or cluster placement;
- optional load generation, Block Explorer, and monitoring components.

The skill creates operator artifacts, not project contribution examples. It must not register generated inventories in `mkdocs.yml`, add maintained example documentation, or update the examples index.

### Authoritative Inputs

Before adapting an inventory, the skill directs the agent to read:

- `examples/inventory/README.md` for the inventory contract;
- the closest maintained example inventory and its `group_vars/all/env.yaml`;
- the relevant `roles/<role>/meta/argument_specs.yaml` files for supported variables, entrypoints, and deployment modes;
- `AGENTS.md` for project rules and cross-role dependencies.

The agent must adapt the closest example rather than reconstructing a topology from memory.

### Guided Workflow

1. Ask for a user-selected output path and recommend placing it outside `examples/inventory/`.
2. Refuse to overwrite existing files without explicit confirmation.
3. Select the closest maintained example based on environment, runtime, crypto, persistence, and security choices.
4. Ask progressive questions, one decision at a time, using the selected example's values as defaults.
5. Gather organizations and domains, orderer group count and scale, committer topology, optional services, host placement, ports, externally reachable addresses, runtime paths, and Kubernetes or OpenShift settings as applicable.
6. Validate and summarize the intended topology before writing files, then ask for confirmation.
7. Generate the complete bundle.
8. Create the secrets file through an interactive Ansible Vault workflow.
9. Parse and validate the resulting inventory without deploying it.
10. Report generated paths, validation evidence, and remaining operator actions.

### Pre-Generation Topology Checks

The skill must ensure that:

- standard inventory parent groups are preserved;
- hostnames are stable and unique;
- each orderer component has `orderer_component_type`;
- each committer component has `committer_component_type`;
- ports are unique where logical services share a target;
- batcher shard identifiers are unique in their intended scope;
- host references resolve to inventory hostnames;
- organization definitions and ownership are consistent;
- selected deployment modes are supported by the relevant role specifications;
- cross-role dependencies such as committer databases, assembler discovery, Block Explorer hosts, and monitoring endpoints remain coherent.

### Generated Bundle

The default output is a complete directory containing:

- the main inventory YAML;
- `group_vars/all/env.yaml`;
- `group_vars/all/vault.yaml`, encrypted with Ansible Vault;
- an operator README covering prerequisites, required environment variables, Vault usage, inventory selection, validation commands, and unresolved operator actions.

The main inventory and environment variables reference Vault variables instead of containing plaintext credentials.

### Secret Handling

The agent must not request, echo, log, or temporarily store plaintext secrets. It creates a documented variable-name skeleton and launches `ansible-vault create` or an equivalent interactive command so the operator enters both the Vault password and secret values directly. The skill requires an interactive terminal for this phase and must stop with clear instructions if one is unavailable.

### Safety

Inventory verification must not start, initialize, stop, tear down, or wipe a network. The skill must distinguish no-TLS debugging configurations from production-appropriate configurations and warn accordingly.

## Change-Validation Skill

### Responsibility

The validation skill reads the repository instructions and working-tree diff, selects the smallest authoritative set of checks, runs safe non-destructive checks, and reports evidence. It uses Make targets rather than rewriting or bypassing project check scripts.

### Validation Selection

| Changed area | Required behavior |
| --- | --- |
| YAML, shell, or Jinja2 files | Run `make check-license-header`. |
| Jinja2 templates | Run `make check-trailing-spaces`. |
| Role `meta/argument_specs.yaml` or role task entrypoints | Run `make check-argument-specs`. |
| Role `argument_specs.yaml` | Run `make check-argument-specs`, `make check-trailing-spaces`, and `make check-license-header` in project-mandated order; after success run `make generate-roles-docs` and inspect generated changes. |
| Generated role defaults or role READMEs | Treat `argument_specs.yaml` as the source; do not edit generated files directly. |
| Documentation or MkDocs navigation | Run `make mkdocs-build`. |
| Inventory bundle | Parse or graph the selected inventory with the project's configured Ansible tooling and verify host/group references. |
| Broad or cross-cutting changes | Combine all applicable targeted checks. |
| Full lint | Run `make lint` only when the user explicitly requests it. |

### Workflow

1. Read `AGENTS.md` and the relevant Makefile targets.
2. Inspect `git status` and the diff, including untracked files relevant to the task.
3. Classify changed files and briefly state the selected checks.
4. Run applicable non-destructive Make targets in dependency order.
5. Inspect generated diffs when a generator changes tracked files.
6. Report commands, pass/fail status, concise failure details, skipped checks and reasons, and whether full lint was omitted because it was not requested.

The skill must not install dependencies or invoke lifecycle/deployment targets such as `start`, `init`, `stop`, `teardown`, or `wipe` as validation.

## Discovery and Project Documentation

Commit the skills beneath `.agents/skills/`, the cross-harness project-local path recognized by the Agent Skills standard ecosystem. A compatible agent receives the skills with the Git checkout, discovers their metadata while operating in the trusted repository, and loads the relevant `SKILL.md` on demand.

Add a concise section to `AGENTS.md` listing the two project-local skills, their triggering purpose, and `.agents/skills/` as the source of truth. Do not add Pi-only settings, symlinks, or package metadata.

## Test-First Skill Development

Develop and verify each skill independently using a RED-GREEN-REFACTOR process:

1. Define realistic evaluation prompts and expected outcomes.
2. Run prompts without the skill and record baseline omissions, unsafe actions, or incorrect decisions.
3. Write the minimum skill guidance addressing observed failures.
4. Run the same prompts with the skill available.
5. Evaluate correctness, question quality, command selection, secret safety, and adherence to project constraints.
6. Refine the body and description, then repeat until the scenarios pass.

Do not create both skill bodies before testing the first. Complete the baseline, implementation, evaluation, and refinement cycle for one skill before starting the next.

### Inventory Evaluation Coverage

Include at least:

- a local Fabric CA and PostgreSQL inventory;
- a Kubernetes cryptogen and YugabyteDB inventory;
- a distributed inventory with custom target placement and port collision risks;
- interactive Vault handling in which the agent never asks for plaintext secrets;
- an operator artifact request that must not alter maintained example indexes or `mkdocs.yml`;
- a near-miss prompt about modifying an existing contributed example, to test triggering and scope boundaries.

### Validation Evaluation Coverage

Include at least:

- a Jinja2-only change;
- an `argument_specs.yaml` change requiring generation after ordered checks;
- documentation and inventory changes;
- a normal validation request that does not authorize `make lint`;
- an explicit request that does authorize `make lint`;
- a near-miss deployment request that must not be treated as validation.

### Evaluation Artifacts

Store test prompts and expected outcomes with each skill in an `evals/evals.json` file or another clearly documented repository-local evaluation location selected during implementation. Keep generated run outputs out of the committed skill package unless they provide durable regression value.

## Acceptance Criteria

- Both skills conform to the Agent Skills frontmatter and directory conventions.
- Compatible agents can discover them from `.agents/skills/` without project-specific agent configuration.
- Inventory creation covers all maintained inventory families through guided adaptation.
- Generated operator bundles do not modify the maintained example catalog.
- Plaintext secrets never pass through agent conversation, command arguments, logs, or temporary files.
- Validation chooses and runs targeted Make checks based on changed files.
- `make lint` is never run without explicit user authorization.
- Neither skill performs deployment or lifecycle operations as part of creation or validation.
- Baseline and with-skill evaluations demonstrate the intended behavioral improvement.
- `AGENTS.md` documents the availability and purpose of the project-local skills.
