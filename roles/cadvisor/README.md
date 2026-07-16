# hyperledger.fabricx.cadvisor

> Runs cAdvisor in container mode to collect per-container CPU, memory, network, and filesystem metrics from Docker or Podman.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch\_logs](#fetch_logs)
  - [ping](#ping)
  - [config/transfer\_grafana\_dashboard](#configtransfer_grafana_dashboard)
  - [container/start](#containerstart)
  - [container/stop](#containerstop)
  - [container/rm](#containerrm)
  - [container/fetch\_logs](#containerfetch_logs)
  - [prometheus/get\_scrapers](#prometheusget_scrapers)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.cadvisor
```

## Tasks

### start

> Start cAdvisor

Starts the local `cadvisor_container_name` container and publishes `cadvisor_port`.

```yaml
- name: Start cAdvisor
  vars:
    # Enables the container backend. cAdvisor currently only supports container mode.
    cadvisor_use_container: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: start
```

### stop

> Stop cAdvisor

Stops the container-backed cAdvisor workload for the host.

```yaml
- name: Stop cAdvisor
  vars:
    # Enables the container backend. cAdvisor currently only supports container mode.
    cadvisor_use_container: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: stop
```

### teardown

> Remove cAdvisor runtime resources

Removes the local cAdvisor runtime container.

```yaml
- name: Remove cAdvisor runtime resources
  vars:
    # Enables the container backend. cAdvisor currently only supports container mode.
    cadvisor_use_container: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: teardown
```

### wipe

> Remove cAdvisor runtime resources

Removes the cAdvisor runtime container for the host. Use this to fully reset the deployment.

```yaml
- name: Remove cAdvisor runtime resources
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: wipe
```

### fetch_logs

> Collect cAdvisor logs

Collects logs from the cAdvisor container for this host.

```yaml
- name: Collect cAdvisor logs
  vars:
    # Enables the container backend. cAdvisor currently only supports container mode.
    cadvisor_use_container: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: fetch_logs
```

### ping

> Check cAdvisor reachability

Verifies that the cAdvisor HTTP port is reachable on the current host.

```yaml
- name: Check cAdvisor reachability
  vars:
    # Sets the TCP port cAdvisor's HTTP server and metrics endpoint listen on. Example: `9400`.
    cadvisor_port: 9400
    # Enables the container backend. cAdvisor currently only supports container mode.
    cadvisor_use_container: true
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: ping
```

### config/transfer_grafana_dashboard

> Transfer the Grafana dashboard for cAdvisor

Copies the bundled cAdvisor Insights dashboard into Grafana by delegating to the Grafana role.

```yaml
- name: Transfer the Grafana dashboard for cAdvisor
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: config/transfer_grafana_dashboard
```

### container/start

> Start cAdvisor in a container

Starts the cAdvisor container with the configured image, port, and host mounts. The container name comes from `cadvisor_container_name` and the image from `cadvisor_image`. Detects the local Docker or Podman client and adapts the storage mount and runtime flags accordingly.

```yaml
- name: Start cAdvisor in a container
  vars:
    # Sets the container name used for the cAdvisor runtime.
    cadvisor_container_name: cadvisor
    # Sets the registry endpoint used to build the default cAdvisor image reference.
    cadvisor_registry_endpoint: "{{ lookup('env', 'CADVISOR_REGISTRY_ENDPOINT') or 'ghcr.io/google' }}"
    # Sets the cAdvisor image name used in the default image reference.
    cadvisor_image_name: cadvisor
    # Sets the cAdvisor image tag used in the default image reference. `v0.49.1` or later is required for Podman support (the `--podman` flag).
    cadvisor_image_tag: v0.60.5
    # Sets the full cAdvisor image reference.
    cadvisor_image: "{{ cadvisor_registry_endpoint }}/{{ cadvisor_image_name }}:{{ cadvisor_image_tag }}"
    # Sets the TCP port cAdvisor's HTTP server and metrics endpoint listen on. Example: `9400`.
    cadvisor_port: 9400
    # Sets the interval at which cAdvisor refreshes its internal container metrics.
    cadvisor_housekeeping_interval: 10s
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: container/start
```

### container/stop

> Stop the cAdvisor container

Stops the cAdvisor container by delegating to the shared container role. Uses the configured container name and image reference to identify the runtime.

```yaml
- name: Stop the cAdvisor container
  vars:
    # Sets the container name used for the cAdvisor runtime.
    cadvisor_container_name: cadvisor
    # Sets the registry endpoint used to build the default cAdvisor image reference.
    cadvisor_registry_endpoint: "{{ lookup('env', 'CADVISOR_REGISTRY_ENDPOINT') or 'ghcr.io/google' }}"
    # Sets the cAdvisor image name used in the default image reference.
    cadvisor_image_name: cadvisor
    # Sets the cAdvisor image tag used in the default image reference. `v0.49.1` or later is required for Podman support (the `--podman` flag).
    cadvisor_image_tag: v0.60.5
    # Sets the full cAdvisor image reference.
    cadvisor_image: "{{ cadvisor_registry_endpoint }}/{{ cadvisor_image_name }}:{{ cadvisor_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: container/stop
```

### container/rm

> Remove the cAdvisor container

Removes the cAdvisor container by delegating to the shared container role.

```yaml
- name: Remove the cAdvisor container
  vars:
    # Sets the container name used for the cAdvisor runtime.
    cadvisor_container_name: cadvisor
    # Sets the registry endpoint used to build the default cAdvisor image reference.
    cadvisor_registry_endpoint: "{{ lookup('env', 'CADVISOR_REGISTRY_ENDPOINT') or 'ghcr.io/google' }}"
    # Sets the cAdvisor image name used in the default image reference.
    cadvisor_image_name: cadvisor
    # Sets the cAdvisor image tag used in the default image reference. `v0.49.1` or later is required for Podman support (the `--podman` flag).
    cadvisor_image_tag: v0.60.5
    # Sets the full cAdvisor image reference.
    cadvisor_image: "{{ cadvisor_registry_endpoint }}/{{ cadvisor_image_name }}:{{ cadvisor_image_tag }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: container/rm
```

### container/fetch_logs

> Fetch logs from the cAdvisor container

Collects logs from the cAdvisor container by delegating to the shared container role. This is the container-mode log path used by the top-level fetch_logs entry point.

```yaml
- name: Fetch logs from the cAdvisor container
  vars:
    # Sets the container name used for the cAdvisor runtime.
    cadvisor_container_name: cadvisor
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: container/fetch_logs
```

### prometheus/get_scrapers

> Build Prometheus scrape targets for cAdvisor

Builds the `cadvisor_prometheus_scrape_services` fact for the cAdvisor hosts listed in `cadvisor_hosts`. cAdvisor is scraped in plain HTTP; it has no native TLS support for its metrics endpoint.

```yaml
- name: Build Prometheus scrape targets for cAdvisor
  vars:
    # Lists the inventory hosts exposed as Prometheus scrape targets. Example: `['orderer-1', 'committer-1']`.
    cadvisor_hosts:
      - "orderer-1"
      - "committer-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.cadvisor
    tasks_from: prometheus/get_scrapers
```
