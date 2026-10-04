# AI Proposal: NEXY Deterministic Interchange Kernel

## Classification
`AI_PROPOSAL / EXPERIMENTAL / NON-CANONICAL`

This document proposes a future integration primitive. It does not amend NEXY law, DOC-C, DOC-D, the current build matrix, or the NEXY.AI implementation.

## Problem
A deterministic control system can still lose determinism at interchange boundaries. Common causes include object insertion order, duplicate JSON keys, Unicode normalization variants, binary floating-point differences, unsafe integers crossing JavaScript boundaries, implicit timestamps, environment-derived fields, and oversized/cyclic inputs.

If identities, evidence references, idempotency keys, replay checks, or cache keys are computed from unstable bytes, higher-level verification can become internally inconsistent even when its reasoning is correct.

## Proposal
Introduce a small deterministic interchange kernel with four responsibilities:

1. validate a deliberately narrow data model;
2. normalize the accepted model deterministically;
3. serialize to a unique UTF-8 text representation;
4. derive domain-separated SHA-256 fingerprints and deterministic envelopes.

## Why it is useful to NEXY
Potential future consumers include:

- evidence object identity;
- Vault deduplication and immutable references;
- replay/capsule identity;
- idempotency keys for critical writes;
- provider/tool request fingerprints;
- deterministic cache keys;
- cross-model/cross-runtime comparison artifacts;
- audit references that survive irrelevant key-order changes.

## Safety posture
NDIK intentionally fails closed. It rejects values that are easy to interpret differently across runtimes instead of guessing a representation.

## Adoption condition
Do not integrate merely because this prototype passes its own tests. A future adoption task should first define a canonical cross-language specification and produce Python/TypeScript conformance vectors against the exact target runtime.
