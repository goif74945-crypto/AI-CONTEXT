# NEXY.AI Failure / Recovery Library

Canonical:
- `failures.jsonl`
- `failure.schema.json`
- `validation-report.md`

Before repair, AI should query this library by:
- symptom/error code;
- affected systems;
- current state;
- attempted recovery;
- historical blocker.

Each record preserves:
`context → symptom → root cause → failed approach → why failed → successful recovery → regression → prevention`.

Designed failure modes and actually observed failures are separate kinds.
