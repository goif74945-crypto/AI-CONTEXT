# Remediation History

## F-001 — Recursive liveness SCC crashed on large cycle

**Discovery method:** stress benchmark after unit/property suite.

**Observed failure:** a 1,000-node dependency cycle caused Python `RecursionError: maximum recursion depth exceeded` in the recursive SCC traversal.

**Root cause:** algorithmic control flow depended on Python call-stack depth. The logical graph operation was valid, but the implementation encoded traversal depth into host recursion depth.

**Repair:** replace recursive SCC traversal with deterministic iterative Kosaraju-style passes using explicit stacks.

**Regression proof:** add `LivenessScaleRegressionTests.test_large_cycle_does_not_depend_on_python_recursion_limit` with a 1,500-node cycle.

**Focused retest:** PASS, 5 liveness tests.

**Stress rerun:** PASS; 1,000-node cycle classified `DEADLOCK`.

**Evidence:** `evidence/BENCHMARK_FAILURE_001.txt`, final `evidence/FULL_TEST.txt`, `evidence/BENCHMARK.json`.
