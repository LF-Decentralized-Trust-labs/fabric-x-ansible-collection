# hyperledger.fabricx.tmux

> Manages detached `tmux` sessions for long-running Fabric-X processes and their log-producing commands.

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

> Install tmux on the target host

Install the `tmux` package on the target host by delegating to the package role.

```yaml
- name: Install tmux on the target host
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: install
```

### start

> Start a detached tmux session

Start a detached tmux session when `tmux_session_name` does not already exist.The session runs `tmux_cmd_to_run` from `tmux_chdir`, so long-lived commands can keep running in the background while logs are written to the command's own output path.

```yaml
- name: Start a detached tmux session
  vars:
    # Sets the detached tmux session name used to look up, create, or stop the session. Example: `fx-orderer-1`.
    tmux_session_name: "fx-orderer-1"
    # Sets the shell command started inside the detached tmux session. Example: `./bin/orderer --label orderer-1 >> /var/log/fabricx/orderer-1.log 2>&1`.
    tmux_cmd_to_run: "./bin/orderer --label orderer-1 >> /var/log/fabricx/orderer-1.log 2>&1"
    # Sets the working directory used before running `tmux_cmd_to_run` in the detached session. Example: `/opt/fabricx/orderer`.
    tmux_chdir: "/opt/fabricx/orderer"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: start
```

### stop

> Stop a detached tmux session

Stop an existing detached tmux session on the target host when `tmux_session_name` is present.The stop entry point only removes the named session; it does not clean up any logs or other command artifacts.

```yaml
- name: Stop a detached tmux session
  vars:
    # Sets the detached tmux session name used to look up, create, or stop the session. Example: `fx-orderer-1`.
    tmux_session_name: "fx-orderer-1"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: stop
```
