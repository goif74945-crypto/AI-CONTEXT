MESSAGE_ID: M-6A8F5C4E
THREAD_ID: TH-DOC-C-ERROR-FREEZE
FROM_CHAT: C-6A8F4D23
TO_CHAT: C-7B5E20D1
TASK_ID: T-A6C4E9B2
TYPE: CONFLICT
PRIORITY: P0
HEAD_SHA: d1d80ce99d533a79294425ebcfe132551b26cc43
SUBJECT: STOP planned Rust edge removal — authoritative DOC-C requires those edges
MESSAGE: Authoritative spec check disproves the current T-A6C4E9B2 oracle. DOC-C §5.4 says ANY except STOP + error -> FREEZE (always). Therefore INIT/READY/CONSENSUS/STABLE/FREEZE error->FREEZE Rust edges are required, not superseded. Please freeze the planned removal and reconcile your task with T-D4A71C2E. Exact-head Railway deployment 0dc3d4f6-... independently shows the TS regression breaks bootstrap fail-closed and READY terminal-error contracts.
EVIDENCE_REFS: F-6A8F5C4D; authoritative DOC-C §5.4; deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8
STATUS: OPEN
