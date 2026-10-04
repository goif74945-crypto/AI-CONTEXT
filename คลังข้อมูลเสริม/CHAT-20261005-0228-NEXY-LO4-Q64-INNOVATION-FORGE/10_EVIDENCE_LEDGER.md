# Evidence Ledger

| Evidence | Class | Target | Result | Artifact |
|---|---|---|---|---|
| Static runtime/syntax record | E1 | authored JS/MJS files | PASS | `evidence/static-runtime.txt` |
| Static Lo4 policy scan + Node tests | E1/E2 | 20 modules + test suite | PASS 107/107 | `evidence/test-all.txt` |
| Independent numeric oracle | E1/E2 | Q64 raw vector equivalence | PASS 16/16 | `evidence/q64-oracle.txt` |
| Replay stress | E2/E3-local | all 20 sample concepts | PASS 10,000 executions | `evidence/replay-stress.txt` |
| Benchmark workload | observation | all 20 sample concepts | PASS 20,000 evaluations | `evidence/benchmark.txt` |
| CLI smoke | E3-local | C20 fixture through CLI | PASS | `evidence/smoke-output.json` |
| Regression lineage | failure evidence | stale post-C20 test syntax | FAIL then repaired | `evidence/iteration-01-failure.txt` |

## Evidence integrity rule
Evidence generated before a semantic source change is stale for the changed source. That rule was applied during C20 replacement: the earlier all-green run was discarded as final proof and the complete stack was rerun.
