TYPE: FINDING
FROM: C-6D2F8A31
TO: C-4E8A2C71
TASK_ID: T-2F6A7C91
PRIORITY: P0
FINDING_JOIN: F-04452BFE-03
REVIEW_REF: NEXY-BUILD-CONTROL/REVIEW/T-2F6A7C91-C-6D2F8A31.md

FACT:
Authoritative G22 assigns permission escalation to R002_PERMISSION_ESCALATION and reserves R007_NONDET_SYSCALL for nondeterministic syscall rejection.
Current Test-AI CapabilityNode and its focused tests still use R007_AUTHORITY_ESCALATION for permission escalation.
Canonical sibling ncf-governance.ts already uses R002 for authority escalation and R007 for nondeterministic syscalls.

ACTION_REQUIRED:
Reconcile stale task/lease state. Before T-2F6A7C91 can be VERIFIED, correct the narrow authority-escalation reason identity and test oracle to R002_PERMISSION_ESCALATION, run exact-SHA focused tests, obtain independent reverify, then release/reconcile CapabilityNode mutation scope for T-04452B01.

NO_DUPLICATE_FINDING: true
