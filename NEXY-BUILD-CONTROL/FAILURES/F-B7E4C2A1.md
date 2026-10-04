FAILURE_ID: F-B7E4C2A1
TASK_ID: T-B7E4C2A1
REPORTER_CHAT: C-6A8F4D23
NEXY_BRANCH: NEXY.AI-Test-AI
OBSERVED_HEAD_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c
STATUS: RESOLVED
SEVERITY: P1
FAILURE_CLASS: VALIDATION_SOURCE_IDENTITY_DRIFT
SERVICE: nexy-validation-branch
RAILWAY_PROJECT_ID: 01537473-6a6d-42a0-856f-40d8a4e6a712
RAILWAY_SERVICE_ID: 3c290782-e2f0-4e5b-87d9-58bae4d4dba8
RAILWAY_ENVIRONMENT_ID: 776c1d3d-20f2-4b9f-9f07-8387ea9e63b8
PROBLEM: Work-branch deployments previously failed before tests because provider commit SHA differed from stale DOC-E tested identity variables.
ROOT_CAUSE: The branch validation service auto-followed NEXY.AI-Test-AI while DOC_E_TESTED_SHA/TREE remained pinned to canonical 9e615b04/a809bc5f. The strict source-identity guard correctly rejected the mismatch.
RESOLUTION:
- freeze immutable work snapshot 5034debdadb1f21c7d5312e6f0ad7fd44280718c
- bind DOC_E_TESTED_SHA to 5034debdadb1f21c7d5312e6f0ad7fd44280718c
- bind DOC_E_TESTED_TREE to eabc3e62cf336d33de49373050f66a19ce5ff86b
- set fresh rerun nonce without intermediate deployment
- pin Railway source to exact commit 5034debdadb1f21c7d5312e6f0ad7fd44280718c
- use a non-attesting branch-validation runtime so canonical NEXY.ai DOC-E provenance is not falsely emitted for NEXY.AI-Test-AI
VERIFICATION: Railway deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8 executed Dockerfile step 9/26 with RAILWAY_GIT_COMMIT_SHA == DOC_E_TESTED_SHA == 5034debd... and completed that identity gate successfully. Build then advanced through executable gates and failed later at step 15/26 npm run test:contract, proving the identity blocker itself was removed.
NEW_FAILURE_CLASS: SOURCE_CONTRACT_FAILURE surfaced after infrastructure repair; 3 test files / 5 assertions failed. State-transition failures were handed to T-D4A71C2E and the conflicting Rust task T-A6C4E9B2 was warned against mirroring the TypeScript regression. See F-6A8F5C4D.
FACT:
- identity gate passed on the frozen snapshot
- source contract suite executed
- contract suite failed for source semantics, not provider identity
ASSUMPTION: None required for identity-drift resolution.
UNKNOWN: Remaining exact-head source test status after active state-matrix repairs land.
EVIDENCE_REFS: Railway deployment 0dc3d4f6-8e94-4446-b309-64536cee30b8; F-6A8F5C4D; M-6A8F5C4D
NEXT_ACTION: Keep the provider frozen for reproducibility until a repaired immutable work snapshot is selected; then repeat exact SHA/tree binding and executable validation.
