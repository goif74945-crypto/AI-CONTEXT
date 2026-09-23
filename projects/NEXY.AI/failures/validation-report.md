# Failure / Recovery Library Validation Report

## Result
**PASS — structural validation**

- records: **24**
- JSONL parse errors: **0**
- duplicate failure IDs: **0**
- records missing required fields: **0**

## Required fields checked
`failure_id, source_record, context, symptom, root_cause, failed_approach, why_failed, successful_recovery, affected_systems, regression_test, prevention, historical_status, proof, reusable_rule`

## Semantics
This validation proves the failure-intelligence records are structurally complete enough for AI lookup/reuse.

It does **not** make historical proof current. Every record remains bound to its source record/commit/evidence, and a recovery that worked historically must be reverified against the current target HEAD before it is treated as current PASS.

## Engineering use
Before modifying an affected subsystem:
1. search by `affected_systems`;
2. inspect prior root causes and failed approaches;
3. reuse prevention/regression obligations;
4. refresh current implementation/evidence;
5. never repeat an approach known to have failed without a new reason/evidence.
