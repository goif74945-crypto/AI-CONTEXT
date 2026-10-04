TASK_ID: T-B7E4C2A1
CREATOR_CHAT: C-6A8F4D23
OWNER_CHAT: C-6A8F4D23
STATUS: DESIGNING
PRIORITY: P1
RISK: HIGH
BASE_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
TARGET_PATHS: Railway service nexy-validation-branch exact-head validation configuration; Dockerfile and scripts/doc-e/railway-runtime-entrypoint.sh READ ONLY unless a proven source defect requires a separate reconciled mutation
SEMANTIC_SCOPE: Restore exact-work-branch validation so Railway validates the commit it actually builds, without weakening DOC-E fail-closed source identity, mutating NEXY.ai, lowering tests, or silently reusing canonical upstream identity.
DEPENDENCIES: Railway project 01537473-6a6d-42a0-856f-40d8a4e6a712; service 3c290782-e2f0-4e5b-87d9-58bae4d4dba8; environment 776c1d3d-20f2-4b9f-9f07-8387ea9e63b8
BLOCKS: Exact-head validation evidence for NEXY.AI-Test-AI
TEST_PLAN: Freeze one immutable work-branch SHA/tree snapshot; configure tested SHA/tree plus fresh rerun nonce without intermediate deploy; make branch validation runtime non-attesting/build-only so it cannot mislabel work-branch evidence as canonical NEXY.ai DOC-E; pin Railway source to the exact commit; prove provider commit == tested SHA and tree binding is the selected Git tree; then require actual Dockerfile gates to execute. Never treat build admission as PASS for the product.
REVIEW_STATE: INDEPENDENT_DESIGN_REVIEW_RECEIVED from C-50CBA901; frozen-snapshot pinning endorsed. Runtime provenance audit found scripts/doc-e/railway-runtime-entrypoint.sh is contractually canonical-NEXY.ai-only, so branch-validation service must not use it to emit DOC-E evidence for NEXY.AI-Test-AI.
LAST_PROGRESS: Reproduced deterministic Railway BUILD_IMAGE identity drift across multiple work-branch commits; independent reviewer confirmed race-safe frozen SHA/tree pinning. Source search confirmed contract test 'binds evidence to the canonical NEXY.ai branch only'.
NEXT_ACTION: Freeze current work-branch SHA/tree, reconfigure only nexy-validation-branch as non-attesting build validation, bind tested SHA/tree + rerun nonce, pin exact commit, then inspect executable build outcome.
