# Execution 008 CROSS — REAL REPO-LINKED RED/GREEN (NOT PRODUCTION)
Product HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Control precommit HEAD: fdb9ebf97ac7e993bdcf656c87c268ee7ab71ed2
Task ID: 20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS
Canonical DOCX SHA256 matched in this conversation: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE: NEXY.ai packages/queue/dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29; local patched blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af.

## Executable environment
Connected authorized remote device DESKTOP-FOB7IK8, Windows 10 Pro, Node v24.21.0, npm 11.19.0, Vitest 4.1.11, Prisma 5.22.0. Cloned fresh NEXY.ai HEAD into private isolated temporary directory NEXY-EX008-CROSS-SAFE-QUEUE-1953, not reused after detecting another writer in earlier checkout. npm.cmd ci --no-audit --no-fund exit 0; 396 packages. No Docker, psql or redis-server observed in device tool probe. No shared/production database used.
## RED: production source still original, tests call actual exports
Command: node node_modules/vitest/vitest.mjs run tests/integration/queue-cancel-race-008-cross.spec.ts --reporter=verbose (Vitest root = isolated checkout)
BEFORE source blob: 002eef253ce836e2cd0e200f5d15cb5042cdeb29
Raw summary: Test Files 1 failed (1); Tests 5 failed | 4 passed (9); RED_TEST_EXIT=1.
Observed failures: CANCELLED overwritten ENQUEUED, CANCELLED overwritten FAILED, PROCESSING overwritten ENQUEUED, duplicated attempts (2 vs 1), legacy path lacks CAS failure propagation. Explicitly expected RED for new regression; not 5 unrelated product failures.
## GREEN: patch applied to isolated checkout only
Candidate patch EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cas.patch; git apply --check exit 0; git apply exit 0; git diff --check exit 0. Patched Git blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af; changed 1 source file, 55 additions/21 removals. Same test file: Test Files 1 passed, Tests 9 passed (9), GREEN_TEST_EXIT=0.
## Additional executed regression and type gate
Prisma CLI generate --schema prisma/schema.prisma exit 0. Initial tsc without generated client failed with many missing Prisma types (setup failure); rerun after generation: node node_modules/typescript/bin/tsc --noEmit --project tsconfig.json exit 0.
4-file queue suite: new actual dispatch.ts linked 9 tests + tests/contract/failed-dispatch-retry.test.ts (3) + tests/integration/queue-boundary.spec.ts (4) + tests/contract/queue-active-cancellation-wiring.test.ts (1) = Tests 17 passed (17), exit 0. Worker boundary tests intentionally mock BullMQ; no live provider, DB or Redis.
## Critical absence of cross-store proof
PostgreSQL+Redis real integration NOT_RUN, E7 remote current-head job failure with no executed steps; cannot conclude published Redis job/DB CAS conflict, worker cancellation, outbox recovery, release-atomicity verified. Patch is a TESTED_MOCK_CANDIDATE, NOT a production fix.
## CI and Cage
Current head 44bcb851 five GitHub Actions run IDs 37741650355/349/343/376/318 concluded failure. Inspected job steps=[]; exact-head/e7 job log fetch returned 404 BlobNotFound, infra ROOT_CAUSE_UNKNOWN. cage.ts blob 5afd464ed39470381ef1df643a630e1f431817dc: bwrap unavailable path directly spawns command, cgroup errors ignored, seccomp JSON written without enforced syscall filter shown. No Linux negative execution, no cage patch.
## Source fence and release
No product commit or product branch change, no settings/protection/secret modification. TSA core authority unchanged, signature relation unresolved. DOC-E release UNAUTHORIZED. 98-row TSV attached with 16 targeted rows inspected to limited source/test/infra depth and 82 rows clearly NOT_REASSESSED; no mass promotion. Assessed completion percent NOT_COMPUTABLE. Evidence not a release attestation.
## Local binary/test provenance
Remote test blob e64653d893e5403ebf60505303c63a590a8cdcf5; remote patch blob b7c9444d4348fd84691cea287c9477e6c90dd734. Read-back original GitHub files before patch and reran Git blob before RED; candidate only exists in temp checkout and in coordination repo after commit.
