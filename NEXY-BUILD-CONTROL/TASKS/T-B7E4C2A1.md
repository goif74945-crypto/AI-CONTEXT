TASK_ID: T-B7E4C2A1
CREATOR_CHAT: C-6A8F4D23
OWNER_CHAT: C-6A8F4D23
STATUS: INSPECTING
PRIORITY: P1
RISK: HIGH
BASE_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
TARGET_PATHS: Railway service nexy-validation-branch exact-head validation configuration; Dockerfile and scripts/doc-e/railway-runtime-entrypoint.sh READ ONLY unless a proven source defect requires a separate reconciled mutation
SEMANTIC_SCOPE: Restore exact-work-branch validation so Railway validates the commit it actually builds, without weakening DOC-E fail-closed source identity, mutating NEXY.ai, lowering tests, or silently reusing canonical upstream identity.
DEPENDENCIES: Railway project 01537473-6a6d-42a0-856f-40d8a4e6a712; service 3c290782-e2f0-4e5b-87d9-58bae4d4dba8; environment 776c1d3d-20f2-4b9f-9f07-8387ea9e63b8
BLOCKS: Exact-head validation evidence for NEXY.AI-Test-AI
TEST_PLAN: Prove deployment metadata commitHash equals target SHA; prove build source-identity gate receives matching tested SHA/tree; then require actual downstream gates to execute. Never treat build admission as PASS for the product.
REVIEW_STATE: SELF_INSPECTION; independent review requested via broadcast
LAST_PROGRESS: Reproduced deterministic Railway BUILD_IMAGE failure across 47a4ab8e, 670f11f9, 6597a534, and 1adfc1c3 because DOC_E_TESTED_SHA remains 9e615b04 while Railway builds work-branch commits.
NEXT_ACTION: Determine the intended exact-head binding mechanism from current authority and provider configuration; repair configuration or source only if the fix preserves strict identity and can survive high-concurrency branch movement.
