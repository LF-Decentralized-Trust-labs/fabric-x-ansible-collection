# hyperledger.fabricx.git

> Performs `git` operations on a node.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [Tasks](#tasks)
  - [install](#install)
  - [clone](#clone)
  - [get_repo_name](#get_repo_name)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## Tasks

### install

Install git on the target host

Installs the Git package on the managed node.

This entry point delegates package installation to the shared package role.

```yaml
- name: Install git on the target host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.git
    tasks_from: install
```

### clone

Clone or update a Git repository into a target directory

Clones a Git repository at the requested revision into a derived destination directory.

Repeated runs update the existing checkout in place through `ansible.builtin.git`.

```yaml
- name: Clone or update a Git repository into a target directory
  vars:
    # Repository path component used to derive the checkout directory name and default repository URIs. The checkout name is computed from the basename of this value.
    git_repo: "string"
    # Parent directory that will contain the checkout created by `clone`. The final destination is derived as `<git_dir>/<repo-basename>@<git_commit>`.
    git_dir: "string"
    # Git branch, tag, or commit to check out. The value is appended to the derived checkout directory name and passed to `ansible.builtin.git` as the revision.
    git_commit: main
    # Hostname inserted into the default HTTPS and SSH repository URI templates.
    git_hub_url: github.com
    # Selects the SSH-derived default repository URI when true; otherwise HTTPS is used.
    git_use_ssh: false
    # Default HTTPS repository URI built from `git_hub_url` and `git_repo`.
    git_https_uri: "https://{{ git_hub_url }}/{{ git_repo }}.git"
    # Default SSH repository URI built from `git_hub_url` and `git_repo`.
    git_ssh_uri: "git@{{ git_hub_url }}:{{ git_repo }}.git"
    # Effective repository URI passed to `ansible.builtin.git`. Defaults to `git_ssh_uri` when `git_use_ssh` is true, otherwise `git_https_uri`.
    git_uri: "{{ git_ssh_uri if git_use_ssh else git_https_uri }}"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.git
    tasks_from: clone
```

### get_repo_name

Compute the repository checkout directory name

Derives `git_repo_name` as `<basename(git_repo`>@<git_commit>).

The resulting fact is used by `clone` before creating the checkout directory.

```yaml
- name: Compute the repository checkout directory name
  vars:
    # Repository path component used to derive the checkout directory name and default repository URIs. The checkout name is computed from the basename of this value.
    git_repo: "string"
    # Git branch, tag, or commit to check out. The value is appended to the derived checkout directory name and passed to `ansible.builtin.git` as the revision.
    git_commit: main
  ansible.builtin.include_role:
    name: hyperledger.fabricx.git
    tasks_from: get_repo_name
```
