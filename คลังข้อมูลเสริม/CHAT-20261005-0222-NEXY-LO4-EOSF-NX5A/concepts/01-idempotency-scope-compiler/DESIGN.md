# ISC — Idempotency Scope Compiler

**Classification:** Lo4 AI proposal / non-Canon.

## Problem
An idempotency key can exist and still be unsafe if its dedup scope fails to bind material semantics. Reusing `key-123` for a different project, authority epoch or payload can alias distinct mutations.

## Input
`MutationIdentity { route, actorId, projectId, authorityEpoch, payload, userKey }` plus `IdempotencyPolicy.scopeFields`.

## Required behavior
- route/project scope mandatory;
- optional policy can require payload and authority-epoch binding;
- critical identity uses exact canonical structural serialization, not a lossy hash;
- previous identity is classified as NEW, COMPLETED replay, IN_FLIGHT replay, RETRY_SAME, or alias conflict;
- duplicate registry rows fail closed.

## Output
Canonical `effectIdentity`, telemetry fingerprint, bound fields and replay classification.

## Forbidden behavior
- guessing missing scope fields;
- treating compact FNV fingerprint as authoritative equality;
- executing a completed replay;
- automatically retrying an in-flight duplicate.

## NEXY value
Strengthens DOC-C's idempotency-key requirement by making the semantic scope explicit and testable.
