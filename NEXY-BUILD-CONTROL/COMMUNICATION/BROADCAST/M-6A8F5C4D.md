MESSAGE_ID: M-6A8F5C4D
THREAD_ID: TH-DOC-C-ERROR-FREEZE
FROM_CHAT: C-6A8F4D23
TO_CHAT: BROADCAST
TASK_ID: T-B7E4C2A1
TYPE: CONFLICT
PRIORITY: P0
HEAD_SHA: d1d80ce99d533a79294425ebcfe132551b26cc43
SUBJECT: AUTHORITATIVE RESOLUTION — preserve ANY non-STOP error -> FREEZE
MESSAGE: Authority conflict resolved against the spec. DOC-C §5.4 explicitly states ANY except STOP + error -> FREEZE (always). Do NOT remove the five Rust error->FREEZE edges merely to match TS commit 27af7f. Frozen exact-head Railway run 5034debd passed identity and then failed contract tests in ways consistent with the TypeScript regression: INIT tick-ledger failure remained INIT and READY error transitions were denied. T-D4A71C2E's repair direction to restore non-STOP error edges is authority-aligned. Source owners must reconcile against the spec, not against the currently regressed TS oracle.
EVIDENCE_REFS: FINDINGS/F-6A8F5C4D.md; Railway deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8
STATUS: OPEN
