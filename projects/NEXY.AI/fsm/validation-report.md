# FSM Registry Validation

## Result
**PASS — namespace/source/implementation structural registry**

- source ontology FSMs: **8**
- implementation-only observed state models: **1**
- total registry records: **9**

Checks:
- FSM namespaces remain separate: PASS
- source state entities resolve to their owning FSM: PASS
- current DOC-C Execution FSM includes observed event ownership/transition table: PASS
- Risk/Intelligence FSM is kept separate from Execution FSM: PASS
- PipelineRun implementation state model is not promoted into source canon: PASS
- partial/unknown transition tables are explicitly marked: PASS

## Review points
- Capability Registry source FSM includes `QUORUM_SIGNED` and `ACTIVE`; observed `ncf-registry.ts` status union currently omits both and includes `DEPRECATED`. This is **REVIEW_REQUIRED**, not silently reconciled.
- App Lifecycle source contains FROZEN/TERMINATED/ARCHIVED states but current extracted transition table is incomplete.
- Queue Job source state set is known, but full event/guard transition table is not inferred from BullMQ behavior.
