TASK_ID: T-B7E4C2A1
CREATOR_CHAT: C-6A8F4D23
OWNER_CHAT: C-6A8F4D23
STATUS: TESTING
PRIORITY: P1
RISK: HIGH
BASE_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
TARGET_PATHS: Railway service nexy-validation-branch exact-head validation configuration; Dockerfile and scripts/doc-e/railway-runtime-entrypoint.sh READ ONLY unless a proven source defect requires a separate reconciled mutation
SEMANTIC_SCOPE: Restore exact-work-branch validation so Railway validates the commit it actually builds, without weakening DOC-E fail-closed source identity, mutating NEXY.ai, lowering tests, or silently reusing canonical upstream identity.
DEPENDENCIES: Railway project 01537473-6a6d-42a0-856f-40d8a4e6a712; service 3c290782-e2f0-4e5b-87d9-58bae4d4dba8; environment 776c1d3d-20f2-4b9f-9f07-8387ea9e63b8
BLOCKS: Exact-head validation evidence for NEXY.AI-Test-AI
TEST_PLAN: Frozen snapshot 5034debdadb1f21c7d5312e6f0ad7fd44280718c / tree eabc3e62cf336d33de49373050f66a19ce5ff86b. Require provider commit == tested SHA, source-identity gate success, then actual downstream Dockerfile gates through build completion. Never treat identity admission alone as product PASS.
REVIEW_STATE: INDEPENDENT_DESIGN_REVIEW_RECEIVED from C-50CBA901; frozen-snapshot pinning endorsed. Runtime provenance audit confirmed scripts/doc-e/railway-runtime-entrypoint.sh is canonical-NEXY.ai-only, so branch validation runtime was changed to non-attesting health runtime rather than emit false DOC-E provenance.
LAST_PROGRESS: Applied provider-only repair. Service source pinned exactly to 5034debd; DOC_E_TESTED_SHA=5034debd; DOC_E_TESTED_TREE=eabc3e62; fresh rerun nonce set without intermediate deploy. Deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8 executed Dockerfile step 9/26 with RAILWAY_GIT_COMMIT_SHA == DOC_E_TESTED_SHA and completed the identity gate successfully; build advanced to cargo check (step 11/26) with no errors observed.
NEXT_ACTION: Continue executable build verification through remaining gates; record exact failure if any, otherwise require successful deploy/health before PASS.
