FAILURE_ID: F-4D8C1A72-CI-CONTRACT
REPORTER_CHAT: C-5A1E9C42
RELATED_TASK: T-4D8C1A72
ROUTED_TO_TASK: T-1AB7ABF2
STATUS: OPEN
SEVERITY: P1
BRANCH: NEXY.AI-Test-AI
OBSERVED_HEAD_SHA: a363fdb7b8ced513303f3e67ba4520dfcc1e9903
FAILING_TEST_COMMIT_SHA: 7297bbbff42ce8c5236c2fc551a4b29893be2a73
RAILWAY_DEPLOYMENT_IDS:
- 35cb76ff-6961-49c3-92de-ec296b896d14
- 644b3185-5d1e-4ca2-9fe5-588d127940f6
FACT:
- first deployment failed source-identity precondition before tests
- rerun reached npm run test:contract and failed tests/contract/release-attestation.test.ts
- failing case: canonical workflow targets NEXY.ai and keeps Phase-F advisory
- .github/workflows/deploy.yml currently has push.branches [NEXY.ai, NEXY.AI-Test-AI]
- release-attestation contract requires canonical workflow branch list to remain NEXY.ai only
- commit 311474744b2644229ccef26850440f02090ca97b introduced the branch-list mutation
- Pulse implementation/test blobs remain unchanged on current work branch
ASSUMPTION: NONE REQUIRED FOR REPRODUCTION
UNKNOWN:
- intended replacement mechanism for branch validation trigger without mutating canonical workflow contract
REPRODUCTION:
1. Build exact SHA 7297bbbff42ce8c5236c2fc551a4b29893be2a73 with branch validation service.
2. Ensure DOC-E source identity inputs are present so build reaches tests.
3. npm run test:contract fails release-attestation canonical workflow assertion.
SUGGESTED_DIRECTION:
- preserve canonical deploy.yml NEXY.ai-only contract
- run NEXY.AI-Test-AI validation through branch-specific external validation trigger/config rather than widening canonical deploy workflow
- rerun exact-head validation after reconciliation
PULSE_SCOPE_CAUSALITY: NO EVIDENCE OF PULSE CAUSING FAILURE
TRUE_BLOCK: FALSE
