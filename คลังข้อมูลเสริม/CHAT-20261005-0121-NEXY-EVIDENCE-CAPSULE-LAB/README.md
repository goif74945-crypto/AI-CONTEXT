# NEXY Evidence Capsule & Selective Disclosure Lab

**Status:** standalone AI-proposed reference lab. Not canonical NEXY architecture. Not production cryptography. Not evidence that NEXY.AI implements this behavior.

**Durable chat code:** `CHAT-20261005-0121-NEXY-EVIDENCE-CAPSULE-LAB`

## Purpose
Explore a derived evidence-view mechanism that can disclose only authorized fields while preserving tamper evidence, provenance binding, freshness, audience binding, and replay controls without rewriting original audit lineage.

## Start here
1. `00_SESSION_MEMORY.md`
2. `design/01_TASK_CONTRACT.md`
3. `design/02_ARCHITECTURE_PROTOCOL.md`
4. `design/03_THREAT_MODEL.md`
5. `reference/reference_impl.py`
6. `reference/test_reference_impl.py`
7. `validation/06_TEST_EVIDENCE.md`
8. `10_FINAL_AUDIT.md`

## What is implemented
- deterministic JSON-like canonicalization profile;
- salted per-field SHA-256 commitments;
- domain-separated Merkle tree/proofs;
- signed capsule header;
- role-scoped selective presentations;
- audience binding;
- validity and maximum-age checks;
- replay-guard hook;
- required-field enforcement;
- fail-closed tamper detection.

## Verification
The compact repository reference implementation and test file are byte-identical to locally executed files by Git blob identity. Python compilation passed and 20/20 tests passed.

A larger exploratory local prototype also reached 32/32 tests during development, but only the compact committed reference is used for repository E1/E2 completion claims.

## Security boundary
The reference signer is `HMAC-SHA256-REFERENCE-ONLY`. It is intentionally unsuitable as a production issuer-authentication architecture because verifiers with the shared key can forge signatures. Production adoption requires asymmetric signing, governed key lifecycle, durable replay storage, cross-language canonicalization vectors, privacy review, and integration evidence.

## Scope
This lab modified only its own folder in `goif74945-crypto/AI-CONTEXT`. No repository whose name contains `NEXY.AI` was modified.