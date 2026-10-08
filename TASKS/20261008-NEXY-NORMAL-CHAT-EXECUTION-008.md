# TASK 20261008-NEXY-NORMAL-CHAT-EXECUTION-008
TITLE: Author Execution 008 handoff for existing normal ChatGPT worker.
MODE: ทำ / CROSS / EVIDENCE_REVIEW / COMMAND_BUILD
GOAL: Stop source-only repetition and require actual repo-integrated queue race implementation/testing plus isolated cage security and CI runner diagnosis.
INPUTS: User-pasted Execution 007 status and committed prior AI-CONTEXT handoff.
VERIFIED_SOURCES:
- Product NEXY.ai @ 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 (read live).
- AI-CONTEXT/main @ fc7dc9570cbe2d3a9a287db1c2613b1f97739cb7 before new writes (read live).
- EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS.md and its model.test.cjs, plus TASKS/LEDGER/CASES/FAILURES from 007, read from exact control commit.
- GitHub Actions runs 37741650349, 37741650343, 37741650376, 37741650355, 37741650318 independently verified as completed/failure on the observed product SHA.
- Jobs for run 37741650349 (1) and 37741650376 (6) showed steps=[] and runner_name="" in GitHub API; true root cause unknown.
AUTHORITATIVE_SPEC: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx; earlier verified SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
ACTIONS:
1. Re-check GitHub heads and control writeback.
2. Read committed 007 evidence and mock model.
3. Verify GitHub run/head/step status directly.
4. Author COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-008.md targeting same ordinary ChatGPT chat.
5. Conduct structural prompt audit and fix discovered CAS-only proof wording.
6. Save closure records and read back.
ARTIFACTS: COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-008.md, this TASK, LEDGER, CASES, FAILURES, command audit evidence.
TESTS_THIS_TASK: no product tests run; command structural audit only.
RISK: Another chat could modify HEAD; test runner may remain unavailable; repo-linked test and full cross-store proof required; cage fail-open risk unresolved; release never approved by this task.
ROLLBACK: AI-CONTEXT only, new forward commit after re-check; no product mutations.
FINAL_STATUS: VERIFIED_WITH_LIMITS for command engineering; PRODUCT_FIX=NOT_PERFORMED.
NEXT: existing normal chat execute full command 008 against live repository.
VERSION: 1
DATE_SOURCE: 2026-10-08 local conversation date.
