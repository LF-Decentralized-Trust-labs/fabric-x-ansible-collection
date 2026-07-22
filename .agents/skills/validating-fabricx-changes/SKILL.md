---
name: validating-fabricx-changes
description: Use when checking, validating, reviewing, or preparing Hyperledger Fabric-X repository changes, especially Ansible roles, argument specifications, templates, inventories, generated role documentation, or MkDocs documentation.
compatibility: Requires repository access, Git, Make, and the project Ansible environment.
---

# Validating Fabric-X Changes

Validate the submitted change with the smallest applicable set of project
checks. Produce evidence for the files that actually changed; do not claim a
check validated a claimed change that is absent from the diff.

## Inspect before selecting checks

1. Read `AGENTS.md`. For a role change, also read that role's
   `meta/argument_specs.yaml`; it is the authoritative interface. For an
   inventory, read the submitted inventory and its configuration before parsing
   it.
2. Read the relevant Makefile targets before running them. In particular,
   distinguish repository checks from targets that run playbooks or alter a
   deployment.
3. Inspect all submitted changes, including staged and relevant untracked
   files. Start with:

   ```sh
   git status --short
   git diff --check
   git diff --cached --check
   git diff --name-only
   git diff --cached --name-only
   git ls-files --others --exclude-standard
   git diff -- <relevant-paths>
   git diff --cached -- <relevant-paths>
   ```

   Read relevant untracked files directly before classifying them. If a claimed
   path is absent, report the corresponding check as skipped rather than
   validating a different file.

4. Classify the actual changed paths using the matrix below. Combine rows for
   cross-cutting changes and run prerequisite checks before generators.

## Changed-file command matrix

| Changed area                                                            | Required validation and follow-up                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Any tracked or untracked YAML (`.yaml` or `.yml`)                       | Run `make check-license-header`. Inspect the submitted YAML diff as well.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Shell (`.sh`) or Jinja2 (`.j2`) file                                    | Verify the required Apache-2.0 header in each changed file explicitly. `make check-license-header` currently scans YAML only, so do not claim it checks shell or Jinja2 headers.                                                                                                                                                                                                                                                                                                                                                                                    |
| Jinja2 template (`.j2`)                                                 | Run `make check-trailing-spaces`; inspect the changed template and its required header.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Role task entrypoint or `roles/<role>/meta/argument_specs.yaml`         | Run `make check-argument-specs`. For a metadata change, use the complete ordered workflow in the next row.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `roles/<role>/meta/argument_specs.yaml`                                 | Run, in this exact order: `make check-argument-specs`, `make check-trailing-spaces`, then `make check-license-header`. Only if all three pass, run `make generate-roles-docs`. Inspect `git diff -- roles/<role>/defaults/main.yaml roles/<role>/README.md` and its staged counterpart. Treat those generated files as output: do not edit them directly. Report generated changes that must be reviewed or committed.                                                                                                                                              |
| Generated `roles/<role>/defaults/main.yaml` or `roles/<role>/README.md` | Do not edit generated output directly. Locate and inspect the corresponding `meta/argument_specs.yaml`; if its source change is present, apply the complete metadata workflow above. If no source change is present, report the generated-only change as a finding.                                                                                                                                                                                                                                                                                                 |
| Markdown documentation or `mkdocs.yml` navigation                       | Inspect the submitted documentation/navigation diff. `make mkdocs-build` first regenerates MkDocs source and writes local build artifacts, so run it only when those outputs can be handled safely (for example, a disposable clean worktree); then inspect status and diffs again.                                                                                                                                                                                                                                                                                 |
| Inventory or inventory environment files                                | Parse the submitted inventory without deployment, using its selected configuration: `ANSIBLE_CONFIG="$INVENTORY_CONFIG" ansible-inventory -i "$INVENTORY" --list >/dev/null` and `ANSIBLE_CONFIG="$INVENTORY_CONFIG" ansible-inventory -i "$INVENTORY" --graph`. Use `--ask-vault-pass` only when the encrypted Vault values are needed to parse; never pass a Vault password via command arguments, environment variables, files, or chat. Review groups, host references, dispatcher variables, and colocated port/node-port assignments from the submitted diff. |
| Broad or mixed changes                                                  | Run every applicable targeted row, preserving the metadata workflow order.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

For an inventory, choose the configuration that belongs to the submitted
bundle; do not silently parse it through the repository's default inventory.
Inventory parsing is read-only with respect to deployment targets, but plugins
can require local tooling or Vault access. Report an unavailable tool or Vault
prompt as a skipped/blocked check rather than installing anything or bypassing
it.

## Boundaries

- Do **not** run `make lint` unless the user directly and explicitly requests
  `make lint`. “Validate,” “full validation,” or a request to run focused
  checks does not authorize it. If authorized, run the focused applicable
  checks too, and report an unavailable or failed lint command honestly.
- Never install dependencies or invoke install targets as validation. Do not
  run `make install`, `make install-deps`, or their install prerequisites.
- Never use deployment or lifecycle commands as validation, even if requested.
  This includes targets that create, configure, start, initialize, stop,
  restart, update, tear down, wipe, clean, or otherwise alter a network or
  remote host, such as `setup`, `configs`, `start`, `init`, `stop`, `restart`,
  `update`, `teardown`, `wipe`, `hard-wipe`, `targets`, `ping`, and
  `run-command`. Offer diff inspection and inventory parsing instead.
- Do not use `make mkdocs-serve`; it starts a server. Do not use cleanup
  targets to hide generated output. Preserve and report any output from a
  generator so the author can review it.

## Completion report

Report:

1. changed paths inspected and their classifications;
2. every command run with pass/fail and concise failure output;
3. generated files or post-generator diffs inspected;
4. skipped or blocked checks with the reason, including absent claimed paths;
5. whether `make lint` was authorized, run, omitted, or deliberately not run;
6. lifecycle/deployment/install commands deliberately not run; and
7. remaining risks, including checks that could not run because tooling, a
   selected configuration, or interactive Vault access was unavailable.
