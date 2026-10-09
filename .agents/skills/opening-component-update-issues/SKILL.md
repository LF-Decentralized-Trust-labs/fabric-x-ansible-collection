---
name: opening-component-update-issues
description: Use when a new tag, release, or version of a component managed by this collection (fabric-x-committer, fabric-x-orderer, fabric-x tools, fabric-ca, monitoring images, etc.) is published and a Component Update issue must be drafted or opened.
compatibility: Requires Git, the GitHub CLI (gh), and network access to the upstream repository.
---

# Opening Component Update Issues

A Component Update issue (form: `.github/ISSUE_TEMPLATE/component-update.yaml`) tells a maintainer exactly what to change to support a new upstream version. An update is **not breaking** only when bumping the version variables is all it needs; anything else is breaking and must be fully described.

## 1. Find the version supported on `main`

Always read `origin/main`, not the working tree:

```bash
git fetch origin
# Roles that consume the upstream (one upstream often feeds several roles, e.g. fabric-x-committer -> committer + loadgen)
git grep -nE '<upstream-repo-or-image-name>' origin/main -- 'roles/*/meta/argument_specs.yaml'
# Pinned versions of each matching role (image tag and binary git commit)
git show origin/main:roles/<role>/meta/argument_specs.yaml | grep -nE -A4 '_(image_tag|git_commit): &'
# Overrides outside role defaults
git grep -nE '<role>_(image_tag|git_commit):' origin/main -- examples playbooks
```

Stop and report if `main` already supports the target, or if an issue already exists:

```bash
gh issue list -R LF-Decentralized-Trust-labs/fabric-x-ansible-collection --label version-support --state all --search '<component> <version>'
```

## 2. Decide whether the update is breaking

Diff upstream `<current>..<target>` (use a local clone if available, otherwise `gh api repos/<owner>/<repo>/compare/<current>...<target>`), and read the release notes (`gh release view <target> -R <owner>/<repo>`). Then compare each upstream change with what the affected roles actually do:

| Question | Upstream places to check | Collection places affected |
| --- | --- | --- |
| Does the start process change? (new/renamed subcommands, flags, env vars, init steps, entrypoint, health checks) | `cmd/`, Dockerfiles, `docker/`, deployment scripts | `roles/<role>/tasks/**` (bin, container, k8s, openshift), start/init playbooks |
| Does the config change? (new, removed, renamed, or reformatted parameters, new defaults that matter) | sample configs and config templates, config structs | `roles/<role>/templates/*.j2`, `roles/<role>/meta/argument_specs.yaml` |
| Do templates or manifests change? (ports, volumes, files, k8s resources) | deployment manifests, docs | `roles/<role>/templates/k8s/**`, container options |
| Do generated artifacts change? (configtx, genesis, crypto layout, namespaces) | `configtx`/crypto code and samples | `configtxgen`, `cryptogen`, `armageddon`, `fxconfig` roles |
| Do inventories or playbooks need new variables or steps? | release notes | `examples/inventory/**`, `playbooks/**` |

If every answer is "no", select `No.` and set `Configuration changes` to `N/A`.

## 3. Write the issue

Title: ``[UPDATE] Update to `<component>:<version>` ``. Component name is the upstream name (e.g. `fabric-x-committer`); target version is the released tag.

For a breaking update, `Configuration changes` lists one entry per change, each with:

- what changed upstream, with links pinned to the target tag (release notes, PR/commit, `https://github.com/<owner>/<repo>/blob/<tag>/<path>`);
- the collection files to change (role tasks, templates, `argument_specs.yaml` options, playbooks, inventories);
- the concrete action (new/removed/renamed variable with its default, new task or playbook step, template diff);
- the affected deployment modes (bin, container, k8s, openshift).

Example entry: "`committer db-init` subcommand added ([cmd/committer/db_init_cmd.go](https://github.com/hyperledger/fabric-x-committer/blob/v1.0.5/cmd/committer/db_init_cmd.go)): add an `init_db` entrypoint to `roles/committer` (bin, container, k8s job) and call it from `playbooks/committer/start.yaml` before starting the committer services."

Body (issue forms render each field as a `###` heading; the dropdown value must match the form verbatim):

```markdown
### Component name

fabric-x-committer

### Target version

v1.0.5

### Breaking changes

Yes - Details on how to support it are provide in the `Configuration changes` section below.

### Configuration changes

- ...
```

Show the draft to the user. Create it only when asked:

```bash
gh issue create -R LF-Decentralized-Trust-labs/fabric-x-ansible-collection \
  --title '[UPDATE] Update to `<component>:<version>`' \
  --label enhancement --label version-support --body-file <draft.md>
```

## Common mistakes

- Reading the version from the working tree or a feature branch instead of `origin/main`.
- Checking only one role when the upstream feeds several (committer + loadgen, orderer + armageddon, fabric-x tools roles).
- Marking `No.` because the release notes say nothing about config: diff the sample configs and `cmd/` anyway.
- Linking upstream `main` instead of the target tag, which drifts over time.
