# hyperledger.fabricx.prometheus

The role `hyperledger.fabricx.prometheus` can be used to run a Prometheus metrics collector.

The role allows to run Prometheus as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [config.transfer](#configtransfer)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)

## Tasks

### config.transfer

The task `config.transfer` allows to generate a `prometheus.yml` configuration file for the Prometheus service.

It supports multiple customizations, for an example please have a look at its usage in this [sample playbook](../../playbooks/monitoring/transfer_configs.yaml).

```yaml
- name: Generate the configuration for Prometheus
  vars:
    prometheus_scrape_interval: 2s
    prometheus_scrape_services:
      - job_name: node_exporter
        targets:
          - hosts: "{{ node_exporter_hosts }}"
            port_to_scrape: node_exporter_port
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: config/transfer
```

### start

The task `start` allows to start the Prometheus container.

```yaml
- name: Start Prometheus
  vars:
    prometheus_scraper_port: 9090
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: start
```

### stop

The task `stop` allows to stop the Prometheus container.

```yaml
- name: Stop Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down Prometheus and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down Prometheus and remove all the artifacts (configuration files and all the runtime-generated artifacts).

```yaml
- name: Wipe Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from Prometheus components from the remote hosts to the control node.

```yaml
- name: Fetch Prometheus logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping Prometheus components on their opened ports. It is useful to check whether Prometheus is up and running.

```yaml
- name: Ping Prometheus
  ansible.builtin.include_role:
    name: hyperledger.fabricx.prometheus
    tasks_from: ping
```
