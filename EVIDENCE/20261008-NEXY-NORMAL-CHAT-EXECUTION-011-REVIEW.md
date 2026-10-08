# EVIDENCE 20261008-NEXY-NORMAL-CHAT-EXECUTION-011 — source & handoff verification
STATUS: SOURCE_VERIFIED / COMMAND_VERIFIED_WITH_LIMITS
Product HEAD observed: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08.
Control EX010 HEAD observed: d71d52f4d384f82c5e27a4edf7593f958c120c1a.
Read 010 files by GitHub:
- TESTS/010/ex010-real-producer-crossstore.mts blob ffff2888b8fc921415b0f1e6c77d2df9f5aa3036.
- TESTS/010/ex010-owner-cancel-transaction-scope.spec.ts blob fdafbf4f238de5c7f8bcd249fc750cc3d6779808.
- EVIDENCE/20261008-NEXY-NORMAL-CHAT-EXECUTION-010-CROSS-cancellation-source-correction.md blob 74b0200b841edfc56204b52b7bb0a93b6c3f8b90.
- EVIDENCE/20261008-NEXY-NORMAL-CHAT-EXECUTION-010-CROSS-98-matrix.tsv blob ad1fcd709cd7600c54f337b9ba5817dc22b212fe.
Product code run-state.ts blob e162efc8b2a45014bcefbd60dc67a95d8a1e1003:
- recordPipelineRunFailure() prisma tx lockPipelineRun lines 409-410, pipelineRun FREEZE lines 532-544 and directiveDispatch CANCELLED lines 547-565;
- cancelPipelineRun() uses recordPipelineRunFailure with cancelDispatch:true lines 833-852;
- LAW commit also obtains lock and checks cancelled dispatch;
- exported standalone cancelDirectiveDispatch() source in dispatch.ts does not itself acquire that lock; do not conflate paths.
EX010 matrix checked: header + 98 rows, 98 unique IDs; 80 NOT_REASSESSED_010, 18 various source/test/blocked statuses.
CI source: E7 37741650376 attempt2 conclusion failure at observed HEAD, no root cause found. Current source-contract 5/5 is prior-worker claim backed by archived test code/report, not test executed by author.
New command: COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-011.md.
Prompt audit: 19 structural source/safety topics checked; clarified exact REQUERY current heads wording. Structural check is not a product test.
NO_PRODUCT_MUTATIONS / NO_RUNTIME_TESTS performed in this instruction-authoring task.
