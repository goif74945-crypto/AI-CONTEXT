# NEXY.AI State Machine Registry

Canonical:
- `fsms.jsonl`
- `fsm.schema.json`
- `execution.json`
- `queue-job.json`
- `constitutional.json`
- `app-lifecycle.json`
- `creator-publication.json`
- `capability-registry.json`
- `anchor-publication.json`
- `risk-intelligence.json`
- `cross-shard-transfer.json`
- `implementation-pipeline-run.json`
- `validation-report.md`

Every transition record has:
`FROM / EVENT / GUARD / ACTION / TO / FAILURE / AUDIT_EVENT`.

When the source does not name an event/guard/action, the field remains explicit `null` or `UNSPECIFIED_BY_SOURCE`; it is never invented.

## Namespace rule
Never merge state labels merely because the names look similar. `FREEZE`, `ACTIVE`, `FINALIZED`, etc. belong to their specific FSM namespace.
