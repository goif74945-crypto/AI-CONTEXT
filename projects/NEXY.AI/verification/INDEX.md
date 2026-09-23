# NEXY.AI Verification Registry

Canonical:
- `test-index.jsonl` — 108 indexed test files at pinned implementation HEAD.
- `requirement-test-matrix.jsonl` — requirement → mapped tests.
- `validation-report.md`
- `checkpoints/` — streaming test extraction.

Statuses:
- `EXPLICIT` = mapping is directly implied by test/domain naming and requirement class.
- `CANDIDATE` = useful likely test relation; inspect before relying on it.
- `NONE` = no test safely mapped yet.

Test existence never implies execution or PASS.
