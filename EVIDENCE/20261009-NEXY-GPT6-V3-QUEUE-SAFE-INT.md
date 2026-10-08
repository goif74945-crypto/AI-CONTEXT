# EX V3 BUILDER: Queue FAILED retry safe integer guard
PRODUCT=NEXY.AI-/NEXY.ai; HEAD=8ed9af89f68fb82f60d4a4f5ccbc06005ce91992; PRODUCT_WRITE=NONE
SOURCE=packages/queue/retry-policy.ts; verified Git blob 3888169fc88784c999c31ff0f19ad673ba0e0f11
TEST_EXISTING=tests/contract/failed-dispatch-retry.test.ts blob e555aa85cc90dc80d4b8670317f39c90ba15715d
CALLER=packages/queue/dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29
DEFECT=isFailedDispatchRetryPolicy accepts Number.isInteger(maxAttempts) even when > Number.MAX_SAFE_INTEGER, not a safely representable retry cap. Dispatch uses policy cap in Prisma selector.
PATCH=replace Number.isInteger with Number.isSafeInteger for policy maxAttempts and dispatch row attempts without widening retryable error allowlist or weakening disabled policy.
SOURCE_CANDIDATE_GIT_BLOB=9eb00e4cad9c5a284e64dccf8a8a2f4753f7882f
TEST_CANDIDATE_GIT_BLOB=c0c65649158e10f8e972cabe426c5ba4986eaa7f
PATCH_CANDIDATE_GIT_BLOB=595f15c1b3802e056070d6104e03cc2412e5025a
RUNNER=isolated Linux Node22.16.0 git2.47.3. Local node:test RED:5/6 pass 1 fail exit1. GREEN:6/6 pass exit0. Standalone tsc --noEmit --strict --target ES2022 --module NodeNext --moduleResolution NodeNext --skipLibCheck packages/queue/retry-policy.ts exit0. git apply --check exit0; git apply exit0; resulting source blob matched.
REAL_PRODUCT_VITEST=NOT_EXECUTED; current-head DB integration NOT_EXECUTED; no authorized isolated PG/Redis; no Product commit because required acceptance evidence absent.
CANONICAL_JSON_V3=other READY candidate source blob9608f1ef5560e4e55eb7047f2b7884b93b7b227f, 14/14 local native GREEN but Product Vitest also NOT_EXECUTED. See previous control commit 64c034dbfc670fd28843f46dba6c04d812804586.
RELEASE_DOC_E=NOT_AUTHORIZED; COMPLETION_PERCENT=NOT_COMPUTABLE, 98 historic categories not exhaustive DOCX atomic inventory.
AUDITOR_APPROVAL=NOT_CLAIMED.
