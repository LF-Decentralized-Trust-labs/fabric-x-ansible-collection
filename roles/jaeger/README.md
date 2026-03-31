# hyperledger.fabricx.jaeger

The role `hyperledger.fabricx.jaeger` can be used to run a Jaeger instance for tracing.

The role allows to run `jaeger` as **container only** (binary is not currently supported).

## Table of Contents <!-- omit in toc -->

- [Variables](#variables)
- [Tasks](#tasks)
  - [config/transfer](#configtransfer)
  - [config/rm](#configrm)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)

## Variables

| Variable                      | Default                                                  | Description                                  |
| ----------------------------- | -------------------------------------------------------- | -------------------------------------------- |
| `jaeger_registry_endpoint`    | `$JAEGER_REGISTRY_ENDPOINT` or `docker.io/jaegertracing` | Container registry endpoint                  |
| `jaeger_image_name`           | `all-in-one`                                             | Container image name                         |
| `jaeger_image_tag`            | `latest`                                                 | Container image tag                          |
| `jaeger_image`                | `{{ registry }}/{{ name }}:{{ tag }}`                    | Full container image reference               |
| `jaeger_container_name`       | `{{ inventory_hostname }}`                               | Name given to the container                  |
| `jaeger_remote_config_dir`    | `{{ remote_config_dir }}`                                | Configuration directory on the remote node   |
| `jaeger_container_config_dir` | `/var/config`                                            | Configuration directory inside the container |
| `jaeger_ui_port`              | `16686`                                                  | Jaeger UI port                               |
| `jaeger_admin_port`           | `14269`                                                  | Jaeger admin port                            |
| `jaeger_http_server_port`     | `14268`                                                  | Jaeger HTTP server port                      |
| `jaeger_http_collector_port`  | `4318`                                                   | Jaeger HTTP collector port (OTLP)            |
| `jaeger_grpc_server_port`     | `14250`                                                  | Jaeger gRPC server port                      |
| `jaeger_collector_port`       | `4317`                                                   | Jaeger gRPC collector port (OTLP)            |

## Tasks

### config/transfer

The task `config/transfer` transfers the Jaeger configuration files on the remote node:

```yaml
- name: Transfer the Jaeger configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/transfer
```

### config/rm

The task `config/rm` removes the Jaeger configuration files on the remote node:

```yaml
- name: Remove the Jaeger configuration files
  ansible.builtin.include_role:
    name: hyperledger.fabricx.jaeger
    tasks_from: config/rm
```

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
