FINDING_ID: F-C-SOL-0616-VALIDATION-BRANCH-METADATA-01
CREATOR_CHAT: C-SOL-20261005-0616-V11
STATUS: OPEN
PRIORITY: P1
CLASS: EXTERNAL_EVIDENCE_IDENTITY_DEFECT
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_EPOCH: EPOCH-20261005-b35ee1bf-608426cb
SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE: e7f603d06db6475a4d72f5d0aed752213d17eb16
CONTROL_HEAD_OBSERVED: 1b8a6f00a01044dfd5d0a53d0a88f65a31a0f92e

## Finding
scripts/doc-e/railway-runtime-entrypoint.sh invokes scripts/doc-e/run-campaign.ts with --branch "NEXY.ai" in both runtime and full modes even when the validation deployment/source target is NEXY.AI-Test-AI.

## Evidence
Dockerfile requires RAILWAY_GIT_COMMIT_SHA, DOC_E_TESTED_SHA, DOC_E_TESTED_TREE, and NEXY_VALIDATION_RERUN and fails closed unless RAILWAY_GIT_COMMIT_SHA equals DOC_E_TESTED_SHA.
The runtime entrypoint independently checks provider/runtime identity, but campaign metadata is still emitted with the hard-coded branch name NEXY.ai.

## Impact
A successful Test-AI validation can produce branch metadata naming NEXY.ai, weakening external-evidence target identity and traceability even when commit/tree identity is exact.

## Constraints
Do not weaken or remove exact-SHA identity checks.
Do not mutate protected upstream NEXY.ai.
T-4E4FDA2B is review-only, so no source repair is performed by this reviewer.

## Required next step
Validation/source owner should determine whether campaign branch must be parameterized from an explicit validated branch identity and add a negative/identity regression test. Any repair must preserve fail-closed SHA/tree binding.
