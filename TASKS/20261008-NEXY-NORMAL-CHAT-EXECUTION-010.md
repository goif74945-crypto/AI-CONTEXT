# TASK 20261008-NEXY-NORMAL-CHAT-EXECUTION-010
MODE: ทำ / CROSS / COMMAND_ENGINEERING / SOURCE_VERIFICATION
STATUS: VERIFIED_WITH_LIMITS_FOR_HANDOFF; PRODUCT_FIX_NOT_EXECUTED
GOAL: source-verify worker Execution 009, audit actual EX009 test harness coverage and issue executable next normal-chat command targeting real service runner and actual dispatch producer.
INPUTS: user-pasted 009 report; live connected GitHub reads; verified 009 control evidence.
PROVENANCE: product goif74945-crypto/NEXY.AI- branch NEXY.ai observed HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08; control goif74945-crypto/AI-CONTEXT main observed HEAD 5bd3f3eacc541205419045a4544e34ac3d0657b2 before 010 writes.
SPEC_SHA256_REQUIRED: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7; hash prior-worker sourced, not recomputed by authoring chat.
SOURCES_READ: 009 evidence summary, candidates, TESTS/009/README.md, docker-compose.yml, ex009-crossstore-pg-redis.mts, cage source regression; E7 attempt2 evidence; product packages/core/tick.ts, packages/queue/dispatch.ts and packages/queue/run-state.ts.
LIVE_VERIFIED_CI: GitHub Actions run 37741650376 attempt=2 failed on source product HEAD; six jobs steps=[]; latest Redis/BullMQ job 113320413296, runner_name empty; cause UNKNOWN.
CRITICAL_DISTINCTION: EX009 harness uses real Prisma + direct BullMQ Queue.add and test probe Worker if services ever run. It does not exercise the candidate actual dispatchDirective() or full production worker. EX009 real service run NOT_RUN in previous 009, no product fix authorized by command only.
OUTPUTS:
- COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-010.md
- TASKS/20261008-NEXY-NORMAL-CHAT-EXECUTION-010.md, LEDGER/20261008-NEXY-NORMAL-CHAT-EXECUTION-010.md, CASES/20261008-NEXY-NORMAL-CHAT-EXECUTION-010.md, FAILURES/20261008-NEXY-NORMAL-CHAT-EXECUTION-010.md, EVIDENCE/20261008-NEXY-NORMAL-CHAT-EXECUTION-010-REVIEW.md
ACCEPTANCE: command read-back + auditable constraints; product regressions and live PG/Redis NOT_RUN by handoff author.
RISK: creating cloud services without permission, stale HEAD, confusing boundary integration with full E2E, TSA forgery, premature release, cage mislabeling.
ROLLBACK: new forward commit in AI-CONTEXT only after HEAD recheck; no Product mutations here.
NEXT: send same worker a short prompt to read full command 010 and act using actual authorized tools.
DATE_SOURCE: 2026-10-08 conversation date, no invented clock.
VERSION: 1
TRACE_ID: 20261008-NEXY-NORMAL-CHAT-EXECUTION-010
