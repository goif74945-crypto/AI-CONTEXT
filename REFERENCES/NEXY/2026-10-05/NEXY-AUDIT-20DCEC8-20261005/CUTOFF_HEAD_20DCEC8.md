# NEXY.AI Read-Only Audit Cutoff — 2026-10-05

## Cutoff identity
- Repository: `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Audit cutoff HEAD: `20dcec8ece81264a193dd17cb442acd2d70a5e18`
- Audit cutoff tree: `2fa314be2b204e2729f6c18c228dea9e13219099`
- Commit: `fix(queue): require TSA time for stale TTL`
- Canonical design SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- CHAT_ID: `NEXY-AUDIT-20DCEC8-20261005`
- Repository mutation by this audit: **NONE**

## Verdict
`PARTIAL / VOLATILE_HEAD / TEST_INFRA_BLOCKED / CLOCK_AUTHORITY_FROZEN / RELEASE_NOT_PROVEN`

## Proven static observations
1. Core logical ticks and TSA elapsed-time authority are separated.
2. LO2 federation, resilience I/O, and queue stale-TTL paths use TSA time or fail closed.
3. Queue cutoff patch removes Date.now() from authoritative stale-TTL decisions and makes packages/queue a blocking determinism-scan root.
4. Phase-F remains experimental/advisory rather than silently promoted into current DOC-C release authority.
5. Several historical MISSING/PARTIAL audit rows now have static evidence, including Global Anchor, 2-of-3 TSA, anchor FSM, dual-signed PermissionGrant, creator public modes, constitutional economy components, Python L1o, and Safety MCU source.
6. Static source cannot prove physical Safety MCU independence or actual hardware kill wiring.

## Exact-head CI evidence
At cutoff, the relevant GitHub Actions runs failed before executable step evidence:
- 37222514525 — NEXY CI / Deploy Gate
- 37222514541 — Exact HEAD test evidence
- 37222514494 — Six-system exact HEAD evidence
- 37222514553 — Layer8 Cargo lock evidence
- 37222514528 — NEXY DOC-E E7 Queue and Rollback

Inspected runnable jobs expose `runner_id=0`, empty runner name, and `steps=[]`. Classification: `TEST_INFRA_BLOCKED`, not source test failure.

## Unresolved blockers
- CLOCK AUTHORITY SCOPE: Core TSA-only wording vs later G19 invariant-TSC wording.
- PRODUCTION TSA INJECTION: no production caller proven in the audited evidence window.
- EXECUTION INFRASTRUCTURE: no exact-head executable test/build evidence.
- VOLATILE HEAD: later commits require a new delta.
- AUDIT MATRIX REBASE: old 301-row matrix is stale and must not be reused for a current completion percentage.

## After-cutoff note
`f544cf263e96c54a330e86d8253040b92e361261` adds TSA injection only in `tests/integration/lo2-runtime-coordinator.spec.ts`; classification remains TEST_FIX / NO_PRODUCTION_INJECTOR_PROOF.
