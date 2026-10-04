# Validation Report

## Environment
Local isolated Python runtime available to this session. No NEXY.AI repository was modified or executed.

## E1 static
- `python -m compileall -q src` -> PASS.
- AST boundary scan across production package -> 0 forbidden network/subprocess/eval/exec/open calls -> PASS.

## E2 unit/negative/regression
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- observed: **55 tests, 55 PASS**.
- includes malformed data, duplicate IDs/sequences, quiet-mode critical override, unknown delta, redaction, future/unknown acknowledgement, deterministic order.

## Coverage
Coverage.py branch run recorded **99% total** across source + tests. Production modules are 97-100% line/branch combined report coverage; uncovered lines are defensive/unreachable representation helpers/assertion guard, not hidden untested execution claims.

## E3 CLI integration
Subprocess CLI tests execute all five commands: `classify`, `route`, `compress`, `delta`, `debt`. Invalid input returns machine-readable `FREEZE` with exit code 2.

## Determinism
10,000 repetitions of the same critical routing input produced one unique canonical output -> PASS for that tested deterministic path.

## Repair/re-test record
First green suite was not accepted as final. Audit found and corrected:
1. trailing collapsed-event accounting semantics;
2. root JSON-pointer redaction behavior.
Full suite was rerun after both corrections.

## Evidence files
- `evidence/unit-test-output.txt`
- `evidence/coverage.txt`
- `evidence/static-compile.txt`
- `evidence/security-static-check.txt`
- `evidence/determinism-check.txt`
- `evidence/example-classify.json`
- `evidence/example-delta.json`
- `evidence/example-debt.json`
- `evidence/SHA256SUMS.txt`

## Unverified
NEXY production integration, UI delivery behavior, persisted acknowledgement storage, distributed ordering, load/fault recovery, and deployment are NOT_VERIFIED.
