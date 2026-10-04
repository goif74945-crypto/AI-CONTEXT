# LEDGER
LEDGER_ID: NEXY-BUILD-01-CORE-20261004
TASK_ID: NEXY-BUILD-01-CORE-20261004
CHAT_ID: NEXY-BUILD-01-CORE
HEAD: cde969ea2d16626a60ad5571e9308ea294289d15
TREE: a6ff8287e3f8aea0dbc674b7dc1ff4f271f3cfb1
DESIGN_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
STATUS: PARTIAL
AUDIT_COVERAGE: PROVISIONAL

| REQ_ID | SYSTEM_ID | SOURCE | SOURCE_LOCATOR | CODE_PATH / SYMBOL | EVIDENCE | STATUS | RISK / NOTE |
|---|---|---|---|---|---|---|---|
| CORE-01-OWNER-001 | CORE-01 | P0 + Layer 9 | single authoritative executor | core-kernel/src/kernel/fsm_state.rs::FsmState | single-owner &mut mutation statically present | NOT_VERIFIED | exact-head test execution unavailable |
| CORE-02-FREEZE-001 | CORE-02 | DOC-B Freeze Law / P0 | unresolved contradiction => FREEZE | packages/law/freeze.ts::buildFreezeEnvelope | centralized transition call statically present | NOT_VERIFIED | runtime persistence proof blocked |
| CORE-03-FSM-001 | CORE-03 | DOC-C canonical state baseline | INIT/READY/RUNNING/VERIFYING/CONSENSUS/STABLE/FREEZE/STOP | packages/core/vnext-state-matrix.ts | state list, ownership, guards and transition table present | NOT_VERIFIED | must execute transition/persistence tests |
| CORE-04-CLOCK-001 | CORE-04 | Layer 9 vs later G19 | clock authority | packages/core/tick.ts; core-kernel gatekeeper; nexy-daemon main | contradictory authority + host/scheduled clock implementations | CONFLICT | UNKNOWN_PRECEDENCE; mutation frozen |
| CORE-05-TERMINAL-001 | CORE-05 | DOC-C/P0 | FREEZE/STOP enforcement | packages/orch-core/system-state.ts; packages/law/freeze.ts | STOP cancellation and centralized FREEZE paths statically present | NOT_VERIFIED | DEGRADED is SystemStatus, not canonical DOC-C state |
| CORE-06-RECOVERY-001 | CORE-06 | Layer 10/P0 | restart/recovery/continue distinction | nexy-daemon/src/main.rs::probe_wal_replay boot flow | corruption/missing/unreadable paths fail closed | PARTIAL | explicit fresh-genesis/clean-reboot authorization path not located yet |
| CORE-07-REPLAY-001 | CORE-07 | Layer 9/10 | ordered replay + divergence integrity | core-kernel/src/storage/durable_integrity.rs::replay_wal_ordered | counter sequence, chain hash and checksum verification statically present | NOT_VERIFIED | exact-head runtime proof blocked |
| CORE-08-CONFIG-001 | CORE-08 | DOC-C runtime config governance | versioned durable config | packages/api/live-config.ts; packages/config/runtime-config.ts | version/hash/rollback mechanisms located | NOT_VERIFIED | targeted tests not executed |
| CORE-09-QUEUE-001 | CORE-09 | P0 Queue Law | QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELLED/EXPIRED | packages/queue/states.ts; workers.ts; retry-policy.ts | taxonomy and guarded retry located | PARTIAL | expiry decision uses BullMQ/Date.now wall-clock boundary; authority classification required |
| CORE-10-WAL-001 | CORE-10 | Layer 10 | WAL-first + integrity fields + ordered replay | core-kernel/src/storage/durable_integrity.rs | canonical WAL frame, checksum, counters, chain, fsync sink interface statically present | NOT_VERIFIED | runtime proof blocked |
| CORE-10-WAL-TAIL-002 | CORE-10 | Layer 10 | partial-tail recovery must not hide interior corruption | durable_integrity.rs::decode_wal_frames_recoverable_tail; daemon probe | only final crash tail recoverable; interior corruption hard-error statically present | NOT_VERIFIED | test execution unavailable |
| CORE-10-SNAPSHOT-003 | CORE-10 | Layer 10 | deterministic snapshot/restore | durable_integrity.rs::SnapshotStore | two-phase snapshot primitives + manifest integrity present | PARTIAL | daemon boot integration with SnapshotStore not located |
| CORE-10-SEGMENT-004 | CORE-10 | Layer 10 | fixed-size segmented WAL | durable_integrity.rs::segment_filename; shadow_wal.rs | filename helper exists, active daemon still uses single WAL_PATH | PARTIAL | end-to-end rollover/segment lifecycle not proven |

## Exact-head evidence state
GitHub Actions rerun attempt 2: BLOCKED_INFRASTRUCTURE.
No executed test step, log, or artifact is available from those attempt-2 jobs.

## Completion
COMPLETION_PERCENT: UNDEFINED
Reason: runtime evidence denominator is not valid at the exact HEAD.

## Next
1. Resolve CORE-04 precedence.
2. Restore executable exact-head runner evidence.
3. Continue source-to-test mapping for all CORE-01..CORE-10 rows.
4. Recheck HEAD before any source mutation.
