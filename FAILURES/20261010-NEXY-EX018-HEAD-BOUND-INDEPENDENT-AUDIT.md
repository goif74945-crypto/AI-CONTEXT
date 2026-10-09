# Failure Record EX018 audit gaps
TASK_ID: 20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT
MODE: ตรวจ / READ_ONLY_PRODUCT / ORIGINAL_DOCX_TO_GITHUB_SOURCE / ACTUAL_VM_TESTS
PRODUCT: goif74945-crypto/NEXY.AI- branch NEXY.ai HEAD 58b1200bd61b867e917057d0019eea78ea9f6b2a
CONTROL_REPO: goif74945-crypto/AI-CONTEXT branch main (records only)
SOURCE: original DOCX SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
MAIN_ARTIFACT: EVIDENCE/20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT-INTERIM-GATE-REPORT.md
TEMP_LEDGER_LOCAL: /mnt/data/NEXY-EX018-AUDIT/TEMP-MEMORY.md
SPEC_PARAGRAPH_LOCAL: /mnt/data/NEXY-EX018-AUDIT/DOC-C-614-PARAGRAPH-SOURCE-REGISTER.json
EVIDENCE_RECORDS: EVIDENCE/20261010-NEXY-EX018-CODE-READ-CORE-001..009.json; RUST-READ-001..004.json; WEB-READ-001..009.json; PRISMA-READ-001..005.json; independent test receipts for UI ModeGuard, client IP, CSRF, OTAC helper negative, active device binding and DOC-C route export static checks.
TESTS: independent Node22 VM 228 total, 225 pass, 3 fail. Original repo Vitest/cargo/real PostgreSQL+Redis/browser not run. No new CI PASS claim.
SOURCE_FILE_READ: 300 distinct full content blob SHA matches, from 889 total tracked blobs. Read coverage 33.75% only; product semantic compliance denominator NOT_COMPUTABLE.
PRODUCT_CHANGES: NONE, audit READ_ONLY.
TRACE_ID: 20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT
VERSION: 1
TIMESTAMP_SOURCE: 2026-10-10 Thailand local.

F1 TEST_FAILURE_3: 2 safeEqual Unicode RangeErrors, 1 computeDeviceId tuple collision; source-only reproducible failures, no direct external exploit proved.
F2 INCOMPLETE_SOURCE_SEMANTIC: 300 of 889 tracked blobs have full content read and SHA verification. Others not yet content-audited in EX018. Even 300 reads are not 300 validated functional units.
F3 FULL_REPO_RUNNER_LIMIT: private GitHub repo unauthenticated Floot public API returns 404; local container git has no private clone auth, Desktop offline, Termalin no connected hosts, Floot Node22 VM lacks Cargo and full Product deps. Tools still allowed direct GitHub reads and real isolated source tests.
F4 CI_UNKNOWN: 4 current-head GitHub workflow failures and 0 steps sample, missing logs; cannot assert passed/failed source tests.
F5 E3_E7_E2E: no authorized disposable PostgreSQL/Redis/browser environment proven; no migration roundtrip or full queue tests conducted.
F6 FEATURE_MATRIX: 143 prior source checkpoints incomplete normative DOC-C universe; 614 paragraph source register does not equal exhaustive atomic requirements. Product completion percent NOT_COMPUTABLE. DOC-E E1–E12 not independent current-head verified.
MITIGATION: continue source and requirements audit; direct source tests scoped honestly; prefer authorized connected runner for full original tests, plus independent current-head readback. Do not claim background execution.
