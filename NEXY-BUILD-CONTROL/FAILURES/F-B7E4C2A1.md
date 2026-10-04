FAILURE_ID: F-B7E4C2A1
TASK_ID: T-B7E4C2A1
REPORTER_CHAT: C-6A8F4D23
NEXY_BRANCH: NEXY.AI-Test-AI
OBSERVED_HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
STATUS: INVESTIGATING
SEVERITY: P1
FAILURE_CLASS: VALIDATION_SOURCE_IDENTITY_DRIFT
SERVICE: nexy-validation-branch
RAILWAY_PROJECT_ID: 01537473-6a6d-42a0-856f-40d8a4e6a712
RAILWAY_SERVICE_ID: 3c290782-e2f0-4e5b-87d9-58bae4d4dba8
RAILWAY_ENVIRONMENT_ID: 776c1d3d-20f2-4b9f-9f07-8387ea9e63b8
PROBLEM: Work-branch deployments fail before tests because the provider commit SHA differs from stale DOC-E tested identity variables.
EXPECTED: For an exact-head branch validation run, the provider source identity and the declared tested SHA/tree must identify the same immutable source revision before gates execute.
ACTUAL: Railway builds NEXY.AI-Test-AI commits while DOC_E_TESTED_SHA remains 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43 and DOC_E_TESTED_TREE remains a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c.
REPRODUCTION:
- deployment 346815e2-d01e-4741-837a-9c389374fab5 built 47a4ab8efd7d29e9ccc20bdbd664cec486d9745b and failed test "$RAILWAY_GIT_COMMIT_SHA" = "$DOC_E_TESTED_SHA"
- deployment 6cb68813-0456-4a4f-958c-5e7be81aca71 built 670f11f9fe99ab5ae1676e5fd463d70f5ae41387 and failed the same gate
- deployment 3df8648e-cedf-4e53-923f-5234b04d3638 built 6597a53485e78021ebbca61f9a8ecc74cb90c084 and failed the same gate
- deployment faf07044-ff27-401d-b3cb-b11060f59219 built 1adfc1c3782f63c32eaa535c05a975bd932a7015 and failed the same gate
ROOT_CAUSE: The validation service follows NEXY.AI-Test-AI automatically, but DOC_E_TESTED_SHA/TREE and rerun identity remain pinned to the canonical 9e615b04 campaign. The strict source-identity guard correctly rejects the mismatch.
FACT:
- The Dockerfile explicitly requires RAILWAY_GIT_COMMIT_SHA == DOC_E_TESTED_SHA.
- Multiple Railway build logs show different work-branch commit SHAs compared against the same stale 9e615b04 value.
- Failures occur at Docker build step 9/26 before typecheck/tests/coverage.
ASSUMPTION: The branch validation service is intended to validate changing work-branch exact heads rather than remain a fixed canonical DOC-E campaign target.
UNKNOWN: The authoritative mechanism intended to atomically bind tested SHA/tree to each rapidly changing work-branch snapshot.
ATTEMPTS: Inspected GitHub CI, Railway deployment metadata, build logs, service configuration, Dockerfile, runtime entrypoint, and existing control tasks.
ALTERNATIVES_TRIED: GitHub Actions cannot provide runtime gate evidence for the same heads because jobs currently terminate with runner_id=0, steps=[], and no log blob; Railway provides executable build evidence but is rejected by identity drift.
AFFECTED_PATHS: Dockerfile; scripts/doc-e/railway-runtime-entrypoint.sh; Railway nexy-validation-branch configuration
AFFECTED_REQUIREMENTS: exact-head evidence; fail-closed deterministic validation; no fake PASS
DOWNSTREAM_BLOCKED: exact-head Railway validation evidence for current work-branch commits
INDEPENDENT_WORK_NOT_BLOCKED: source implementation, reviews, static inspection, independent tests on other available runners
TEMP_WORKAROUND: None accepted. Manually chasing a fast-moving branch with static tested SHA/tree variables is not yet proven race-safe.
EVIDENCE_REFS: Railway deployments 346815e2-d01e-4741-837a-9c389374fab5, 6cb68813-0456-4a4f-958c-5e7be81aca71, 3df8648e-cedf-4e53-923f-5234b04d3638, faf07044-ff27-401d-b3cb-b11060f59219; Dockerfile source-identity gate
NEXT_ACTION: Establish a race-safe exact-head binding design that preserves strict identity, then execute and verify it.
