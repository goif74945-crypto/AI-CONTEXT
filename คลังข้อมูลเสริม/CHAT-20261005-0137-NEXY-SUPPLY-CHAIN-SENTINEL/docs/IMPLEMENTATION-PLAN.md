# NEXY Supply-Chain Sentinel Implementation Plan

> For agentic workers: use test-driven development. Steps are ordered so each behavior is proven before production implementation.

**Goal:** Build a deterministic, fail-closed dependency drift sentinel usable as a future NEXY.AI sidecar without modifying NEXY.AI.

**Architecture:** Standard-library Python package. Parsers create normalized package records; canonical hashing seals snapshots; diffing classifies drift; policy maps evidence/drift to `ALLOW` or `FREEZE`; CLI exposes snapshot/diff/verify.

**Tech Stack:** Python 3.11+ standard library, `unittest`, JSON, SHA-256.

**Spec:** `docs/DESIGN.md`

## Global constraints
- No network access.
- No third-party runtime dependencies.
- Unknown/unsupported state freezes.
- Stable JSON and sorting for deterministic output.
- Additive-only storage in AI-CONTEXT.

## Tasks
1. Write failing tests for canonical hashes, npm parsing, Python requirements parsing and strict policy.
2. Implement model/canonical/parser/policy primitives until focused tests pass.
3. Write failing tests for snapshot tamper detection and drift classification.
4. Implement snapshot/diff/verification engine until tests pass.
5. Write failing CLI behavior tests.
6. Implement CLI and module entrypoint.
7. Run full regression suite and `compileall`.
8. Capture evidence and upload exact tested files.
9. Re-read uploaded paths from GitHub and record final state.
