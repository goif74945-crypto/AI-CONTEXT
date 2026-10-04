# NCAF Reference Lab

`NEXY Companion Adaptive Fabric` is an **AI-proposed, not-adopted** set of five deterministic companion concepts created for future evaluation alongside NEXY.AI.

## Contents
- `00_SESSION_MEMORY.md` durable resume state.
- `01_TASK_CONTRACT.md` scope, invariants, acceptance criteria.
- `02_MASTER_DESIGN.md` five concept designs.
- `03_NEXY_COMPATIBILITY_AUDIT.md` read-only compatibility findings and prohibitions.
- `src/ncaf/` executable Python reference implementation.
- `tests/` focused and randomized invariant tests.
- `evidence/TEST_EVIDENCE.md` executed proof record.

## Run
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src tests
```

## Authority
This folder cannot authorize NEXY.AI behavior. It is a lab artifact stored in AI-CONTEXT for comparison, future design review, and possible later adapter work under an explicit authoritative specification.
