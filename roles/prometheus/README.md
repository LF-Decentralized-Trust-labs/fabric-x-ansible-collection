# hyperledger.fabricx.prometheus

The role `hyperledger.fabricx.prometheus` can be used to run a Prometheus metrics collector. Specifically, Prometheus is configured to collect metrics from:

- committer components (through the `prometheus_committer_sidecars`, `prometheus_committer_coordinators`, `prometheus_committer_verifiers`, `prometheus_committer_validators` variables);
- load generator (through the `prometheus_load_generators` variable);
- Yugabyte cluster (through the `prometheus_yb_masters` and `prometheus_yb_tservers` variables);
- node exporters (through the `prometheus_node_exporters` variable).

The role allows to run Prometheus as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)

## Tasks

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
