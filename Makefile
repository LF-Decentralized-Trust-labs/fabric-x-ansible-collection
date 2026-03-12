#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# exported vars
PROJECT_DIR := $(CURDIR)
ANSIBLE_CONFIG ?= $(PROJECT_DIR)/examples/ansible.cfg
ANSIBLE_CACHE_PLUGIN ?= jsonfile
ANSIBLE_CACHE_PLUGIN_CONNECTION ?= $(PROJECT_DIR)/out/ansible_fact_cache

export ANSIBLE_CONFIG
export ANSIBLE_CACHE_PLUGIN
export ANSIBLE_CACHE_PLUGIN_CONNECTION
export PROJECT_DIR

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
install:
	@echo "$(COLOR_CYAN)==> Building and installing hyperledger.fabricx collection...$(COLOR_RESET)"
	@ansible-galaxy collection build -f
	@ansible-galaxy collection install $$(ls -1 | grep fabricx) -f
	@rm -f $$(ls -1 | grep fabricx)

# Check the linting correctness (e.g. make lint)
.PHONY: lint
lint:
	@echo "$(COLOR_CYAN)==> Running ansible-lint checks...$(COLOR_RESET)"
	ansible-lint --offline roles playbooks examples

# Check the license header
.PHONY: check-license-header
check-license-header:
	@echo "$(COLOR_CYAN)==> Checking license headers...$(COLOR_RESET)"
	./ci/check_license_header.sh

# Check that no trailing spaces are added in the j2 files
.PHONY: check-license-header
check-trailing-spaces:
	@echo "$(COLOR_CYAN)==> Checking for trailing spaces in templates...$(COLOR_RESET)"
	./ci/check_trailing_spaces.sh

# =======================
# Deployment
# =======================

# Install the utilities needed to run the components on the targeted remote hosts (e.g. make install-prerequisites).
.PHONY: install-prerequisites
install-prerequisites:
	@echo "$(COLOR_CYAN)==> Installing prerequisites on remote hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook hyperledger.fabricx.install_prerequisites --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Log the container engine within a Container Registry (aka CR) (e.g. make login-cr CONTAINER_REGISTRY=icr.io CONTAINER_REGISTRY_USERNAME=iamapikey CONTAINER_REGISTRY_PASSWORD=my_api_key).
.PHONY: login-cr
login-cr:
	@echo "$(COLOR_CYAN)==> Logging into container registry [$(COLOR_GREEN)$(CONTAINER_REGISTRY)$(COLOR_CYAN)] for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook hyperledger.fabricx.log_in_container_registry --extra-vars '{"target_hosts": "$(TARGET_HOSTS)", "container_registry": "$(CONTAINER_REGISTRY)", "container_registry_username": "$(CONTAINER_REGISTRY_USERNAME)", "container_registry_password": "$(CONTAINER_REGISTRY_PASSWORD)"}'

# Build all the artifacts, the binaries and configuration files (e.g. make setup).
.PHONY: setup
setup: artifacts binaries configs

# Build all the artifacts (e.g. make artifacts).
.PHONY: artifacts
artifacts: generate-crypto genesis-block

# Generate the crypto material (e.g. make build-crypto).
.PHONY: generate-crypto
generate-crypto:
	@echo "$(COLOR_CYAN)==> Generating crypto material for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/20-generate-crypto.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Build the genesis block for the network (e.g. make genesis-block).
.PHONY: genesis-block
genesis-block:
	@echo "$(COLOR_CYAN)==> Building genesis block for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/21-build-genesis-block.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Build the targeted binaries on the controller node (e.g. make binaries).
.PHONY: binaries
binaries:
	@echo "$(COLOR_CYAN)==> Building/installing binaries for hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/30-binaries.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Clean all the artifacts (configs and bins) built on the controller node (e.g. make clean).
.PHONY: clean
clean: clean-cache
	@echo "$(COLOR_CYAN)==> Cleaning local artifacts and cache...$(COLOR_RESET)"
	rm -rf ./out

# Clean the Ansible cache (e.g. make clean-cache).
.PHONY: clean-cache
clean-cache:
	@echo "$(COLOR_CYAN)==> Cleaning Ansible cache...$(COLOR_RESET)"
	rm -rf $(ANSIBLE_CACHE_PLUGIN_CONNECTION)

# Create/Ship the configs to the remote nodes (e.g. make fabric_x configs).
.PHONY: configs
configs:
	@echo "$(COLOR_CYAN)==> Creating and shipping configs to remote nodes [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/40-configs.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Start the targeted hosts (e.g. make fabric_x start).
.PHONY: start
start:
	@echo "$(COLOR_CYAN)==> Starting hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/60-start.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Stop the targeted hosts (e.g. make fabric_x stop).
.PHONY: stop
stop:
	@echo "$(COLOR_CYAN)==> Stopping hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/70-stop.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Teardown the targeted hosts (e.g. make fabric_x teardown).
.PHONY: teardown
teardown:
	@echo "$(COLOR_CYAN)==> Tearing down hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/80-teardown.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

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
	@echo "$(COLOR_CYAN)==> Wiping configs and binaries from remote hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/100-wipe.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Wipe the deploy folder from the remote hosts (e.g. make fabric_x hard-wipe).
.PHONY: hard-wipe
hard-wipe:
	@echo "$(COLOR_CYAN)==> Wiping deploy folder from remote hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/110-hard-wipe.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# =======================
# Utils
# =======================

# Generate Makefile targets for all inventory hosts (e.g. make targets)
.PHONY: targets
targets:
	@echo "$(COLOR_CYAN)==> Generating Makefile targets for all inventory hosts...$(COLOR_RESET)"
	ansible-playbook "hyperledger.fabricx.generate_target_hosts"

# Run a generic command on the targeted hosts (e.g. make run-command COMMAND="echo 'hello-world'")
.PHONY: run-command
run-command:
	@echo "$(COLOR_CYAN)==> Running command on hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]: $(COLOR_RESET)$(COMMAND)"
	ansible-playbook "$(PLAYBOOK_PATH)/10-run-command.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)", "command": "$(COMMAND)"}'

# Ping the targeted host to check whether is reachable (e.g. make fabric_x ping).
.PHONY: ping
ping:
	@echo "$(COLOR_CYAN)==> Checking component ports on hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/90-ping.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}';

# Get the metrics from the targeted components and assert they are working correctly (e.g make load_generators get-metrics).
.PHONY: get-metrics
get-metrics:
	@echo "$(COLOR_CYAN)==> Collecting metrics from hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/93-get-metrics.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)", "assert_metrics": "$(ASSERT_METRICS)"}'

# Fetch the logs from the targeted hosts (e.g. make fabric_x fetch-logs).
.PHONY: fetch-logs
fetch-logs:
	@echo "$(COLOR_CYAN)==> Fetching logs from hosts [$(COLOR_GREEN)$(TARGET_HOSTS)$(COLOR_CYAN)]...$(COLOR_RESET)"
	ansible-playbook "$(PLAYBOOK_PATH)/96-fetch-logs.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Set the TPS limit rate (e.g. make limit-rate LIMIT=1000).
.PHONY: limit-rate
limit-rate:
	@echo "$(COLOR_CYAN)==> Setting TPS rate limit to $(COLOR_GREEN)$(LIMIT)$(COLOR_CYAN)...$(COLOR_RESET)"
	ansible-playbook hyperledger.fabricx.loadgen.limit_rate --extra-vars '{"loadgen_limit_rate": "$(LIMIT)"}';
