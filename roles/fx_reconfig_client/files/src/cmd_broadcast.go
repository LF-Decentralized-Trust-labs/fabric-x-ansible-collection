// Copyright IBM Corp. All Rights Reserved.
//
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"strings"
	"sync"
	"time"

	cb "github.com/hyperledger/fabric-protos-go-apiv2/common"
	ab "github.com/hyperledger/fabric-protos-go-apiv2/orderer"
	"google.golang.org/protobuf/proto"
)

// runBroadcast sends one already-signed common.Envelope to every given
// Router endpoint via the standard Fabric Broadcast RPC, matching Fabric-X's
// own BroadcastTxClient.SendTx behavior confirmed by Yoav Tock: a config
// transaction is submitted to ALL Routers in the network, not just the
// submitting party's own Router (SendTxTo is a test-only variant for
// exercising specific subsets).
//
// When --quorum is not given (or is 0), the default required ack count
// mirrors BroadcastTxClient.SendTx's own fault-tolerance formula: for N >= 3
// endpoints, tolerate up to floor(N/3) failures (quorum = N - floor(N/3));
// for N < 3, require all endpoints to ack.
func runBroadcast(args []string) error {
	fs := flag.NewFlagSet("broadcast", flag.ExitOnError)
	envelopePath := fs.String("envelope", "", "Path to the signed common.Envelope proto bytes (required)")
	endpointsCSV := fs.String("endpoints", "", "Comma-separated list of router host:port endpoints (required)")
	quorum := fs.Int("quorum", 0, "Minimum number of SUCCESS acks required (default: N - floor(N/3) for N>=3 endpoints, else N)")
	tlsCA := fs.String("tls-ca", "", "Path to the routers' TLS CA cert PEM (omit for plaintext)")
	tlsClientCert := fs.String("tls-client-cert", "", "Path to the client mTLS certificate PEM (omit unless mTLS)")
	tlsClientKey := fs.String("tls-client-key", "", "Path to the client mTLS private key PEM (omit unless mTLS)")
	tlsServerName := fs.String("tls-server-name", "", "Override the TLS server name to verify against, applied to every endpoint (omit to derive it per-endpoint)")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *envelopePath == "" || *endpointsCSV == "" {
		return fmt.Errorf("--envelope and --endpoints are required")
	}

	endpoints := splitAndTrim(*endpointsCSV)
	if len(endpoints) == 0 {
		return fmt.Errorf("--endpoints resolved to an empty list")
	}
	if *quorum <= 0 {
		*quorum = defaultQuorum(len(endpoints))
	}

	raw, err := os.ReadFile(*envelopePath)
	if err != nil {
		return fmt.Errorf("read %s: %w", *envelopePath, err)
	}
	envelope := &cb.Envelope{}
	if err := proto.Unmarshal(raw, envelope); err != nil {
		return fmt.Errorf("unmarshal envelope: %w", err)
	}

	opts := dialOpts{tlsCAPath: *tlsCA, tlsClientCert: *tlsClientCert, tlsClientKey: *tlsClientKey, tlsServerName: *tlsServerName}

	type result struct {
		endpoint string
		status   cb.Status
		err      error
	}
	results := make(chan result, len(endpoints))
	var wg sync.WaitGroup
	for _, endpoint := range endpoints {
		wg.Add(1)
		go func(endpoint string) {
			defer wg.Done()
			status, err := broadcastTo(context.Background(), endpoint, envelope, opts)
			results <- result{endpoint: endpoint, status: status, err: err}
		}(endpoint)
	}
	wg.Wait()
	close(results)

	successes := 0
	for r := range results {
		if r.err != nil {
			fmt.Printf("router %s: error: %v\n", r.endpoint, r.err)
			continue
		}
		fmt.Printf("router %s: status=%s\n", r.endpoint, r.status)
		if r.status == cb.Status_SUCCESS {
			successes++
		}
	}

	fmt.Printf("%d/%d routers acked SUCCESS (quorum required: %d)\n", successes, len(endpoints), *quorum)
	if successes < *quorum {
		return fmt.Errorf("quorum not reached: %d/%d SUCCESS acks (required %d)", successes, len(endpoints), *quorum)
	}
	return nil
}

func defaultQuorum(n int) int {
	if n < 3 {
		return n
	}
	return n - n/3
}

func broadcastTo(ctx context.Context, endpoint string, envelope *cb.Envelope, opts dialOpts) (cb.Status, error) {
	conn, err := dial(ctx, endpoint, opts)
	if err != nil {
		return cb.Status_UNKNOWN, fmt.Errorf("dial: %w", err)
	}
	defer conn.Close()

	client := ab.NewAtomicBroadcastClient(conn)
	callCtx, cancel := context.WithTimeout(ctx, 30*time.Second)
	defer cancel()

	stream, err := client.Broadcast(callCtx)
	if err != nil {
		return cb.Status_UNKNOWN, fmt.Errorf("open broadcast stream: %w", err)
	}
	defer stream.CloseSend()

	if err := stream.Send(envelope); err != nil {
		return cb.Status_UNKNOWN, fmt.Errorf("send envelope: %w", err)
	}

	resp, err := stream.Recv()
	if err != nil {
		return cb.Status_UNKNOWN, fmt.Errorf("receive broadcast response: %w", err)
	}
	return resp.GetStatus(), nil
}

func splitAndTrim(csv string) []string {
	var out []string
	for _, part := range strings.Split(csv, ",") {
		part = strings.TrimSpace(part)
		if part != "" {
			out = append(out, part)
		}
	}
	return out
}
