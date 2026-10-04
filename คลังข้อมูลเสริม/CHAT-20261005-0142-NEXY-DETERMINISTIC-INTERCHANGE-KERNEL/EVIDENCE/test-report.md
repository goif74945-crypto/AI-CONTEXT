# Verification Report

## Claim
The NDIK Python reference implementation deterministically canonicalizes its accepted data model, rejects specified ambiguity classes, and detects deterministic-envelope tampering.

## Target
Standalone supplemental prototype `CHAT-20261005-0142-NEXY-DETERMINISTIC-INTERCHANGE-KERNEL`.

## Evidence class
Executed local syntax + unit/property/conformance tests + example execution + deterministic repeat benchmark.

## Observed
- Python compile: PASS.
- Pytest: **33/33 PASS**.
- 120 object-key permutations: one canonical representation and one fingerprint.
- 1,000 repeated executions: byte/fingerprint identity preserved.
- Valid conformance vectors: PASS.
- Invalid conformance vectors: expected typed error codes observed.
- Example envelope: build + verify PASS.
- Tampering tests: payload and metadata mutations rejected.
- Resource limits: depth/node/output-byte negative tests PASS.
- Unicode hardening: NFC equivalence accepted; normalization collision and surrogate code points rejected.

## Performance observation
A deterministic loop performing both canonical bytes and fingerprint over an 8,028-byte canonical payload completed 500 rounds in 2.219905 seconds (~225.23 rounds/s) on the current sandbox runtime.

This is not a performance acceptance threshold and not evidence about NEXY production infrastructure.

## Status
`PASS` for the standalone Python reference implementation.

## Not verified
- TypeScript/Rust byte-for-byte conformance;
- production NEXY integration;
- storage/backend compatibility;
- cryptographic authenticity/signatures;
- deployment behavior;
- production-scale performance.
