# NEXY Lo4 Exactly-Once Effect Safety Fabric (EOSF)

**Mission:** `CHAT-20261005-0222-NEXY-LO4-EOSF-NX5A`  
**Authority:** AI-proposed Lo4 only. **Not Canon. Not current NEXY implementation. Not production proof.**

EOSF is a standalone TypeScript reference package for protecting autonomous external side effects from duplicate execution, retry amplification, stale workers, outbox inconsistency, and incomplete cancellation.

It exists because current NEXY design already requires idempotency keys, fail-closed retry behavior, queue cancellation on FREEZE/STOP, payload revalidation and deterministic queue states. EOSF explores a deeper proof layer around those laws without changing NEXY itself.

## Five systems

| # | System | Core question |
|---|---|---|
| 1 | ISC — Idempotency Scope Compiler | Does the mutation identity bind every semantic dimension required to prevent key aliasing? |
| 2 | RAB — Retry Amplification Bounder | What is the exact bounded worst-case external-effect attempt count, and is every retry explicitly safe? |
| 3 | LFCG — Lease Fencing Commit Gate | Can a stale or wrong worker commit after lease reacquisition? |
| 4 | OES — Outbox Effect Seal | Is an effect PREPARED/COMMITTED/EMITTED exactly once under replay, and do registry/outbox states agree? |
| 5 | CCC — Cancellation Closure Certifier | Does FREEZE/STOP cancel the whole affected subtree and account for every already-materialized effect? |

## Integration flow

`Mutation -> ISC -> RAB -> LFCG -> OES -> CCC -> READY | SUPPRESS_REPLAY | FREEZE`

No module executes a network request, writes a database, sends an email, commits a repository, or mutates an external system. It only evaluates explicit data contracts.

## Local verified evidence
- TypeScript strict typecheck: PASS.
- 42/42 unit, negative, integration and property tests: PASS.
- Coverage: 99.23% lines / 86.64% branches / 100% functions.
- Stress campaign: 55,000 checks PASS.
- Determinism probe: byte-identical across two separate Node processes.
- Static executable-source I/O token audit: PASS.

See `evidence/` and each `concepts/*/EVIDENCE.md`.

## Critical truth boundary
The word **exactly-once** here means the reference protocol can express and test the invariants required for exactly-once *effect safety*. It does **not** magically create distributed exactly-once semantics. A real promotion would still require transactional persistence, uniqueness constraints, durable fencing, crash recovery, provider-specific idempotency behavior, and E3–E6 NEXY evidence.
