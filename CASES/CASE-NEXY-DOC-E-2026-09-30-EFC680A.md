# CASE-NEXY-DOC-E-2026-09-30-EFC680A

CASE_ID: CASE-NEXY-DOC-E-2026-09-30-EFC680A
status: MITIGATED / EXTERNAL_RELEASE_BLOCK_REMAINS
severity: S4 release blocker
scope: DOC-E evidence convergence
version: 2

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
