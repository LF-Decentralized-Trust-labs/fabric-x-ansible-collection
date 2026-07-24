// Copyright IBM Corp. All Rights Reserved.
//
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"flag"
	"fmt"
	"os"

	cb "github.com/hyperledger/fabric-protos-go-apiv2/common"
	"google.golang.org/protobuf/proto"
)

// runExtractConfigUpdate reads the config_update bytes field straight out of
// a common.ConfigUpdateEnvelope proto, byte-for-byte, with no re-encoding.
//
// This exists because ConfigUpdateEnvelope.config_update is itself an opaque
// bytes field holding a marshaled common.ConfigUpdate. Producing that field
// by decoding it to JSON (for configtxlator's protolator extension, which is
// how the envelope gets built) and then re-encoding a fresh copy for signing
// is not guaranteed to reproduce the exact same bytes: ConfigUpdate embeds
// several protobuf map fields (ConfigGroup.groups/values/policies), and two
// independent marshal passes -- each configtxlator invocation is a fresh
// process/container -- can order map entries differently despite identical
// content. A signature computed over a differently-ordered re-encoding won't
// verify against the copy that actually ships in the envelope, and every
// signer would fail policy evaluation with zero satisfied sub-policies.
// Reading the field directly out of the already-built envelope sidesteps
// that risk entirely: proto.Unmarshal copies the stored byte slice as-is,
// it does not re-serialize it.
func runExtractConfigUpdate(args []string) error {
	fs := flag.NewFlagSet("extract-config-update", flag.ExitOnError)
	envelopePath := fs.String("envelope", "", "Path to a common.ConfigUpdateEnvelope proto (required)")
	output := fs.String("output", "", "Path to write the raw common.ConfigUpdate proto bytes (required)")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *envelopePath == "" || *output == "" {
		return fmt.Errorf("--envelope and --output are required")
	}

	raw, err := os.ReadFile(*envelopePath)
	if err != nil {
		return fmt.Errorf("read %s: %w", *envelopePath, err)
	}
	envelope := &cb.ConfigUpdateEnvelope{}
	if err := proto.Unmarshal(raw, envelope); err != nil {
		return fmt.Errorf("unmarshal ConfigUpdateEnvelope: %w", err)
	}
	if len(envelope.ConfigUpdate) == 0 {
		return fmt.Errorf("%s has an empty config_update field", *envelopePath)
	}

	if err := os.WriteFile(*output, envelope.ConfigUpdate, 0o644); err != nil {
		return fmt.Errorf("write %s: %w", *output, err)
	}

	fmt.Printf("wrote %d bytes of ConfigUpdate to %s\n", len(envelope.ConfigUpdate), *output)
	return nil
}

// runMergeSignatures splices a set of already-produced common.ConfigSignature
// files into an unsigned common.ConfigUpdateEnvelope's signatures list and
// re-marshals it -- entirely in-process, with no configtxlator/JSON round
// trip involved. The envelope's config_update bytes are carried over
// unchanged from the unmarshaled input (see runExtractConfigUpdate for why
// that matters); ConfigSignature itself has no map fields, so this
// operation carries none of that risk on its own, but keeping the whole
// splice in typed Go avoids depending on that being true forever.
func runMergeSignatures(args []string) error {
	fs := flag.NewFlagSet("merge-signatures", flag.ExitOnError)
	envelopePath := fs.String("envelope", "", "Path to the unsigned common.ConfigUpdateEnvelope proto (required)")
	signaturesCSV := fs.String("signatures", "", "Comma-separated paths to common.ConfigSignature proto files (required)")
	output := fs.String("output", "", "Path to write the resulting common.ConfigUpdateEnvelope proto bytes (required)")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *envelopePath == "" || *signaturesCSV == "" || *output == "" {
		return fmt.Errorf("--envelope, --signatures, and --output are required")
	}

	raw, err := os.ReadFile(*envelopePath)
	if err != nil {
		return fmt.Errorf("read %s: %w", *envelopePath, err)
	}
	envelope := &cb.ConfigUpdateEnvelope{}
	if err := proto.Unmarshal(raw, envelope); err != nil {
		return fmt.Errorf("unmarshal ConfigUpdateEnvelope: %w", err)
	}

	for _, sigPath := range splitAndTrim(*signaturesCSV) {
		sigRaw, err := os.ReadFile(sigPath)
		if err != nil {
			return fmt.Errorf("read %s: %w", sigPath, err)
		}
		sig := &cb.ConfigSignature{}
		if err := proto.Unmarshal(sigRaw, sig); err != nil {
			return fmt.Errorf("unmarshal ConfigSignature %s: %w", sigPath, err)
		}
		envelope.Signatures = append(envelope.Signatures, sig)
	}

	out, err := proto.Marshal(envelope)
	if err != nil {
		return fmt.Errorf("marshal ConfigUpdateEnvelope: %w", err)
	}
	if err := os.WriteFile(*output, out, 0o644); err != nil {
		return fmt.Errorf("write %s: %w", *output, err)
	}

	fmt.Printf("wrote ConfigUpdateEnvelope with %d signature(s) to %s\n", len(envelope.Signatures), *output)
	return nil
}
