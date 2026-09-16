# 12. Using Ansible Vault for Secrets

Every sample inventory so far, including the one you built in the last lesson, stores its credentials in plain text: `postgres_password: example`, `secret: adminPWD`. That is fine for a local learning exercise on your own machine. It is not fine for an inventory you commit, share, or run against anything that matters. This lesson replaces plaintext credentials with [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html)-encrypted ones, using the collection's own reference inventory as a worked example.

> [!NOTE]
> Estimated time: 25 minutes. Builds on [11. Write Your Own Inventory](./11-write-your-own-inventory.md).

## Table of Contents <!-- omit in toc -->

- [What You Will Learn](#what-you-will-learn)
- [The Reference Inventory](#the-reference-inventory)
- [Viewing It](#viewing-it)
- [How a Vaulted Value Looks in an Inventory](#how-a-vaulted-value-looks-in-an-inventory)
- [Stop Typing the Password: `ANSIBLE_VAULT_PASSWORD_FILE`](#stop-typing-the-password-ansible_vault_password_file)
- [Deploying It](#deploying-it)
- [Encrypting Your Own Secrets](#encrypting-your-own-secrets)
  - [A Whole File: `ansible-vault create` / `edit`](#a-whole-file-ansible-vault-create--edit)
  - [One Value In Place: `ansible-vault encrypt_string`](#one-value-in-place-ansible-vault-encrypt_string)
- [Applying This to Your Own Inventory](#applying-this-to-your-own-inventory)
- [Exercise](#exercise)
- [Next](#next)

## What You Will Learn

- Where the collection's Vault-compatible reference inventory lives and what makes it different from `fabric-x.yaml`.
- How to view and run a Vault-protected inventory.
- How to set `ANSIBLE_VAULT_PASSWORD_FILE` so you stop typing `--vault-password-file` on every command.
- How to encrypt a whole file, or a single value in place, with `ansible-vault`.
- How to move your own inventory's credentials from lesson 11 behind Vault.

## The Reference Inventory

[`examples/inventory/local/fabric-x-vault.yaml`](../../examples/inventory/local/fabric-x-vault.yaml) is byte-for-byte the same topology as [`fabric-x.yaml`](../../examples/inventory/local/fabric-x.yaml) — same hosts, same ports, same groups — with every credential encrypted instead of written in the open:

| Plaintext (`fabric-x.yaml`) | Vaulted (`fabric-x-vault.yaml`) |
| --------------------------------------------------- | ------------------------------------------------------------------------ |
| `postgres_password: example` | `postgres_password: !vault \|` followed by an encrypted block |
| `fabric_ca_admin.secret: adminPWD` | `secret: !vault \|` followed by an encrypted block |
| `grafana_password: adminPWD` | `grafana_password: !vault \|` followed by an encrypted block |
| `orderer.secret: "{{ inventory_hostname }}PWD"` | `orderer.secret: "{{ inventory_hostname }}{{ vault_identity_secret_suffix }}"`, where `vault_identity_secret_suffix` is itself a Vault-encrypted value defined once in `all.vars` |

That last row is worth pausing on. Fabric CA enrollment secrets are built from a per-host template (`<hostname>PWD`), not one fixed string, so there is nothing single to encrypt per host. Instead, the collection encrypts the shared *suffix* once and lets every host's Jinja expression reference it — one Vault-protected variable standing in for what would otherwise be dozens of near-identical secrets.

> [!NOTE]
> Every plaintext value this lesson decrypts (`example`, `adminPWD`, `sc_secret_pwd`, `block_explorer_pwd`, `PWD`) is already sitting in the open in `fabric-x.yaml`. This inventory exists to demonstrate the mechanism, not to protect a real secret — treat it as a worked example, not a security boundary. Use a Vault password nobody else knows for anything beyond this lesson.

## Viewing It

The password used to encrypt `fabric-x-vault.yaml` for this tutorial is `fabricx-vault-demo`:

```shell
echo -n 'fabricx-vault-demo' > .vault_pass
```

You might reach for `ansible-vault view` next, the way you would for a whole encrypted file — but it fails here:

```shell
.venv/bin/ansible-vault view --vault-password-file .vault_pass examples/inventory/local/fabric-x-vault.yaml
# [ERROR]: Input is not vault encrypted data.
```

`ansible-vault view` only decrypts a file that is encrypted *as a whole*. `fabric-x-vault.yaml` is not — most of it is plain YAML, with individual values encrypted in place as `!vault` blocks (the technique this lesson focuses on; the whole-file alternative is covered later, in [Encrypting Your Own Secrets](#encrypting-your-own-secrets)). Ansible only decrypts an inline value at the moment a task or template actually reads it, so seeing the plaintext means asking Ansible to read it — which is exactly what this repository's `vault-view` target does:

```shell
export ANSIBLE_INVENTORY=examples/inventory/local/fabric-x-vault.yaml
make vault-view TARGET_HOSTS=fca-orderer-org1-db VAULT_VAR_NAME=postgres_password
```

This runs [`examples/playbooks/998-vault-view.yaml`](../../examples/playbooks/998-vault-view.yaml), which prints the named variable for the targeted host or group, decrypted — `example`, here. Omit `VAULT_VAR_NAME` to print every variable instead of one, and omit `TARGET_HOSTS` (default `all`) to print the whole inventory, every host.

> [!TIP]
> Every Vault-protected value in `fabric-x-vault.yaml` is also written as a `# decrypted value: ...` comment directly above its encrypted block, so you can look one up by just reading the file — no command needed. This particular inventory exists purely to demonstrate the mechanism, so nothing in it is worth protecting from a curious reader; do not carry that habit into an inventory holding real credentials.

You can also query a single variable directly, exactly as you validated your own inventory in lesson 11:

```shell
.venv/bin/ansible-inventory -i examples/inventory/local/fabric-x-vault.yaml --vault-password-file .vault_pass --graph
.venv/bin/ansible fca-orderer-org1-db -i examples/inventory/local/fabric-x-vault.yaml \
  --vault-password-file .vault_pass -m ansible.builtin.debug -a "msg={{ postgres_password }}"
```

The second command prints `example` — Ansible transparently decrypts the value the moment a task or template reads it. Nothing downstream of the inventory (roles, playbooks, generated configuration) needs to know or care that a variable came from a Vault-encrypted block instead of plain text.

## How a Vaulted Value Looks in an Inventory

Open [`fabric-x-vault.yaml`](../../examples/inventory/local/fabric-x-vault.yaml) and find `fabric_ca_dbs.vars.postgres_password`:

```yaml
postgres_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          61633237636237613434616238623766373335653438613236623634356263663664313631323666
          ...
```

Three things to notice:

- `!vault` is a YAML tag. It tells Ansible's loader "decrypt this before handing it to anything else" — the surrounding inventory does not need any special syntax to consume it.
- The header line `$ANSIBLE_VAULT;1.1;AES256` records the format version and cipher, not the password. Losing the password still means losing the data; this line alone decrypts nothing.
- The block is a YAML literal scalar (`|`), so its continuation lines only need to be indented *more* than the `key:` line — the exact column does not matter, which is why you will see different indentation depths for a top-level `all.vars` entry versus one nested five groups deep.

## Stop Typing the Password: `ANSIBLE_VAULT_PASSWORD_FILE`

Passing `--vault-password-file .vault_pass` on every command gets old fast — and none of the `make` targets you have used throughout this tutorial (`make setup`, `make vault-view`, `make vault-encrypt`, ...) have a flag for it at all. Ansible's own `ANSIBLE_VAULT_PASSWORD_FILE` environment variable solves this without adding anything to `examples/ansible.cfg`:

```shell
export ANSIBLE_VAULT_PASSWORD_FILE="$PWD/.vault_pass"
```

Every `ansible`, `ansible-playbook`, `ansible-inventory`, and `ansible-vault` command in this shell session now decrypts using `.vault_pass` automatically, including inside `make` targets — they run in the same environment. The commands from [Viewing It](#viewing-it) no longer need a flag:

```shell
.venv/bin/ansible-inventory -i examples/inventory/local/fabric-x-vault.yaml --graph
```

> [!WARNING]
> This is session-wide, not scoped to `fabric-x-vault.yaml`. Once exported, **every** Ansible command in this shell tries to use `.vault_pass` as its Vault password — including ones against inventories with no Vault content at all, like `fabric-x.yaml` or the inventory you built in lesson 11. If `.vault_pass` is missing, or holds the wrong password, those commands fail too, immediately, with no graceful fallback. Unset it (and remove the file) once you are done with this lesson:
>
> ```shell
> unset ANSIBLE_VAULT_PASSWORD_FILE
> rm -f .vault_pass
> ```
>
> `.vault_pass` is gitignored (`.vault_pass*` in [`.gitignore`](../../.gitignore)). Never commit it, and never put a real Vault password in a file, environment variable, or command line that ends up in a shell history you share.

## Deploying It

Viewing the file proves the decryption works. Actually running it proves the rest of the collection — roles, playbooks, generated configuration — behaves identically whether a credential came from plain text or from Vault. Nothing else changes from how you have deployed every other inventory in this tutorial, since `ANSIBLE_VAULT_PASSWORD_FILE` from the previous section is already exported:

```shell
export ANSIBLE_INVENTORY=examples/inventory/local/fabric-x-vault.yaml
make setup start init
make ping
```

If you skipped straight here: `make` targets have no flag for the Vault password, so this only works with `ANSIBLE_VAULT_PASSWORD_FILE` already exported, as shown in [Stop Typing the Password](#stop-typing-the-password-ansible_vault_password_file) above.

When you are done experimenting, tear down and clean up — the network, the password file, and the environment variable must not stay behind:

```shell
make teardown wipe
unset ANSIBLE_VAULT_PASSWORD_FILE
rm -f .vault_pass
```

> [!TIP]
> [`examples/inventory/docs/local/fabric-x-vault.md`](../../examples/inventory/docs/local/fabric-x-vault.md) is this inventory's own reference page, with the same steps and a summary of exactly which variables are Vault-protected.

## Encrypting Your Own Secrets

There are two distinct techniques for bringing Vault into your own inventory. Neither is more secure than the other — AES-256 either way — they trade off differently, and picking one is a structural decision for the file, not a per-value one:

| | Whole file (`create` / `edit`) | One value in place (`encrypt_string`) |
| --- | --- | --- |
| What gets encrypted | Every variable in the file, including names | Only the one value you run it on |
| The key in your inventory | Renamed to a `vault_*` variable, referenced from elsewhere (`{{ vault_committer_db_password }}`) | Unchanged — `postgres_password:` stays `postgres_password:`, only its value becomes a `!vault` block |
| Rest of the file | Untouched, still plain YAML | Untouched, still plain YAML |
| Best for | A dedicated secrets file you keep entirely separate, e.g. an operator's own bundle | A mostly-public or mostly-readable inventory where only specific fields need to be opaque |
| Used by | The [`creating-fabricx-inventories`](../../.agents/skills/creating-fabricx-inventories/SKILL.md) agent skill's `group_vars/all/vault.yaml` | `fabric-x-vault.yaml`, this lesson's [Applying This to Your Own Inventory](#applying-this-to-your-own-inventory) |

### A Whole File: `ansible-vault create` / `edit`

Use this for a dedicated secrets file, referenced by variable name from your main inventory — the pattern the [`creating-fabricx-inventories`](../../.agents/skills/creating-fabricx-inventories/SKILL.md) agent skill uses for an operator bundle's `group_vars/all/vault.yaml`:

```shell
.venv/bin/ansible-vault create my-network/group_vars/all/vault.yaml
```

This opens your `$EDITOR` on a decrypted buffer; write plain YAML (`vault_committer_db_password: sc_secret_pwd`) and it is encrypted on save. The file on disk is fully encrypted, including variable names — `cat` it and you see only an `$ANSIBLE_VAULT` header. Edit it later with `ansible-vault edit`, and inspect it without opening an editor with `ansible-vault view`.

### One Value In Place: `ansible-vault encrypt_string`

Use this when you want most of the inventory readable and only specific values protected — the pattern `fabric-x-vault.yaml` uses throughout. The convenient way is the `make` target this repository wires up for exactly this:

```shell
make vault-encrypt VAULT_VAR_NAME=postgres_password
# Type the value, then press Enter followed by Ctrl-D:
sc_secret_pwd
```

The equivalent raw command:

```shell
.venv/bin/ansible-vault encrypt_string --vault-password-file .vault_pass --stdin-name 'postgres_password'
```

Either way prints a ready-to-paste `key: !vault |` block, exactly like the ones in `fabric-x-vault.yaml`. Paste it in place of the plaintext value at the same indentation as the key it replaces — the file stays otherwise readable, and only the credential itself is opaque.

> [!WARNING]
> Do not pass the secret as a trailing command-line argument (`encrypt_string --name X 'the-secret'`). It lands in your shell history in plain text, in a file most shells keep forever. `--stdin-name` reads the value from stdin instead, so it is only ever typed, never remembered by the shell — though note it is *not* hidden as you type it, the way a password prompt would be, so avoid running this where someone can see your screen.
>
> Separately: encrypting the same plaintext twice produces *different* ciphertext each time — `encrypt_string` uses a random salt per call. That is expected; both blocks decrypt to the same value. Do not compare inventories by diffing ciphertext.

## Applying This to Your Own Inventory

Go back to the inventory you wrote in [lesson 11](./11-write-your-own-inventory.md) and its `sc_user` / `sc_secret_pwd` warning. Replace the plaintext `postgres_password`:

```shell
make vault-encrypt VAULT_VAR_NAME=postgres_password
# Type the value, then press Enter followed by Ctrl-D:
sc_secret_pwd
```

Paste the resulting block over the plaintext line in `my-network/fabric-x-minimal.yaml`, at `committer-db`'s existing indentation. Then confirm it still resolves:

```shell
.venv/bin/ansible-inventory -i my-network/fabric-x-minimal.yaml --vault-password-file .vault_pass \
  --host committer-db | grep -A1 postgres_password
.venv/bin/ansible committer-db -i my-network/fabric-x-minimal.yaml --vault-password-file .vault_pass \
  -m ansible.builtin.debug -a "msg={{ postgres_password }}"
```

The first command shows the encrypted block (proof it is stored safely); the second shows `sc_secret_pwd` (proof it still works). Everything downstream — the role, the rendered configuration, the running PostgreSQL container — is unaffected, because decryption happens at the moment Ansible reads the variable, not at any point your roles or playbooks would need to change.

## Exercise

> [!TIP]
> Finish the job on your lesson-11 inventory.
>
> 1. Encrypt `postgres_password` as shown above.
> 2. The load generator's `secret: orderer-loadgenPWD` is a per-host template, like the orderer identity secrets in `fabric-x-vault.yaml`. Introduce a `vault_identity_secret_suffix` variable in `all.vars`, encrypt just the `PWD` suffix, and update the load generator's `secret:` line to reference it the same way `fabric-x-vault.yaml` does.
> 3. Confirm both with `ansible-inventory --host` and an `ansible ... -m debug` call.
> 4. Export `ANSIBLE_VAULT_PASSWORD_FILE` for your own bundle so you stop passing `--vault-password-file` by hand, the same way this lesson did for `fabric-x-vault.yaml`. Then think about what changes if you want that to persist across shells instead of just this session.

<details markdown="1">
<summary>Solution</summary>

Step 1 is exactly the [Applying This to Your Own Inventory](#applying-this-to-your-own-inventory) section above.

Step 2:

```shell
make vault-encrypt VAULT_VAR_NAME=vault_identity_secret_suffix
# Type the value, then press Enter followed by Ctrl-D:
PWD
```

Paste the result into `all.vars`, alongside `organizations:`. Then change the load generator:

```yaml
    load_generators:
      hosts:
        orderer-loadgen:
          organization:
            <<: *Org1
            role: peer
            users:
              - name: orderer-loadgen
                secret: "{{ inventory_hostname }}{{ vault_identity_secret_suffix }}"
```

Step 3:

```shell
.venv/bin/ansible-inventory -i my-network/fabric-x-minimal.yaml --vault-password-file .vault_pass \
  --host orderer-loadgen | grep -A2 secret
.venv/bin/ansible orderer-loadgen -i my-network/fabric-x-minimal.yaml --vault-password-file .vault_pass \
  -m ansible.builtin.debug -a "msg={{ organization.users[0].secret }}"
```

The second prints `orderer-loadgenPWD` — identical to the plaintext version, because `vault_identity_secret_suffix` decrypts to `PWD` and the surrounding Jinja expression is unchanged.

Step 4:

```shell
export ANSIBLE_VAULT_PASSWORD_FILE="$PWD/.vault_pass"
```

This is exactly what this lesson used for `fabric-x-vault.yaml` — no extra file, no configuration to maintain. Its sharp edge is the one from the [warning above](#stop-typing-the-password-ansible_vault_password_file): it is session-wide, so every Ansible command you run afterward — against this inventory or any other — tries to use `.vault_pass`, and fails immediately if that file is missing or holds the wrong password. That is fine for a bundle only you run, in a shell you control.

To make it persist across shells instead, the direct option is a one-line addition to your own `ansible.cfg`:

```ini
[defaults]
vault_password_file = ./.vault_pass
```

This has the identical failure mode, permanently, for anyone who runs a command in that directory without `.vault_pass` in place — including CI. If that matters (multiple people, or CI, running commands against the same repository without necessarily having Vault secrets configured), point `vault_password_file` at an executable script instead of a fixed path: Ansible treats an executable `vault_password_file` as a resolver and uses its stdout as the password, so the script can check whether `.vault_pass` exists and print a harmless placeholder when it does not — failing only once something actually needs to decrypt, not on every command. This collection's own CI takes a different, narrower route for the same problem: it exports `ANSIBLE_VAULT_PASSWORD_FILE` for just the one job that tests `fabric-x-vault.yaml`, scoped with GitHub Actions' `$GITHUB_ENV`, so every other job's non-Vaulted inventory is entirely unaffected — see [`.github/workflows/test.yaml`](../../.github/workflows/test.yaml).

</details>

## Next

| Previous | Next |
| --------------------------------------------------------------- | ------------------------------------------------------ |
| [11. Write Your Own Inventory](./11-write-your-own-inventory.md) | [13. Troubleshooting](./13-troubleshooting.md) |
