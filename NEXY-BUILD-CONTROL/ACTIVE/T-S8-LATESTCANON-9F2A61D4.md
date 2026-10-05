# ACTIVE CLAIM — T-S8-LATESTCANON-9F2A61D4

- CHAT_ID: C-SOL-20261006-S8-LATESTCANON-9F2A61D4
- PROJECT: NEXY.AI / NEXY-IGNIS
- SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
- INTEGRATION_BRANCH: NEXY.AI-Test-AI
- BASE_SHA: 07dd617109fd4730582f3615cdaf2bbbe277b585
- WORKER_BRANCH: work/NEXY-AI-Test-AI/T-S8-LATESTCANON-9F2A61D4
- STATUS: FROZEN_FOR_SINGLE_BRANCH_MIGRATION
- MUTATION_SCOPE:
  - packages/api/canonical.ts
  - packages/api/artifact-list-projection.ts
  - tests/contract/artifact-list-latest-canon.test.ts
- REQUIREMENT_BINDING:
  - DOC-D S8 Artifact List / Open Artifact
  - UI truth law: displayed artifact version must come from deterministic backend truth
  - DOC-C versioning law: revisions/commits are append-only version history
- GAP:
  - handleArtifacts computes latest_canon_version with commits.at(-1) after flattening unordered Prisma relations.
  - relation result order is not an authority for recency, so the S8 card can display an older CANON version as latest.
- REQUIRED_BEHAVIOR:
  - choose latest commit deterministically by createdTick with id as a stable tie-breaker.
  - preserve total commit_count and existing artifact filtering/RBAC.
  - add executable pure contract tests with deliberately unsorted commit input.
- FORBIDDEN:
  - no NEXY.ai mutation.
  - no direct NEXY.AI-Test-AI mutation.
  - no semantic version parsing as a substitute for durable chronology.
  - no fabricated test evidence.


## Candidate evidence — 2026-10-06
- PR: https://github.com/goif74945-crypto/NEXY.AI-/pull/86
- CANDIDATE_SHA: cca8d20af2e1c48518ca46f64557f23c14153c98
- BASE_SHA: 07dd617109fd4730582f3615cdaf2bbbe277b585
- TARGET_AT_CHECK: 07dd617109fd4730582f3615cdaf2bbbe277b585
- STATIC_DIFF: 3 files; canonical.ts changes 5 lines, plus pure projection helper and isolated contract test.
- VALIDATION_STATUS: BLOCKED_INFRA; exact candidate has 0 workflow runs and 0 commit statuses.
- TEST_CLAIM: NONE. Test source exists but has not executed on an available runner.
- INTEGRATION_DECISION: FAIL_CLOSED until exact-candidate executable evidence exists.

- MIGRATION_PROPOSAL: NEXY-BUILD-CONTROL/PRODUCT-PROPOSALS/S8-ARTIFACT-LIST/C-SOL-20261006-S8-LATESTCANON-9F2A61D4/PROPOSAL-S8-LATESTCANON-9F2A61D4.json
- SOURCE_BRANCH_WRITE_ALLOWED: FALSE
- NEXT_PRODUCT_PATH: proposal review/discussion/vote/lease only
