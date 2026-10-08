# TASK 20261008-NEXY-EX012-LAW-PRODUCT-REPAIR
TITLE: Fix LAW quorum cardinality in Product with actual plugin tests.
MODE: ทำ / CROSS / ACTUAL_IMPLEMENTATION
SCOPE: NEXY.AI-/NEXY.ai LAW release candidate validation; write AI-CONTEXT/main only for audit records.
INPUTS: user-provided EX011 worker report, authoritative DOCX, original current GitHub LAW source, previous patch/test from AI-CONTEXT.
OUTPUT: Actual NEXY.ai commit 90fac4835788e867559858fc92d093ded3dcb1eb, 2 Product files modified/created; EVIDENCE and 98-row scoped matrix.
ACTIONS: Connected GitHub live HEAD/source, connected Desktop Commander, cloned checkout, npm deps, copied exact regression, ran RED, applied exact patch, recovered Prisma generation, reran GREEN 58/58 and backend tsc=0, ran broad 905/911, created and fast-forwarded atomic GitHub commit with expected head; read back source/test blobs.
TESTS: targeted RED 2 failed 3 pass; GREEN 58/58; backend TypeScript exit0; broad 6 failures and 905/911 passes, not full pass.
SUCCESS: Actual minimal Product source and regression commit verified.
FAILURES: 2 cargo ENOENT, 2 tier-depth, 2 current-head attestation in broad tests. PG/Redis G3 not run. CI pre-step failed. DOC-E blocked.
RISKS: wider runtime and release unverified, CI root cause unknown, product is not production-ready.
ROLLBACK: review latest NEXY.ai head and revert only commit 90fac4835788e867559858fc92d093ded3dcb1eb with new forward commit after authority and tests; do not force/reset.
STATUS: VERIFIED_WITH_LIMITS_PRODUCT_LOCAL_REPAIR / RELEASE_BLOCKED.
DATE_SOURCE: 2026-10-08 Asia/Bangkok conversation.
TRACE_ID: 20261008-NEXY-EX012-LAW-PRODUCT-REPAIR
