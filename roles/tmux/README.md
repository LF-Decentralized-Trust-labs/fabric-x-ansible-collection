# hyperledger.fabricx.tmux

The role `hyperledger.fabricx.tmux` can be used to run a `tmux` session.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [install](#install)
  - [start](#start)
  - [stop](#stop)

## Tasks

### install

The task `install` installs the `tmux` package on the desired machine:

```yaml
- name: Install tmux
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: install
```

### start

The task `start` allows to start a detached session of `tmux`.

The task is idempotent, i.e. if a session with that name already exists, `tmux` doesn't restart the session.

```yaml
- name: Start a "sample-session" with tmux
  vars:
    tmux_session_name: "sample-session"
    tmux_cmd_to_run: "echo 'Hello World'"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: start
```

### stop

The task `stop` allows to stop a session of `tmux`.

```yaml
- name: Stop the "sample-session" tmux session
  vars:
    tmux_session_name: "sample-session"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: stop
```
