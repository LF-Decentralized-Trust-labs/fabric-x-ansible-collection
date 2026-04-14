#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# exported vars
PROJECT_DIR := $(CURDIR)
OUT_DIR ?= $(PROJECT_DIR)/out

# Load local overrides from a .env file if present
-include $(PROJECT_DIR)/.env

# venv
USE_VENV ?= true
VENV_DIR := $(PROJECT_DIR)/.venv
VENV_BIN_DIR := $(VENV_DIR)/bin

# Ansible vars
ANSIBLE_CONFIG ?= $(PROJECT_DIR)/examples/ansible.cfg
ANSIBLE_CACHE_PLUGIN ?= jsonfile
ANSIBLE_CACHE_PLUGIN_CONNECTION ?= $(OUT_DIR)/ansible_fact_cache

# Ansible
export ANSIBLE_CONFIG
export ANSIBLE_CACHE_PLUGIN
export ANSIBLE_CACHE_PLUGIN_CONNECTION
export PROJECT_DIR

# Ansible commands
# Set USE_VENV=false to fall back to system-installed Ansible commands.
# Defaults to true (venv-based commands).
ifeq ($(USE_VENV),true)
ANSIBLE_PLAYBOOK ?= $(VENV_BIN_DIR)/ansible-playbook
ANSIBLE_GALAXY ?= $(VENV_BIN_DIR)/ansible-galaxy
ANSIBLE_LINT ?= $(VENV_BIN_DIR)/ansible-lint
ANSIBLE_PYTHON_INTERPRETER ?= $(VENV_BIN_DIR)/python
export ANSIBLE_PYTHON_INTERPRETER
else
ANSIBLE_PLAYBOOK ?= ansible-playbook
ANSIBLE_GALAXY ?= ansible-galaxy
ANSIBLE_LINT ?= ansible-lint
ANSIBLE_PYTHON_INTERPRETER ?= python3
endif

