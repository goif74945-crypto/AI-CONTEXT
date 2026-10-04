# Verification Evidence

## Environment
- sandbox Python: 3.13.5
- dependency model: Python standard library only
- target: standalone package under `/mnt/data/nexy_five_forge` before AI-CONTEXT write-back
- NEXY.AI implementation repository: not modified and not used as a test target

## E1 Static evidence
Command:

```bash
python -m compileall -q .
```

Observed: PASS, no syntax/bytecode compilation error.

## E2 Unit/property evidence
Command:

```bash
python -m unittest discover -s tests -v
```

Observed after repair: **23 tests, 23 PASS, 0 FAIL**.

Covered negative paths include mandatory-context overflow, unknown dependencies, insufficient evidence class, budget failure, inconsistent recovery repairs, skill step drift, weak evidence, secret-like literals, and uncoverable mutation-blocking assumptions.

## E3 prototype integration evidence
`tests/test_integration_pipeline.py` executes a synthetic flow across all five modules:

`assumption burn-down -> tool evidence route -> context packing -> recovery recipe -> skill compilation`

Observed: PASS in sandbox.

This is E3 only for the standalone prototype components. It is **not** NEXY.AI integration evidence.

## Repeatability
The complete 23-test suite was executed 10 additional times with the same code. Observed: 10/10 PASS. See `REPEATABILITY_EVIDENCE.json`.

## Defect/fix evidence
Initial suite result: 16 PASS / 1 FAIL (17-test initial suite). Failure: Skill Compiler returned `step sequence drift detected` before reporting a secret-bearing trace. Root cause: secret scanning occurred after semantic step-consistency validation. Fix: move secret-safety gate before step-drift gate. Required suite rerun then passed; subsequent expanded suite reached 23/23 PASS.

## Microbenchmark evidence
See `BENCHMARK_EVIDENCE.json`. Three algorithmic hot paths were each invoked 2,000 times in the sandbox. This is local microbenchmark evidence only and must not be used as a production latency/SLO claim.

## Evidence boundary
- standalone design/code: VERIFIED at E1/E2, plus one synthetic E3 integration test;
- NEXY.AI adapter/integration: NOT_VERIFIED;
- web/API/DB integration: NOT_APPLICABLE to this prototype;
- deployment: NOT_VERIFIED;
- production scale/security: NOT_VERIFIED.
