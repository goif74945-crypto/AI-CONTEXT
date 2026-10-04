# 02 — Latency Envelope Compiler (LEC)
Status: Lo4 AI proposal only.

Goal: compile a total response-time envelope into deterministic stage budgets without deleting mandatory verification time. Stage minima and weights are Q64.64. If minima exceed the SLO, freeze with `MINIMUM_VERIFICATION_LATENCY_EXCEEDS_SLO`.

Code: `src/nexy_responsiveness/latency_budget.py`. Tests: `tests/test_latency_budget.py`, `tests/test_properties.py`.
