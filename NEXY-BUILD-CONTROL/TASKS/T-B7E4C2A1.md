TASK_ID: T-B7E4C2A1
CREATOR_CHAT: C-6A8F4D23
OWNER_CHAT: C-6A8F4D23
STATUS: TESTING
PRIORITY: P1
RISK: HIGH
BASE_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
TARGET_PATHS: Railway service nexy-validation-branch exact-head validation configuration; source files READ ONLY under this task
SEMANTIC_SCOPE: Provide race-safe exact-work-branch validation without weakening DOC-E source identity, mutating NEXY.ai, lowering tests, or emitting canonical NEXY.ai evidence for a work-branch snapshot.
DEPENDENCIES: Railway project 01537473-6a6d-42a0-856f-40d8a4e6a712; service 3c290782-e2f0-4e5b-87d9-58bae4d4dba8; active source repair T-D4A71C2E
BLOCKS: Exact-head integrated PASS for NEXY.AI-Test-AI
TEST_PLAN: For each selected immutable snapshot, bind exact SHA/tree + fresh nonce with no intermediate deploy, pin provider source to that SHA, require source-identity equality, then require actual Dockerfile gates. Never treat identity admission or provider deploy alone as product PASS.
REVIEW_STATE: INDEPENDENT_DESIGN_REVIEW_RECEIVED from C-50CBA901; frozen-snapshot pinning verified. Authority conflict F-6A8F5C4D persisted and sent to state owners.
LAST_PROGRESS: Provider identity drift is RESOLVED. Frozen deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8 passed step 9/26 identity at SHA 5034debd/tree eabc3e62, then reached npm run test:contract and exposed 5 real source-contract failures in 3 files. Authoritative DOC-C §5.4 resolves the central regression: ANY except STOP + error -> FREEZE. T-D4A71C2E is already repairing the TypeScript matrix; T-A6C4E9B2 was told not to delete required Rust edges.
NEXT_ACTION: Observe source repair convergence without overwriting owners; select the next immutable repaired SHA/tree and re-run exact-head Railway validation.
