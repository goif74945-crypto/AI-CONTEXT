# Verification Record — Local Candidate

## Environment
- Python: 3.13.5
- Runtime: isolated local container for this ChatGPT execution
- External Python dependencies: none required by implementation/tests

## E1 — Static
- `python3 -m compileall -q .` → PASS / exit 0.
- Local secret-pattern scanner → PASS / 0 findings.
- Canonical serializer rejects unsupported/non-finite values by design.

## E2 — Unit / property
`PYTHONHASHSEED=1 python3 run_all_tests.py` → **34 tests PASS**.

`PYTHONHASHSEED=777 python3 run_all_tests.py` → **34 tests PASS**.

Property/regression tests include:
- ICG: first 120 permutations of five interpretations produce an identical result.
- EAP: 160 random small planning instances exactly match exhaustive brute-force optimal plans.
- CNS: random mutation campaign preserves a deliberately stable authorized decision.
- REC: 100 randomized mapping insertion orders yield identical capsule content.
- IEQE: 150 random simple quorum instances match an independent pairwise oracle.

## E3 — Standalone integration
`integration/test_mesh.py` verifies:
- all five modules compose to `READY` on the legal happy path;
- decision-relevant ambiguity freezes at ICG;
- common-mode evidence freezes at IEQE.

This is **E3 for the standalone research implementation only**. It is not E3 evidence for the protected NEXY implementation repository.

## Metrics before GitHub persistence
- 50 files (including evidence artifacts present at metric time)
- 23 Python files
- 1,289 Python lines
- 7 test files / 500 test lines
- 20 Markdown files / 488 Markdown lines

See raw artifacts under `evidence/`.

## Verification boundary
- Real NEXY adapter execution: NOT_VERIFIED.
- Browser/user E2E: NOT_VERIFIED.
- Target-runtime load/fault behavior: NOT_VERIFIED.
- Deployment: NOT_VERIFIED.
- Production safety/security guarantee: NOT_VERIFIED.
