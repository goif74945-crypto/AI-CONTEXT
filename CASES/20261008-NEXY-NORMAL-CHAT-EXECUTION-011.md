# CASE 20261008-NEXY-NORMAL-CHAT-EXECUTION-011
CASE_ID: EX011-LOCK-CORRECTION-AND-RUNNER-DEADLOCK
STATUS: OPEN
CAUSE: Previous source-risk summary conflated unlocked standalone cancelDirectiveDispatch with canonical OWNER cancel path; repeated EX009/010 test harness creation did not produce actual PG/Redis integration because no safe authorized runner was available.
EVIDENCE: product run-state.ts canonical OWNER cancel using recordPipelineRunFailure transaction, advisory lock and FREEZE+dispatch CANCELLED; EX010 correction doc at control commit d71d52f. EX010 harness is source-importable but unexecuted with real services.
IMPACT: overbroad LAW race claim may direct incorrect patching; repeated harness creation produces false sense of progress.
CORRECTION: scope remaining source concern to standalone cancel-helper reachability and actual transaction interleavings; finite verified runner discovery, then pivot to independent tested DOC-C issue when G3 impossible.
NEGATIVE TEST: real two-connection PG serialization when accessible; source-contract test not substitute.
SECURITY: no production DB/test use, no weakening isolation, no invented TSA or release.
PREVENTION: source-to-claim proof level, explicit no-progress gate, real execution receipts and accurate PARTIAL.
NEXT: COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-011.md for same worker.
