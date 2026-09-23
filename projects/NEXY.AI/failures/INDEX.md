# NEXY.AI Failure / Recovery Intelligence Library

Normalized engineering experience for reuse before debugging/repair.

## Stats
- records: **24**
- resolved/recovery examples: **17**
- active/blocking findings: **7**

## Search rule
Before changing a subsystem, search `failure-library.jsonl` by:
- affected_systems
- failure_id
- root_cause
- failed_approach
- reusable_rule

## Historical proof rule
Historical PASS remains proof for its historical commit only. It contributes a recovery pattern, not current-HEAD status.

## Streaming provenance
`checkpoints/` preserves normalization batches so this library can be rebuilt without depending on one context window.
