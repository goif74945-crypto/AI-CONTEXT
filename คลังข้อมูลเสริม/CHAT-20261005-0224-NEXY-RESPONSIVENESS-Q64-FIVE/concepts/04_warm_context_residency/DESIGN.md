# 04 — Warm Context Residency Controller (WCRC)
Status: Lo4 AI proposal only.

Goal: use limited context residency without evicting controlling truth. Strong-authority chunks and counterevidence are pinned; optional chunks use Q64.64 freshness/reuse/dependency-distance utility. If pinned material exceeds budget, freeze rather than silently dropping authority.

Code: `src/nexy_responsiveness/warmset.py`. Tests: `tests/test_warmset.py`, `tests/test_properties.py`.
