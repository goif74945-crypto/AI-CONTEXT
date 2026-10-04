# Validation Report

## Evidence produced locally
- TDD RED: initial tests failed because package implementation did not exist.
- Initial GREEN attempt: 28 tests, 26 pass / 2 fail, exposing a one-ULP Q64 conservation boundary defect.
- Correction: conservation comparison changed from exact equality to an explicit maximum one raw Q64 unit residual.
- Regression replay: reverting that correction makes the target regression test fail; restoring it makes the test pass.
- Expanded adversarial suite: 37/37 PASS.
- Deterministic/property stress: 1,000 checks PASS.
- Static compilation: PASS, exit code 0.

## Important observed failure
The first stress invocation failed with `ModuleNotFoundError` because the test script was executed without the project root on Python's import path. The failed log is preserved as `evidence/STRESS_INITIAL_FAIL.txt`; rerun with `PYTHONPATH=.` passed 1,000 checks. This was a harness invocation defect, not hidden from the evidence record.

## Evidence classes
- E0: artifact presence once published.
- E1: Python compilation/static import proof.
- E2: unit/adversarial behavior proof.
- E3: isolated cross-engine composition via `PipelineIntegrationTests` only.

## Not proven
- integration with a NEXY implementation repository;
- actual user-facing NEXY workflow;
- provider/runtime/deployment behavior;
- production concurrency;
- production performance/security;
- correctness of any real-world calibration used to populate quantitative inputs;
- Canon status.
