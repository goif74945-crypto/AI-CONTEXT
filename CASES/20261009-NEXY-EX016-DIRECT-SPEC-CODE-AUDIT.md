# CASE EX016-CANONICAL-JSON-INTEGRITY
STATUS: VERIFIED_RED_AT_CURRENT_HEAD / FIX_REQUIRED
SEVERITY: S3 correctness, could affect integrity/idempotency hashes depending input reachability.
PRODUCT_HEAD: 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992
SOURCE_BLOB: packages/core/canonical-json.ts blob 3894381cc80648c31f38b7b88035a64ee1d9cde6, locally git hash-object identical.
REAL_EXECUTION: Node22 native node:test 10 cases, 4 PASS, 6 FAIL, exit1, positive stable ordering/array/undefined/nonfinite controls pass.
FAILED: sparse hole initial [,1] -> invalid JSON [,1]; sparse middle [1,,3] -> invalid JSON; Date/Map -> {}; symbol-only object -> {}; getter accessed; cyclic -> RangeError.
AFFECTED_CALLERS: packages/api/directives.ts SHA/idempotency; packages/api/owner-roles.ts and live-config.ts change requests; packages/api/cold-snapshot.ts content hash; packages/config/runtime-config.ts diff. These are source-level call-sites, not proven production exploits.
NEXT_FIX_ACCEPTANCE: add source-linked regression for nonplain/holes/accessor, minimal fail-closed repair preserving supported JSON ordering, full Vitest, dependent consumer tests and GitHub HEAD readback.
TEST_ARTIFACT: NEXY-EX016-SOURCE-TEST/canonical-json-red.test.mjs with raw EX016_CANONICAL_RED.log from local container; first-party Git blob matched.
NO PRODUCT MUTATION by auditor.
