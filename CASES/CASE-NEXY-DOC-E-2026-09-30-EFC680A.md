# CASE-NEXY-DOC-E-2026-09-30-EFC680A

CASE_ID: CASE-NEXY-DOC-E-2026-09-30-EFC680A
status: MITIGATED / EXTERNAL_RELEASE_BLOCK_REMAINS
severity: S4 release blocker
scope: DOC-E evidence convergence

## Cause
The original GitHub-hosted Actions execution plane instantiated jobs without executable steps/logs. DOC-E therefore needed an alternate real execution plane. Subsequent Railway validation exposed several harness defects before application-runtime evidence could be trusted.

## Proven incidents and recoveries
1. GitHub Actions no-step environment failure
   - jobs instantiated, steps/logs unavailable
   - classified environment-plane failure, not source-test failure
2. Railway validation image missing Prisma generation
   - typecheck produced broad Prisma type failures
   - fixed by running npx prisma generate before typecheck
3. Railway validation image missing Rust toolchain
   - contract suite failed on spawnSync cargo ENOENT
   - fixed by installing Rust stable + native/OpenSSL build dependencies
4. E7 runtime attempted npm run build:web and was SIGKILLed
   - no OOM claim made; Railway memory sample did not prove OOM
   - fixed by prebuilding exact-head web artifact in image and requiring apps/web/.next/BUILD_ID
5. E7 fixture violated production API schema/auth identity
   - API returned 422 SCHEMA_VIOLATION
   - fixed to canonical ULIDs, seeded OWNER/project identity, CSRF and device-binding cookie
6. E10/E12 receipts became stale after HEAD drift
   - stale receipts were removed, never rewritten as if current
   - real provider rollback + restore were executed to create fresh exact-head provider evidence

## Current proof
Final current-head campaign:
- deployment: 46542beb-fefb-4745-a217-42f546a103ab
- SHA: e82edcd9e6ab1322526499a45ecb72ff9a487e4a
- tree: 5cc36e3b85e775c462c4a2baf6a05abe7150f049
- E1-E10: PASS
- E11: BLOCKED_EXTERNAL
- E12: PASS
- release_authorized=false
- deploy_authorized=false
- evidence_root_sha256=3da765cb2c0123c9b718dc1f38bd16273bb03f1eba20ea9ab015cb06c774ad85
- attestation_sha256=d816e1053143e373b71b6e921ebb6b2378b3dacbff5d480cd61913972033b3a1

Provider rollback proof:
- rollback deployment 367ffe4d-794d-4d10-8c2d-e4573c6afb8a -> 45ec2284e4f8fc1062917a355152216f4b2e132e = SUCCESS
- restore deployment db54cf4f-55ae-4218-acdb-840225a2fd05 -> e82edcd9e6ab1322526499a45ecb72ff9a487e4a = SUCCESS
- E8 provider-log monitoring drill emitted all six canonical alarm classes on both validation campaigns

## Remaining condition
E11 requires authorized external engineering/security/migration signoff. It cannot be supplied by the assistant. Until E11 is valid, release and deployment remain blocked by design.

## Prevention
- keep exact-head SHA/tree/provider execution ID in every evidence record
- reject stale external receipts
- keep E3 migration rollback separate from E12 application rollback
- require real provider execution and monitoring receipts
- preserve BLOCKED_EXTERNAL instead of converting missing human authorization into PASS
