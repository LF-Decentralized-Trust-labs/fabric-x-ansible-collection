#!/usr/bin/env bash

#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# Vault password resolver wired in as `vault_password_file` in examples/ansible.cfg.
# Ansible treats an executable vault_password_file as a script and uses its stdout
# as the password, so this can stay configured for every command without requiring
# a local Vault password file: resolution only matters once Ansible actually
# decrypts vaulted content, so any inventory without Vault-encrypted variables
# (every sample except examples/inventory/local/fabric-x-vault.yaml) keeps working
# with no password file present. See docs/tutorial/12-using-ansible-vault-for-secrets.md.
#
# Create `.vault_pass` at the repository root (gitignored by `.vault_pass*` in
# .gitignore; never commit it) with your Vault password to use this automatically.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
vault_pass_file="${repo_root}/.vault_pass"

if [[ -f "$vault_pass_file" ]]; then
    cat "$vault_pass_file"
else
    # No local Vault password configured. Emitting a placeholder (rather than
    # nothing) keeps every command that never touches vaulted content working;
    # Ansible only reports an error at the point a Vault-encrypted variable is
    # actually decrypted.
    echo "no-local-vault-pass-configured"
fi
