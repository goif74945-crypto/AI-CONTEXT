# NEXY.AI Semantic Diff + Change Impact

Files:
- `semantic-diff-spec.json`
- `change-impact-index.jsonl`
- `validation-report.md`

Example query:

> If Queue idempotency changes, what requirements, invariants, dependents, failures, tests and evidence must be reviewed?

Use `change-impact-index.jsonl` for the graph expansion, then compare BEFORE/AFTER using `semantic-diff-spec.json`.

Git diff answers **what text changed**.
Semantic diff answers **what system meaning changed**.
