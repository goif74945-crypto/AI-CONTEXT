# Failure / Fix Log

## F-001 — expected TDD RED
- Symptom: `ModuleNotFoundError: No module named 'qcp'`.
- Cause: tests were intentionally executed before implementation existed.
- Purpose: establishes RED phase.
- Evidence: `TDD_RED.txt`.

## F-002 — Q64 conservation false negative
- Symptom: mathematically conserved decimal stages froze under exact raw equality.
- Root cause: decimal values independently quantized into Q64.64 can distribute rounding so two equivalent sums differ by one raw unit.
- Correction: accept residual only when `abs(left.raw-right.raw) <= 1`.
- Safety boundary: 2 raw units or more still freeze; tolerance is exact Q64 representation law, not floating epsilon.
- Evidence: `TDD_GREEN_INITIAL.txt`, `ULP_REGRESSION_RED.txt`, `ULP_REGRESSION_GREEN.txt`, adversarial 1-ULP/2-ULP test.

## F-003 — stress harness import failure
- Symptom: direct `python3 tests/stress_properties.py` could not import `qcp`.
- Root cause: Python placed `tests/` rather than project root at the head of module search path for that direct script invocation.
- Correction: execute with `PYTHONPATH=.`.
- Evidence: `STRESS_INITIAL_FAIL.txt` then `STRESS.txt` with `STRESS_PASS 1000`.
