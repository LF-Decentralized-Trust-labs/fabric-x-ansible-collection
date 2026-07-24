// Copyright IBM Corp. All Rights Reserved.
//
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"context"
	"flag"
	"fmt"
	"os"

	cb "github.com/hyperledger/fabric-protos-go-apiv2/common"
	ab "github.com/hyperledger/fabric-protos-go-apiv2/orderer"
	"github.com/hyperledger/fabric/protoutil"
	"google.golang.org/protobuf/proto"
)

// runFetchConfig fetches the current channel config block from an Assembler
// via the standard Fabric Deliver API. It follows the same two-step
// resolution "peer channel fetch config" uses against a classic orderer
// (and the same resolution Yoav Tock described: pull the newest block,
// follow its LAST_CONFIG metadata pointer, then fetch that block by number
// unless the newest block already is the config block).
func runFetchConfig(args []string) error {
	fs := flag.NewFlagSet("fetch-config", flag.ExitOnError)
	endpoint := fs.String("endpoint", "", "Assembler address, host:port (required)")
	channelID := fs.String("channel", "", "Channel ID (required)")
	mspID := fs.String("mspid", "", "MSP ID of the signing (reader) identity (required)")
	cert := fs.String("cert", "", "Path to the signing identity's certificate PEM (required)")
	key := fs.String("key", "", "Path to the signing identity's private key PEM (required)")
	tlsCA := fs.String("tls-ca", "", "Path to the Assembler's TLS CA cert PEM (omit for plaintext)")
	tlsClientCert := fs.String("tls-client-cert", "", "Path to the client mTLS certificate PEM (omit unless mTLS)")
	tlsClientKey := fs.String("tls-client-key", "", "Path to the client mTLS private key PEM (omit unless mTLS)")
	tlsServerName := fs.String("tls-server-name", "", "Override the TLS server name to verify against (omit to derive it from --endpoint)")
	output := fs.String("output", "", "Path to write the raw config block proto (required)")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *endpoint == "" || *channelID == "" || *mspID == "" || *cert == "" || *key == "" || *output == "" {
		return fmt.Errorf("--endpoint, --channel, --mspid, --cert, --key, and --output are required")
	}

	id, err := loadIdentity(*mspID, *cert, *key)
	if err != nil {
		return err
	}

	ctx := context.Background()
	opts := dialOpts{tlsCAPath: *tlsCA, tlsClientCert: *tlsClientCert, tlsClientKey: *tlsClientKey, tlsServerName: *tlsServerName}

	newest, err := pullBlock(ctx, *endpoint, *channelID, id, opts, seekNewest())
	if err != nil {
		return fmt.Errorf("fetch newest block: %w", err)
	}

	lastConfigIndex, err := protoutil.GetLastConfigIndexFromBlock(newest)
	if err != nil {
		return fmt.Errorf("read last config index from newest block: %w", err)
	}

	configBlock := newest
	if lastConfigIndex != newest.GetHeader().GetNumber() {
		configBlock, err = pullBlock(ctx, *endpoint, *channelID, id, opts, seekSpecified(lastConfigIndex))
		if err != nil {
			return fmt.Errorf("fetch config block %d: %w", lastConfigIndex, err)
		}
	}

	raw, err := proto.Marshal(configBlock)
	if err != nil {
		return fmt.Errorf("marshal config block: %w", err)
	}
	if err := os.WriteFile(*output, raw, 0o644); err != nil {
		return fmt.Errorf("write %s: %w", *output, err)
	}

	fmt.Printf("wrote config block %d (channel %s) to %s\n", configBlock.GetHeader().GetNumber(), *channelID, *output)
	return nil
}

func seekNewest() *ab.SeekInfo {
	pos := &ab.SeekPosition{Type: &ab.SeekPosition_Newest{Newest: &ab.SeekNewest{}}}
	return &ab.SeekInfo{
		Start:         pos,
		Stop:          pos,
		Behavior:      ab.SeekInfo_BLOCK_UNTIL_READY,
		ErrorResponse: ab.SeekInfo_BEST_EFFORT,
	}
}

func seekSpecified(number uint64) *ab.SeekInfo {
	pos := &ab.SeekPosition{Type: &ab.SeekPosition_Specified{Specified: &ab.SeekSpecified{Number: number}}}
	return &ab.SeekInfo{
		Start:         pos,
		Stop:          pos,
		Behavior:      ab.SeekInfo_BLOCK_UNTIL_READY,
		ErrorResponse: ab.SeekInfo_BEST_EFFORT,
	}
}

// pullBlock opens one Deliver stream against endpoint, sends a signed seek
// request built from seekInfo, and returns the single block delivered. It
// treats DELIVER_SEEK_INFO envelopes as one-shot: the seek range always
// resolves to exactly one block (Newest/Newest or Specified/Specified).
func pullBlock(ctx context.Context, endpoint, channelID string, id *identity, opts dialOpts, seekInfo *ab.SeekInfo) (*cb.Block, error) {
	conn, err := dial(ctx, endpoint, opts)
	if err != nil {
		return nil, fmt.Errorf("dial %s: %w", endpoint, err)
	}
	defer conn.Close()

	client := ab.NewAtomicBroadcastClient(conn)
	stream, err := client.Deliver(ctx)
	if err != nil {
		return nil, fmt.Errorf("open deliver stream: %w", err)
	}
	defer stream.CloseSend()

	tlsCertHash, err := clientTLSCertHash(opts)
	if err != nil {
		return nil, fmt.Errorf("compute client TLS cert hash: %w", err)
	}
	envelope, err := protoutil.CreateSignedEnvelopeWithTLSBinding(cb.HeaderType_DELIVER_SEEK_INFO, channelID, id, seekInfo, 0, 0, tlsCertHash)
	if err != nil {
		return nil, fmt.Errorf("create seek envelope: %w", err)
	}
	if err := stream.Send(envelope); err != nil {
		return nil, fmt.Errorf("send seek envelope: %w", err)
	}

	resp, err := stream.Recv()
	if err != nil {
		return nil, fmt.Errorf("receive deliver response: %w", err)
	}

	switch t := resp.GetType().(type) {
	case *ab.DeliverResponse_Block:
		return t.Block, nil
	case *ab.DeliverResponse_Status:
		return nil, fmt.Errorf("deliver rejected: status=%s", t.Status)
	default:
		return nil, fmt.Errorf("unexpected deliver response: %v", resp)
	}
}
