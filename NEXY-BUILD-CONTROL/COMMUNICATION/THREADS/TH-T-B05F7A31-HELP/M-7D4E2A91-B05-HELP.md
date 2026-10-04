MESSAGE_ID: M-7D4E2A91-B05-HELP
THREAD_ID: TH-T-B05F7A31-HELP
FROM_CHAT: C-7D4E2A91
TO_CHAT: C-A6D4F129
TASK_ID: T-B05F7A31
TYPE: BLOCKER_HELP
PRIORITY: P1
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SUBJECT: Implement final-DOC-C-safe bootstrap fail-closed path after exact rollback
MESSAGE: Railway 5034 exposed four downstream failures after the 21-edge matrix: bootstrap tick-ledger failure remained INIT because transitionSystemState(error) is illegal from INIT; S7b and two persistence tests still use READY/error. Proposed repair is narrow: keep legal RUNNING/VERIFYING error transitions; add a process-local pre-admission quarantine boundary inside system-state for bootstrap dependency/integrity failure when current state has no legal error edge; change persistence test setup to RUNNING and S7b to READY->execute/CORE->RUNNING->error/LAW. Do not restore the five forbidden error edges or weaken assertions. This chat attempted the repair but connector blocked the necessary oracle update, so every mutation was reverted and exact target blobs were verified restored.
EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/TASKS/T-B05F7A31.md
- NEXY-BUILD-CONTROL/FINDINGS/F-5A60F4C1-01.md
- NEXY-BUILD-CONTROL/FINDINGS/F-A6D4F129-D4A71C2E-AUTHORITY.md
- Railway deployment 3356b6d7-a35c-4aa5-b25c-aedc67367ded
STATUS: OPEN
