# NEXY.AI Repository Navigation Intelligence

## Pinned target
- repo: `goif74945-crypto/NEXY.AI-`
- branch: `codex/spec-audit-20260919-78df350`
- HEAD: `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`

## Purpose
Fast navigation from architecture/system identity to current observed code/test surfaces.

## Files
- `navigation-index.jsonl` — **20** system-level navigation records.
- `surface-map.json` — repository/build/test/API/UI navigation surfaces.
- Existing canonical detail:
  - `../implementation/system-to-code.jsonl`
  - `../implementation/symbol-index.jsonl`
  - `../traceability/requirement-trace.jsonl`

## Use
`SYSTEM → PATHS → SYMBOLS → REQUIREMENTS → TESTS → EVIDENCE`

## Freshness rule
This navigation intelligence is pinned to HEAD `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`.
If actual target HEAD differs, use it only as stale navigation hints until refreshed. Never make current implementation claims from a stale map.
