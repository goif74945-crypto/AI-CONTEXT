# Artifact Manifest

Status: `Lo4_AI_PROPOSAL_ONLY / REFERENCE_IMPLEMENTATION`

Core:
- `qcp/fixed.py` — checked signed Q64.64 arithmetic.
- `qcp/uncertainty.py` — UMC.
- `qcp/robustness.py` — DRC.
- `qcp/budget.py` — VBR.
- `qcp/reversibility.py` — RHL.
- `qcp/expectation.py` — EDB.
- `qcp/pipeline.py` — conservative isolated composition.
- `qcp/__init__.py` — package surface.

Design/context:
- `README.md`, `DESIGN.md`.
- `design/01_UMC.md` through `design/05_EDB.md`.
- `02_NOVELTY_COLLISION_MATRIX.md`.
- `03_INTEGRATION_CONTRACT.md`.
- `04_VALIDATION_REPORT.md`.
- `05_FUTURE_RESEARCH.md`.

Verification:
- `tests/test_fixed.py`, `tests/test_systems.py`, `tests/stress_properties.py`.
- `evidence/TDD_RED.txt`.
- `evidence/TDD_GREEN_INITIAL.txt`.
- `evidence/TDD_GREEN_AFTER_FIX.txt`.
- `evidence/ULP_REGRESSION_RED.txt`, `evidence/ULP_REGRESSION_GREEN.txt`.
- `evidence/ADVERSARIAL_TESTS.txt`.
- `evidence/STRESS_INITIAL_FAIL.txt`, `evidence/STRESS.txt`.
- `evidence/STATIC_COMPILE.txt`.
- `evidence/FINAL_TESTS.txt` and `evidence/HASHES.sha256` after final seal.
- `evidence/EVIDENCE.md`, `evidence/FAILURE_FIX_LOG.md`.

Transient `__pycache__` files are intentionally excluded from publication.
