# EX017 V4 Canonical JSON production source commit evidence
ROLE=BUILDER, INDEPENDENT_AUDITOR=PENDING, RELEASE_GATE=NOT_APPROVED
PRODUCT_BRANCH=NEXY.ai
PRODUCT_START_HEAD=8ed9af89f68fb82f60d4a4f5ccbc06005ce91992
PRODUCT_END_HEAD=206f6a9aaf67f1e7a3ee090722ef65617eea9d70
PRODUCT_COMMIT=206f6a9aaf67f1e7a3ee090722ef65617eea9d70 (fast-forward parent START, force=false, expected_sha=START)
CHANGED_PATHS=packages/core/canonical-json.ts;tests/contract/ex017-canonical-failclosed.test.ts;tests/contract/ex017-consumer-hash-shapes.test.ts. No other files.
PRE_SOURCE_GIT_BLOB=3894381cc80648c31f38b7b88035a64ee1d9cde6
POST_SOURCE_GIT_BLOB=c0c14ca5a6fa16e2ebc9da191774d3306fc6c1ee
NEGATIVE_VITEST_TEST_BLOB=b6d8646b35780a13510025616593869ff940ab7b
FINGERPRINT_DTO_TEST_BLOB=b974522c7ae60910f54094600b8e351e163f014c
GITHUB_READ_BACK=VERIFIED exact HEAD and ALL 3 blobs using live GitHub connector; compare 1 commit ahead, 0 behind, 3 files.
TEST_ENV=Higgsfield isolated Linux sandbox for website repo source export; no repo credentials sent; Node22.16.0 via npm npx node@22, Vitest4.1.11 installed via Yarn, TypeScript5.8.3. This was a minimal exact-source checkout, NOT full Product repository. GitHub original source blob matched before tests. Existing canonical-json.test.ts was exported from GitHub source, plus new regression and DTO consumer-shape test.
VITEST_RED_ORIGINAL=9 pass, 9 fail /18, exit1; command node node_modules/vitest/vitest.mjs run tests/contract/canonical-json.test.ts tests/contract/ex017-canonical-failclosed.test.ts --reporter=dot, NODE22; log sha256 1c7d7f7a885f27209862aa63619107ffd03de248258d96754a8f854c583c4250d.
VITEST_GREEN=25 pass, 0 fail, exit0; command node node_modules/vitest/vitest.mjs run 3 test files including ex017-consumer-hash-shapes.test.ts; log sha256 f53c98c4079463df2bce64a3121cd3ac35b6e8552440116152ab9deb615acda1.
TYPECHECK_STANDALONE=tsc --noEmit --strict --target ES2022 --module NodeNext --moduleResolution NodeNext --skipLibCheck packages/core/canonical-json.ts exit0; empty log sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
DTO_SHAPES_TESTED=directives submit idempotency fingerprint, OWNER role change, Live Config update and rollback, Cold Snapshot nested revision serialization, runtime config diff shape, accessor negative case. These are DTO-only, not actual API/DB integration.
EXPLICIT_LIMITS=Original full Product consumer Vitest suites, full-backend typecheck, web typecheck, PG/Redis G3, Rust Cargo, Browser E2E, release CI, production DOC-E receipt and independent Auditor NOT_EXECUTED_OR_VERIFIED for this new HEAD.
SPEC_HASH=b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 original DOCX actual bytes verified.
ACCEPTANCE=CANONICAL_JSON_LOCAL_REGRESSION_VERIFIED / PRODUCT_PATCH_READBACK_VERIFIED / FULL_DOC_C_AND_AUDITOR_NOT_VERIFIED. Never mark all 143 VERIFIED.
NEXT_READY=Queue retry safe integer candidate, verified old source + real Vitest on same isolated runner, then source fence / commit if green; API consumer integration on authorized full repo runner.
