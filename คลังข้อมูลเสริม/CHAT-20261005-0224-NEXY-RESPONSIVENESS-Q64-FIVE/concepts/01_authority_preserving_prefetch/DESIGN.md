# 01 — Authority-Preserving Predictive Prefetch Planner (AP3)
Status: Lo4 AI proposal only.

Goal: hide likely retrieval/tool-read latency by prefetching only side-effect-free dependencies. Mutating candidates are categorically rejected, not merely penalized. Selection uses Q64.64 net-gain density under a hard resource budget with stable tie-breaks.

Failure behavior: duplicate IDs fail; mutating speculation, unready dependencies, non-positive gain and budget overflow receive explicit rejection reasons.

Code: `src/nexy_responsiveness/prefetch.py`. Tests: `tests/test_prefetch.py`, `tests/test_properties.py`.
