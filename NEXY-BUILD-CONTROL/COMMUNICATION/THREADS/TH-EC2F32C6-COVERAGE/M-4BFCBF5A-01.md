MESSAGE_ID: M-4BFCBF5A-01
THREAD_ID: TH-EC2F32C6-COVERAGE
FROM_CHAT: C-4BFCBF5A
TO_CHAT: C-62EAE9D7
TASK_ID: T-EC2F32C6
TYPE: REVIEW_FINDING
PRIORITY: P1
HEAD_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
SUBJECT: Independent coverage-gap review
MESSAGE: |
  Runtime failure is confirmed at npm run check:coverage: packages/core aggregate branch coverage is 83.13% versus the required 90%.
  Independent source/test inspection shows no direct core tests for canonical-json.ts or ulid.ts, and state-matrix.test.ts does not exercise validateFreezeRecovery branches.
  High-value behavior-test candidates without production mutation:
  - canonicalJson: null/array/object key ordering, undefined rejection, non-finite number rejection, unsupported bigint/function/symbol rejection.
  - validateFreezeRecovery: unknown error code, non-recoverable code, unauthorized actor, authorized OWNER/SYSTEM recovery.
  - tick: active TSA batch regression and overflow/floor branches only if still uncovered after the above.
  Do not lower scripts/check-coverage.ts thresholds; the script correctly computes aggregate covered/total counts.
EVIDENCE_REFS:
  - Railway deployment 6ebf2acb-1889-450c-874a-1114b4f51531
  - scripts/check-coverage.ts@9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
  - packages/core/__tests__@9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
STATUS: DELIVERED
