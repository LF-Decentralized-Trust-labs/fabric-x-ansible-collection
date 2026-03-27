# hyperledger.fabricx.grafana

The role `hyperledger.fabricx.grafana` can be used to run a Grafana instance to visualize the Fabric-X components metrics.

The role comes with 4 predefined dashboards:

- A dashboard for the CommitterX metrics;
- A dashboard for the Grafana metrics (useful to keep an eye on the CPU, RAM, network statuses of the machines);
- A dashboard to look at the Yugabyte cluster stats;
- A dashboard for Postgres Exporter metrics.

Grafana fetches the metrics through `prometheus`.

The role allows to run Grafana as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [crypto/setup](#cryptosetup)
  - [crypto/fetch](#cryptofetch)
  - [crypto/rm](#cryptorm)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)

## Variables

| Variable                       | Default                                             | Description                                  |
| ------------------------------ | --------------------------------------------------- | -------------------------------------------- |
| `grafana_registry_endpoint`    | `$GRAFANA_REGISTRY_ENDPOINT` or `docker.io/grafana` | Container registry endpoint                  |
| `grafana_image_name`           | `grafana-oss`                                       | Container image name                         |
| `grafana_image_tag`            | `latest`                                            | Container image tag                          |
| `grafana_image`                | `{{ registry }}/{{ name }}:{{ tag }}`               | Full container image reference               |
| `grafana_container_name`       | `{{ inventory_hostname }}`                          | Name given to the container                  |
| `grafana_remote_config_dir`    | `{{ remote_config_dir }}`                           | Configuration directory on the remote node   |
| `grafana_container_config_dir` | `/etc/grafana/provisioning`                         | Configuration directory inside the container |
| `grafana_datasource_file`      | `datasources.yaml`                                  | Datasource provisioning file name            |
| `grafana_dashboards_file`      | `dashboards.yaml`                                   | Dashboards provisioning file name            |
| `grafana_dashboard_file`       | `dashboard.json`                                    | Dashboard definition file name               |
| `grafana_use_tls`              | `false`                                             | Enable TLS                                   |
| `grafana_tls_private_key_file` | `server.key`                                        | TLS private key file name                    |
| `grafana_tls_cert_file`        | `server.crt`                                        | TLS certificate file name                    |
| `grafana_web_port`             | `3000`                                              | Grafana web UI port                          |

## Tasks

### crypto/setup

The task `crypto/setup` allows to generate the crypto material needed to run Grafana with TLS using [openssl](../openssl/README.md):

```yaml
- name: Setup the crypto material for Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/setup
```

### crypto/fetch

The task `crypto/fetch` fetches the TLS certificate of a Grafana running with TLS:

```yaml
- name: Fetch the TLS certificate of Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/fetch
```

### crypto/rm

The task `crypto/rm` removes the crypto material generated for Grafana:

```yaml
- name: Remove the Grafana crypto files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: crypto/rm
```

### config/transfer

The task `config/transfer` transfers the Grafana configuration files on the remote node:

```yaml
- name: Transfer the Grafana configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Grafana configuration files on the remote node:

```yaml
- name: Remove the Grafana configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: config/rm
```

### start

The task `start` allows to start the Grafana container.

```yaml
- name: Start Grafana
  vars:
    grafana_web_port: 3000
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: start
```

### stop

The task `stop` allows to stop the Grafana container.

```yaml
- name: Stop Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down Grafana and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down Grafana and remove all the artifacts (configuration files and all the runtime-generated artifacts).

```yaml
- name: Wipe Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from Grafana components from the remote hosts to the control node.

```yaml
- name: Fetch Grafana logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping Grafana components on their opened ports. It is useful to check whether Grafana is up and running.

```yaml
- name: Ping Grafana
  ansible.builtin.include_role:
    name: hyperledger.fabricx.grafana
    tasks_from: ping
```
