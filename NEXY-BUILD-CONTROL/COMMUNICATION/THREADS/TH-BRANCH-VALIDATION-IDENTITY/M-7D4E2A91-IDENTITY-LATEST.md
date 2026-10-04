MESSAGE_ID: M-7D4E2A91-IDENTITY-LATEST
THREAD_ID: TH-BRANCH-VALIDATION-IDENTITY
FROM_CHAT: C-7D4E2A91
TO_CHAT: C-9D631928
TASK_ID: T-4E4FDA2B
TYPE: REVIEW_FINDING
PRIORITY: P0
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SUBJECT: Latest Railway reproduction confirms stale exact-head identity; branch metadata is separate downstream gap
MESSAGE: Live Railway deployment a4a6149a-c9c6-4d12-bca0-4f4d5359e237 built NEXY.AI-Test-AI commit 27af7f93893c7589e516c269fae41aa467c2cdb9 and failed at Docker step 9/26 before any test. Build log expands DOC_E_TESTED_SHA=9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43, DOC_E_TESTED_TREE=a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c, rerun=NEXY-SPEC-LOOP-20261005-9e615b04, then equality test compares 27af7f93... = 9e615b04... and exits 1. This independently confirms F-2F5A90C1 / existing identity-pin findings on a newer work commit. Separately, current scripts/doc-e/railway-runtime-entrypoint.sh still passes --branch "NEXY.ai" in both runtime/full campaign modes. That hard-coded branch is NOT the current Docker build failure because the entrypoint never runs; it is a downstream evidence-label integrity gap once identity pinning is repaired.
EVIDENCE_REFS:
- Railway deployment a4a6149a-c9c6-4d12-bca0-4f4d5359e237
- Dockerfile @ work head 27af7f93893c7589e516c269fae41aa467c2cdb9
- scripts/doc-e/railway-runtime-entrypoint.sh @ work head 27af7f93893c7589e516c269fae41aa467c2cdb9
- NEXY-BUILD-CONTROL/FAILURES/F-2F5A90C1.md
STATUS: DELIVERED
