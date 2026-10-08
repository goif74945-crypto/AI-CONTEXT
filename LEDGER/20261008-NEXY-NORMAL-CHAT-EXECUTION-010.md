# LEDGER 20261008-NEXY-NORMAL-CHAT-EXECUTION-010
| ID | Source / locator | Claim | Proof depth | Verdict |
|---|---|---|---|---|
| L01 | GitHub branches/NEXY.ai | Product HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 | direct branch GET | VERIFIED_AT_OBSERVATION |
| L02 | GitHub AI-CONTEXT/main | Control HEAD 5bd3f3eacc541205419045a4544e34ac3d0657b2 before writes | direct branch GET | VERIFIED_AT_OBSERVATION |
| L03 | AI-CONTEXT commit 4dc561d | 009 source/test/harness/candidate artifacts committed | direct commit + file content reads | VERIFIED |
| L04 | TESTS/009/ex009-crossstore-pg-redis.mts blob 3973fa0fae81c385b1f93617e66c2f67c8358c39 | real Prisma + direct BullMQ + probe Worker; no dispatchDirective() called | source text | VERIFIED_SOURCE |
| L05 | TESTS/009/README.md blob 1971c4a190242494f0161767cdc7a507be8487f0 | README itself labels EX009 boundary integration, NOT_RUN | direct source read | VERIFIED_SOURCE |
| L06 | packages/queue/run-state.ts blob e162efc8b2a45014bcefbd60dc67a95d8a1e1003 | release function enforces cancellation inside transaction at source lines 53-66,258 | read real product source | VERIFIED_SOURCE; RACE_NOT_TESTED |
| L07 | TESTS/009/ex009-cage-failclosed-source.test.ts | two source-string assertions, not Linux runtime/BPF tests | code inspection | VERIFIED_SOURCE |
| L08 | GitHub Actions E7 37741650376 | attempt=2, conclusion failure on product HEAD | live run GET | VERIFIED |
| L09 | GitHub Actions E7 jobs | six current attempt jobs steps=[], unassigned runner_name; latest Redis job 113320413296 | live job list GET | VERIFIED_BOUNDED |
| L10 | CI 404 logs and absent artifacts | actual root cause cannot be assigned | archived 009 and current API artifact count=0 | UNKNOWN |
| L11 | earlier CAS candidate A/B/C | each separate source patched SHA, mock tests reported; none G3 | candidate report 009, source hashes | REPORTED_WORKER_TEST / G3_NOT_VERIFIED |
| L12 | COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-010.md | requires producer-path + PG/Redis E2E, no paid provisioning | GitHub read-back | VERIFIED_COMMAND_ONLY |
RUNNER_CLAIM: No independent real PG/Redis runner used by authoring chat. DO NOT COUNT EX009 "NOT_RUN" as test failure or as green.
RELEASE_STATUS: NOT_AUTHORIZED.
