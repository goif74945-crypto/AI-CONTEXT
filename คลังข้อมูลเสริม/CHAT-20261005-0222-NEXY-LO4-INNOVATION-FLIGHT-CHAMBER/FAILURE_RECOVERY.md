# Failure Recovery Evidence

## Failure FR-001
- Stage: first local verification run
- Observed: `ImportError: Start directory is not importable: .../tests`
- Root cause: Python 3.13 `unittest` discovery with explicit `top_level_dir` requires the tests directory to be importable.
- Smallest correction: created `tests/__init__.py`.
- Re-verification: `python run_verification.py`.
- Result after correction: PASS, 25 tests, 0 failures/errors, compile PASS.
- Regression: a second full verification run also PASSed.

## Determinism check
`MANIFEST.sha256` was generated twice after identical source state and had the same SHA-256 both times:
`9e5f2038c7feca7ca8c7c491dda768dbde1f93b91cffd513c9569a21bbdd238f`

This proves only deterministic manifest generation for the tested local artifact state. It does not prove deterministic behavior of an integrated NEXY runtime.
