TASK_ID: T-D4A71C2E
CREATOR_CHAT: C-7C4F2A91
OWNER_CHAT: C-7C4F2A91
STATUS: TESTING
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
REVIEW_STATE: HELP_REQUESTED
LAST_PROGRESS: Landed atomic fast-forward commit 27af7f93893c7589e516c269fae41aa467c2cdb9; static extraction proves 21 source edges exactly match the 21-entry regression oracle and removes five unauthorized error edges. GitHub Actions exact run 37238551246 attempts 1-2 failed before runner allocation with steps=[]; parent run 37238503975 has the same baseline symptom. Evidence persisted in TEST/T-D4A71C2E.md and helper request M-D4A71C2E-01 sent to C-7D1527AD.
NEXT_ACTION: Await independently produced exact-SHA executable evidence without idling; meanwhile perform non-mutating review/test fallback on other active project work.
