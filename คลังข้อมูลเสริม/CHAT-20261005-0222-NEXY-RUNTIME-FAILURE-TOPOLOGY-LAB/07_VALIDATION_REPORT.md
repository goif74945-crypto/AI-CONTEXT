# Validation Report

Status at this record: **LOCAL E1/E2/E3 VERIFIED; REMOTE E0 PERSISTENCE PENDING**

## Target identity
- project: NEXY Runtime Failure Topology Lab
- chat code: `CHAT-20261005-0222-NEXY-RUNTIME-FAILURE-TOPOLOGY-LAB`
- local staging root: `/mnt/data/nexy_runtime_failure_topology_lab`
- intended repository root: `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0222-NEXY-RUNTIME-FAILURE-TOPOLOGY-LAB/`
- NEXY compatibility snapshot read-only: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

## TDD history
### Initial RED
`PYTHONPATH=src python3 -m unittest discover -s tests -v`

Observed: expected import failures because production modules did not yet exist. Evidence: `evidence/01_tdd_red.txt`.

### First GREEN
After the first implementation, 39 tests passed. Evidence: `evidence/02_green_attempt_1.txt`.

### Remediation cycle 1
Independent review added tests for:
- livelock repeated suffix after a transient prefix;
- prior non-idempotent retry history laundering;
- prior non-retryable retry history laundering.

All three tests failed against the then-current implementation, recorded in `evidence/03_regression_red.txt`. The implementation was repaired and the suite returned to 42 passing tests in the executed session. That intermediate GREEN console stream was not persisted because `unittest` emitted on stderr; final post-repair regression is persisted in `evidence/14_final_local_test_run.txt`.

### Remediation cycle 2
Review found that the salvage compiler could set `whole_task_complete=True` merely because every *presented* node was safe. The compiler does not own the authoritative task denominator, so that was an authority overreach. A focused RED test reproduced the defect in `evidence/05_salvage_authority_red.txt`. The compiler was changed so it never mints whole-task completion. Final persisted regression proof is `evidence/14_final_local_test_run.txt`.

### Remediation cycle 3
Stress probing exposed `RecursionError` on a long acyclic wait chain in the original recursive SCC implementation. The defect was captured by a 1,500-node RED regression in `evidence/08_deadlock_stack_red.txt`. Deadlock SCC traversal was replaced with an iterative algorithm. The focused repair passed in-session; final persisted full regression proof is `evidence/14_final_local_test_run.txt`.

### Expanded adversarial coverage
Canonicalization, disjoint cycles, retry streak resets, independent salvage branches, and explicit dependency exclusion were added. Those cases are included in the final persisted suite `evidence/14_final_local_test_run.txt`.

## Final local gates
### E1 static
Command:
`PYTHONPATH=src python3 scripts/verify.py`

Observed:
- source files scanned: 7;
- Python compile: PASS;
- forbidden effectful import/call findings: 0;
- status: PASS.

Evidence: `evidence/13_static_verification.txt`.

This AST check is a bounded policy check, not a universal security proof.

### E2 unit/adversarial/regression
Command:
`PYTHONPATH=src python3 -m unittest discover -s tests -v`

Observed final local run: **52 tests, 52 passed, 0 failed, 0 errors**.
Evidence: `evidence/14_final_local_test_run.txt`.

### E3 local integration
The full suite includes `tests/test_integration.py`, which composes all five modules in one failure scenario. The executable example was also run:
`PYTHONPATH=src python3 examples/demo.py`

Observed demo states:
- Deadlock Sentinel: `DEADLOCK`;
- Livelock Detector: `LIVELOCK`;
- Retry Governor: `QUARANTINE_STORM`;
- Poison Quarantine: `QUARANTINE`;
- Salvage Compiler: `SALVAGE_READY`, included `requirements` and `design`, excluded failed `execution`, `whole_task_complete=false`.

Evidence: `evidence/15_demo_output.json`.

### Determinism probe
Command:
`PYTHONPATH=src python3 scripts/determinism_probe.py`

Observed 6/6 permutations for deadlock fixture and 6/6 permutations for salvage fixture each collapsed to one fingerprint. Status PASS. Evidence: `evidence/16_determinism_probe.txt`.

### Scaling probe
Command:
`PYTHONPATH=src python3 scripts/scaling_probe.py`

Observed stack-safe correctness through a 10,000-node acyclic wait graph. Final five-run median local timings recorded approximately 0.002 s / 1k, 0.0066 s / 2.5k, 0.0135 s / 5k, 0.029 s / 10k in this environment. Evidence: `evidence/17_scaling_probe_final.txt`.

**Interpretation:** timing is observational only and is not a NEXY performance SLA or production benchmark.

## Evidence boundary
Verified locally:
- E1 static policy properties;
- E2 unit/adversarial behavior for authored fixtures;
- E3 composition in this standalone reference package.

Not verified:
- NEXY integration/runtime behavior;
- distributed lock ownership telemetry quality;
- worker crash recovery;
- provider failure behavior;
- queue correctness under concurrency;
- production false-positive/false-negative rates;
- deployment/E6;
- physical/E7.

Remote E0 persistence/read-back remains pending until GitHub publication and exact-byte verification complete.
