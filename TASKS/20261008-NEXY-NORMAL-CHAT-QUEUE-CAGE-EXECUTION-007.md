# TASK 20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007
TITLE: Create execution command for same normal ChatGPT worker after handoff 006.
MODE: ทำ / CROSS / COMMAND_AUTHORING / ADVERSARIAL_AUDIT
GOAL: Produce and persist executable next instruction targeting real cancellation race and sandbox isolation.
SCOPE: Audit current source and prior worker evidence; hand off bounded repair steps to existing worker normal chat.
NON_GOALS: Product mutation or proof of runtime repairs in this authoring task.
INPUTS: User-provided Handoff 006 report; AI-CONTEXT/EVIDENCE/20261008-NEXY-HANDOFF-006-CROSS.md; CASES/20261008-NEXY-HANDOFF-006-CROSS.md.
PRODUCT_HEAD_AT_INITIAL_OBSERVATION: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_HEAD_AT_INITIAL_OBSERVATION: 07e3a8f690d84f6da97850387450b4b307727453
TOOLS: connected GitHub branch/commit and source-file reads; create_file control repo; fetch_file read-back.
ACTIONS: read live heads; read five previous handoff 006 artifacts; read product dispatch/jobs/workers/retry/cage sources; author next command; read-back and validate 17 command-invariant topics.
ARTIFACT: COMMANDS/20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007.md
SOURCE_FINDINGS:
- packages/queue/dispatch.ts: enqueueDirective awaited; id-only success/failure update can overwrite terminal state after concurrent cancellation.
- jobs.ts and workers.ts demonstrate Redis external side effects, claim and cancellation fences; database CAS alone cannot establish full closure.
- cage.ts bwrap false branch executes trusted executable via direct spawn; seccompJson written without visible applied syscall filter; full isolation not verified.
TESTS_PERFORMED: GitHub source read, command content read-back and 17 prompt-invariant checks. NO product tests.
DECISION: require actual current-head recheck; targeted test RED, minimal guarded repair, worker/Redis cleanup; security fail-closed investigation; no fake product pass.
RISKS: missing live execution runner; other chat may change HEAD; normative TSA ambiguity; DOC-E release approvals missing.
ROLLBACK: forward revert control artifacts only after current HEAD compare; no force/reset.
STATUS: VERIFIED_WITH_LIMITS_FOR_COMMAND_ONLY
NEXT_ACTION: paste short launch instruction in SAME already-working normal chat directing it to read COMMANDS/20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007.md and execute.
VERSION: 1
DATE_SOURCE: conversation date 2026-10-08 Asia/Bangkok, not precise timestamp.
TRACE: 20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007
