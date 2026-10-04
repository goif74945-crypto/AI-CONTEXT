# Local Verification Report

Date: 2026-10-05 (+07:00)
Environment observed during local execution:
- Python `3.13.5`
- Linux `6.18.44 x86_64`
- Node `v22.16.0`
- TypeScript compiler `5.8.3`
- npm `10.9.2`

## E1 — Python syntax/static compilation

Command:
```text
python -m compileall -q lo4lab tests
```
Result: PASS.

## E2 — Python unit + deterministic fuzz/regression

Command:
```text
PYTHONPATH=. python -m unittest discover -s tests -v
```
Final result: `Ran 33 tests ... OK`.

Coverage includes malformed input, duplicate IDs, unsafe answering, fragile margins, strict-boundary violations, four-valued algebra identities, cycle detection, missing parents, dominance, unverified influence, contract scope expansion, invariant/evidence weakening, unknown-evidence freeze and deterministic randomized invariant checks.

## E1/E2 — TypeScript

Commands:
```text
cd typescript
npm run build
npm test
```
Results:
- strict `tsc` build: PASS;
- Node test runner: 6/6 PASS.

## E3 — Cross-module release composition

Python integration tests verify:
- all five gates permit only `RELEASE_CANDIDATE` when all local conditions pass;
- UNKNOWN evidence freezes;
- contract assumption drift freezes.

Status: PASS for local reference composition.

## E3 — Python/TypeScript representative parity

Initial parity verifier result: **FAIL** because raw JSON string comparison treated Python `0.0` and JavaScript `0` as different strings.

Root cause: verifier compared serialization text rather than parsed JSON numeric semantics.

Correction: parse both outputs as JSON and compare semantic values.

Re-run command:
```text
python interop/compare.py
```
Final result:
```text
PARITY PASS
{"aurora":{"status":"PASS","unsafe_answer_rate":0.0},"contract_drift":{"status":"FREEZE","total_cost":8},"margin":{"minimum_margin":0.09,"release_status":"RELEASE"},"traceweight":{"dominance_ratio":0.5,"dominant_source":"a","status":"PASS"},"upa":{"releaseable":false,"state":"CONFLICT"}}
```

## Local microbenchmark
See `BENCHMARK_LOCAL.txt`. This is descriptive sandbox evidence only, not an SLA or production performance claim.

## Evidence limitations
No test in this folder proves integration with the actual NEXY repository, production runtime, deployment environment, real provider behavior, security hardening or canonical promotion.
