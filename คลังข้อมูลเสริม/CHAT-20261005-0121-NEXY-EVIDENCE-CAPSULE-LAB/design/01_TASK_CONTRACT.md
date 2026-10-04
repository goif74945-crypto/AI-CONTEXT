# Task Contract — NEXY Evidence Capsule & Selective Disclosure Lab

## Status
AI-PROPOSED / REFERENCE LAB / NOT NEXY RUNTIME

## Objective
Design and prove a standalone reference mechanism that lets a NEXY-like system disclose only authorized evidence fields while preserving integrity, provenance binding, freshness, audience binding, and replay resistance.

## Authority
This lab is subordinate to the canonical AI-CONTEXT execution/security/verification rules and NEXY project authority. It does not amend DOC-B, DOC-C, the 837-row normalized matrix, or any NEXY implementation repository.

## Authorized scope
Only this supplemental folder inside `goif74945-crypto/AI-CONTEXT`.

## Protected scope
- every repository whose name contains `NEXY.AI`;
- existing canonical NEXY law/spec/context;
- repository settings/workflows/issues/PRs;
- credentials, tokens, private keys and production secrets.

## Success invariants
1. Original evidence/audit lineage is never rewritten by redaction.
2. A disclosed field must verify against the committed record root.
3. Undisclosed field values are not included in the presentation.
4. Unauthorized role/field combinations fail closed.
5. Header and presentation tampering are detected.
6. Audience mismatch is rejected.
7. Expired/stale presentations are rejected.
8. Replayed presentations can be rejected with a replay store.
9. Deterministic inputs with fixed salts/nonces produce deterministic capsule IDs.
10. Reference cryptography is clearly labeled non-production.

## Required evidence
- E0: committed artifacts are re-fetchable.
- E1: Python source compiles and committed Git blob identity matches tested local bytes.
- E2: executable unit/adversarial tests pass against those exact bytes.
- No E3-E6 claim is permitted without future integration/runtime/deployment evidence.

## Stop conditions
Freeze work if any mutation would cross protected scope, if source authority conflicts materially, or if exact tested bytes cannot be proven.