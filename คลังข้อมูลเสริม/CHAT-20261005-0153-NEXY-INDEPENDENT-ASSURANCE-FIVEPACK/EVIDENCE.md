# Evidence — NEXY Independent Assurance Five-Pack

## Evidence boundary
These results prove the standalone reference implementation in this execution environment. They do **not** prove behavior inside the NEXY.AI implementation, production deployment, or adoption into governing NEXY law.

## Source/context evidence used for design compatibility
The work was bootstrapped from `AI-CONTEXT/INDEX.md`, `AI-EXECUTION-KERNEL.md`, global security/verification rules, NEXY overview/current 837-row source matrix, and relevant deep context on SWARM/JUDGE, capability governance, human control surfaces, DOC-C and final architecture. Existing sibling names under `คลังข้อมูลเสริม/` were inspected to reduce direct duplication. The five candidate collision searches returned no direct matches for the exact candidate themes. This is collision screening, not a mathematical proof that no semantically related work exists anywhere.

## TDD / repair trace
1. Initial test execution failed at import because `src/` was not on the module path. This was classified as harness failure, not product failure.
2. Harness was corrected using `PYTHONPATH=src`; the RED run then correctly failed because the five implementation modules did not yet exist.
3. After implementation, `unittest discover` returned zero tests because the suite used pytest-style test functions. That run was explicitly rejected as non-evidence.
4. Runner was corrected to pytest and the first valid GREEN run passed 15 tests.
5. Negative, edge, cross-module and determinism tests were added; the expanded package reached 31 then 35 passing tests.
6. A compact standalone artifact was created for durable persistence. The exact persisted code/test pair was then re-tested independently: 32 tests passed.

## Fresh decisive proof for the exact persisted bundle
Command:

`PYTHONPATH=. python -m pytest -q`

Observed in `FINAL_TEST.txt`:

`32 passed in 0.07s`

`EXIT_CODE=0`

## Static proof for the exact persisted bundle
Command:

`PYTHONPATH=. python -m compileall -q nexy_assurance_fivepack.py test_nexy_assurance_fivepack.py`

Observed in `STATIC.txt`:

`COMPILE_EXIT=0`

Runtime: Python 3.13.5 was used in the larger local package verification. No claim is made for untested Python implementations or platforms.

## Coverage intent
The compact suite contains tests for:
- IAQ correlated replicas, fake quorum, independent failures, empty input, duplicate identity and order invariance;
- ECG clean roots, target-derived oracle, shared untrusted/trusted roots, cycles, direct overlap and edge-order invariance;
- RAAS low risk, high-risk production promotion, irreversible/no-compensation freeze, permission changes, invalid scales and repeatability;
- CTR retirement, stale/future snapshots, explicit restore, replacement, invalid self-replacement and canonical digest ordering;
- AIG duplicate suppression, changed critical delivery, exact critical duplicate suppression, noncritical budget, evidence changes and time regression;
- one integrated high-risk flow across all five mechanisms.

## Evidence classification
- code presence/content: E0;
- Python compilation: E1;
- module behavior: E2-style local execution;
- cross-module standalone flow: local E3-like package interaction only;
- NEXY implementation integration: NOT_VERIFIED;
- NEXY E2E/runtime/operational behavior: NOT_VERIFIED;
- NEXY deployment: NOT_VERIFIED.

## Truth constraints
A passing standalone test does not establish adoption, compatibility with an unknown future NEXY HEAD, production security, calibrated risk scoring, correctness of supplied provenance metadata, or deployment readiness. Those claims require separate evidence.
