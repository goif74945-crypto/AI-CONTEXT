# Unknown Closure Planner — Evidence

- Implementation: `engine.py`
- Tests: `test_engine.py`
- Evidence: E2 unit + deterministic permutation fuzz.
- Verified behaviors: cheapest exact cover, known-blocker fast path, impossible closure → FREEZE, input-order independence.
- Shared fuzz campaign: 500 shuffled probe-order checks.
- Live user-question UX: NOT_VERIFIED.
