# NEXY.AI Implementation / Repository Map

Pinned snapshot:
- repo: `goif74945-crypto/NEXY.AI-`
- branch: `codex/spec-audit-20260919-78df350`
- HEAD: `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`
- PR #8: OPEN / DRAFT / UNMERGED at the observed revision.

Canonical files:
- `repository-map.json`
- `system-to-code.jsonl`
- `symbol-index.jsonl`
- `mapping-rules.json`
- `coverage.json`
- `validation-report.md`
- `checkpoints/`

## Rule
This registry answers **where implementation material lives**, not whether it is correct.

`implementation exists` ≠ `requirement satisfied` ≠ `test passed` ≠ `deployment proven`.

Before editing:
1. require current HEAD to match the map;
2. locate entity through `system-to-code.jsonl`;
3. open all EXACT/GROUP/CANDIDATE files needed;
4. resolve governing requirements/invariants/contracts;
5. only then construct a change plan.

CANDIDATE is never a safe automatic patch target.
