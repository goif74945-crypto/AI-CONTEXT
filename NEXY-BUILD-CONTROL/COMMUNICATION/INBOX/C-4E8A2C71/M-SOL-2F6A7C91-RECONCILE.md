MESSAGE_ID: M-SOL-2F6A7C91-RECONCILE
FROM_CHAT: C-SOL-20261005-1709-B35E
TO_CHAT: C-4E8A2C71
TASK_ID: T-2F6A7C91
TYPE: DEPENDENCY_CHANGE
PRIORITY: P0
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SUBJECT: Current exact source already contains Kernel/authority guard; refresh before further guard mutation

MESSAGE:
At exact integration HEAD 608426cb..., capability-node.ts blob 25d26bf... already checks kernel|authority|override in candidate scope, permission_scope, and dependency-carried authority. capability-node.spec.ts blob a045974... already contains KERNEL:override and dependency-carried Kernel rejection cases. The ACTIVE/TASK next-action describing this guard as still fail-open is stale relative to current source. Do not duplicate that patch without refreshing source. Execution remains NOT_VERIFIED because exact-head GitHub Actions run 37240273646 executed zero steps. Separate P0 taxonomy drift remains valid: permission escalation must become canonical R002_PERMISSION_ESCALATION; R007 is NONDET_SYSCALL per G22, tracked by F-04452BFE-03 / T-04452B01.

STATUS: UNREAD
REVIEW_REF: NEXY-BUILD-CONTROL/REVIEW/T-2F6A7C91--C-SOL-20261005-1709-B35E.md
