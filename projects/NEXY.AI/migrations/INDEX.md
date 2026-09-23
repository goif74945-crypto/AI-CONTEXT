# NEXY.AI Migration Registry

## Target snapshot
- repo: `goif74945-crypto/NEXY.AI-`
- branch: `codex/spec-audit-20260919-78df350`
- HEAD: `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`

## Files
- `migrations.jsonl` — **4** observed migrations in exact order.
- `migration.schema.json`
- `validation-report.md`

## Critical semantics
`down_script_present=true` does **not** mean rollback has been executed successfully.

Current DOC-E registry has no exact-current-HEAD rollback proof, therefore every migration currently has:
`rollback_verified = NOT_VERIFIED_CURRENT_HEAD`.

For migrations without an explicit `migration.down.sql`, this registry records absence of that file only. It does not claim rollback is impossible through some other authorized procedure.

## AI use
Before persistence/schema change:
1. resolve affected objects;
2. identify migration predecessor/order;
3. inspect forward and rollback path;
4. calculate state/contract/invariant impact;
5. require real apply→rollback evidence before deployment claims.
