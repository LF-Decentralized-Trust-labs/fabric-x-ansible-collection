# Fxconfig Mixed-Policy State Fix Design

## Problem

The `fxconfig` container namespace creation task stores the rewritten threshold
policy in the host-scoped `fxconfig_threshold_namespace_policy` fact. When the
same host creates a threshold namespace followed by an MSP-policy namespace,
that fact remains defined for the second role invocation.

The volume list is reset for the MSP-policy invocation, but the container
environment currently selects the stale threshold fact through the `default`
filter. The second container therefore receives `threshold:/tmp/pubkey.pem`
without the corresponding PEM mount and exits because `/tmp/pubkey.pem` does
not exist.

## Scope

Change only `roles/fxconfig/tasks/container/namespace/create.yaml`. Do not
change public role variables, argument specifications, generated role
documentation, playbooks, or maintained example inventories.

The regression playbook used during implementation is temporary test evidence
and must not be committed.

## Design

Replace the threshold-only internal fact with an effective container-policy
fact that is initialized from the current namespace policy on every role
invocation:

- The base container-input task sets
  `fxconfig_container_namespace_policy` to `fxconfig_namespace_policy` and
  resets `fxconfig_volumes` to the output-directory mount.
- The threshold-policy task overwrites
  `fxconfig_container_namespace_policy` with
  `threshold:/tmp/pubkey.pem` and appends the source certificate mount.
- The container environment assigns `FXCONFIG_POLICY` directly from
  `fxconfig_container_namespace_policy`; it does not use a fallback to a
  potentially stale fact.

This keeps the existing two-task structure and makes every invocation fully
initialize the internal state it consumes. Binary-mode namespace creation is
unchanged.

## Data Flow

For a threshold policy:

1. Initialize the effective policy to the host-side threshold policy and reset
   the volume list.
2. Rewrite the effective policy to `threshold:/tmp/pubkey.pem`.
3. Add the host certificate to `/tmp/pubkey.pem` volume mount.
4. Start the fxconfig container with the rewritten policy and both mounts.

For an MSP DSL policy such as
`OR('Org1MSP.member', 'Org2MSP.member')`:

1. Initialize the effective policy to the exact DSL string and reset the
   volume list.
2. Skip threshold rewriting.
3. Start the fxconfig container with the exact DSL string and only the output
   mount.

The order of namespace declarations no longer affects either path.

## Regression Test

Create a temporary, uncommitted Ansible playbook that directly invokes
`hyperledger.fabricx.fxconfig` with `tasks_from: container/namespace/create`
twice on localhost:

1. Invoke it with a threshold policy and a dummy certificate path.
2. Assert that the effective container policy is
   `threshold:/tmp/pubkey.pem` and that the PEM mount is present.
3. Invoke it with `OR('Org1MSP.member', 'Org2MSP.member')`.
4. Assert that the effective container policy is exactly the MSP DSL string,
   the volume list contains only the output mount, and no PEM mount remains.

Set `container_client` to a non-runtime sentinel so the shared container role
does not dispatch to Docker or Podman. This exercises the role's state
transitions without pulling an image, starting a container, or modifying a
Fabric-X deployment. Remove the temporary playbook after capturing the result.

## Validation

Run the temporary regression playbook before the fix to confirm the MSP-policy
assertion fails, then run it after the fix to confirm all assertions pass.
Run the repository checks applicable to a changed role task YAML file:

- `make check-argument-specs`
- `make check-license-header`
- `git diff --check`

Inspect the final diff and status to confirm that only the role task file is
part of the implementation change and that the temporary regression playbook
is absent. Do not run `make lint`, deployment or lifecycle targets, install
targets, or documentation generation.

## Success Criteria

- A threshold namespace followed by an MSP-policy namespace uses the correct
  policy and mounts for both iterations.
- MSP DSL policy text is preserved exactly.
- Threshold policy behavior remains unchanged.
- Namespace order no longer changes container inputs.
- No public role interface or generated documentation changes.
- No test artifact or maintained inventory change is committed.
