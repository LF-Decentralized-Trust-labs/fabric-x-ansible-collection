# hyperledger.fabricx.semaphore_ui

> Installs and runs Semaphore UI as a binary so operators can launch this collection's playbooks and inventories from a web UI with a live view of progress. Semaphore runs `ansible-playbook` as a local subprocess on its own host, so that host is a persistent control node, matching the collection's fetch/distribute crypto model. The role also seeds a Semaphore project from the repository already on disk: one repository, one inventory per supported example family, and one task template per supported example playbook.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [bin/install](#bininstall)
  - [bin/start](#binstart)
  - [bin/stop](#binstop)
  - [bin/rm](#binrm)
  - [bin/fetch\_logs](#binfetch_logs)
  - [crypto/setup](#cryptosetup)
  - [crypto/openssl/generate\_cert](#cryptoopensslgenerate_cert)
  - [start](#start)
  - [stop](#stop)
  - [fetch\_logs](#fetch_logs)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [ping](#ping)
  - [effective\_address](#effective_address)
  - [config/transfer](#configtransfer)
  - [db/setup](#dbsetup)
  - [config/rm](#configrm)
  - [data/rm](#datarm)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.semaphore_ui
```

## Tasks

### bin/install

> Install the Semaphore UI binary

Downloads the platform-matched Semaphore UI release archive and extracts it, unless the binary is already present.

```yaml
- name: Install the Semaphore UI binary
  vars:
    # Base directory on the managed host under which the Semaphore UI binary is installed.
    remote_node_dir: "/var/lib/fabricx"
    # Semaphore UI release version to install.
    semaphore_ui_version: 2.18.28
    # Selects the release asset prefix. `semaphore_community` is the MIT-licensed open-source build; `semaphore` is the commercially-licensed build.
    semaphore_ui_edition: semaphore_community
    # Executable name of the installed Semaphore UI binary. Also used as its tmux session name.
    semaphore_ui_bin_name: semaphore
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: bin/install
```

### bin/start

> Start the Semaphore UI binary

Starts Semaphore UI in a tmux session and waits for its web port to become reachable.

```yaml
- name: Start the Semaphore UI binary
  vars:
    # Base directory on the managed host for `semaphore_ui_remote_config_dir`.
    remote_config_dir: "/var/lib/fabricx/config"
    # Executable name of the installed Semaphore UI binary. Also used as its tmux session name.
    semaphore_ui_bin_name: semaphore
    # Directory on the managed host holding the rendered Semaphore UI server configuration and project seed files.
    semaphore_ui_remote_config_dir: "{{ remote_config_dir }}"
    # File name of the rendered Semaphore UI server configuration.
    semaphore_ui_config_file: config.json
    # TCP port the Semaphore UI web server listens on. Not the Semaphore UI default of 3000, since Grafana already binds that port on the local family's control node.
    semaphore_ui_port: 3010
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: bin/start
```

### bin/stop

> Stop the Semaphore UI binary

Stops the tmux session running Semaphore UI.

```yaml
- name: Stop the Semaphore UI binary
  vars:
    # Executable name of the installed Semaphore UI binary. Also used as its tmux session name.
    semaphore_ui_bin_name: semaphore
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: bin/stop
```

### bin/rm

> Remove the Semaphore UI binary

Deletes the installed Semaphore UI binary from the managed host.

```yaml
- name: Remove the Semaphore UI binary
  vars:
    # Executable name of the installed Semaphore UI binary. Also used as its tmux session name.
    semaphore_ui_bin_name: semaphore
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: bin/rm
```

### bin/fetch_logs

> Fetch Semaphore UI log output

Copies the Semaphore UI log file from the managed host to the control node without failing when the file is absent.

```yaml
- name: Fetch Semaphore UI log output
  vars:
    # Executable name of the installed Semaphore UI binary. Also used as its tmux session name.
    semaphore_ui_bin_name: semaphore
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: bin/fetch_logs
```

### crypto/setup

> Generate the Semaphore UI TLS certificate

Dispatches TLS certificate generation for Semaphore UI's native HTTPS listener when `semaphore_ui_use_tls` is enabled.

```yaml
- name: Generate the Semaphore UI TLS certificate
  vars:
    # Enables Semaphore UI's native TLS termination (no reverse proxy) using the certificate generated by `crypto/setup`.
    semaphore_ui_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: crypto/setup
```

### crypto/openssl/generate_cert

> Generate the Semaphore UI TLS certificate with OpenSSL

Generates a self-signed TLS certificate and private key for Semaphore UI's native HTTPS listener.

```yaml
- name: Generate the Semaphore UI TLS certificate with OpenSSL
  vars:
    # Base directory on the managed host for `semaphore_ui_remote_config_dir`.
    remote_config_dir: "/var/lib/fabricx/config"
    # Directory on the managed host holding the rendered Semaphore UI server configuration and project seed files.
    semaphore_ui_remote_config_dir: "{{ remote_config_dir }}"
    # Sets the Semaphore UI TLS private key filename.
    semaphore_ui_tls_private_key_file: server.key
    # Sets the Semaphore UI TLS certificate filename.
    semaphore_ui_tls_cert_file: server.crt
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: crypto/openssl/generate_cert
```

### start

> Start the Semaphore UI binary

Migrates and seeds the database if it is missing (`db/setup`), starts the Semaphore UI binary, then prints its effective URL and admin username.

```yaml
- name: Start the Semaphore UI binary
  vars:
    # Login of the Semaphore UI admin user created on `config/transfer`.
    semaphore_ui_username: "admin"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: start
```

### stop

> Stop the Semaphore UI binary

Stops the Semaphore UI binary.

```yaml
- name: Stop the Semaphore UI binary
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: stop
```

### fetch_logs

> Fetch Semaphore UI log output

Copies the Semaphore UI log file from the managed host to the control node without failing when the file is absent.

```yaml
- name: Fetch Semaphore UI log output
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: fetch_logs
```

### teardown

> Stop Semaphore UI and remove its data

Stops the Semaphore UI binary and deletes its data directory (SQLite database, scratch space, and generated secrets). Leaves the installed binary and rendered configuration files in place. A subsequent `start` re-migrates and re-seeds the database (`db/setup`).

```yaml
- name: Stop Semaphore UI and remove its data
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: teardown
```

### wipe

> Remove all Semaphore UI state

Runs `teardown`, then also removes the installed binary and the rendered configuration files.

```yaml
- name: Remove all Semaphore UI state
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: wipe
```

### ping

> Check whether the Semaphore UI port is reachable

Probes `semaphore_ui_port` on the managed host without failing the play.

```yaml
- name: Check whether the Semaphore UI port is reachable
  vars:
    # TCP port the Semaphore UI web server listens on. Not the Semaphore UI default of 3000, since Grafana already binds that port on the local family's control node.
    semaphore_ui_port: 3010
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: ping
```

### effective_address

> Compute the reachable Semaphore UI URL

Sets `semaphore_ui_effective_address` from `actual_host`, `semaphore_ui_port`, and `semaphore_ui_use_tls`.

```yaml
- name: Compute the reachable Semaphore UI URL
  vars:
    # Real machine host.
    actual_host: "myvpc.cloud.ibm.com"
    # TCP port the Semaphore UI web server listens on. Not the Semaphore UI default of 3000, since Grafana already binds that port on the local family's control node.
    semaphore_ui_port: 3010
    # Enables Semaphore UI's native TLS termination (no reverse proxy) using the certificate generated by `crypto/setup`.
    semaphore_ui_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: effective_address
```

### config/transfer

> Render the Semaphore UI server configuration and project seed

Generates and persists the server secrets on first run, then renders `config.json` and the project seed file from templates. Database migration and seeding is not done here: `start` does it (`db/setup`), skipping it when the database already exists.

```yaml
- name: Render the Semaphore UI server configuration and project seed
  vars:
    # Base directory on the managed host for `semaphore_ui_remote_config_dir`.
    remote_config_dir: "/var/lib/fabricx/config"
    # Base directory on the managed host for `semaphore_ui_remote_data_dir`.
    remote_data_dir: "/var/lib/fabricx/data"
    # Project root directory on the managed host. Seeded as the Semaphore UI repository's absolute path, since it is a `local` repository that Semaphore UI runs in place rather than cloning, so generated artifacts (for example `out/control-node`) persist across runs.
    project_dir: "/path/to/hyperledger/fabricx"
    # Root output directory for generated material, as resolved by `examples/inventory/vars.yaml`. Exported to every Semaphore UI task as `ANSIBLE_CACHE_PLUGIN_CONNECTION`, mirroring the Makefile's own `ANSIBLE_CACHE_PLUGIN_CONNECTION` export.
    out_dir: "/path/to/hyperledger/fabricx/out"
    # Directory on the managed host holding the rendered Semaphore UI server configuration and project seed files.
    semaphore_ui_remote_config_dir: "{{ remote_config_dir }}"
    # Directory on the managed host holding the Semaphore UI SQLite database, scratch space, and generated secrets.
    semaphore_ui_remote_data_dir: "{{ remote_data_dir }}"
    # File name of the rendered Semaphore UI server configuration.
    semaphore_ui_config_file: config.json
    # File name of the rendered Semaphore UI project seed, consumed by `semaphore project import`.
    semaphore_ui_project_seed_file: project.json
    # File name of the Semaphore UI SQLite database.
    semaphore_ui_database_file: database.db
    # TCP port the Semaphore UI web server listens on. Not the Semaphore UI default of 3000, since Grafana already binds that port on the local family's control node.
    semaphore_ui_port: 3010
    # Enables Semaphore UI's native TLS termination (no reverse proxy) using the certificate generated by `crypto/setup`.
    semaphore_ui_use_tls: false
    # Sets the Semaphore UI TLS private key filename.
    semaphore_ui_tls_private_key_file: server.key
    # Sets the Semaphore UI TLS certificate filename.
    semaphore_ui_tls_cert_file: server.crt
    # Absolute path on the managed host of the `ansible.cfg` exported as `ANSIBLE_CONFIG` to every Semaphore UI task, so a task launched from the UI picks up the same Ansible settings (`host_key_checking`, `gathering`, `deprecation_warnings`, and so on) as running `make <target>` from a shell. Defaults to the repository's own `examples/ansible.cfg`, the very file the Makefile itself exports as `ANSIBLE_CONFIG`. Point this at any other file, inside or outside `project_dir`, to run Semaphore UI tasks under a different Ansible configuration.
    semaphore_ui_ansible_config_path: "{{ project_dir }}/examples/ansible.cfg"
    # Name of the Semaphore UI project seeded on `config/transfer`.
    semaphore_ui_project_name: Fabric-X
    # Name of the Semaphore UI repository seeded on `config/transfer`.
    semaphore_ui_repository_name: Fabric-X collection
    # Inventories seeded as Semaphore UI `file` inventories, one per Fabric-X network sample under `examples/inventory`. Each item needs `name` and `path` (relative to `project_dir`). Not discovered automatically; kept in sync by hand with `examples/inventory`. Add, rename, or remove an entry here when a sample inventory is added, renamed, or removed there.
    semaphore_ui_inventories:
      - name: Fabric-X - local
        path: examples/inventory/local/fabric-x.yaml
      - name: Fabric-X - local (cryptogen)
        path: examples/inventory/local/fabric-x-cryptogen.yaml
      - name: Fabric-X - local (yugabyte)
        path: examples/inventory/local/fabric-x-yugabyte.yaml
      - name: Fabric-X - local (bin)
        path: examples/inventory/local/fabric-x-bin.yaml
      - name: Fabric-X - local (no mtls)
        path: examples/inventory/local/fabric-x-no-mtls.yaml
      - name: Fabric-X - local (no tls)
        path: examples/inventory/local/fabric-x-no-tls.yaml
      - name: Fabric-X - k8s
        path: examples/inventory/k8s/fabric-x.yaml
      - name: Fabric-X - k8s (yugabyte)
        path: examples/inventory/k8s/fabric-x-yugabyte.yaml
      - name: Fabric-X - k8s (cryptogen)
        path: examples/inventory/k8s/fabric-x-cryptogen.yaml
      - name: Fabric-X - k8s (no mtls)
        path: examples/inventory/k8s/fabric-x-no-mtls.yaml
      - name: Fabric-X - k8s (no tls)
        path: examples/inventory/k8s/fabric-x-no-tls.yaml
      - name: Fabric-X - openshift
        path: examples/inventory/openshift/fabric-x.yaml
      - name: Fabric-X - openshift (cryptogen)
        path: examples/inventory/openshift/fabric-x-cryptogen.yaml
      - name: Fabric-X - distributed
        path: examples/inventory/distributed/fabric-x.yaml
    # Name of the empty Semaphore UI environment seeded on `config/transfer` and attached to every seeded task template.
    semaphore_ui_environment_name: Default
    # Task templates seeded for the numbered example playbooks under `examples/playbooks/`. Each item needs `name` and `playbook`, and an optional `inventory` name. Omitted entirely from the seed if not set — there is no fallback to any other `semaphore_ui_inventories` entry. Not discovered automatically; kept in sync by hand with `examples/playbooks`. Add, rename, or remove an entry here when a numbered playbook is added, renamed, or removed there. An optional `limit` sets this template's default Ansible `--limit`, rendered as-is. Set to `["all:!semaphore_ui"]` on the `teardown`/`wipe`/`hard-wipe` entries by default, so they never tear Semaphore UI down along with a Fabric-X network sharing its inventory. An operator can still override it per run through the Limit field. An optional `survey_vars` list adds extra Semaphore UI survey variables to this template only, on top of `target_hosts` and any project-wide `semaphore_ui_extra_survey_vars`. Each item follows Semaphore UI's own survey variable schema, same as `semaphore_ui_extra_survey_vars`.
    semaphore_ui_job_templates:
      - name: 010 - Fabric-X - Binaries
        playbook: examples/playbooks/10-binaries.yaml
        inventory: Fabric-X - local
      - name: 020 - Fabric-X - Generate Crypto
        playbook: examples/playbooks/20-generate-crypto.yaml
        inventory: Fabric-X - local
      - name: 021 - Fabric-X - Build Genesis Block
        playbook: examples/playbooks/21-build-genesis-block.yaml
        inventory: Fabric-X - local
      - name: 030 - Fabric-X - Configs
        playbook: examples/playbooks/30-configs.yaml
        inventory: Fabric-X - local
      - name: 040 - Fabric-X - Start
        playbook: examples/playbooks/40-start.yaml
        inventory: Fabric-X - local
      - name: 041 - Fabric-X - Init
        playbook: examples/playbooks/41-init.yaml
        inventory: Fabric-X - local
      - name: 050 - Fabric-X - Stop
        playbook: examples/playbooks/50-stop.yaml
        inventory: Fabric-X - local
      - name: 060 - Fabric-X - Teardown
        playbook: examples/playbooks/60-teardown.yaml
        inventory: Fabric-X - local
        limit: 
          - "all:!semaphore_ui"
      - name: 070 - Fabric-X - Ping
        playbook: examples/playbooks/70-ping.yaml
        inventory: Fabric-X - local
      - name: 093 - Fabric-X - Get Metrics
        playbook: examples/playbooks/93-get-metrics.yaml
        inventory: Fabric-X - local
      - name: 095 - Fabric-X - Fetch Crypto
        playbook: examples/playbooks/95-fetch-crypto.yaml
        inventory: Fabric-X - local
      - name: 096 - Fabric-X - Fetch Logs
        playbook: examples/playbooks/96-fetch-logs.yaml
        inventory: Fabric-X - local
      - name: 100 - Fabric-X - Wipe
        playbook: examples/playbooks/100-wipe.yaml
        inventory: Fabric-X - local
        limit: 
          - "all:!semaphore_ui"
      - name: 110 - Fabric-X - Hard Wipe
        playbook: examples/playbooks/110-hard-wipe.yaml
        inventory: Fabric-X - local
        limit: 
          - "all:!semaphore_ui"
    # Additional Semaphore UI survey variables appended to every seeded task template's survey variables, alongside the always-present `target_hosts` one. Each item follows Semaphore UI's own survey variable schema.
    semaphore_ui_extra_survey_vars:
      - name: "log_level"
        title: "Log level"
        type: "enum"
        values:
          - name: "debug"
            value: "debug"
          - name: "info"
            value: "info"
    # Sets `skip_galaxy_install` on every seeded task template. Must stay `true`: Semaphore UI otherwise runs `ansible-galaxy` against this repository's own `requirements.yml` before each task, adding unnecessary network calls and non-determinism to every run.
    semaphore_ui_skip_galaxy_install: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: config/transfer
```

### db/setup

> Migrate and seed the Semaphore UI database if it is missing

Checks whether the Semaphore UI SQLite database file exists and, only if it does not, ensures the data directory exists, runs database migrations, then ensures the admin user and the Fabric-X project exist. A repeated run against a live instance is a no-op. Run this only against a stopped server: the CLI commands used here write directly to the SQLite database, so running them while the server is live risks contending for the same file. Idempotent, but not a reconciler. The admin user is only created if it does not already exist, and the project import is a safe no-op if a project with the same name already exists — but it will not update an existing project when `semaphore_ui_inventories`/`semaphore_ui_job_templates` change.

```yaml
- name: Migrate and seed the Semaphore UI database if it is missing
  vars:
    # Base directory on the managed host under which the Semaphore UI binary is installed.
    remote_node_dir: "/var/lib/fabricx"
    # Base directory on the managed host for `semaphore_ui_remote_config_dir`.
    remote_config_dir: "/var/lib/fabricx/config"
    # Base directory on the managed host for `semaphore_ui_remote_data_dir`.
    remote_data_dir: "/var/lib/fabricx/data"
    # Executable name of the installed Semaphore UI binary. Also used as its tmux session name.
    semaphore_ui_bin_name: semaphore
    # Directory on the managed host holding the rendered Semaphore UI server configuration and project seed files.
    semaphore_ui_remote_config_dir: "{{ remote_config_dir }}"
    # Directory on the managed host holding the Semaphore UI SQLite database, scratch space, and generated secrets.
    semaphore_ui_remote_data_dir: "{{ remote_data_dir }}"
    # File name of the rendered Semaphore UI server configuration.
    semaphore_ui_config_file: config.json
    # File name of the Semaphore UI SQLite database.
    semaphore_ui_database_file: database.db
    # File name of the rendered Semaphore UI project seed, consumed by `semaphore project import`.
    semaphore_ui_project_seed_file: project.json
    # Login of the Semaphore UI admin user created on `config/transfer`.
    semaphore_ui_username: "admin"
    # Email address of the Semaphore UI admin user created on `config/transfer`.
    semaphore_ui_email: "admin@example.com"
    # Password of the Semaphore UI admin user created on `config/transfer`. Store this value in Ansible Vault.
    semaphore_ui_password: "my_semaphore_password"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: db/setup
```

### config/rm

> Remove the Semaphore UI configuration files

Deletes the directory holding the rendered Semaphore UI server configuration and project seed files.

```yaml
- name: Remove the Semaphore UI configuration files
  vars:
    # Base directory on the managed host for `semaphore_ui_remote_config_dir`.
    remote_config_dir: "/var/lib/fabricx/config"
    # Directory on the managed host holding the rendered Semaphore UI server configuration and project seed files.
    semaphore_ui_remote_config_dir: "{{ remote_config_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: config/rm
```

### data/rm

> Remove the Semaphore UI data directory

Deletes the directory holding the Semaphore UI SQLite database, scratch space, and generated secrets.

```yaml
- name: Remove the Semaphore UI data directory
  vars:
    # Base directory on the managed host for `semaphore_ui_remote_data_dir`.
    remote_data_dir: "/var/lib/fabricx/data"
    # Directory on the managed host holding the Semaphore UI SQLite database, scratch space, and generated secrets.
    semaphore_ui_remote_data_dir: "{{ remote_data_dir }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.semaphore_ui
    tasks_from: data/rm
```
