# Lo4 EOSF — Role Court Audit

Classification: `AI-PROPOSED / EXPERIMENTAL / NOT CANON / STANDALONE REFERENCE IMPLEMENTATION`.

## Builder
EOSF addresses a concrete DOC-C boundary: mutating routes need idempotency, automatic retry is disallowed by default, failed jobs retry only when explicitly safe, and FREEZE/STOP cancel work. The five systems add deterministic proof machinery around effect identity, retry amplification, lease fencing, outbox emission, and cancellation closure.

## Adversary
A local library cannot guarantee universal exactly-once behavior in an open distributed system. External providers can acknowledge ambiguously, storage can be non-transactional, clocks/leases can drift, and compensation can fail. Therefore EOSF must freeze rather than claim exactly-once when durable commit-point facts are unavailable.

## Security reviewer
Critical identity/equality must not depend on the prototype FNV-64 telemetry digest. Final implementation uses exact canonical structural seals for effect identity and outbox payload equality. No module performs network/filesystem/subprocess execution. Capability to emit/commit remains outside this lab.

## Reliability reviewer
The important split-brain case is an old worker attempting commit after a newer lease exists. LFCG rejects stale/future fences and expired/revoked leases. Retry topology is bounded before execution, and cancellation requires compensation for every declared materialized external effect regardless of terminal job label.

## Evidence judge
Evidence supports only the standalone reference implementation:
- E1: strict TypeScript typecheck/build.
- E2: unit/negative/property/stress checks.
- E3-local: integration of the five modules in one deterministic decision surface.
It does not establish live NEXY integration, provider exactly-once delivery, deployment safety, or production security.

## Integrator
Promotion requires a NEXY-owned adapter, durable transactional backing stores, exact-head integration tests, provider-specific ambiguity handling, real cancellation/compensation tests, fault injection, observability, and formal Canon promotion. Until then EOSF remains advisory/non-governing.

## Court verdict
`ELIGIBLE_FOR_ARCHITECT_REVIEW`, not `CANON`, not production-ready. The reference implementation is useful because it converts several failure classes into explicit deterministic FREEZE/SUPPRESS/READY outcomes while refusing to invent durable state.
