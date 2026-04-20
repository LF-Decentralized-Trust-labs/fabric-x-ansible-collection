# hyperledger.fabricx.tmux

> Runs `tmux` sessions for managing long-running processes.

## Table of Contents <!-- omit in toc -->

- [Tasks](#tasks)
  - [Lifecycle](#lifecycle)
    - [install](#install)
    - [start](#start)
    - [stop](#stop)
- [Variables](#variables)

## Tasks

### Lifecycle

| Task                            | Description         |
| ------------------------------- | ------------------- |
| [install](./tasks/install.yaml) | Installs tmux       |
| [start](./tasks/start.yaml)     | Starts tmux session |
| [stop](./tasks/stop.yaml)       | Stops tmux session  |

#### install

Installs the `tmux` package on the desired machine:

```yaml
- name: Install tmux
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: install
```

#### start

Starts a detached session of `tmux`. The task is idempotent, i.e. if a session with that name already exists, `tmux` doesn't restart the session.

```yaml
- name: Start a "sample-session" with tmux
  vars:
    tmux_session_name: "sample-session"
    tmux_cmd_to_run: "echo 'Hello World'"
    tmux_chdir: "/var/hyperledger/fabricx"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: start
```

#### stop

Stops a session of `tmux`:

```yaml
- name: Stop the "sample-session" tmux session
  vars:
    tmux_session_name: "sample-session"
  ansible.builtin.include_role:
    name: hyperledger.fabricx.tmux
    tasks_from: stop
```

---

## Variables

See [`defaults/main.yaml`](defaults/main.yaml) for full variable documentation.
