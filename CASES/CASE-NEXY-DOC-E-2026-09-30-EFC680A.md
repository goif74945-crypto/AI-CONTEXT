# CASE-NEXY-DOC-E-2026-09-30-EFC680A

CASE_ID: CASE-NEXY-DOC-E-2026-09-30-EFC680A
status: MITIGATED / EXTERNAL_RELEASE_BLOCK_REMAINS
severity: S4 release blocker
scope: DOC-E evidence convergence
version: 3

## Cause
The original GitHub-hosted Actions plane instantiated jobs without executable steps/logs. An alternate real execution plane was required. Railway validation then exposed harness defects that were repaired without weakening production contracts.

## Proven incidents and recoveries
1. GitHub Actions no-step environment failure: environment-plane failure, not source-test failure.
2. Missing Prisma generation before typecheck: repaired in validation image.
3. Missing Rust toolchain: repaired with Rust stable + native/OpenSSL dependencies.
4. Runtime build:web was SIGKILLed: moved exact-head web build to image build phase; no unsupported OOM claim.
5. BUILD_ID guard used wrong path: corrected to apps/web/.next/BUILD_ID.
6. E7 fixture violated API schema/auth identity: corrected to canonical ULIDs, seeded OWNER/project, CSRF and device binding.
7. E7 harness missing existsSync import: repaired and contract-guarded.
8. E9 diagnostics were hardened with labelled assertions; final exact-head campaigns pass E9.
9. Stale E10/E12 receipts were blanked rather than accepted.
10. Real application rollback and restore were executed on the isolated validation service to create current provider proof.

## Latest exact-head proof
- deployment: 8d6180ec-1a6e-4fab-9c3d-19da8daf1ba6
- SHA: e82edcd9e6ab1322526499a45ecb72ff9a487e4a
- tree: 5cc36e3b85e775c462c4a2baf6a05abe7150f049
- E1-E10: PASS
- E11: BLOCKED_EXTERNAL
- E12: PASS
- release_authorized=false
- deploy_authorized=false
- blocking_reasons=[E11:BLOCKED_EXTERNAL]
- evidence_root_sha256=9fb0c7cf13d920a2dededd4ac90e39d66b7f6716d4c7cb733d700502d3a02465
- attestation_sha256=a8082bc1386cd5cb8f8c62fcf10fdd8a2082b02d13b05578d42f97e6437e5d8a

## Rollback proof
- from current deployment: 227a6752-9b4c-4671-8c71-1eaeb013b725
- rollback deployment: d16a8141-365d-4408-ab9e-4ab2ea05ac5b
- rollback target: 45ec2284e4f8fc1062917a355152216f4b2e132e
- rollback status: SUCCESS
- rollback E1-E9 including E8 monitoring: PASS
- restored/final deployment: 8d6180ec-1a6e-4fab-9c3d-19da8daf1ba6
- final E10/E12: PASS

## Remaining condition
Only E11 remains unresolved. It requires authorized external engineering/security/migration signoff and cannot be supplied, inferred, or self-signed by the assistant.

## Prevention
- exact SHA/tree/provider execution identity in every evidence record
- reject stale external receipts
- E3 migration rollback never substitutes for E12 application rollback
- provider execution and monitoring receipts must be real
- missing human authorization stays BLOCKED_EXTERNAL


## Canonical branch consolidation update
- NEXY.ai is verified as repository default/canonical branch.
- DOC-E and NEXY.ai diverged from merge base 0f9c8c65e2ab7b959f03264569430afc256f268a.
- NEXY.ai side changed 7 files; DOC-E side changed 41 files; changed-file intersection was empty.
- merged tree preserved the NEXY.ai-side blobs byte-for-byte and overlaid all DOC-E blobs byte-for-byte.
- merge commit: 6c53f51aa734c39d4e98176f7718e9597d4c59fa
- canonical cleanup commit: d7f824ed7f4b70e5308f3b8bb6a31fbf1ad0a61e
- canonical tree: 4cf698ed37f87d68df1c30a3e55bd4bd80a36c5e
- temporary refs are synchronized to canonical HEAD; they are not authority.
- post-merge Railway deployment 09da96e1-f989-43d4-9e5e-3001b5e36335 is BUILDING at this record version.
- release remains NOT AUTHORIZED until current-head validation and E11 are complete.
