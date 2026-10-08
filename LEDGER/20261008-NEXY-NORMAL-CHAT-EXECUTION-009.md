# LEDGER 20261008-NEXY-NORMAL-CHAT-EXECUTION-009
| ID | Source | Claim | Proof / limit | Status |
|---|---|---|---|---|
| 009-01 | GitHub NEXY.ai branch | Product HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 | live branch read | VERIFIED_AT_OBSERVATION |
| 009-02 | packages/queue/dispatch.ts | ID-only update after awaited enqueue persists | exact blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29 and code match | VERIFIED_SOURCE |
| 009-03 | AI-CONTEXT commit 85d9e9ac | worker source artifacts persisted | direct GitHub commit/file reads | VERIFIED |
| 009-04 | original patch blob ac06e695 | missing final LF, known invalid as reported | directly verified content endsWith newline=false; git apply failure from correction evidence, not our own execution | VERIFIED_CONTENT / REPORTED_APPLY_FAIL |
| 009-05 | FIXED patch blob b7c9444d | restores final LF | direct check endsWith newline=true; reverse/forward round-trip and patched source 36e56aef reported by worker | VERIFIED_CONTENT / REPORTED_APPLY_PASS |
| 009-06 | second 008 patch blob 3296992a | distinct patched source 94340b7 | direct file read and archived logs | VERIFIED_PROVENANCE; don't conflate tests |
| 009-07 | first 008 logs | RED 5 failed / 4 passed and GREEN 9/9 | archived report/test, author did not execute runtime | HISTORICAL_WORKER_TEST |
| 009-08 | other 008 logs | RED 6 failed / 3 passed and GREEN 9/9 | archived raw logs, author did not execute runtime | HISTORICAL_WORKER_TEST |
| 009-09 | source/worker evidence | real PG Redis transaction and release race closure | no real E2E data present | NOT_VERIFIED |
| 009-10 | COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-009.md | requires candidate provenance and PG/Redis E2E gates | command GitHub read-back | VERIFIED_COMMAND_ONLY |
PRODUCT_CHANGED_IN_AUTHORING: NONE; REQUIRED_NEXT_ACTION: requery HEAD and run/author real cross-store tests.
