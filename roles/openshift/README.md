# hyperledger.fabricx.openshift

> Provides OpenShift helper tasks for Route resources.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [route/apply](#routeapply)
  - [route/rm](#routerm)
  - [route/ping](#routeping)
  - [cluster/login](#clusterlogin)
  - [cluster/service\_account\_login](#clusterservice_account_login)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.openshift
```

## Tasks

### route/apply

> Apply an OpenShift Route

Creates or updates an OpenShift Route targeting a named Service port. Renders passthrough TLS termination when `openshift_route_use_tls` is true.

```yaml
- name: Apply an OpenShift Route
  vars:
    # Specifies the namespace targeted by the OpenShift resource. Example: `fabric-x`.
    k8s_namespace: "fabric-x"
    # Specifies the OpenShift Route resource name. Example: `orderer-router-1-rpc`.
    openshift_route_name: "orderer-router-1-rpc"
    # Specifies the external host assigned to the OpenShift Route. Example: `orderer.apps.example.com`.
    openshift_route_host: "orderer.apps.example.com"
    # Specifies the Service targeted by the OpenShift Route. Example: `orderer-router-1`.
    openshift_route_service_name: "orderer-router-1"
    # Specifies the named Service port targeted by the OpenShift Route. Example: `rpc`.
    openshift_route_service_port: "rpc"
    # Specifies labels to render on the OpenShift Route.
    openshift_route_labels: {}
    # Controls whether the Route uses passthrough TLS termination.
    openshift_route_use_tls: false
    # Specifies the TLS termination type to render on the OpenShift Route.
    openshift_route_tls_termination: passthrough
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openshift
    tasks_from: route/apply
```

### route/rm

> Remove an OpenShift Route

Deletes the named OpenShift Route from `k8s_namespace`.

```yaml
- name: Remove an OpenShift Route
  vars:
    # Specifies the namespace targeted by the OpenShift resource. Example: `fabric-x`.
    k8s_namespace: "fabric-x"
    # Specifies the OpenShift Route resource name. Example: `orderer-router-1-rpc`.
    openshift_route_name: "orderer-router-1-rpc"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openshift
    tasks_from: route/rm
```

### route/ping

> Check an OpenShift Route host

Checks the external OpenShift Route host on port 80 or 443, depending on `openshift_route_use_tls`.

```yaml
- name: Check an OpenShift Route host
  vars:
    # Specifies the external host assigned to the OpenShift Route. Example: `orderer.apps.example.com`.
    openshift_route_host: "orderer.apps.example.com"
    # Controls whether the Route uses passthrough TLS termination.
    openshift_route_use_tls: false
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openshift
    tasks_from: route/ping
```

### cluster/login

> Login to a managed OpenShift cluster with a personal token

Logs in to a managed OpenShift cluster using a personal user token.

```yaml
- name: Login to a managed OpenShift cluster with a personal token
  vars:
    # OpenShift cluster API server URL for login Required for managed OpenShift cluster login Example: `https://api.cluster.example.com:6443`
    openshift_cluster_login_server: "https://api.cluster.example.com:6443"
    # Personal user token for interactive OpenShift login Can be set via OPENSHIFT_PERSONAL_TOKEN environment variable
    openshift_cluster_personal_token: "{{ lookup('env', 'OPENSHIFT_PERSONAL_TOKEN') | trim }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openshift
    tasks_from: cluster/login
```

### cluster/service_account_login

> Login to a managed OpenShift cluster with a service account

Mints a service-account token and logs in to a managed OpenShift cluster. Selects the configured OpenShift project after login.

```yaml
- name: Login to a managed OpenShift cluster with a service account
  vars:
    # OpenShift cluster API server URL for login Required for managed OpenShift cluster login Example: `https://api.cluster.example.com:6443`
    openshift_cluster_login_server: "https://api.cluster.example.com:6443"
    # OpenShift namespace/project to use
    openshift_cluster_namespace: "{{ k8s_namespace }}"
    # Service account name to be used by automation after login Example: `ansible-deployer`
    openshift_cluster_service_account_name: "ansible-deployer"
    # Duration for the service account token
    openshift_cluster_service_account_token_duration: 12h
  ansible.builtin.include_role:
    name: hyperledger.fabricx.openshift
    tasks_from: cluster/service_account_login
```
