// Copyright IBM Corp. All Rights Reserved.
//
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"os"
	"time"

	"github.com/hyperledger/fabric/common/util"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/credentials/insecure"
)

// dialOpts describes the connection material needed to reach one Arma
// Router/Assembler gRPC endpoint. tlsCAPath may be empty for a plaintext
// (no-TLS) deployment; tlsClientCert/tlsClientKey are only needed when the
// endpoint requires mTLS. tlsServerName overrides the name used for SNI and
// certificate verification -- needed whenever the dial address doesn't
// literally match a SAN entry on the server cert (for example, a
// port-forwarded/NATed address such as 127.0.0.1 dialing a container whose
// cert only lists its LAN IPs).
type dialOpts struct {
	tlsCAPath     string
	tlsClientCert string
	tlsClientKey  string
	tlsServerName string
}

func dial(ctx context.Context, endpoint string, opts dialOpts) (*grpc.ClientConn, error) {
	creds, err := transportCredentials(opts)
	if err != nil {
		return nil, err
	}
	dialCtx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()
	return grpc.DialContext(dialCtx, endpoint, grpc.WithTransportCredentials(creds), grpc.WithBlock())
}

func transportCredentials(opts dialOpts) (credentials.TransportCredentials, error) {
	if opts.tlsCAPath == "" {
		return insecure.NewCredentials(), nil
	}

	caPEM, err := os.ReadFile(opts.tlsCAPath)
	if err != nil {
		return nil, fmt.Errorf("read tls-ca %s: %w", opts.tlsCAPath, err)
	}
	pool := x509.NewCertPool()
	if !pool.AppendCertsFromPEM(caPEM) {
		return nil, fmt.Errorf("no certificates parsed from tls-ca %s", opts.tlsCAPath)
	}

	tlsConfig := &tls.Config{RootCAs: pool}
	if opts.tlsServerName != "" {
		tlsConfig.ServerName = opts.tlsServerName
	}

	if opts.tlsClientCert != "" && opts.tlsClientKey != "" {
		clientCert, err := tls.LoadX509KeyPair(opts.tlsClientCert, opts.tlsClientKey)
		if err != nil {
			return nil, fmt.Errorf("load client tls cert/key: %w", err)
		}
		tlsConfig.Certificates = []tls.Certificate{clientCert}
	}

	return credentials.NewTLS(tlsConfig), nil
}

// clientTLSCertHash returns SHA-256 of the client's DER-encoded mTLS
// certificate, as required by Fabric's deliver-request TLS binding (the
// server rejects a Deliver seek envelope with "client didn't include its TLS
// cert hash" otherwise). Returns nil, nil when no client cert is configured
// (plaintext / server-TLS-only deployments have nothing to bind to).
func clientTLSCertHash(opts dialOpts) ([]byte, error) {
	if opts.tlsClientCert == "" {
		return nil, nil
	}
	certPEM, err := os.ReadFile(opts.tlsClientCert)
	if err != nil {
		return nil, fmt.Errorf("read tls-client-cert %s: %w", opts.tlsClientCert, err)
	}
	block, _ := pem.Decode(certPEM)
	if block == nil {
		return nil, fmt.Errorf("no PEM block found in %s", opts.tlsClientCert)
	}
	return util.ComputeSHA256(block.Bytes), nil
}
