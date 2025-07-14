# hyperledger.fabricx.grafana

The role `hyperledger.fabricx.grafana` can be used to run a Grafana instance to visualize the Fabric-X components metrics.

The role comes with 3 predefined dashboards:

- a dashboard for the CommitterX metrics;
- a dashboard for the Node Exporter metrics;
- a dashboard to look at the Yugabyte cluster stats.

Grafana fetches the metrics through `prometheus`.

The role allows to run Grafana as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)

## Tasks

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
