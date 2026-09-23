# NEXY.AI Implementation / Repository Map

## Pinned target
- repo: `goif74945-crypto/NEXY.AI-`
- branch: `codex/spec-audit-20260919-78df350`
- HEAD: `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`

## Files
- `repository-map.json` — tree/navigation/build/test/API/UI inventory for the exact HEAD.
- `system-to-code.jsonl` — ontology/system → observed files/symbols.
- `symbol-index.jsonl` — file → declared symbols/imports from the prior streaming symbol pass.
- `checkpoints/` — streaming extraction checkpoints.
- `validation-report.md` — structural/pinning validation.

## Semantics
- `PRESENT_E0` = code/file/symbol presence only.
- `NOT_MAPPED` = no mapping established in this pass; not automatically MISSING.
- runtime/test satisfaction is handled by Requirement↔Test↔Evidence traceability.

## Staleness
This entire implementation map is revision-bound. If branch HEAD != `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`, refresh before making current implementation claims.
