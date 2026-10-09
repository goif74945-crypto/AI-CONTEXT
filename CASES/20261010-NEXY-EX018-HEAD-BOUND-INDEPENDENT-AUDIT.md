# Case EX018 OTAC helpers
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

CASE_ID: EX018-OTAC-HELPERS-UNICODE-AND-DEVICE-TUPLE-COLLISION
SEVERITY: S3 library correctness, runtime security exploitability NOT PROVEN.
OBSERVED: 14 directly executed helper cases, 11 pass, 3 fail, Node exit 1 on current Product exact source blob bb6134ab1946c8cfa8f130eb7eea5a777d02c58e.
DEFECT1: safeEqual compares JavaScript UTF-16 code-unit length then uses timingSafeEqual on UTF-8 byte buffers; equal code-unit length with differing byte count throws RangeError rather than false.
DEFECT2: computeDeviceId combines user agent and IP without unambiguous serialization; distinct tuples yield identical preimage string and sha256.
NEGATIVE_REACHABILITY_RESEARCH: exact-head Repo Code Bridge complete code search: computeDeviceId definition only; safeEqual helper definition only. Actual auth session binding uses packages/auth/device-binding.ts which passed 13 scoped tests. Do not equate test repro to credential bypass.
NEXT: check spec/public API and normalization, add negative tests, fix library semantics without breaking stored device IDs or current sessions, run genuine auth integration, independent auditor verify.
PREVENTION: byte length before timingSafeEqual; use structured/length-prefixed encoding for tuple, migrate only with compatibility plan; no fake runtime exploit evidence.
