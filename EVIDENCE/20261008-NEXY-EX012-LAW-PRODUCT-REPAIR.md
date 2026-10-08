# EX012 LIVE PRODUCT REPAIR EVIDENCE
TASK_ID: 20261008-NEXY-EX012-LAW-PRODUCT-REPAIR
MODE: ทำ / EXECUTE_NOW / CROSS / SOURCE_FENCED / ACTUAL_EXECUTION
STATUS: LAW_LOCAL_REPAIR_VERIFIED_WITH_LIMITS; GLOBAL_PRODUCT_NOT_READY

## Source and authority
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.ai (only authorized product branch)
INITIAL_PRODUCT_HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
NEW_PRODUCT_HEAD: 90fac4835788e867559858fc92d093ded3dcb1eb
CONTROL_INITIAL_HEAD: 4f31a7ca1c5ad0c23c6d96860e57ebe72dd0d64e
AUTHORITATIVE_DOCX_SHA256_LOCALLY_COMPUTED: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
DOC_C_RELEVANT: P9916 quorum_min=2, P9917 evidence_min=2 (1-based python-docx paragraphs). Broader consensus requirement P8609 quorum_satisfied + release_policy_passed. This is source-grounded guard; not proof of all 98 requirements.

## Real connected plugin and independent tests
RUNNER: connected Remote Desktop Commander DESKTOP-FOB7IK8 Windows, Node v24.21.0. Fresh isolated clone directory NEXY-EX012-LAW-2235. Git clone HEAD and law blob verified against Github. npm installed test dependencies; initial npm --ignore-scripts omitted Prisma client so two related suites initially failed on missing .prisma/client/default; fixed via real Prisma CLI generate exit0. No code assertions weakened.
OLD_SOURCE_BLOB: f0ae1b06774e11cb2c0f417bc36c0d398347b036
PATCH_SOURCE_AI_CONTEXT: PATCHES/011/ex011-law-quorum-cardinality.patch SHA d9247cf4f91c624683d21c3a4225510cd32b0822
NEW_SOURCE_BLOB: 696acae9428a347e91eb32a26b692f6d913f1bf0
TEST_BLOB: 417f3932f3eaf649eb11e56963838727f3537f67
RED_COMMAND: node node_modules/vitest/vitest.mjs run tests/contract/ex011-law-quorum-cardinality.test.ts --reporter=dot
RED_RESULT: 2 failed, 3 passed / 5, actual original exported Product LAW source. Failing assertions were impossible quorumCount>agentIds cases.
PATCH_APPLY: git apply --check, git apply, git diff --check exit0; hash-object resulting source matched NEW_SOURCE_BLOB.
GREEN_COMMAND: node node_modules/vitest/vitest.mjs run tests/contract/ex011-law-quorum-cardinality.test.ts tests/contract/release-spine.test.ts tests/contract/runtime-config-consumers.test.ts tests/coverage/core-state-matrix.test.ts tests/coverage/judge-law.test.ts --reporter=dot
GREEN_RESULT: 5 files, 58/58 passed. Combined same-process backend typecheck exit0:
node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
BROAD_COMMAND: node node_modules/vitest/vitest.mjs run tests/contract tests/coverage --reporter=json --outputFile=EX012-BROAD.json
BROAD_RESULT: 911 total tests, 905 pass, 6 fail; 300 suites, 8 suite failures.
FAILED_TEST_CASES: core-kernel-no-authoritative-rng.test.ts cargo ENOENT; core-kernel-rust.test.ts cargo ENOENT; core-kernel-tier-depth-compile.test.ts two failed (spawn/compilation result unavailable); current-head-attestation.test.ts two failed (exit code 1 in fixture). These failures are outside the modified LAW file by test name and assertion, but full root causes are NOT_VERIFIED. Do not call broad gate passed.
CURRENT_HEAD_ACTIONS: 4 observed workflows concluded failure; exact HEAD evidence run 37811868233 job 113430495465 steps=[], runner_name empty. Root cause UNKNOWN.

## Actual Product mutation
GITHUB_API_TRANSACTION: source blob 696acae9428a347e91eb32a26b692f6d913f1bf0 and test blob 417f3932f3eaf649eb11e56963838727f3537f67 used in one Git tree 4e04321dc95e289eff2c0e3cff5868427626a6db; commit 90fac4835788e867559858fc92d093ded3dcb1eb parent 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08. update_ref branch NEXY.ai expected_sha=old HEAD force=false success. GitHub read-back HEAD and both source blobs verified.
PRODUCT_CHANGED:
- packages/law/prerelease.ts
- tests/contract/ex011-law-quorum-cardinality.test.ts
NO OTHER PRODUCT FILE CHANGE. NO NEW BRANCH. NO DEPLOY.
SOURCE_CHANGE: add quorumCount <= count of supplied distinct validated agentIds to isReleaseCandidate. No lowering DOC-C default release threshold, no disabling assertions.
RELEASE: NOT_AUTHORIZED by DOC-E; PG/Redis G3 NOT_RUN; production worker/Cage NOT_VERIFIED.
AUDIT: 7 newly inspected current-head metadata/source/test rows out of 98 identified; remaining 91 NOT_REASSESSED_012. This is mixed-depth audit, NOT completion. Assessed completion NOT_COMPUTABLE.
