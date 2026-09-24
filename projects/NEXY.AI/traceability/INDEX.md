# NEXY.AI Requirement Traceability Spine

Canonical trace:
`SOURCE → REQUIREMENT → SYSTEM/ENTITY → IMPLEMENTATION → TEST → EVIDENCE → VERDICT`

Files:
- `requirement-trace.jsonl` — one trace record per canonical requirement.
- `test-index.jsonl` — test-file inventory at pinned implementation HEAD.
- `evidence-index.jsonl` — DOC-E evidence-file locations at pinned HEAD.
- `coverage.json`

## Status semantics
- implementation ref = location/presence only.
- `CURATED_CANDIDATE_STATIC` / `DOMAIN_CANDIDATE_STATIC` = test candidate, not proof the test covers or passes the requirement.
- `EXACT_LOCATION_NOT_VALIDATED` = evidence document location is known; evidence validity/freshness has not yet been judged.
- `NOT_EVALUATED` = no compliance verdict.

This prevents “test file exists = PASS” and “evidence markdown exists = deployment proven.”
