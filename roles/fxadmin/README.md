# hyperledger.fabricx.fxadmin

> Fetches and decodes the Fabric-X channel configuration, patches it, and drives the fxadmin endorse/merge/prepare/submit flow for live network reconfigurations.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [bin/build](#binbuild)
  - [bin/compute\_update](#bincompute_update)
  - [bin/decode](#bindecode)
  - [bin/follow](#binfollow)
  - [bin/install](#bininstall)
  - [bin/ledger/config\_latest](#binledgerconfig_latest)
  - [bin/rm](#binrm)
  - [bin/transfer](#bintransfer)
  - [bin/tx/endorse](#bintxendorse)
  - [bin/tx/merge](#bintxmerge)
  - [bin/tx/prepare](#bintxprepare)
  - [bin/tx/submit](#bintxsubmit)
  - [compute\_update](#compute_update)
  - [config/mtls/transfer](#configmtlstransfer)
  - [config/transfer](#configtransfer)
  - [container/compute\_update](#containercompute_update)
  - [container/decode](#containerdecode)
  - [container/follow](#containerfollow)
  - [container/ledger/config\_latest](#containerledgerconfig_latest)
  - [container/tx/endorse](#containertxendorse)
  - [container/tx/merge](#containertxmerge)
  - [container/tx/prepare](#containertxprepare)
  - [container/tx/submit](#containertxsubmit)
  - [crypto/cryptogen/transfer](#cryptocryptogentransfer)
  - [crypto/fabric\_ca/enroll](#cryptofabric_caenroll)
  - [crypto/fetch](#cryptofetch)
  - [decode](#decode)
  - [follow](#follow)
  - [ledger/config\_latest](#ledgerconfig_latest)
  - [patch\_config\_value](#patch_config_value)
  - [tx/endorse](#txendorse)
  - [tx/merge](#txmerge)
  - [tx/prepare](#txprepare)
  - [tx/submit](#txsubmit)
  - [wipe](#wipe)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.fxadmin
```

## Tasks

### bin/build

> Build the fxadmin binary

Builds the fxadmin Go binary from the configured Fabric-X source package by delegating compilation to the shared bin role.

```yaml
- name: Build the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Selects the Git ref used by build and install workflows. Pinned to a commit rather than the `v1.0.0` tag: `tools/fxadmin` was added to the `hyperledger/fabric-x` repository after `v1.0.0` was cut, so `go install ...@v1.0.0` fails with "module found, but does not contain package". Bump this once a tagged release actually includes `tools/fxadmin`.
    fxadmin_git_commit: 05bd6b7bf4686837a129baef5916d360810eee5b
    # Defines the Git host used to resolve the Fabric-X source repository.
    fxadmin_git_hub_url: github.com
    # Defines the Fabric-X source repository path.
    fxadmin_git_repo: hyperledger/fabric-x
    # Defines the Go package path containing the fxadmin source code.
    fxadmin_source_code_package: tools/fxadmin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/build
```

### bin/compute_update

> Compute a ConfigUpdate with the fxadmin binary

Runs `fxadmin compute-update` with the local fxadmin binary to compute the delta between the current and modified channel configuration.

```yaml
- name: Compute a ConfigUpdate with the fxadmin binary
  vars:
    # Sets the control-node directory searched for CLI binaries. Only entrypoints that never leave the control node (`decode`, `compute_update`, `tx/merge`) prefix commands with this directory; entrypoints that authenticate as an organization's identity run on that organization's own reference host instead, using the standard per-host `bin_remote_dir`.
    cli_bin_dir: "string"
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines the local decoded current channel configuration JSON file.
    fxadmin_current_config_json: "/tmp/fabricx/config-build/fxadmin-artifacts/current_config.json"
    # Defines the local modified channel configuration JSON file, produced by `patch_config_value` and consumed by `compute_update`.
    fxadmin_modified_config_json: "/tmp/fabricx/config-build/fxadmin-artifacts/modified_config.json"
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/compute_update
```

### bin/decode

> Decode a configuration block with the fxadmin binary

Runs `fxadmin decode` with the local fxadmin binary to convert a protobuf configuration block into JSON.

```yaml
- name: Decode a configuration block with the fxadmin binary
  vars:
    # Sets the control-node directory searched for CLI binaries. Only entrypoints that never leave the control node (`decode`, `compute_update`, `tx/merge`) prefix commands with this directory; entrypoints that authenticate as an organization's identity run on that organization's own reference host instead, using the standard per-host `bin_remote_dir`.
    cli_bin_dir: "string"
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the local protobuf-encoded configuration block to decode into JSON.
    fxadmin_config_block: "/tmp/fabricx/config-build/fxadmin-artifacts/config.pb"
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/decode
```

### bin/follow

> Follow the ledger with the fxadmin binary

Runs `fxadmin follow` with the local fxadmin binary and rendered admin configuration to confirm a submitted configuration update commits, then fetches the resulting block back to the control node.

```yaml
- name: Follow the ledger with the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines how long `follow` waits for the submitted configuration update to commit.
    fxadmin_follow_timeout: 60s
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the control-node destination path that `fxadmin_output` is fetched back to once the command completes on a remote organization reference host.
    fxadmin_output_fetch_dest: "string"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/follow
```

### bin/install

> Install the fxadmin binary

Installs the fxadmin Go package from the configured Fabric-X source package by delegating to the shared bin role.

```yaml
- name: Install the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the Go package path used to install fxadmin.
    fxadmin_bin_package: "{{ fxadmin_git_hub_url }}/{{ fxadmin_git_repo }}/{{ fxadmin_source_code_package }}"
    # Selects the Git ref used by build and install workflows. Pinned to a commit rather than the `v1.0.0` tag: `tools/fxadmin` was added to the `hyperledger/fabric-x` repository after `v1.0.0` was cut, so `go install ...@v1.0.0` fails with "module found, but does not contain package". Bump this once a tagged release actually includes `tools/fxadmin`.
    fxadmin_git_commit: 05bd6b7bf4686837a129baef5916d360810eee5b
    # Defines the Git host used to resolve the Fabric-X source repository.
    fxadmin_git_hub_url: github.com
    # Defines the Fabric-X source repository path.
    fxadmin_git_repo: hyperledger/fabric-x
    # Defines the Go package path containing the fxadmin source code.
    fxadmin_source_code_package: tools/fxadmin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/install
```

### bin/ledger/config_latest

> Fetch the latest channel configuration block with the fxadmin binary

Runs `fxadmin ledger config latest` with the local fxadmin binary and rendered admin configuration to fetch the current channel configuration block, then fetches it back to the control node.

```yaml
- name: Fetch the latest channel configuration block with the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the control-node destination path that `fxadmin_output` is fetched back to once the command completes on a remote organization reference host.
    fxadmin_output_fetch_dest: "string"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/ledger/config_latest
```

### bin/rm

> Remove the fxadmin binary

Removes the fxadmin binary from the managed host by delegating cleanup to the shared bin role.

```yaml
- name: Remove the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/rm
```

### bin/transfer

> Transfer the fxadmin binary

Transfers the previously built fxadmin binary to the managed host by delegating to the shared bin role.

```yaml
- name: Transfer the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/transfer
```

### bin/tx/endorse

> Endorse a ConfigUpdate with the fxadmin binary

Copies a ConfigUpdate protobuf file to the managed host, endorses it with the local fxadmin binary and rendered admin configuration, then fetches the endorsement into the shared endorsements directory.

```yaml
- name: Endorse a ConfigUpdate with the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the local ConfigUpdate protobuf file to endorse.
    fxadmin_config_update: "/tmp/fabricx/config-build/fxadmin-artifacts/config_update.pb"
    # Defines the local directory that collects one endorsement file per required organization before merging.
    fxadmin_endorsements_dir: "/tmp/fabricx/config-build/fxadmin-artifacts/endorsements"
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/tx/endorse
```

### bin/tx/merge

> Merge endorsements with the fxadmin binary

Collects endorsement files from the shared endorsements directory and writes a merged ConfigUpdateEnvelope using the local fxadmin binary.

```yaml
- name: Merge endorsements with the fxadmin binary
  vars:
    # Sets the control-node directory searched for CLI binaries. Only entrypoints that never leave the control node (`decode`, `compute_update`, `tx/merge`) prefix commands with this directory; entrypoints that authenticate as an organization's identity run on that organization's own reference host instead, using the standard per-host `bin_remote_dir`.
    cli_bin_dir: "string"
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the local directory that collects one endorsement file per required organization before merging.
    fxadmin_endorsements_dir: "/tmp/fabricx/config-build/fxadmin-artifacts/endorsements"
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/tx/merge
```

### bin/tx/prepare

> Prepare a transaction with the fxadmin binary

Runs `fxadmin tx prepare` with the local fxadmin binary and rendered admin configuration to turn a merged, endorsed ConfigUpdate envelope into a submittable transaction, then fetches it back to the control node.

```yaml
- name: Prepare a transaction with the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the local merged, endorsed ConfigUpdate envelope to prepare into a submittable transaction.
    fxadmin_endorsed_config_update: "/tmp/fabricx/config-build/fxadmin-artifacts/merged.pb"
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the control-node destination path that `fxadmin_output` is fetched back to once the command completes on a remote organization reference host.
    fxadmin_output_fetch_dest: "string"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/tx/prepare
```

### bin/tx/submit

> Submit a transaction with the fxadmin binary

Runs `fxadmin tx submit` with the local fxadmin binary and rendered admin configuration to broadcast the prepared transaction.

```yaml
- name: Submit a transaction with the fxadmin binary
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the local prepared transaction file to submit.
    fxadmin_config_tx: "/tmp/fabricx/config-build/fxadmin-artifacts/config_tx.pb"
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: bin/tx/submit
```

### compute_update

> Compute a ConfigUpdate

Dispatches ConfigUpdate computation to either the host binary or a transient container based on `fxadmin_use_bin`.

```yaml
- name: Compute a ConfigUpdate
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: compute_update
```

### config/mtls/transfer

> Transfer fxadmin mTLS client material

Copies the client certificate and key consumed by fxadmin for mTLS connections into `fxadmin_remote_config_dir`/mtls.

```yaml
- name: Transfer fxadmin mTLS client material
  vars:
    # Defines the certificate path used for fxadmin mTLS, local to the host this task runs on (see `fxadmin_remote_config_dir`). Unlike `hyperledger.fabricx.fxconfig`, fxadmin has no single deployed host to borrow a default TLS identity from -- every organization.users identity gets its own dedicated TLS material, synced onto that identity's own reference host by `config/transfer` before this path is read, so the caller (see playbooks/fxadmin/configs.yaml) always supplies this explicitly.
    fxadmin_mtls_client_cert_path: "{{ fxadmin_remote_config_dir }}/tls/client.crt"
    # Defines the private key path used for fxadmin mTLS, local to the host this task runs on (see `fxadmin_remote_config_dir`). Unlike `hyperledger.fabricx.fxconfig`, fxadmin has no single deployed host to borrow a default TLS identity from -- every organization.users identity gets its own dedicated TLS material, synced onto that identity's own reference host by `config/transfer` before this path is read, so the caller (see playbooks/fxadmin/configs.yaml) always supplies this explicitly.
    fxadmin_mtls_client_key_path: "{{ fxadmin_remote_config_dir }}/tls/client.key"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: config/mtls/transfer
```

### config/transfer

> Transfer fxadmin configuration material

Creates the remote fxadmin configuration directory, renders the admin configuration file, copies MSP material, and stages mTLS assets when the target network enables mTLS.

```yaml
- name: Transfer fxadmin configuration material
  vars:
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the configuration directory mounted inside the fxadmin container.
    fxadmin_container_config_dir: /config
    # Defines the source MSP directory copied into the fxadmin configuration directory.
    fxadmin_msp_config_path: "/tmp/fabricx/config-build/crypto/ordererOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    # Defines the MSP identifier written into the rendered admin configuration.
    fxadmin_msp_id: "{{ organization.name }}MSP"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
    # Enables mTLS material rendering and transfer for fxadmin, mirroring the target Fabric-X network's mTLS setting.
    fxadmin_use_mtls: false
    # Enables TLS in the rendered admin configuration, mirroring the target Fabric-X network's TLS setting.
    fxadmin_use_tls: false
    # Provides organization metadata used by tasks that read `organization.*`, including names and users.
    organization:{'name': 'Org1', 'domain': 'org1.example.com', 'users': [{'name': 'Admin', 'endorser': true}]}
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: config/transfer
```

### container/compute_update

> Compute a ConfigUpdate with the fxadmin container

Mounts the current and modified configuration JSON files and the reference block into a transient fxadmin container, then runs `fxadmin compute-update`.

```yaml
- name: Compute a ConfigUpdate with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines the local decoded current channel configuration JSON file.
    fxadmin_current_config_json: "/tmp/fabricx/config-build/fxadmin-artifacts/current_config.json"
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the local modified channel configuration JSON file, produced by `patch_config_value` and consumed by `compute_update`.
    fxadmin_modified_config_json: "/tmp/fabricx/config-build/fxadmin-artifacts/modified_config.json"
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/compute_update
```

### container/decode

> Decode a configuration block with the fxadmin container

Mounts the configuration block into a transient fxadmin container and runs `fxadmin decode`.

```yaml
- name: Decode a configuration block with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the local protobuf-encoded configuration block to decode into JSON.
    fxadmin_config_block: "/tmp/fabricx/config-build/fxadmin-artifacts/config.pb"
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/decode
```

### container/follow

> Follow the ledger with the fxadmin container

Mounts the rendered admin configuration and the reference block into a transient fxadmin container, runs `fxadmin follow`, then fetches the resulting block back to the control node.

```yaml
- name: Follow the ledger with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the configuration directory mounted inside the fxadmin container.
    fxadmin_container_config_dir: /config
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines how long `follow` waits for the submitted configuration update to commit.
    fxadmin_follow_timeout: 60s
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the control-node destination path that `fxadmin_output` is fetched back to once the command completes on a remote organization reference host.
    fxadmin_output_fetch_dest: "string"
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/follow
```

### container/ledger/config_latest

> Fetch the latest channel configuration block with the fxadmin container

Mounts the rendered admin configuration and the reference block into a transient fxadmin container, runs `fxadmin ledger config latest`, then fetches it back to the control node.

```yaml
- name: Fetch the latest channel configuration block with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the configuration directory mounted inside the fxadmin container.
    fxadmin_container_config_dir: /config
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the control-node destination path that `fxadmin_output` is fetched back to once the command completes on a remote organization reference host.
    fxadmin_output_fetch_dest: "string"
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/ledger/config_latest
```

### container/tx/endorse

> Endorse a ConfigUpdate with the fxadmin container

Copies a ConfigUpdate protobuf file to the managed host, mounts the rendered admin configuration into a transient fxadmin container, and fetches the endorsement into the shared endorsements directory.

```yaml
- name: Endorse a ConfigUpdate with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the local ConfigUpdate protobuf file to endorse.
    fxadmin_config_update: "/tmp/fabricx/config-build/fxadmin-artifacts/config_update.pb"
    # Defines the configuration directory mounted inside the fxadmin container.
    fxadmin_container_config_dir: /config
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the local directory that collects one endorsement file per required organization before merging.
    fxadmin_endorsements_dir: "/tmp/fabricx/config-build/fxadmin-artifacts/endorsements"
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/tx/endorse
```

### container/tx/merge

> Merge endorsements with the fxadmin container

Mounts the shared endorsements directory into a transient fxadmin container and writes a merged ConfigUpdateEnvelope.

```yaml
- name: Merge endorsements with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the local directory that collects one endorsement file per required organization before merging.
    fxadmin_endorsements_dir: "/tmp/fabricx/config-build/fxadmin-artifacts/endorsements"
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/tx/merge
```

### container/tx/prepare

> Prepare a transaction with the fxadmin container

Mounts the endorsed ConfigUpdate envelope and the rendered admin configuration into a transient fxadmin container, runs `fxadmin tx prepare`, then fetches the prepared transaction back to the control node.

```yaml
- name: Prepare a transaction with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the configuration directory mounted inside the fxadmin container.
    fxadmin_container_config_dir: /config
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the local merged, endorsed ConfigUpdate envelope to prepare into a submittable transaction.
    fxadmin_endorsed_config_update: "/tmp/fabricx/config-build/fxadmin-artifacts/merged.pb"
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the output artifact path written by the current fxadmin command, local to the host the task runs on.
    fxadmin_output: "string"
    # Defines the control-node destination path that `fxadmin_output` is fetched back to once the command completes on a remote organization reference host.
    fxadmin_output_fetch_dest: "string"
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/tx/prepare
```

### container/tx/submit

> Submit a transaction with the fxadmin container

Mounts the prepared transaction and the reference block into a transient fxadmin container and runs `fxadmin tx submit`.

```yaml
- name: Submit a transaction with the fxadmin container
  vars:
    # Defines the fxadmin binary name.
    fxadmin_bin_name: fxadmin
    # Defines the fxadmin admin configuration filename.
    fxadmin_config_file: admin.yaml
    # Defines the local prepared transaction file to submit.
    fxadmin_config_tx: "/tmp/fabricx/config-build/fxadmin-artifacts/config_tx.pb"
    # Defines the configuration directory mounted inside the fxadmin container.
    fxadmin_container_config_dir: /config
    # Defines the base container name used by fxadmin workflows. Includes `inventory_hostname` by default so container names never collide when this role runs across multiple hosts in parallel.
    fxadmin_container_name: "fxadmin-{{ inventory_hostname }}"
    # Defines the local reference configuration block used by fxadmin for identity and network endpoint discovery. For the very first invocation this is the channel's genesis/bootstrap block; afterwards it is the block most recently fetched via `ledger/config_latest`.
    fxadmin_current_block: "/tmp/fabricx/config-build/genesis.block"
    # Defines the fxadmin container image.
    fxadmin_image: "{{ fxadmin_registry_endpoint }}/{{ fxadmin_image_name }}:{{ fxadmin_image_tag }}"
    # Defines the image name used by the fxadmin container image.
    fxadmin_image_name: fabric-x-tools
    # Defines the image tag used by the fxadmin container image.
    fxadmin_image_tag: 1.0.0
    # Defines the registry endpoint used by the fxadmin container image.
    fxadmin_registry_endpoint: "{{ lookup('env', 'FXADMIN_REGISTRY_ENDPOINT') or 'docker.io/hyperledger' }}"
    # Defines the fxadmin remote configuration directory.
    fxadmin_remote_config_dir: "{{ remote_config_dir }}/fxadmin"
    # Provides the base remote configuration directory used by the role.
    remote_config_dir: "/opt/hyperledger/fabricx/config"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: container/tx/submit
```

### crypto/cryptogen/transfer

> Fetch a cryptogen-generated identity

Fetches the `<fxadmin_identity_name>@<domain>` identity (MSP and TLS material) cryptogen unconditionally generates for an orderer organization, which `hyperledger.fabricx.cryptogen`'s own fetch task never copies to the control node.

```yaml
- name: Fetch a cryptogen-generated identity
  vars:
    # Defines the base local build directory used to derive fxadmin's own artifacts and, as a fallback, cryptogen's output location.
    config_build_dir: "string"
    # Sets the directory where cryptogen writes generated crypto material. Owned by `hyperledger.fabricx.cryptogen`; only reliably set while that role's own tasks are executing, so fxadmin falls back to deriving it from `config_build_dir` otherwise.
    cryptogen_output_dir: "string"
    # Defines the local directory that stores fetched crypto artifacts consumed by fxadmin.
    fetched_artifacts_dir: "/tmp/fabricx/config-build"
    # Selects which of organization.users a crypto provisioning task acts on, by name.
    fxadmin_identity_name: "ordererorg1-admin"
    # Defines the Fabric CA `--id.type` used to register the identity (for example `admin` or `client`), which drives its NodeOU role classification. Sourced from the identity's organization.users entry.
    fxadmin_identity_type: "string"
    # Provides organization metadata used by tasks that read `organization.*`, including names and users.
    organization:{'name': 'Org1', 'domain': 'org1.example.com', 'users': [{'name': 'Admin', 'endorser': true}]}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: crypto/cryptogen/transfer
```

### crypto/fabric_ca/enroll

> Register and enroll an identity with Fabric CA

Registers and enrolls an org-level identity (MSP and a dedicated TLS identity) for an orderer organization on its Fabric CA host, then fetches the enrolled material to the control node. Nothing else provisions this identity today; orderer nodes only enroll their own node identity.

```yaml
- name: Register and enroll an identity with Fabric CA
  vars:
    # Defines the local directory that stores fetched crypto artifacts consumed by fxadmin.
    fetched_artifacts_dir: "/tmp/fabricx/config-build"
    # Selects which of organization.users a crypto provisioning task acts on, by name.
    fxadmin_identity_name: "ordererorg1-admin"
    # Defines the Fabric CA enrollment secret for the identity, sourced from its organization.users entry.
    fxadmin_identity_secret: "string"
    # Defines the Fabric CA `--id.type` used to register the identity (for example `admin` or `client`), which drives its NodeOU role classification. Sourced from the identity's organization.users entry.
    fxadmin_identity_type: "string"
    # Provides organization metadata used by tasks that read `organization.*`, including names and users.
    organization:{'name': 'Org1', 'domain': 'org1.example.com', 'users': [{'name': 'Admin', 'endorser': true}]}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: crypto/fabric_ca/enroll
```

### crypto/fetch

> Provision every identity declared in an orderer organization's users

Dispatches identity provisioning for every entry in `organization.users` to either the cryptogen or Fabric CA path based on whether `organization.fabric_ca_host` is defined.

```yaml
- name: Provision every identity declared in an orderer organization's users
  vars:
    # Provides organization metadata used by tasks that read `organization.*`, including names and users.
    organization:{'name': 'Org1', 'domain': 'org1.example.com', 'users': [{'name': 'Admin', 'endorser': true}]}
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: crypto/fetch
```

### decode

> Decode a configuration block

Dispatches configuration block decoding to either the host binary or a transient container based on `fxadmin_use_bin`.

```yaml
- name: Decode a configuration block
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: decode
```

### follow

> Follow the ledger until a configuration update commits

Dispatches ledger following to either the host binary or a transient container based on `fxadmin_use_bin`.

```yaml
- name: Follow the ledger until a configuration update commits
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: follow
```

### ledger/config_latest

> Fetch the latest channel configuration block

Dispatches fetching the latest channel configuration block to either the host binary or a transient container based on `fxadmin_use_bin`.

```yaml
- name: Fetch the latest channel configuration block
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: ledger/config_latest
```

### patch_config_value

> Patch a decoded channel configuration

Reads the decoded current channel configuration JSON, deep-merges a caller-supplied partial structure into it, and writes the resulting modified configuration JSON. Contains no business logic of its own -- the caller supplies the exact nested path and value to change, keeping this role a generic fxadmin wrapper reusable by any future reconfiguration flow.

```yaml
- name: Patch a decoded channel configuration
  vars:
    # Defines the local decoded current channel configuration JSON file.
    fxadmin_current_config_json: "/tmp/fabricx/config-build/fxadmin-artifacts/current_config.json"
    # Defines a partial JSON structure deep-merged into the decoded current configuration to produce the modified configuration. Shaped like the nested path within the decoded config that needs to change; the caller supplies this, keeping the role itself agnostic of any specific reconfiguration business rule. Channel-config groups are keyed by the plain organization name (for example `Org1`), not its MSP ID (`Org1MSP`).
    fxadmin_json_patch:
      channel_group:
        groups:
          Orderer:
            groups:
              Org1:
                values:
                  Endpoint:
                    value:
                      host: "orderer1-assembler"
                      port: 7060
    # Defines the local modified channel configuration JSON file, produced by `patch_config_value` and consumed by `compute_update`.
    fxadmin_modified_config_json: "/tmp/fabricx/config-build/fxadmin-artifacts/modified_config.json"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: patch_config_value
```

### tx/endorse

> Endorse a ConfigUpdate

Dispatches ConfigUpdate endorsement to either the host binary or a transient container based on `fxadmin_use_bin`.

```yaml
- name: Endorse a ConfigUpdate
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: tx/endorse
```

### tx/merge

> Merge endorsements

Dispatches endorsement merging to either the host binary or a transient container based on `fxadmin_use_bin`, then removes the spent per-organization endorsement files.

```yaml
- name: Merge endorsements
  vars:
    # Defines the local directory that collects one endorsement file per required organization before merging.
    fxadmin_endorsements_dir: "/tmp/fabricx/config-build/fxadmin-artifacts/endorsements"
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: tx/merge
```

### tx/prepare

> Prepare a transaction

Dispatches transaction preparation to either the host binary or a transient container based on `fxadmin_use_bin`.

```yaml
- name: Prepare a transaction
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: tx/prepare
```

### tx/submit

> Submit a transaction

Dispatches transaction submission to either the host binary or a transient container based on `fxadmin_use_bin`.

```yaml
- name: Submit a transaction
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: tx/submit
```

### wipe

> Remove generated fxadmin files

Removes the fxadmin binary when the host-binary workflow is selected.

```yaml
- name: Remove generated fxadmin files
  vars:
    # Selects the host-binary workflow instead of the container workflow.
    fxadmin_use_bin: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.fxadmin
    tasks_from: wipe
```
