# Assurance Budget Planner — Evidence

- Implementation: `engine.py`
- Tests: `test_engine.py`
- Evidence: E2 unit + deterministic permutation fuzz.
- Verified behaviors: cheapest independent plan, budget freeze, insufficient independence freeze, same-domain duplicate does not count twice, input-order independence.
- Shared fuzz campaign: 500 shuffled validator-order checks.
- Real provider quality/cost calibration: NOT_VERIFIED.
