# EX018 Proof Ledger
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

L01 DOCX: byte SHA256 verified, DOC-C P9885-P10498 614 original paragraphs / 612 nonempty, per-paragraph JSON archive SHA f2e8fb75e682b9c23b7a0a27cbe20d81e54e716a4a7a2d453d3f826911c117a4.
L02 GitHub: exact HEAD 58b1200bd61b867e917057d0019eea78ea9f6b2a; 889 blobs. Repo Code Bridge no-match index across 889 candidates, 887 eligible text, skipped 2, failed 0, completed true; does not prove semantics.
L03 Full content read 103 canonical package + 41 Rust + 99 web + 57 Prisma = 300; each content SHA matches Git tree, all JSON evidence files read back.
L04 Independent tests source-specific 14 Canonical, 118 DOC-C base/FSM, 42 ModeGuard, 14 IP, 13 CSRF, 14 OTAC helpers (11 PASS, 3 FAIL), 13 active device-token binding = 228 total, 225 PASS 3 FAIL. Distinct scope, not full original Product tests.
L05 Real RED: OTAC `safeEqual('é','a')`, `safeEqual('🙂','ab')` throw RangeError; `computeDeviceId('foo1','2.3.4.5') === computeDeviceId('foo','12.3.4.5')` true due raw concat.
L06 Exact-head full search of names found no imports/callers of those helpers; no live session bypass proven, device-binding.ts uses another fixed-size SHA.
L07 12/12 DOC-C HTTP method exports matched; real HTTP/RBAC/CSRF E2E not proved.
L08 Prisma 28 up scripts and 28 down scripts; manual migration source inspected for ownership fail-closed; PostgreSQL migration not executed.
L09 GitHub current head 4 workflows failed with sample jobs 0 steps; actual code test outcomes cannot be derived from 0-step jobs.
L10 Source-only coverage 300/889=33.75%; actual full feature denominator unknown; product completion NOT_COMPUTABLE; DOC-E signoff NOT VERIFIED.
SOURCE_TO_PROOF: See EVIDENCE/20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT-INTERIM-GATE-REPORT.md plus individual proof file paths.
