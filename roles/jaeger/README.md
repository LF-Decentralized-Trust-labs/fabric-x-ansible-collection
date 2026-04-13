# hyperledger.fabricx.jaeger

> Runs a Jaeger instance for distributed tracing.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [Config](#config)
    - [config/transfer](#configtransfer)
    - [config/rm](#configrm)
  - [Lifecycle](#lifecycle)
    - [start](#start)
    - [stop](#stop)
    - [teardown](#teardown)
    - [wipe](#wipe)
    - [fetch_logs](#fetch_logs)
    - [ping](#ping)
- [Variables](#variables)

## Tasks

### Config

| Task                                            | Description                    |
| ----------------------------------------------- | ------------------------------ |
| [config/transfer](./tasks/config/transfer.yaml) | Transfers Jaeger configuration |
| [config/rm](./tasks/config/rm.yaml)             | Removes configuration          |

#### config/transfer

Transfers the Jaeger configuration files on the remote node:

```yaml
- name: Transfer the Jaeger configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/transfer
```

#### config/rm

Removes the Jaeger configuration files on the remote node:

```yaml
- name: Remove the Jaeger configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/rm
```

### Lifecycle

| Task                                  | Description             |
| ------------------------------------- | ----------------------- |
| [start](./tasks/start.yaml)           | Starts Jaeger container |
| [stop](./tasks/stop.yaml)             | Stops Jaeger container  |
| [teardown](./tasks/teardown.yaml)     | Removes container       |
| [wipe](./tasks/wipe.yaml)             | Removes all data        |
| [fetch_logs](./tasks/fetch_logs.yaml) | Collects logs           |
| [ping](./tasks/ping.yaml)             | Health check            |

#### start

Starts the Jaeger container:

```yaml
- name: Start Jaeger
  vars:
    jaeger_collector_port: 4317
    jaeger_ui_port: 16686
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: start
```

#### stop

Stops the Jaeger container:

```yaml
- name: Stop Jaeger
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: stop
```

#### teardown

Removes the Jaeger container:

```yaml
- name: Teardown Jaeger
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: teardown
```

#### wipe

Removes all Jaeger data:

```yaml
- name: Wipe Jaeger
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: wipe
```

#### fetch_logs

Collects Jaeger logs:

```yaml
- name: Fetch Jaeger logs
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: fetch_logs
```

#### ping

Health check for Jaeger:

```yaml
- name: Ping Jaeger
  vars:
    jaeger_ui_port: 16686
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: ping
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
