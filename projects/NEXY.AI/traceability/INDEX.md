# NEXY.AI Traceability Spine

Canonical:
- `requirement-code-test-evidence.jsonl`
- `tests/test-index.jsonl`
- `evidence/evidence-index.jsonl`
- `validation-report.md`

Trace spine:

`SOURCE → REQUIREMENT → ONTOLOGY ENTITY → CODE → TEST → EVIDENCE → VERDICT`

This stage establishes navigable links. It deliberately does **not** invent test execution or PASS.

## Freshness law
Evidence is usable only for the exact revision/environment/claim it proves.

An artifact from another commit remains useful historical evidence but cannot establish current-HEAD PASS.
