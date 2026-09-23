# NEXY.AI State Machine Registry

## Rule
These FSMs are intentionally separate semantic machines. Identical state names in different FSMs do not imply one global state.

## Registered FSMs
- `constitutional.json` — Constitutional FSM — FUTURE_ARCHITECTURE — NOT_VERIFIED_RUNTIME
- `execution.json` — DOC-C Execution FSM — DOC_C_CURRENT_BUILD — IMPLEMENTATION_PRESENT_E0
- `app-lifecycle.json` — Application Lifecycle FSM — FUTURE_ARCHITECTURE — NOT_VERIFIED_RUNTIME
- `creator-publication.json` — Creator Publication FSM — FUTURE_ARCHITECTURE — NOT_VERIFIED_RUNTIME
- `capability-registry.json` — Capability Registry Admission FSM — FUTURE_ARCHITECTURE — NOT_VERIFIED_RUNTIME
- `queue-job.json` — Queue Job FSM — DOC_C_CURRENT_BUILD — IMPLEMENTATION_PRESENT_E0
- `risk-intelligence.json` — Risk / Intelligence State Model — CURRENT_ARCHITECTURE — NOT_VERIFIED_RUNTIME
- `cross-shard-transfer.json` — Cross-Shard Transfer Protocol FSM — FUTURE_ARCHITECTURE — NOT_VERIFIED_RUNTIME
- `anchor-publication.json` — Anchor Publication FSM — FUTURE_ARCHITECTURE — NOT_VERIFIED_RUNTIME

## Transition contract
Each transition records:
`FROM / EVENT / GUARD / ACTION / TO / FAILURE / AUDIT_EVENT`.

When the source names a sequence but not the event/guard, the registry uses `SOURCE_NOT_NAMED` rather than inventing semantics.

## Evidence boundary
Only DOC-C execution and queue mappings are bound to current implementation code at pinned HEAD `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`; presence is E0, not runtime PASS.
