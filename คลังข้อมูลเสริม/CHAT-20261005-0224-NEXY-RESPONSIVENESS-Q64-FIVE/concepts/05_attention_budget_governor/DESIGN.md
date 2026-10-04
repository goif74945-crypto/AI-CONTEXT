# 05 — Attention Budget Governor (ABG)
Status: Lo4 AI proposal only.

Goal: reduce optional interruptions without hiding critical state. Severity, urgency, user value and interruption cost use Q64.64. Blocker, security and authority-conflict notices always surface even when the optional budget is exhausted.

Code: `src/nexy_responsiveness/attention.py`. Tests: `tests/test_attention.py`, `tests/test_properties.py`.
