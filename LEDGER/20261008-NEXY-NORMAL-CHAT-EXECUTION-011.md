# LEDGER 20261008-NEXY-NORMAL-CHAT-EXECUTION-011
| ID | Source | Claim / proof | Verdict |
|---|---|---|---|
| L01 | live GitHub NEXY.ai | HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 | VERIFIED_AT_OBSERVATION |
| L02 | live GitHub AI-CONTEXT main | EX010 end HEAD d71d52f4d384f82c5e27a4edf7593f958c120c1a | VERIFIED_AT_OBSERVATION |
| L03 | GitHub commit d71d52 | EX010 owner-cancel correction and source-contract test exist | VERIFIED_STORED |
| L04 | product run-state.ts blob e162efc8b2a45014bcefbd60dc67a95d8a1e1003 lines 400-410,532-565,800-857 | canonical OWNER cancel and LAW release use same advisory lock, FREEZE+CANCELLED transaction | VERIFIED_SOURCE_ONLY |
| L05 | product dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29 lines 301-319 | standalone cancel helper lacks same explicit advisory lock | VERIFIED_SOURCE_ONLY; runtime reachability unknown |
| L06 | EX010 source-contract test blob fdafbf4f238de5c7f8bcd249fc750cc3d6779808 | tests inspect source text/order; 5/5 PASS reported by worker | SOURCE_VERIFIED / RUN_CLAIM_HISTORICAL |
| L07 | TESTS/010/ex010-real-producer-crossstore.mts blob ffff2888b8fc921415b0f1e6c77d2df9f5aa3036 | real product-producer harness source exists; no PG/Redis execution | VERIFIED_FILE / G3_NOT_RUN |
| L08 | EX010 98 matrix blob ad1fcd709cd7600c54f337b9ba5817dc22b212fe | 98 rows, 98 distinct IDs, 80 NOT_REASSESSED_010 | VERIFIED_CONTENT |
| L09 | GitHub Actions run 37741650376 attempt2 | FAILURE and no job steps for observed jobs | VERIFIED_AT_OBSERVATION; root cause unknown |
| L10 | COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-011.md | same normal chat, finite runner probes, independent READY work, head fence, security/release gates | VERIFIED_READBACK_EXPECTED |
UNRESOLVED: PostgreSQL/Redis cross-store integration, production worker, Linux cage enforcement, TSA authority injection, DOC-E approvals. No product mutation or real service testing in authoring turn.
