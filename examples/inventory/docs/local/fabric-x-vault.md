# local/fabric-x-vault.yaml

[`fabric-x-vault.yaml`](../../local/fabric-x-vault.yaml) is the same topology as [`fabric-x.yaml`](../../local/fabric-x.yaml) — same hosts, same ports, same groups — with every credential encrypted using [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html) instead of stored as plain text.

Use this inventory as a reference for a secured deployment strategy, or as a starting point for encrypting the credentials of your own inventory. See [12. Using Ansible Vault for Secrets](../../../../docs/tutorial/12-using-ansible-vault-for-secrets.md) for how to configure, view, and edit it.

## Table of Contents <!-- omit in toc -->

- [Network Diagram](#network-diagram)
- [What Is Vaulted](#what-is-vaulted)
- [Running It](#running-it)
- [Inventory Details](#inventory-details)

## Network Diagram

This inventory is topologically identical to `fabric-x.yaml`; see that inventory's [network diagram](./fabric-x.md#network-diagram) for the service layout.

## What Is Vaulted

Every credential is replaced with an `!vault |` encrypted block, or, for the per-host Fabric CA enrollment secrets, with a Jinja expression referencing a single Vault-encrypted variable shared across hosts:

| Variable | Where |
| --------------------------------- | ------------------------------------------------------------------ |
| `postgres_password` | Fabric CA databases, the committer database, the Block Explorer database |
| `fabric_ca_admin.secret` | Every Fabric CA server |
| `grafana_password` | The Grafana host |
| `vault_identity_secret_suffix` | Referenced by every orderer, committer, and load generator enrollment secret (`all.vars`) |

## Running It

The password used to encrypt this inventory is `fabricx-vault-demo`, documented here so the reference is actually runnable — every plaintext value it protects is already public in `fabric-x.yaml`, so this is a worked example of the mechanism, not a real secret boundary:

```shell
echo -n 'fabricx-vault-demo' > .vault_pass
export ANSIBLE_INVENTORY=examples/inventory/local/fabric-x-vault.yaml
make setup start init
```

`examples/ansible.cfg` resolves the Vault password automatically through [`scripts/resolve_vault_password.sh`](../../../../scripts/resolve_vault_password.sh) once `.vault_pass` exists, so no `--vault-password-file` or `--ask-vault-pass` flag is needed on any command, including the `make` targets. Remove `.vault_pass` when you are done; it is gitignored and must never be committed.

## Inventory Details

See [`fabric-x.yaml`'s inventory details](./fabric-x.md#inventory-details) — the deployed services, their organization, and their security posture are unchanged. The only difference is how credentials are stored, not what they are or how the network behaves.
