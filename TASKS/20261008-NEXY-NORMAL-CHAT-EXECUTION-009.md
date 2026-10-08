# TASK 20261008-NEXY-NORMAL-CHAT-EXECUTION-009
MODE: ทำ / CROSS / COMMAND_AUTHORING / INDEPENDENT_SOURCE_REVIEW
GOAL: verify Execution 008 records and author evidence-fenced 009 command for SAME normal ChatGPT worker.
INPUT: user-pasted Execution 008 status; live product and AI-CONTEXT GitHub reads.
PRODUCT_HEAD_VERIFIED_AT_OBSERVATION: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_HEAD_008_VERIFIED_AT_OBSERVATION: 85d9e9ac0f59e3bb64014ddf2a97948cc859fe21
SOURCE: Product packages/queue/dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
EVIDENCE: AI-CONTEXT latest 008 patch correction, RED/GREEN logs, Vitest tests, distinct patch families.
RESULT: Product dispatch still has vulnerable id-only state changes after Redis await. Verified 008 source-linked tests/logs archived; did NOT execute those tests independently in authoring chat.
ARTIFACT: COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-009.md
CHECKS: Live product/control HEAD, exact product blob, original patch blob without final LF, FIXED patch blob with final LF, two separately sourced RED/GREEN families, review of command safety gates.
NON_GOALS: No product code mutation or app runtime test.
RISKS: Single-writer concurrent edits, semantic compatibility across patch candidates, PG/Redis missing, cage unisolated Linux fallback, DOC-E release unverified.
ROLLBACK: Coordination-only forward revert after live HEAD recheck.
STATUS: VERIFIED_WITH_LIMITS for command and source review, PARTIAL for product implementation.
NEXT: same worker read command and execute real PG/Redis validation or build importable E2E harness without fake pass.
VERSION: 1
DATE_SOURCE: 2026-10-08 Asia/Bangkok.
