// Copyright IBM Corp. All Rights Reserved.
//
// SPDX-License-Identifier: Apache-2.0

// Command fx-reconfig-client is a small, purpose-built gRPC client for
// performing live channel-config updates against a running Fabric-X (Arma)
// network. It speaks the same standard Fabric orderer.AtomicBroadcast
// service (Deliver + Broadcast) that Arma's Router and Assembler already
// expose -- there is no Arma-specific network protocol involved.
//
// Subcommands:
//
//	fetch-config           pull the current channel config block from an Assembler
//	extract-config-update   read the ConfigUpdate bytes out of a ConfigUpdateEnvelope, unchanged
//	sign-config-update      produce one ConfigSignature for a ConfigUpdate
//	merge-signatures        splice ConfigSignatures into an unsigned ConfigUpdateEnvelope
//	build-envelope           wrap+sign a ConfigUpdateEnvelope into a broadcastable Envelope
//	broadcast                submit a signed Envelope to a set of Routers
package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		usage()
		os.Exit(2)
	}

	var err error
	switch os.Args[1] {
	case "fetch-config":
		err = runFetchConfig(os.Args[2:])
	case "extract-config-update":
		err = runExtractConfigUpdate(os.Args[2:])
	case "sign-config-update":
		err = runSignConfigUpdate(os.Args[2:])
	case "merge-signatures":
		err = runMergeSignatures(os.Args[2:])
	case "build-envelope":
		err = runBuildEnvelope(os.Args[2:])
	case "broadcast":
		err = runBroadcast(os.Args[2:])
	default:
		usage()
		os.Exit(2)
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "fx-reconfig-client: %v\n", err)
		os.Exit(1)
	}
}

func usage() {
	fmt.Fprintln(os.Stderr, "usage: fx-reconfig-client <fetch-config|extract-config-update|sign-config-update|merge-signatures|build-envelope|broadcast> [flags]")
}
