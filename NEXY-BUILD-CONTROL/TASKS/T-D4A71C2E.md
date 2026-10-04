TASK_ID: T-D4A71C2E
CREATOR_CHAT: C-7C4F2A91
OWNER_CHAT: C-7C4F2A91
STATUS: IMPLEMENTING
PRIORITY: P2
RISK: MEDIUM
BASE_SHA: 1adfc1c3782f63c32eaa535c05a975bd932a7015
TARGET_PATHS:
- packages/core/vnext-state-matrix.ts
- tests/contract/state-matrix.test.ts
SEMANTIC_SCOPE: Align the executable VNext transition relation to the authoritative DOC-C §5.2 matrix plus the explicitly authorized §5.4 OWNER hard-kill cancel transitions; remove unapproved error edges and add an exact-set regression test. No event-ownership, guard, freeze-reason, global error-routing, or protected-branch changes.
DEPENDENCIES:
- Authoritative Spec DOC-C §5.2 transition table
- Authoritative Spec DOC-C §5.3 illegal-transition law
- Authoritative Spec DOC-C §5.4 OWNER hard-kill law
BLOCKS: none
TEST_PLAN:
- Run targeted contract and core state-matrix tests at the resulting exact work-branch SHA.
- Inspect GitHub Actions typecheck and Contract tests for the exact resulting SHA.
- Do not claim unrelated full-branch PASS from focused evidence.
REVIEW_STATE: NOT_STARTED
LAST_PROGRESS: Reproduced a spec/source mismatch: five error→FREEZE edges exist outside the authoritative DOC-C state/event matrix; target blobs are unchanged at work HEAD 1adfc1c3782f63c32eaa535c05a975bd932a7015.
NEXT_ACTION: Recheck branch HEAD and lease set, apply the smallest transition-table repair plus exact-set regression test, then execute exact-SHA verification.
