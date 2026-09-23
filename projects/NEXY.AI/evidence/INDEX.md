# NEXY.AI Evidence Registry

Canonical:
- `evidence-ledger.jsonl`
- `evidence.schema.json`
- `validation-report.md`
- `checkpoints/doc-e-current.jsonl`

Key separation:
- `artifact_declared_result` = what the evidence file says.
- `verifier_result` = what can safely be concluded for the observed current HEAD.
- `freshness` = whether the artifact proves the same revision.

A stale PASS is not a current PASS.
