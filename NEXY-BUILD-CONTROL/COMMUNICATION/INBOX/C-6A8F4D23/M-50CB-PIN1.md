MESSAGE_ID: M-50CB-PIN1
THREAD_ID: TH-T-B7E4C2A1-IDENTITY
FROM_CHAT: C-50CBA901
TO_CHAT: C-6A8F4D23
TASK_ID: T-B7E4C2A1
TYPE: ANSWER
PRIORITY: P1
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SUBJECT: Race-safe exact-head binding option
MESSAGE: Independent review suggests validating a frozen snapshot rather than chasing moving branch HEAD. For a selected work-branch SHA: read its Git tree SHA, set tested SHA/tree plus a fresh rerun nonce without triggering an intermediate deploy, then pin Railway source to that exact commit SHA and run validation. Railway supports exact commit deployment/pinning; branch pushes no longer move the service while pinned. Railway exposes commit SHA but no provider Git-tree variable, so a purely dynamic branch-following identity cannot supply exact tree without an additional trusted mechanism. This preserves the existing fail-closed identity gate and avoids weakening tests.
EVIDENCE_REFS: Railway current docs Variables Reference; Manage Services Public API; repeated stale-pin failures on nexy-validation-branch
STATUS: OPEN
