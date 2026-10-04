# Evidence — EMCR

- Claim: capability-specific empirical routing, budget filtering, calibration penalty and probe/freeze semantics work in the reference.
- Evidence class: E1 static + E2 unit.
- Environment: Python 3.13.5, local isolated container.
- Unit command: `cd 03_empirical_model_calibration_router && python3 -m unittest -v test_reference.py`.
- Observed: 5 tests, 5 PASS.
- Negative paths proven: insufficient evidence → PROBE; budget violation → FREEZE; malformed confidence → FREEZE; unrelated capability evidence ignored.
- Limitations: real provider performance, online drift behavior, production SLOs, provider costs and NEXY model-admission integration are NOT_VERIFIED.
