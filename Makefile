#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# exported vars
ANSIBLE_CONFIG ?= ./examples/ansible.cfg
ANSIBLE_CACHE_PLUGIN ?= jsonfile
ANSIBLE_CACHE_PLUGIN_CONNECTION ?= /tmp/ansible_fact_cache
PROJECT_DIR := $(CURDIR)

export ANSIBLE_CONFIG
export ANSIBLE_CACHE_PLUGIN
export ANSIBLE_CACHE_PLUGIN_CONNECTION
export PROJECT_DIR

# Makefile vars
PLAYBOOK_PATH := $(CURDIR)/examples/playbooks
TARGET_HOSTS ?= all
ASSERT_METRICS ?= false
LIMIT ?= 1000

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
	@ansible-galaxy collection build -f
	@ansible-galaxy collection install $$(ls -1 | grep fabricx) -f
	@rm -f $$(ls -1 | grep fabricx)

# Check the linting correctness (e.g. make lint)
.PHONY: lint
lint:
	ansible-lint --offline roles playbooks examples

# Check the license header
.PHONY: check-license-header
check-license-header:
	./ci/check_license_header.sh

#########################
# Deployment
#########################

# Install the utilities needed to run the components on the targeted remote hosts (e.g. make install-prerequisites).
.PHONY: install-prerequisites
install-prerequisites:
	ansible-playbook hyperledger.fabricx.install_prerequisites --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Build all the artifacts, the binaries and transfer them to the remote hosts (e.g. make setup).
.PHONY: setup
setup: build transfer

# Build all the artifacts and the binaries on the localhost (e.g. make build).
.PHONY: build
build: build-configs build-bins

# Transfer all the artifacts and the binaries to the remote hosts (e.g. make transfer).
.PHONY: transfer
transfer: transfer-configs transfer-bins

# Build the config artifacts on the controller node (e.g. make build-configs).
.PHONY: build-configs
build-configs:
	ansible-playbook "$(PLAYBOOK_PATH)/20-build-configs.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Build the targeted binaries on the controller node (e.g. make build-bins).
.PHONY: build-bins
build-bins:
	ansible-playbook "$(PLAYBOOK_PATH)/30-build-bins.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Clean all the artifacts (configs and bins) built on the controller node (e.g. make clean).
.PHONY: clean
clean: clean-cache
	rm -rf ./out

# Clean the Ansible cache (e.g. make clean-cache).
.PHONY: clean-cache
clean-cache:
	rm -rf $(ANSIBLE_CACHE_PLUGIN_CONNECTION)

# Transfer the targeted config artifacts to the remote nodes (e.g. make fabric_x transfer-configs).
.PHONY: transfer-configs
transfer-configs:
	ansible-playbook "$(PLAYBOOK_PATH)/40-transfer-configs.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Transfer the targeted binaries to the remote nodes (e.g. make fabric_x transfer-bins).
.PHONY: transfer-bins
transfer-bins:
	ansible-playbook "$(PLAYBOOK_PATH)/50-transfer-bins.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Start the targeted hosts (e.g. make fabric_x start).
.PHONY: start
start:
	ansible-playbook "$(PLAYBOOK_PATH)/60-start.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Stop the targeted hosts (e.g. make fabric_x stop).
.PHONY: stop
stop:
	ansible-playbook "$(PLAYBOOK_PATH)/70-stop.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Teardown the targeted hosts (e.g. make fabric_x teardown).
.PHONY: teardown
teardown:
	ansible-playbook "$(PLAYBOOK_PATH)/80-teardown.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Restart the targeted hosts (e.g. make fabric_x restart).
.PHONY: restart
restart: teardown start

# Start a Node Exporter container on the targeted hosts (e.g. make fabric_x node-exporter-start).
.PHONY: node-exporter-start
node-exporter-start:
	ansible-playbook hyperledger.fabricx.node_exporter.start --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Stop the Node Exporter container on the targeted hosts (e.g. make fabric_x node-exporter-stop).
.PHONY: node-exporter-stop
node-exporter-stop:
	ansible-playbook hyperledger.fabricx.node_exporter.stop --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Teardown the Node Exporter container on the targeted hosts (e.g. make fabric_x node-exporter-teardown).
.PHONY: node-exporter-teardown
node-exporter-teardown:
	ansible-playbook hyperledger.fabricx.node_exporter.teardown --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Wipe out the config artifacts and the binaries from the remote hosts (e.g. make fabric_x wipe).
.PHONY: wipe
wipe:
	ansible-playbook "$(PLAYBOOK_PATH)/100-wipe.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

#########################
# Utils
#########################

# Ping the targeted host to check whether is reachable (e.g. make fabric_x ping).
.PHONY: ping
ping:
	ansible-playbook "$(PLAYBOOK_PATH)/90-ping.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}';

# Get the metrics from the targeted components and assert they are working correctly (e.g make load_generators get-metrics).
.PHONY: get-metrics
get-metrics:
	ansible-playbook "$(PLAYBOOK_PATH)/93-get-metrics.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)", "assert_metrics": "$(ASSERT_METRICS)"}'

# Fetch the logs from the targeted hosts (e.g. make fabric_x fetch-logs).
.PHONY: fetch-logs
fetch-logs:
	ansible-playbook "$(PLAYBOOK_PATH)/96-fetch-logs.yaml" --extra-vars '{"target_hosts": "$(TARGET_HOSTS)"}'

# Set the TPS limit rate (e.g. make limit-rate LIMIT=1000).
.PHONY: limit-rate
limit-rate:
	ansible-playbook hyperledger.fabricx.loadgen.limit_rate --extra-vars '{"loadgen_limit_rate": "$(LIMIT)"}';

#########################
# Common target hosts
#########################

# Target the Fabric CA servers for the command being run (e.g. make fabric_cas start).
.PHONY: fabric_cas
fabric_cas:
	@$(eval TARGET_HOSTS = fabric_cas):

# Target the fabric_x components for the command being run (e.g. make fabric_x start).
.PHONY: fabric_x
fabric_x:
	@$(eval TARGET_HOSTS = fabric_x):

# Target the Fabric-X Orderer components for the command being run (e.g. make fabric_x_orderers start).
.PHONY: fabric_x_orderers
fabric_x_orderers:
	@$(eval TARGET_HOSTS = fabric_x_orderers):

# Target the Fabric-X Committer components for the command being run (e.g. make fabric_x_committer start).
.PHONY: fabric_x_committer
fabric_x_committer:
	@$(eval TARGET_HOSTS = fabric_x_committer):

# Target the load_generators for the command being run (e.g. make load_generators start).
.PHONY: load_generators
load_generators:
	@$(eval TARGET_HOSTS = load_generators):

# Target the monitoring instances for the command being run (e.g. make monitoring start).
.PHONY: monitoring
monitoring:
	@$(eval TARGET_HOSTS = monitoring):
