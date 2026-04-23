# hyperledger.fabricx.tmux

> Runs `tmux` sessions for managing long-running processes.

## Table of Contents <!-- omit in toc -->

- [Role Defaults](#role-defaults)
- [ansible-doc](#ansible-doc)
- [Tasks](#tasks)
  - [install](#install)
  - [start](#start)
  - [stop](#stop)

## Role Defaults

See [`defaults/main.yaml`](defaults/main.yaml) for the generated role defaults and inline variable descriptions.

## ansible-doc

You can view the role documentation in your terminal running:

```shell
ansible-doc -t role hyperledger.fabricx.tmux
```

## Tasks

### install

Install tmux

Install the `tmux` package on the target host by delegating to the package role.

```yaml
- name: Install tmux
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: install
```

### start

Start a tmux session

Start a detached tmux session when `tmux_session_name` does not already exist.

The session runs `tmux_cmd_to_run` from `tmux_chdir` on the target host.

```yaml
- name: Start a tmux session
  vars:
    # Sets the tmux session name used to look up, create, or stop the detached session. Example: `sample-session`.
    tmux_session_name: "string"
    # Sets the shell command started inside the new detached tmux session. Example: `echo 'Hello World'`.
    tmux_cmd_to_run: "string"
    # Sets the working directory used before running `tmux_cmd_to_run` in the detached session. Example: `/var/hyperledger/fabricx`.
    tmux_chdir: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: start
```

### stop

Stop a tmux session

Stop an existing tmux session on the target host when `tmux_session_name` is present.

```yaml
- name: Stop a tmux session
  vars:
    # Sets the tmux session name used to look up, create, or stop the detached session. Example: `sample-session`.
    tmux_session_name: "string"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: stop
```
