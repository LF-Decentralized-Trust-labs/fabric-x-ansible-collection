#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# =======================
# Common target hosts
# =======================

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