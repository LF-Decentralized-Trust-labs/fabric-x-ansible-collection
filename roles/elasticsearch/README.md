# hyperledger.fabricx.elasticsearch

The role `hyperledger.fabricx.elasticsearch` can be used to run an ElasticSearch container.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [start](#start)
  - [stop](#stop)
  - [teardown](#teardown)
  - [wipe](#wipe)
  - [fetch_logs](#fetch_logs)
  - [ping](#ping)

## Tasks

### start

The task `start` allows to start an ElasticSearch container:

```yaml
- name: Start an ElasticSearch container
  vars:
    elasticsearch_http_port: 9200
    elasticsearch_transport_port: 9300
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: start
```

### stop

The task `stop` allows to stop an ElasticSearch container.

```yaml
- name: Stop the ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: stop
```

### teardown

The task `teardown` allows to shut down an ElasticSearch container and remove all the data stored by the container on the persistent volume.

```yaml
- name: Teardown the ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: teardown
```

### wipe

The task `wipe` allows to shut down an ElasticSearch container and remove all the data stored by the container on the persistent volume.

```yaml
- name: Wipe the ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: wipe
```

### fetch_logs

The task `fetch_logs` allows to fetch the logs from an ElasticSearch container.

```yaml
- name: Fetch the ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: fetch_logs
```

### ping

The task `ping` allows to ping an ElasticSearch container. It is useful to check whether the instances are running or if they are not running/reachable.

```yaml
- name: Ping the ElasticSearch container
  ansible.builtin.include_role:
    name: hyperledger.fabricx.elasticsearch
    tasks_from: ping
```
