# Verification Report

Status: PASS for the standalone prototype verification scope. Production/NEXY integration: NOT_VERIFIED.

## Failure-and-recovery evidence
The first direct benchmark execution failed with `ModuleNotFoundError: shadowguard` because Python placed `benchmarks/` rather than the project root on the import path. The smallest correction added the project root to `sys.path` inside the benchmark harness only. The full verification sequence was then rerun.

## E1 static evidence
`python -m compileall -q shadowguard tests benchmarks` completed successfully after the harness fix.

## E2 unit/property evidence
Executed unittest suite: 24 tests, all PASS. Coverage includes positive/negative behavior, all 3x3 stable/candidate outcome pairs, E0-E7 evidence-class cases, authority truncations, fail-closed mutation catalog, JSONL error handling, duplicate/nondeterminism behavior, and a 1,000-case identity corpus.

## CLI fixture evidence
- PASS fixture: exit 0, status `PASS`, findings `{'MATCH': 2}`.
- Deliberately unsafe fixture: exit 1, status `FAIL`, findings `{'ACTION_DIVERGENCE': 1, 'AUTHORITY_REGRESSION': 1, 'EVIDENCE_PROFILE_DOWNGRADE': 1, 'FREEZE_BYPASS': 1, 'SAFETY_LABEL_REGRESSION': 2}`.

## Capacity smoke benchmark
Local 10,000-case comparison: status `PASS`, 10000 compared in 0.152233 seconds, approximately 65688.82 cases/sec in this container. This is a smoke benchmark, not a production SLO.

## Evidence limitations
No browser, network, external provider, NEXY runtime, production deployment or exhaustive 837-row NEXY integration validation was run. No claim beyond this standalone prototype is authorized.
