#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# =======================
# Common target hosts
# =======================

# Appends $(1) to TARGET_HOSTS if a group/host target already ran in this
# invocation, otherwise initializes TARGET_HOSTS to just $(1). This lets
# group/host targets be chained (e.g. make fabric_x_orderers
# fabric_x_committers start) so their hosts are unioned via the Ansible
# ":" pattern operator instead of the last target overwriting the others.
define add_target_hosts
$(eval TARGET_HOSTS := $(if $(_target_hosts_chained),$(TARGET_HOSTS):$(1),$(1)))$(eval _target_hosts_chained := 1)
endef

# Target all the network within the inventory (e.g. make network start).
.PHONY: network
network:
	@$(call add_target_hosts,network):

# Target the Fabric CAs for the command being run (e.g. make fabric_cas start).
.PHONY: fabric_cas
fabric_cas:
	@$(call add_target_hosts,fabric_cas):

# Target the Fabric CA DBs for the command being run (e.g. make fabric_ca_dbs start).
.PHONY: fabric_ca_dbs
fabric_ca_dbs:
	@$(call add_target_hosts,fabric_ca_dbs):

# Target the Fabric CA servers for the command being run (e.g. make fabric_ca_servers start).
.PHONY: fabric_ca_servers
fabric_ca_servers:
	@$(call add_target_hosts,fabric_ca_servers):

# Target the fabric_x components for the command being run (e.g. make fabric_x start).
.PHONY: fabric_x
fabric_x:
	@$(call add_target_hosts,fabric_x):

# Target the Fabric-X Orderer components for the command being run (e.g. make fabric_x_orderers start).
.PHONY: fabric_x_orderers
fabric_x_orderers:
	@$(call add_target_hosts,fabric_x_orderers):

# Target the Fabric-X Committer components for the command being run (e.g. make fabric_x_committers start).
.PHONY: fabric_x_committers
fabric_x_committers:
	@$(call add_target_hosts,fabric_x_committers):

# Target the Fabric-X Block Explorer components for the command being run (e.g. make fabric_x_block_explorer start).
.PHONY: fabric_x_block_explorer
fabric_x_block_explorer:
	@$(call add_target_hosts,fabric_x_block_explorer):

# Target the Fabric-X EVM components for the command being run (e.g. make fabric_x_evm start).
.PHONY: fabric_x_evm
fabric_x_evm:
	@$(call add_target_hosts,fabric_x_evm):

# Target the load_generators for the command being run (e.g. make load_generators start).
.PHONY: load_generators
load_generators:
	@$(call add_target_hosts,load_generators):

# Target the monitoring instances for the command being run (e.g. make monitoring start).
.PHONY: monitoring
monitoring:
	@$(call add_target_hosts,monitoring):