# EX-V3 BUILDER / CANONICAL JSON FAIL-CLOSED EVIDENCE
MODE=EXECUTE_NOW / EVIDENCE_DRIVEN / BUILDER; INDEPENDENT_AUDITOR_APPROVAL=NOT_CLAIMED
PRODUCT_REPO=goif74945-crypto/NEXY.AI-; PRODUCT_BRANCH=NEXY.ai; PRODUCT_START_HEAD=8ed9af89f68fb82f60d4a4f5ccbc06005ce91992 (GitHub observed at V3 start)
AUTHORITATIVE_DOCX_SHA256=b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (local sha256sum on original uploaded DOCX)
SPEC_LOCATORS=P4102 Canonical JSON->SHA-256 SpecHash; P9450 idempotency_key prevents duplicate execution; P10031 all mutating routes require idempotency_key unless exempt. These anchors do NOT prove all DOC-C/D/E requirements.
CURRENT_SOURCE=packages/core/canonical-json.ts git blob 3894381cc80648c31f38b7b88035a64ee1d9cde6, locally hash verified to prior exact GitHub fetch.
PROPOSED_LOCAL_SOURCE_BLOB=9608f1ef5560e4e55eb7047f2b7884b93b7b227f
PROPOSED_VITEST_TEST_BLOB=334ca8d7baffe22b24ca2f0b572a0b521f24ad6a
PROPOSED_PATCH_BLOB=e622299fda50e30587bffc14eaba5c08f9dabbde
PATCH_APPLICABILITY=git apply --check exit0; git apply exit0; actual resulting Git blob=9608f1...
LOCAL_RUNNER=isolated Linux node22.16.0; git2.47.3; globally installed tsc (no npm registry access).
LOCAL_ORIGINAL_RED_COMMAND=node --experimental-strip-types --no-warnings --test tests/contract/ex-v3-native.test.mjs with CANONICAL_MODULE pointing to original .ts; EXIT=1; PASS=4 FAIL=10 total14.
LOCAL_V2_PATCH_RED=PASS10 FAIL4/14 EXIT1, due array-index accessor, extra array string prop, symbol array prop, nonenumerable record prop.
LOCAL_V3_PATCH_GREEN=PASS14 FAIL0/14 EXIT0.
LOCAL_STANDALONE_TSC=tsc --noEmit --strict --target ES2022 --module NodeNext --moduleResolution NodeNext --skipLibCheck packages/core/canonical-json.ts EXIT0.
FIX_SEMANTICS=reject sparse arrays, non-plain objects, cycles, own symbols, own extra array props, non-enumerable fields, accessors without invoking ordinary object getter; preserve shared acyclic refs, nested key sort, explicit JSON primitives, array order. Proxy traps and extreme recursion not fully proven safe.
VITEST_PRODUCT_TESTS=NOT_EXECUTED: no accessible full Product checkout/node_modules; isolated container git clone failed DNS github.com, npm registry timeout; Windows Desktop Commander offline. Do not conflate native node:test with Vitest. Consumer Directive/OWNER/LiveConfig/ColdSnapshot tests NOT_EXECUTED on patched source.
CI_HEAD_TEST=reran specific old exact-head Contract tests job 113455262303, GitHub accepted rerun, run37819115716 attempt2 still failed; new job113524749115 steps=[]; job logs fetch 404 BlobNotFound. Cause UNKNOWN, cannot attribute source.
RAILWAY=NEXY Validation R2 environment production only non-ephemeral; nexy-validation source pinned OLD 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43; PG+Redis services SUCCESS launch only, NOT an isolated G3 runner. NO RAILWAY WRITE.
PRODUCT_COMMIT=NONE; DOC_E_RELEASE=NOT_AUTHORIZED; 98 historic rows NOT exhaustive atomic spec inventory; completion NOT_COMPUTABLE.
ARTIFACT_PACKAGE=conversation download NEXY_EX_V3_IMPORT_PACKAGE.zip SHA256 ae4d45b13985174e34d1c2ea9b3f9e015863c818aba6d48c63b79d4b9593e5ac; GitHub evidence is a report only, artifact bytes remain conversation-local unless separately uploaded.
NEXT_READY=obtain isolated authorized runner with actual Vitest deps; run existing canonical-json.test.ts, new candidate, Directive, OWNER, LiveConfig, ColdSnapshot, full typecheck; assess diff and then Product prepare+commit with expected-head fence, readback. Continue independent traceability while blocked.
