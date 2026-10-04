# NEXY Cross-Runtime Contract Forge

**Work-session code:** `CHAT-20261005-0138-NEXY-CROSS-RUNTIME-CONTRACT-FORGE`  
**Status:** COMPLETE as a standalone supplemental tool and design artifact.  
**Integration status with NEXY.AI:** NOT INTEGRATED.  
**Authority:** AI proposal/tooling only. This directory is not NEXY.AI law, DOC-C, or a replacement for any canonical project specification.

## Purpose

This project is a standalone, deterministic contract compiler and drift auditor intended to reduce semantic divergence between TypeScript and Rust implementations of shared NEXY concepts.

It was motivated by a read-only observation at NEXY.AI commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`: `core-kernel/src/kernel/vnext_matrix.rs` explicitly describes itself as a Rust mirror of `packages/core/vnext-state-matrix.ts` and says the two must agree on transitions, event ownership, error codes, freeze recovery, and release behavior. Hand-maintained mirrors create a future drift surface even when each implementation is individually correct.

The forge does **not** modify or depend on the NEXY.AI repository at runtime. It consumes a language-neutral manifest, validates it fail-closed, normalizes it deterministically, fingerprints its semantics, generates TypeScript and Rust representations, emits shared fixtures/snapshots, and audits observed runtime snapshots for drift.

## Scope boundary

### IN SCOPE

- deterministic language-neutral contract manifests;
- strict validation and resource limits;
- canonical semantic normalization;
- semantic and full-manifest SHA-256 fingerprints;
- TypeScript generation;
- `#![no_std]` Rust generation without allocation types;
- shared conformance fixtures;
- expected runtime snapshots;
- deep fail-closed snapshot drift audit;
- CLI behavior and exit-code contracts;
- evidence and future integration guidance.

### OUT OF SCOPE

- editing `goif74945-crypto/NEXY.AI-`;
- declaring this manifest authoritative for NEXY.AI;
- replacing DOC-B/DOC-C/DOC-D/DOC-E;
- automatically ingesting arbitrary source code and inferring authoritative contracts;
- deploying code;
- network services;
- Rust compilation in the current local environment, because `rustc`/`cargo` were not installed;
- proving production integration.

## Core pipeline

```text
manifest.json
  -> safety + schema validation
  -> semantic normalization
  -> semantic fingerprint
  -> deterministic compiler
       -> contract.generated.ts
       -> contract.generated.rs
       -> contract.snapshot.json
       -> contract.fixtures.json
       -> contract.normalized.json
       -> compile-evidence.json
  -> runtime snapshot audit
       -> PASS when byte-semantic structure matches
       -> FAIL + path-level diffs on drift
```

## CLI

```bash
node src/cli.mjs validate examples/vnext-product-state.contract.json
node src/cli.mjs compile examples/vnext-product-state.contract.json generated
node src/cli.mjs snapshot examples/vnext-product-state.contract.json
node src/cli.mjs audit examples/vnext-product-state.contract.json generated/contract.snapshot.json
npm test
```

Exit behavior:

- `0`: successful command / audit PASS;
- `1`: invalid manifest or operational validation failure;
- `2`: audit detected semantic/runtime drift;
- `64`: CLI usage error.

## Verification result

- Node test suite: **22/22 PASS**.
- Node syntax/static parse: **PASS**.
- Generated TypeScript strict compilation: **PASS**.
- Independent compile A/B artifact diff: **PASS, byte-identical**.
- Self-audit of emitted runtime snapshot: **PASS**.
- Injected actor-enum drift: **FAIL as required, exit code 2**, with path-level diffs.
- Coverage observation: **96.29% line / 81.05% branch / 97.96% functions** across the executed Node test command. No coverage threshold is claimed.
- Generated Rust compile: **NOT_VERIFIED**, because the current environment had no `rustc` or `cargo`.

See `evidence/VERIFICATION.md` for the exact evidence boundary and `docs/04_NEXY_COMPATIBILITY_OBSERVATIONS.md` for read-only NEXY source observations.
