# NEXY.AI FSM Registry

Canonical:
- `fsm-registry.jsonl` — all source FSMs plus explicitly labeled implementation-only state models.
- `execution.json`
- `constitutional.json`
- `app-lifecycle.json`
- `creator-publication.json`
- `anchor-publication.json`
- `capability-registry.json`
- `queue-job.json`
- `risk-intelligence.json`
- `pipeline-run.observed.json`
- `validation-report.md`

## Absolute rule
**Never merge FSM namespaces because state names look similar.**

A valid transition is identified by:
`FSM namespace + FROM + EVENT + GUARD + ACTION + TO + FAILURE/AUDIT semantics`.

Implementation-only state models remain explicitly non-canonical until a governing source promotes them.
