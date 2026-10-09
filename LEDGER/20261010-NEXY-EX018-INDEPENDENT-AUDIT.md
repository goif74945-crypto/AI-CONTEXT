# LEDGER
TASK_ID: 20261010-NEXY-EX018-INDEPENDENT-AUDIT
MODE: ตรวจ / independent GitHub current-head original DOCX audit; Product READ_ONLY.
PRODUCT_HEAD_FREEZE: 58b1200bd61b867e917057d0019eea78ea9f6b2a on NEXY.ai, readback immediately before task closure. GitHub tree 889 blobs, 1092 tree entries.
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 computed from original DOCX bytes in container; 12537 paragraphs.
SOURCE_READ: 250 UNIQUE original Github Product blobs fetched/read in selected sets: canonical first-party packages 103, Rust 41, Prisma schema+migrations 57, DOC-D UI screen page TSX 11, DOC-D named components 14, DOC-C route wrappers 12, DOC-E receipt files 12. 250/889=28.12% of ALL repository blob file-read coverage, NOT source feature acceptance or completion.
SOURCE_RECORDS: EVIDENCE/20261010-NEXY-EX018-CODE-READ-CORE-001.json through -009.json (103 SHA-checked); EVIDENCE/20261010-NEXY-EX018-RUST-SOURCE-READ-001.json through -004.json (41); EVIDENCE/20261010-NEXY-EX018-PRISMA-SOURCE-READ-001.json through -005.json (57); plus DOC-D-11-PAGES, DOC-D-14-COMPONENTS, DOC-C-12-API-ROUTES, DOC-E-12-CURRENT-HEAD-REVIEW and SAFEEQUAL-RED-GREEN-PROOF source evidence.
ACTUAL INDEPENDENT NEW TESTS: Node22 isolated VM on original GitHub source: canonicalJson 14 PASS /14; DOC-C defaults/status/states/errors/FSM/guard/recovery 118 PASS/118; logical TSA tick 10 PASS/10; Auth OTAC/CSRF/device-binding/client-IP 15 PASS/16 (1 FAIL), combined 157 PASS /158 selected original current-source tests; not repository Vitest pass %. Isolated helper patch experiment original 2 PASS/3 FAIL1 => hypothetical patched 3 PASS/3, no Product mutation.
CONFIRMED DEFECT: packages/auth/otac.ts blob bb6134ab1946c8cfa8f130eb7eea5a777d02c58e safeEqual('é','x') throws ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH instead of false because JS char-length check does not equal UTF8 buffer byte lengths. Repo-wide source search found no direct Product caller of this exported helper, so exploitability is NOT_VERIFIED. Source-only fix proof in EVIDENCE/20261010-NEXY-EX018-SAFEEQUAL-RED-GREEN-PROOF.json.
RUST: 41/41 source reads with unsafe/panic/unwrap candidate flags, contextual follow-up showed many are intentional kernel-halt/const-depth/test-code; Rust cargo test NOT_RUN because no connected cargo runner. No Rust exploit/invariant failure claimed.
PRISMA: 28 migration dirs, all with up+down SQL; 57/57 original files read. Two forward DROP COLUMN migrations had documented backfill/hashing before removal. No PostgreSQL migration execution; real rollback NOT_VERIFIED.
UI: S7 source OWNER recover CTA on recoverable incident, nonowner read-only; source-only not browser E2E.
CI: 4 exact-head GitHub Actions workflows conclusion failure, inspected job steps=[], failure root cause unknown; no current HEAD full test receipt inferred.
DOC-E: 12/12 Product files checked, each refers OLD 0d0d82bdc7d04ef8248f310d106cf5e4c1dd7a3d, current-head proof in those files NOT_VERIFIED; E11 old pack says no human signoff. Not proof no evidence elsewhere.
LEGACY_REGISTER: 143/143 historic EX016 IDs unique, anchored to old HEAD; not exhaustive DOC-C atomic requirements. Do not count old SOURCE_EXACT as current functional VERIFIED.
FINAL_GLOBAL_COMPLETION: NOT_COMPUTABLE; partial source-read coverage not feature completion. PRODUCT_WRITES: NONE.
LIMITS: 639 GitHub blobs not in the 250 selected read sets, full repository test/TypeScript/browser/PG+Redis/Rust not executed; avoid fabricated conclusion. No secrets copied.
TIMESTAMP_SOURCE: 2026-10-10 Asia/Bangkok user local timestamp.

CLAIM_CHAIN: DOCX original SHA -> exact P9913-P9946 numeric config, P9952/P9954-P9993 state/error, P10352-P10498 FSM; GitHub fetched original package blob SHA -> isolated Node test stdout/exit -> PASS/FAIL per bounded set. Source read coverage 250/889=28.12%, not TEST or DOC-C feature coverage. Separate direct code README test claims from real independent tests.
