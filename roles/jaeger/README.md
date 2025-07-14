# hyperledger.fabricx.jaeger

The role `hyperledger.fabricx.jaeger` can be used to run a Jaeger instance for tracing.

The role allows to run `jaeger` as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)

## Tasks

### start

The task `start` allows to start the Jaeger container.

```yaml
- name: Start Jaeger
  vars:
    jaeger_collector_port: 4317
    jaeger_ui_port: 16686
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: start
```

### stop

The task `stop` allows to stop the Jaeger container.

```yaml
- name: Stop Jaeger
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down Jaeger and remove all the artifacts being generated during runtime.

```yaml
- name: Teardown Jaeger
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down Jaeger and remove all the artifacts (configuration files and all the runtime-generated artifacts).

```yaml
- name: Wipe Jaeger
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from Jaeger components from the remote hosts to the control node.

```yaml
- name: Fetch Jaeger logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping Jaeger components on their opened ports. It is useful to check whether Jaeger is up and running.

```yaml
- name: Ping Jaeger
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: ping
```
