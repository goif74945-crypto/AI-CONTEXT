# Evidence — IVS

- Claim: transitive impact propagation and deterministic cost-aware verification scheduling work for supplied dependency/coverage metadata.
- Evidence class: E1 static + E2 unit.
- Environment: Python 3.13.5, local isolated container.
- Unit command: `cd 04_incremental_verification_scheduler && python3 -m unittest -v test_reference.py`.
- Observed: 5 tests, 5 PASS.
- Negative paths proven: uncovered impacted node → FREEZE; invalid test cost → FREEZE; deterministic tie-break verified.
- Limitations: dependency graph completeness, real test coverage truth, globally optimal scheduling, project-wide speedup and NEXY CI integration are NOT_VERIFIED.
