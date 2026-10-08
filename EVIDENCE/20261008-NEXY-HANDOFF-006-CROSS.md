# NEXY HANDOFF 006 CROSS — source evidence (2026-10-08)
STATUS: PARTIAL / EVIDENCE_ONLY / NOT_PROD_READY
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
PRODUCT_HEAD_SNAPSHOT: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_REPO: goif74945-crypto/AI-CONTEXT
CONTROL_HEAD_PREWRITE: 0f17aa37322d8b9a6e1b21dc94cafc44176079a3
SPEC_UPLOADED_FILENAME: แอป [NEXY-IGNIS] ที่กำลังพัฒนา(20261008-072414).docx
SPEC_SHA256_COMPUTED_THIS_CHAT: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_HASH_MATCH: YES (direct local hash, not other-chat assertion)
SPEC_PARAGRAPHS: 12537; P09844 BUILD obligations DOC-C only; P09845 DEPLOY authority DOC-E only.
DOC_C_DEFAULTS P09932=OTAC TTL 300000; P09936=session TTL 21600000; P09946=queue TTL 900000; P09947=max concurrency 10.
DOC_E P10977-P10982 requires engineering/security/migration signoffs, rollback and monitoring verification. No release approval established.
SOURCE_COMMIT: https://github.com/goif74945-crypto/NEXY.AI-/commit/44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
BASE_COMPARE: 8b406a63f10aa1424225a80453393af2e4cb78b5...44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 ahead=1; behind=0; 5 files changed.
BLOB_SHA_1: packages/api/auth.ts e1c8c3edbb219d8d584682983cc0996b8f834934
BLOB_SHA_2: packages/phase-f/lo3/cage.ts 5afd464ed39470381ef1df643a630e1f431817dc
BLOB_SHA_3: tests/integration/auth/single-use-and-logout-replay.spec.ts 33660427806d9b8bf8c29e69e549444d246be29a
BLOB_SHA_4: packages/queue/dispatch.ts 002eef253ce836e2cd0e200f5d15cb5042cdeb29
BLOB_SHA_5: packages/queue/workers.ts 3134e7b6bf83f7200959e3e267b28f5ea28b6392
BLOB_SHA_6: packages/core/tick.ts 517614809c8cefa3e516348b1268f6dca4a744e5
BLOB_SHA_7: packages/api/vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b
NOTE: above BLOB_SHA values are Git object SHAs, not SHA-256 content digests.
SOURCE_FINDING_AUTH: auth.ts lines 847-864 conditional otacPending.updateMany consumed=false, failedAttempts<max and expiresAt>new Date(), inside Serializable transaction before session creation. New tests use in-memory mock; NO REAL DATABASE RACE TEST executed in this chat.
SOURCE_FINDING_LOGOUT: auth.ts lines 1283-1295 requires idempotency requestId/action/actor/resourceKind/resourceId/outcome and branch checks session.revoked before replay success.
SOURCE_FINDING_QUEUE_RISK: dispatch.ts lines 110-182 reads row before enqueueDirective await; success update where only id and catch failure update where only id. Concurrent CANCELLED transition may be overwritten by ENQUEUED or FAILED. THIS IS A SOURCE-REACHABLE INTERLEAVING, NOT A MEASURED INCIDENT. See CASES companion.
SOURCE_FINDING_BWRAP: cage.ts lines 287-312 bwrap probe; 319-367 trusted command; 527-568 Linux path falls through to direct spawn(trustedCommand.executable) when bwrap unavailable; seccompJson written but no visible application to process in examined Linux path. Isolation compliance NOT_VERIFIED.
SOURCE_FINDING_TSA: tick.ts currentTsaBatchTimeMs throws TSA_BATCH_TIME_REQUIRED absent injection; dispatch.ts transforms to TSA_TIME_AUTHORITY_UNAVAILABLE. workers.ts validates before consume using injected TSA boundary. DOC-C supplies TTL, no literal explicit queue TSA signature verification clause. Do not substitute host clock or fake TSA.
SOURCE_FINDING_CI: GitHub combined-status API returned statuses=[] and commit workflow-runs API returned [] (tool only returns PR-triggered first-page runs, so this is NOT proof no CI). Repo Code Bridge ci_dispatch call for exact-head-evidence workflow returned 403 REPOSITORY_READ_ONLY despite repo_status advertising ALLOW. Actual current-head CI run evidence unavailable in this chat.
TESTS_EXECUTED_PRODUCT: NONE. SOURCE CONTRACT REVIEW ONLY. Local MODEL-ONLY state interleaving asserts id-only overwrite and CAS preservation; not production/Prisma/Redis test.
HISTORICAL_MATRIX_SOURCE: EVIDENCE/20261008-NEXY-CONTINUOUS-REPAIR-EXECUTION-003.tsv at control HEAD 0f17aa37322d8b9a6e1b21dc94cafc44176079a3; 98 rows, VERIFIED 14, PARTIAL 9, MISMATCH 4, NOT_VERIFIED 62, SPEC_SOURCE_ACCESS_BLOCKED 4, INFRA_BLOCKED 5; historical at 8b406a63, NOT new-head certification.
CURRENT_HEAD_MATRIX_COMPLETION_PERCENT: NOT_COMPUTABLE until requirements are re-assessed and tested; do not reuse old 51.9% as current.
RELEASE_AUTHORIZED: FALSE; DEPLOY_AUTHORIZED: FALSE.