# Color codes for echo messages
COLOR_CYAN := \033[0;36m
COLOR_GREEN := \033[0;32m
COLOR_RESET := \033[0m

# Makefile vars
PLAYBOOK_PATH := $(PROJECT_DIR)/examples/playbooks
TARGET_HOSTS ?= all
ASSERT_METRICS ?= false
LIMIT ?= 1000

# Vars to log into CR using env vars
CONTAINER_REGISTRY ?=
CONTAINER_REGISTRY_USERNAME ?=
CONTAINER_REGISTRY_PASSWORD ?=

# include the predefined target groups
include $(PROJECT_DIR)/target_groups.mk

# conditionally include the generated target hosts (if exists)
-include $(PROJECT_DIR)/target_hosts.mk

# Print the list of supported commands.
.PHONY: help
help:
	@awk ' \
		/^#/ { \
			sub(/^#[ \t]*/, "", $$0); \
			help_msg = $$0; \
		} \
		/^[a-zA-Z0-9][^ :]*:/ { \
			if (help_msg) { \
				split($$1, target, ":"); \
				printf "  %-40s %s\n", target[1], help_msg; \
				help_msg = ""; \
			} \
		} \
	' $(MAKEFILE_LIST)

# Install the hyperledger.fabricx Ansible collection locally
.PHONY: install
install: install-deps
	@DEST=$$(echo "$${ANSIBLE_COLLECTIONS_PATH:-$(HOME)/.ansible/collections}" | cut -d: -f1)/ansible_collections/hyperledger/fabricx; \
	REALPATH_DEST=$$(realpath $$DEST 2>/dev/null); \
	REALPATH_PROJ=$$(realpath $(PROJECT_DIR)); \
	case "$$REALPATH_PROJ" in \
	  "$$REALPATH_DEST"|"$$REALPATH_DEST"/*) \
	    printf "$(COLOR_CYAN)⚠️  Skipping: PROJECT_DIR is within the Galaxy install destination — running 'make install' would overwrite your checkout.$(COLOR_RESET)\n"; \
	    exit 1 ;; \
	esac
	@printf "$(COLOR_CYAN)🚩 Building and installing hyperledger.fabricx collection...$(COLOR_RESET)\n"
	$(ANSIBLE_GALAXY) collection build -f
	$(ANSIBLE_GALAXY) collection install $$(ls -1 | grep fabricx) -f
	@rm -f $$(ls -1 | grep fabricx)

# Install the dependencies needed to run this collection (e.g. make install-deps).
.PHONY: install-deps
install-deps: install-venv install-python-deps install-ansible-deps

# Install venv for local Python setup
.PHONY: install-venv
install-venv:
	@printf "$(COLOR_CYAN)🚩 Installing venv...$(COLOR_RESET)\n"
	python3 -m venv $(VENV_DIR)

.PHONY: install-python-deps
install-python-deps:
	@printf "$(COLOR_CYAN)🚩 Installing Python dependencies...$(COLOR_RESET)\n"
	$(ANSIBLE_PYTHON_INTERPRETER) -m pip install --upgrade pip
	$(ANSIBLE_PYTHON_INTERPRETER) -m pip install -r $(PROJECT_DIR)/requirements.txt

# Install the Ansible collections needed to run the scripts.
.PHONY: install-ansible-deps
install-ansible-deps:
	@printf "$(COLOR_CYAN)🚩 Installing Ansible dependencies...$(COLOR_RESET)\n"
	$(ANSIBLE_GALAXY) collection install -r requirements.yml

# Install the utilities needed to run the components on the targeted remote hosts (e.g. make install-remote-node-deps).
.PHONY: install-remote-node-deps
install-remote-node-deps:
	@printf "$(COLOR_CYAN)🚩 Installing prerequisites on remote hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) hyperledger.fabricx.install_prerequisites --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Check the linting correctness (e.g. make lint)
.PHONY: lint
lint:
	@printf "$(COLOR_CYAN)🚩 Running ansible-lint checks...$(COLOR_RESET)\n"
	$(ANSIBLE_LINT) --offline roles playbooks examples

# Check the license header
.PHONY: check-license-header
check-license-header:
	@printf "$(COLOR_CYAN)🚩 Checking license headers...$(COLOR_RESET)\n"
	./ci/check_license_header.sh

# Check that no trailing spaces are added in the j2 files
.PHONY: check-license-header
check-trailing-spaces:
	@printf "$(COLOR_CYAN)🚩 Checking for trailing spaces in templates...$(COLOR_RESET)\n"
	./ci/check_trailing_spaces.sh

# =======================
# Deployment
# =======================

# Log the container engine within a Container Registry (aka CR) (e.g. make login-cr CONTAINER_REGISTRY=icr.io CONTAINER_REGISTRY_USERNAME=iamapikey CONTAINER_REGISTRY_PASSWORD=my_api_key).
.PHONY: login-cr
login-cr:
	@printf "$(COLOR_CYAN)🚩 Logging into container registry [$(COLOR_GREEN)$(CONTAINER_REGISTRY)$(COLOR_CYAN)] for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) hyperledger.fabricx.log_in_container_registry --extra-vars '{"target_hosts": "$(TARGET_HOSTS)", "container_registry": "$(CONTAINER_REGISTRY)", "container_registry_username": "$(CONTAINER_REGISTRY_USERNAME)", "container_registry_password": "$(CONTAINER_REGISTRY_PASSWORD)"}'

# Build all the artifacts, the binaries and configuration files (e.g. make setup).
.PHONY: setup
setup: binaries artifacts configs

# Build all the artifacts (e.g. make artifacts).
.PHONY: artifacts
artifacts: generate-crypto genesis-block

# Generate the crypto material (e.g. make build-crypto).
.PHONY: generate-crypto
generate-crypto:
	@printf "$(COLOR_CYAN)🚩 Generating crypto material for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/20-generate-crypto.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Build the genesis block for the network (e.g. make genesis-block).
.PHONY: genesis-block
genesis-block:
	@printf "$(COLOR_CYAN)🚩 Building genesis block for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/21-build-genesis-block.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Build the targeted binaries on the controller node (e.g. make binaries).
.PHONY: binaries
binaries:
	@printf "$(COLOR_CYAN)🚩 Building/installing binaries for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/10-binaries.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Clean all the artifacts (configs and bins) built on the controller node (e.g. make clean).
.PHONY: clean
clean: clean-cache
	@printf "$(COLOR_CYAN)🚩 Cleaning local artifacts and cache...$(COLOR_RESET)\n"
	rm -rf $(OUT_DIR)

# Clean the Ansible cache (e.g. make clean-cache).
.PHONY: clean-cache
clean-cache:
	@printf "$(COLOR_CYAN)🚩 Cleaning Ansible cache...$(COLOR_RESET)\n"
	rm -rf $(ANSIBLE_CACHE_PLUGIN_CONNECTION)

# Create/Ship the configs to the remote nodes (e.g. make fabric_x configs).
.PHONY: configs
configs:
	@printf "$(COLOR_CYAN)🚩 Creating and shipping configs to remote nodes [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/30-configs.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Start the targeted hosts (e.g. make fabric_x start).
.PHONY: start
start:
	@printf "$(COLOR_CYAN)🚩 Starting hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/40-start.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Stop the targeted hosts (e.g. make fabric_x stop).
.PHONY: stop
stop:
	@printf "$(COLOR_CYAN)🚩 Stopping hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/50-stop.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Teardown the targeted hosts (e.g. make fabric_x teardown).
.PHONY: teardown
teardown:
	@printf "$(COLOR_CYAN)🚩 Tearing down hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/60-teardown.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Update the targeted hosts (e.g. make fabric_x update).
.PHONY: update
update: stop binaries start

# Restart the targeted hosts (e.g. make fabric_x restart).
.PHONY: restart
restart: stop start

# Hard restart the targeted hosts by deleting runtime generated data (e.g. make fabric_x hard-restart).
.PHONY: hard-restart
hard-restart: teardown start

# Wipe out the config artifacts and the binaries from the remote hosts (e.g. make fabric_x wipe).
.PHONY: wipe
wipe:
	@printf "$(COLOR_CYAN)🚩 Wiping configs and binaries from remote hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/100-wipe.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Wipe the deploy folder from the remote hosts (e.g. make fabric_x hard-wipe).
.PHONY: hard-wipe
hard-wipe:
	@printf "$(COLOR_CYAN)🚩 Wiping deploy folder from remote hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/110-hard-wipe.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# =======================
# Utils
# =======================

# Generate Makefile targets for all inventory hosts (e.g. make targets)
.PHONY: targets
targets:
	@printf "$(COLOR_CYAN)🚩 Generating Makefile targets for all inventory hosts...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "hyperledger.fabricx.generate_target_hosts"

# Run a generic command on the targeted hosts (e.g. make run-command COMMAND="echo 'hello-world'")
.PHONY: run-command
run-command:
	@printf "$(COLOR_CYAN)🚩 Running command on hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]: $(COLOR_RESET)$(COMMAND)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/999-run-command.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)", "command": "$(COMMAND)"}'

# Ping the targeted host to check whether is reachable (e.g. make fabric_x ping).
.PHONY: ping
ping:
	@printf "$(COLOR_CYAN)🚩 Checking component ports on hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/70-ping.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}';

# Get the metrics from the targeted components and assert they are working correctly (e.g make load_generators get-metrics).
.PHONY: get-metrics
get-metrics:
	@printf "$(COLOR_CYAN)🚩 Collecting metrics from hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/93-get-metrics.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)", "assert_metrics": "$(ASSERT_METRICS)"}'

# Fetch the logs from the targeted hosts (e.g. make fabric_x fetch-logs).
.PHONY: fetch-logs
fetch-logs:
	@printf "$(COLOR_CYAN)🚩 Fetching logs from hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/96-fetch-logs.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Fetch the crypto material from the targeted hosts (e.g. make fabric_x fetch-crypto).
.PHONY: fetch-crypto
fetch-crypto:
	@printf "$(COLOR_CYAN)🚩 Fetching crypto material from hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) "$(PLAYBOOK_PATH)/95-fetch-crypto.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Set the TPS limit rate (e.g. make limit-rate LIMIT=1000).
.PHONY: limit-rate
limit-rate:
	@printf "$(COLOR_CYAN)🚩 Setting TPS rate limit to $(COLOR_GREEN)$(LIMIT)$(COLOR_CYAN)...$(COLOR_RESET)\n"
	$(ANSIBLE_PLAYBOOK) hyperledger.fabricx.loadgen.limit_rate --extra-vars '{"loadgen_limit_rate": "$(LIMIT)"}';
