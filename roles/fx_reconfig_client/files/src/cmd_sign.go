// Copyright IBM Corp. All Rights Reserved.
//
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"bytes"
	"flag"
	"fmt"
	"os"

	cb "github.com/hyperledger/fabric-protos-go-apiv2/common"
	"github.com/hyperledger/fabric/protoutil"
	"google.golang.org/protobuf/proto"
)

// runSignConfigUpdate produces one common.ConfigSignature for a raw
// common.ConfigUpdate proto, matching the signing-bytes construction Fabric
// itself uses to verify these signatures: SignatureHeader bytes concatenated
// with the ConfigUpdate bytes (see protoutil.ConfigUpdateEnvelopeAsSignedData
// upstream, and reconfig.md's "each admin signs the config_update.pb bytes").
// Each required party runs this independently against their own admin
// identity; the resulting ConfigSignature is later spliced into the
// ConfigUpdateEnvelope.signatures list.
func runSignConfigUpdate(args []string) error {
	fs := flag.NewFlagSet("sign-config-update", flag.ExitOnError)
	configUpdatePath := fs.String("config-update", "", "Path to the raw common.ConfigUpdate proto bytes (required)")
	mspID := fs.String("mspid", "", "MSP ID of the signing identity (required)")
	cert := fs.String("cert", "", "Path to the signing identity's certificate PEM (required)")
	key := fs.String("key", "", "Path to the signing identity's private key PEM (required)")
	output := fs.String("output", "", "Path to write the resulting common.ConfigSignature proto (required)")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *configUpdatePath == "" || *mspID == "" || *cert == "" || *key == "" || *output == "" {
		return fmt.Errorf("--config-update, --mspid, --cert, --key, and --output are required")
	}

	configUpdateBytes, err := os.ReadFile(*configUpdatePath)
	if err != nil {
		return fmt.Errorf("read %s: %w", *configUpdatePath, err)
	}

	id, err := loadIdentity(*mspID, *cert, *key)
	if err != nil {
		return err
	}

	creator, err := id.Serialize()
	if err != nil {
		return fmt.Errorf("serialize identity: %w", err)
	}
	nonce, err := protoutil.CreateNonce()
	if err != nil {
		return fmt.Errorf("create nonce: %w", err)
	}
	sigHeader := &cb.SignatureHeader{Creator: creator, Nonce: nonce}
	sigHeaderBytes, err := proto.Marshal(sigHeader)
	if err != nil {
		return fmt.Errorf("marshal signature header: %w", err)
	}

	signingBytes := bytes.Join([][]byte{sigHeaderBytes, configUpdateBytes}, nil)
	signature, err := id.Sign(signingBytes)
	if err != nil {
		return fmt.Errorf("sign: %w", err)
	}

	configSig := &cb.ConfigSignature{SignatureHeader: sigHeaderBytes, Signature: signature}
	raw, err := proto.Marshal(configSig)
	if err != nil {
		return fmt.Errorf("marshal config signature: %w", err)
	}
	if err := os.WriteFile(*output, raw, 0o644); err != nil {
		return fmt.Errorf("write %s: %w", *output, err)
	}

	fmt.Printf("wrote ConfigSignature (mspid=%s) to %s\n", *mspID, *output)
	return nil
}

// runBuildEnvelope wraps a (fully signed) common.ConfigUpdateEnvelope into a
// broadcast-ready common.Envelope: Payload{Header: {ChannelHeader: type
// CONFIG_UPDATE, channel_id}, Data: marshaled ConfigUpdateEnvelope}, signed
// once by the submitting identity. This is the same shape "peer channel
// update" produces internally via protoutil.CreateSignedEnvelope, and
// matches reconfig.md's Envelope{Payload{Data: ConfigUpdateEnvelope},
// Signature: client signature}.
func runBuildEnvelope(args []string) error {
	fs := flag.NewFlagSet("build-envelope", flag.ExitOnError)
	channelID := fs.String("channel", "", "Channel ID (required)")
	configUpdateEnvelopePath := fs.String("config-update-envelope", "", "Path to the raw common.ConfigUpdateEnvelope proto bytes (required)")
	mspID := fs.String("mspid", "", "MSP ID of the submitting identity (required)")
	cert := fs.String("cert", "", "Path to the submitting identity's certificate PEM (required)")
	key := fs.String("key", "", "Path to the submitting identity's private key PEM (required)")
	output := fs.String("output", "", "Path to write the resulting common.Envelope proto (required)")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *channelID == "" || *configUpdateEnvelopePath == "" || *mspID == "" || *cert == "" || *key == "" || *output == "" {
		return fmt.Errorf("--channel, --config-update-envelope, --mspid, --cert, --key, and --output are required")
	}

	raw, err := os.ReadFile(*configUpdateEnvelopePath)
	if err != nil {
		return fmt.Errorf("read %s: %w", *configUpdateEnvelopePath, err)
	}
	configUpdateEnvelope := &cb.ConfigUpdateEnvelope{}
	if err := proto.Unmarshal(raw, configUpdateEnvelope); err != nil {
		return fmt.Errorf("unmarshal ConfigUpdateEnvelope: %w", err)
	}

	id, err := loadIdentity(*mspID, *cert, *key)
	if err != nil {
		return err
	}

	envelope, err := protoutil.CreateSignedEnvelope(cb.HeaderType_CONFIG_UPDATE, *channelID, id, configUpdateEnvelope, 0, 0)
	if err != nil {
		return fmt.Errorf("create signed envelope: %w", err)
	}

	envelopeBytes, err := proto.Marshal(envelope)
	if err != nil {
		return fmt.Errorf("marshal envelope: %w", err)
	}
	if err := os.WriteFile(*output, envelopeBytes, 0o644); err != nil {
		return fmt.Errorf("write %s: %w", *output, err)
	}

	fmt.Printf("wrote signed Envelope (channel=%s, mspid=%s) to %s\n", *channelID, *mspID, *output)
	return nil
}
