# Validation Evidence

Status: `E0/E1/E2/E3 PASS FOR REFERENCE ARTIFACTS / NOT PRODUCTION OR NEXY DEPLOYMENT EVIDENCE`

## E1 — static
- `PYTHONPATH=src python -m compileall -q src tests tools` -> PASS.
- AST import audit across 12 `src/nexy_outcome/*.py` files -> PASS, zero banned import findings.
- both JSON schema documents parsed with `python -m json.tool` -> PASS.

Artifacts: `evidence/static-check-output.txt`, `evidence/source-static-audit.json`, `evidence/schema-check-output.txt`.

## E2 — unit/adversarial/property
Executed command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Observed final result: **45 tests, OK**. Coverage includes strict contract validation; missing/invalid observation FREEZE; hard/forbidden failure; soft PARTIAL; exact Pareto tradeoffs; benefit-regression anti-gaming; exact bounded recovery; NaN/Infinity/non-JSON adversarial inputs; and 100 deterministic verifier replays.

Artifact: `evidence/final-test-output.txt`.

## E3 — integration
The executed suite includes a composed five-engine pipeline and CLI coverage for compile, verify, frontier, regression, recovery, plus malformed/unknown-operation fail-closed behavior. Representative output: `evidence/representative-output.json`.

## Performance observation
`tools/benchmark.py` was executed in the local sandbox. Raw result is `evidence/benchmark.json`. Timings are informational only, not a production SLA.

## Failure/repair evidence
`09_FAILURE_REPAIR_LEDGER.md` records:
1. an incorrect Pareto test oracle fixed without weakening engine semantics;
2. a real non-finite observation serialization defect fixed at the root and regression-tested.

## E0 — repository presence and exact persisted identity
A recursive Git tree read-back of `goif74945-crypto/AI-CONTEXT/main` at observed HEAD `9b968218f83cc86abdda44002a5e64f00a9975ed` found:
- expected mission files: 56;
- observed mission files: 56;
- missing: 0;
- blob mismatches: 0;
- extras: 0.

`evidence/persistence-proof.json` records this checkpoint. Tested source/test identities are separately recorded in `TESTED_CONTENT_SHA256.txt`.

## Evidence boundary
These results prove the standalone reference artifact in its test environment. They do not prove NEXY.AI implementation, production deployment, target-runtime performance, cryptographic trust, or live observation provenance.
