# Failure Semantics

Classification: **AI_PROPOSED_REFERENCE**

| System | Condition | Output | Interpretation |
|---|---|---|---|
| Deadlock | wait graph acyclic | `CLEAR` | no structural wait cycle observed |
| Deadlock | SCC >1 or self-wait | `DEADLOCK` | structural blocking cycle observed |
| Deadlock | malformed edge/identity/type | exception / fail closed | topology cannot be trusted |
| Livelock | progress increases | `PROGRESSING` | current window shows declared progress |
| Livelock | no progress, no cycle | `STALLED` | inactivity/slowness, not proven thrash |
| Livelock | repeated multi-state suffix cycle, no progress | `LIVELOCK` | active oscillation without progress |
| Livelock | progress counter regresses | `FREEZE` | supplied progress history is inconsistent |
| Retry | non-retryable latest failure | `STOP_NON_RETRYABLE` | retry forbidden by explicit fact |
| Retry | non-idempotent latest failure | `STOP_NON_IDEMPOTENT` | cannot mint idempotency |
| Retry | prior illegal retry exists | `FREEZE_INVALID_HISTORY` | later metadata cannot launder invalid history |
| Retry | same-signature threshold reached | `QUARANTINE_STORM` | repeated retry would amplify identical failure |
| Retry | global attempt cap reached | `EXHAUSTED` | retry budget consumed |
| Retry | legal bounded case | `RETRY` | advisory retry with deterministic delay |
| Poison | repeated same input/revision/signature below threshold | `CLEAR` | not enough repeated evidence yet |
| Poison | threshold reached | `QUARANTINE` | isolate exact poison triple |
| Poison | revision/input/signature changes or latest pass | streak reset / `CLEAR` | do not carry stale poison identity forward |
| Salvage | node not PASS/verified/evidenced/identified/display-safe | exclude | never expose unproven partial result |
| Salvage | dependency excluded | exclude dependent | preserve dependency closure |
| Salvage | unknown dependency/cycle/duplicate identity | exception / fail closed | result graph contract invalid |
| Salvage | at least one safe dependency-closed node | `SALVAGE_READY` | safe partial payloads exist |
| Salvage | no node safe | `NOTHING_SAFE` | do not manufacture a partial answer |
| Salvage | every presented node safe | still `whole_task_complete=False` | presented graph is not authoritative task denominator |

## Recovery principle
The mesh separates **diagnosis** from **authority**. A deadlock/livelock/quarantine signal can justify a future NEXY-owned freeze/replan decision, but the reference library does not perform compensation, abort work, reschedule workers, mutate queues, release locks, or expose results directly.
