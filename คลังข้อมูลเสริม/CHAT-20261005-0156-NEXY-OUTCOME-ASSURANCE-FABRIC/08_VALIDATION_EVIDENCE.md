# Validation Evidence

Status at this document revision: `LOCAL_VERIFICATION_PASS / REPOSITORY_PERSISTENCE_PENDING`

## Evidence classes

### E1 — static
- `PYTHONPATH=src python -m compileall -q src tests tools` -> PASS.
- AST import audit across 12 `src/nexy_outcome/*.py` files -> PASS, zero banned import findings.
- both JSON schema documents parsed with `python -m json.tool` -> PASS.

Artifacts:
- `evidence/static-check-output.txt`
- `evidence/source-static-audit.json`
- `evidence/schema-check-output.txt`

### E2 — unit/adversarial/property
Final executed command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Observed final result: **45 tests, OK**, including:
- strict contract validation;
- missing/invalid observation FREEZE;
- hard/forbidden outcome failures;
- soft partial outcomes;
- exact Pareto tradeoffs;
- benefit-regression anti-gaming;
- exact bounded recovery planning;
- NaN/Infinity and non-JSON adversarial inputs;
- 100 deterministic verifier replays.

Artifact: `evidence/final-test-output.txt`.

### E3 — integration
Executed test suite includes:
- one composed five-engine pipeline test;
- CLI compile + verify;
- CLI frontier;
- CLI regression;
- CLI recovery;
- malformed/unknown CLI operation fail-closed behavior.

Representative deterministic outputs are stored in `evidence/representative-output.json`.

### Performance observation
`tools/benchmark.py` was executed in the local sandbox. Raw result is `evidence/benchmark.json`. Timings are informational only and are not a production SLA.

### Failure/repair evidence
`09_FAILURE_REPAIR_LEDGER.md` records two observed failure cycles and exact correction class:
1. invalid Pareto test oracle;
2. non-finite observation serialization defect.

## E0 — repository presence/read-back
Pending at this document revision. Completion requires persisted source/test bytes to be compared with local tested content; do not use this pre-persistence revision as proof of repository identity.
