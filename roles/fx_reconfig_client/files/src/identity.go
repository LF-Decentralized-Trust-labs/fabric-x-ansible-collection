// Copyright IBM Corp. All Rights Reserved.
//
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"crypto/ecdsa"
	"crypto/rand"
	"crypto/sha256"
	"crypto/x509"
	"encoding/asn1"
	"encoding/pem"
	"fmt"
	"math/big"
	"os"

	mspproto "github.com/hyperledger/fabric-protos-go-apiv2/msp"
	"google.golang.org/protobuf/proto"
)

// identity implements protoutil.Signer (Sign([]byte) ([]byte, error);
// Serialize() ([]byte, error)) on top of a plain X.509 cert + EC private key
// pair, mirroring the identity Fabric's own CLIs (peer, cryptogen) build from
// MSP material. It intentionally does not depend on Fabric's MSP/BCCSP
// packages so that this tool only pulls in the small, stable "protoutil" +
// "fabric-protos-go-apiv2" surface.
type identity struct {
	mspID   string
	certPEM []byte
	key     *ecdsa.PrivateKey
}

func loadIdentity(mspID, certPath, keyPath string) (*identity, error) {
	certPEM, err := os.ReadFile(certPath)
	if err != nil {
		return nil, fmt.Errorf("read cert %s: %w", certPath, err)
	}
	if _, err := parseCertificate(certPEM); err != nil {
		return nil, fmt.Errorf("parse cert %s: %w", certPath, err)
	}

	keyPEM, err := os.ReadFile(keyPath)
	if err != nil {
		return nil, fmt.Errorf("read key %s: %w", keyPath, err)
	}
	key, err := parseECDSAKey(keyPEM)
	if err != nil {
		return nil, fmt.Errorf("parse key %s: %w", keyPath, err)
	}

	return &identity{mspID: mspID, certPEM: certPEM, key: key}, nil
}

func parseCertificate(certPEM []byte) (*x509.Certificate, error) {
	block, _ := pem.Decode(certPEM)
	if block == nil {
		return nil, fmt.Errorf("no PEM block found")
	}
	return x509.ParseCertificate(block.Bytes)
}

func parseECDSAKey(keyPEM []byte) (*ecdsa.PrivateKey, error) {
	block, _ := pem.Decode(keyPEM)
	if block == nil {
		return nil, fmt.Errorf("no PEM block found")
	}
	if key, err := x509.ParseECPrivateKey(block.Bytes); err == nil {
		return key, nil
	}
	raw, err := x509.ParsePKCS8PrivateKey(block.Bytes)
	if err != nil {
		return nil, fmt.Errorf("unsupported private key encoding (want SEC1 EC or PKCS8): %w", err)
	}
	key, ok := raw.(*ecdsa.PrivateKey)
	if !ok {
		return nil, fmt.Errorf("private key is not ECDSA")
	}
	return key, nil
}

// Serialize returns a marshaled msp.SerializedIdentity, the same on-wire
// "Creator" shape used throughout Fabric's config/transaction envelopes.
func (id *identity) Serialize() ([]byte, error) {
	return proto.Marshal(&mspproto.SerializedIdentity{
		Mspid:   id.mspID,
		IdBytes: id.certPEM,
	})
}

// Sign hashes msg with SHA-256 and produces a low-S ECDSA signature, matching
// the canonical signature form Fabric's BCCSP normalizes to and requires for
// signature verification to succeed (see FAB low-S malleability handling).
func (id *identity) Sign(msg []byte) ([]byte, error) {
	digest := sha256.Sum256(msg)
	r, s, err := ecdsa.Sign(rand.Reader, id.key, digest[:])
	if err != nil {
		return nil, err
	}
	s = toLowS(id.key.PublicKey, s)
	return asn1.Marshal(ecdsaSignature{R: r, S: s})
}

type ecdsaSignature struct {
	R, S *big.Int
}

// toLowS re-implements Fabric's canonical low-S signature normalization
// (see internal/cryptogen/csp.toLowS upstream; that package is Go-internal
// to the fabric module and cannot be imported directly from here).
func toLowS(pub ecdsa.PublicKey, s *big.Int) *big.Int {
	halfOrder := new(big.Int).Rsh(pub.Curve.Params().N, 1)
	if s.Cmp(halfOrder) == 1 {
		s = new(big.Int).Sub(pub.Curve.Params().N, s)
	}
	return s
}
