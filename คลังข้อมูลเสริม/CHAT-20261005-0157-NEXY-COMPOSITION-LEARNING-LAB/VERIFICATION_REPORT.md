# Verification Report

> **Scope:** standalone auxiliary lab only. This report does not prove NEXY.AI runtime behavior or production integration.

## Evidence classes
- E0: local artifact presence; GitHub E0/read-back is pending until persistence gate.
- E1: Python bytecode compilation + architecture import-boundary tests.
- E2: executed unit, negative, property/adversarial, CLI subprocess, and cross-concept tests.
- E3-E7: not claimed.

## Test evolution
1. Initial implementation: 36/36 PASS.
2. Added property/adversarial suite: 40 PASS / 1 FAIL; test-harness root cause repaired.
3. Re-run: 41/41 PASS.
4. Added ten hardening tests: 10/10 RED before implementation hardening.
5. Hardened implementation; caught and repaired one recursive-helper regression.
6. Full regression exposed one stale property expectation after stronger C3 policy coverage rule; test input corrected without weakening production rule.
7. Full suite: 51/51 PASS.
8. Added fail-closed CLI behavior: full suite 53/53 PASS.
9. Added architecture dependency-boundary tests: focused 2/2 PASS.
10. After C1/C4 optimization and all hardening, fresh final regression: **55/55 PASS**.
11. `python -m compileall -q src tests benchmarks`: exit 0.
12. Five CLI examples were each repeated in three independent Python subprocesses; stdout and exit code were stable for all 5/5 commands. Raw hashes are in `evidence/determinism.json`.

## Final local verification gate
- Full tests: PASS, 55/55.
- Compileall: PASS, exit 0.
- Cross-process determinism sample: PASS for 5/5 example commands × 3 runs each.
- Exact receipt: `evidence/final-tests.log`.

## CLI evidence
`evidence/cli_examples.log` records actual subprocess outputs for all five systems. Expected gate behavior was observed:
- C1 PASS => exit 0.
- C2 emergent risk => FREEZE, exit 2.
- C3 REVERIFY => exit 2, intentionally blocking.
- C4 compiled bounded correction => PASS, exit 0.
- C5 minimal risk reproducer => PASS, exit 0.

## Benchmark evidence
See `BENCHMARK_REPORT.md` and raw `evidence/benchmark.json`. No production performance claim is made.
