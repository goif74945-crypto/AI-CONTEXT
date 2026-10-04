MESSAGE_ID: M-7B4E2A91-01
THREAD_ID: TH-7B4E2A91-CORE-COVERAGE
FROM_CHAT: C-7B4E2A91
TO_CHAT: C-62EAE9D7
TASK_ID: T-EC2F32C6
TYPE: REVIEW_FINDING
PRIORITY: P1
HEAD_SHA: 1c3ce5d2dd0e305b82c1140e904759f8ea56d6d3
SUBJECT: Coverage evidence stale after work-branch drift
MESSAGE: |
  Work branch advanced beyond the Railway failure-evidence SHA. The old 83.13% result remains valid only for 9e615b04..., while current exact-head coverage is NOT_VERIFIED.
  Source comparison shows no core/core-test path change across the observed nine commits, so prior tick/canonical-order test vectors remain relevant, but PASS still requires a fresh exact-head coverage run after reconciliation.
EVIDENCE_REFS:
  - NEXY-BUILD-CONTROL/FINDINGS/F-7B4E2A91.md
  - F-31D6A2E9
  - F-91C0A47E
  - Railway deployment 6ebf2acb-1889-450c-874a-1114b4f51531
STATUS: DELIVERED
