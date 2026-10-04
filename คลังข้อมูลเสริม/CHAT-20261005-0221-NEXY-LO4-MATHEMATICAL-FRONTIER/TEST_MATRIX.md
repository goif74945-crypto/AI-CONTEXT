# Test Matrix

| Gate | Method | Expected | Current result |
|---|---|---|---|
| TDD feature absence | pre-implementation unit invocation | not implemented | RED observed |
| Focused unit behavior | 5 concept unit modules | all pass | PASS |
| Minimal-cut oracle | deterministic random corpus vs brute-force transversal oracle | exact equality | PASS |
| Dominator oracle | computed dominators vs intersection of independently enumerated simple paths | exact equality | PASS |
| Liveness permutation | all permutations of cycle input | invariant output | PASS |
| Liveness scale regression | 1,500-node cycle | DEADLOCK without recursion failure | PASS |
| Symmetry permutation | all permutations of 3 interchangeable workers | one canonical key | PASS |
| JSON rejection | set / NaN payloads | reject | PASS |
| Tournament authority | eligible/rejected candidate sets | promotion always false | PASS |
| Tournament permutation | all permutations of candidate list | identical result | PASS |
| Static bytecode compilation | `python -m compileall -q lo4_frontier` | exit 0 | PASS |
| Stress observations | benchmark script | complete without exception | PASS after F-001 remediation |

Exact raw outputs are stored under `evidence/`.
