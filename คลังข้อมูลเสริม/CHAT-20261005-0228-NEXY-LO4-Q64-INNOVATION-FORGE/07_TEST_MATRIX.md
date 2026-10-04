# Verification Matrix

| Gate | Evidence class | Mechanism | Final result |
|---|---|---|---|
| JavaScript syntax | E1 | `node --check` over `src`, `scripts`, `tests`, `bench` | PASS |
| Lo4 marker/count | E1 | `scripts/static-check.mjs` | PASS: exactly 20 modules |
| Forbidden float/network/eval patterns | E1 | static regex scan of concept modules | PASS |
| Q64 core arithmetic/boundaries | E2 | `tests/q64.test.js` | PASS |
| 20 concept happy/fail paths | E2 | `tests/concepts.test.js` | PASS |
| Deterministic and structural invariants | E2 | `tests/invariants.test.js` | PASS |
| Adversarial inputs | E2 | `tests/adversarial.test.js` | PASS |
| CLI behavior/exit semantics | E3-local | `tests/cli.test.js` + smoke | PASS |
| Cross-concept chain | E3-local | `tests/integration-chain.test.js` | PASS |
| Independent Q64 implementation oracle | E1/E2 cross-check | Python Fraction/Decimal, 16 vectors | PASS 16/16 |
| Repeated deterministic replay | E2/E3-local | 500 cycles × 20 concepts | PASS 10,000 executions |
| Workload execution | observational | 1,000 cycles × 20 concepts | PASS 20,000 evaluations |

## Node suite total
Final `npm run test:all`: **107 tests, 107 passed, 0 failed, 0 skipped**.

## Regression lineage
A post-refactor run failed at parser stage because stale C20 assertions remained in `tests/integration-chain.test.js`. The repair removed only obsolete test lines; then the complete matrix was rerun. The failure is preserved in `evidence/iteration-01-failure.txt`.

## Evidence boundary
The matrix proves the standalone authored project under the observed local runtimes. It does not prove NEXY.AI integration, production performance, deployment, external model behavior, or physical safety.
