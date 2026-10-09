# 20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT — ตรวจกับ DOCX จริงและ Product HEAD จริง
MODE: ตรวจ / READ_ONLY_PRODUCT / INDEPENDENT / EVIDENCE_FIRST
STATUS: PARTIAL_AUDIT, NOT FULL_PRODUCT_VERIFICATION
PRODUCT: goif74945-crypto/NEXY.AI- branch NEXY.ai
FROZEN_HEAD: 58b1200bd61b867e917057d0019eea78ea9f6b2a
SPEC: uploaded แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx; recomputed SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
ORIGINAL_SPEC_DOC_C: zero-based paragraph P9885-P10498, 614 paragraphs, 612 nonempty. Local verbatim source register SHA-256 f2e8fb75e682b9c23b7a0a27cbe20d81e54e716a4a7a2d453d3f826911c117a4 (this register is paragraph-level and not an exhaustive atomic feature denominator).
CURRENT_REPO_TREE: 1092 tree entries; 889 Git tracked blobs, 887 eligible UTF8 text blobs searched by Repo Code Bridge, 2 skipped; failed_files 0, coverage_complete true for one exact search query. This is search coverage, NOT semantic audit.

## 1. Actual file reads and evidence readbacks
| Source category | Unique files actually fetched full content | Git SHA exact |
|---|---:|---:|
| canonical API/Auth/Core/LAW/JUDGE/SWARM/Queue/Contracts/etc. packages | 103/103 in this selected folder filter | 103/103 |
| Rust .rs across kernel and daemon | 41/41 | 41/41 |
| apps/web TS/TSX/JS/CSS/MJS | 99/99 | 99/99 |
| prisma/schema.prisma and migration SQL sources | 57/57 | 57/57 |
| DISTINCT TOTAL source-read subset | 300 | 300 |

BASIC_BLOB_READ_COVERAGE_FOR_889 = 300/889 = 33.75%; This is a file-read inventory percentage only. More tracked blobs (including tests/scripts/experimental/evidence) are not part of this subset. Semantic/functional AUDIT_COVERAGE is separately UNKNOWN because the complete applicable DOC-C atomic requirements denominator is not locked. Never call 33.75% product completion.
ALL source evidence is in AI-CONTEXT/EVIDENCE/20261010-NEXY-EX018-CODE-READ-CORE-001..009.json, RUST-READ-001..004.json, WEB-READ-001..009.json, PRISMA-READ-001..005.json. Each persisted JSON entry contains exact git blob, file path, line count, imports/exports or static risk signals as applicable. Readback on 243 non-DB files verified SHA in every row, Prisma 57/57 readbacks independently verified. These are FULL TEXT READS + MACHINE INDEX, not manual semantic proof of all code paths.

## 2. Independent ACTUAL real Node22 VM source tests; seven separately executed suites
| Unit under independent test | Git source blob | Executed | PASS | FAIL | Exit |
|---|---|---:|---:|---:|---:|
| canonical-json | c0c14ca5a6fa16e2ebc9da191774d3306fc6c1ee | 14 | 14 | 0 | 0 |
| DOC-C exact config/error/status/FSM | a3141a649be7e40ec79f417f53bba9b73081232b, 04efcc7161c5415922e11e16174013d1d4ea40a3, b6a1737688399cf0571236f23c0b5ce0f7de5847, 27e1281fba330784cc3bf2c30e9e1e82f951479b | 118 | 118 | 0 | 0 |
| UI modeguard | 3391a429c9e80ee2c7fe174aea7ee1444cc08e7d | 42 | 42 | 0 | 0 |
| Auth client IP/proxy header | d5e8f552024dc2ccd26ca9cbaf089a5c1b24b57a | 14 | 14 | 0 | 0 |
| Auth CSRF issuance/validation | 3444b32561d8b5a11951822810381da66c3c8f92 | 13 | 13 | 0 | 0 |
| OTAC helper primitives | bb6134ab1946c8cfa8f130eb7eea5a777d02c58e | 14 | 11 | 3 | 1 |
| Actual session-device-token binding helper | 04b6e9b0b63b4ff9cc61bd65000f0b316a6d9bf4 | 13 | 13 | 0 | 0 |
| TOTAL independent scoped tests | one frozen HEAD | 228 | 225 | 3 | one failing suite |

SCOPED_PASS_RATE=225/228=98.68% for only these 228 independently executed Node tests; this percentage is NOT project completion, NOT all repo tests, NOT full Vitest/cargo/Prisma/Browser/Redis regression. Runner: Floot isolated Node 22.23.2, original source bytes fetched from GitHub and executed with --experimental-strip-types or --experimental-transform-types; some independent unit assertions use test-local request/response spies, NOT actual production HTTP integration.

## 3. Reproducible new findings, adversarially qualified
FINDING-EX018-AUTH-01 S3 library correctness:
`packages/auth/otac.ts` exports `safeEqual(a,b)` which compares JS string code-unit length before crypto.timingSafeEqual(Buffer.from(utf8)). `safeEqual("é","a")` and `safeEqual("🙂","ab")` throw `RangeError ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH` instead of returning false for unequal UTF-8 byte lengths. Two real negative tests FAILED on source blob bb6134ab....
FINDING-EX018-AUTH-02 S3 utility tuple-collision:
`computeDeviceId(userAgent,ip)` SHA256(userAgent+ip) without framing, so ("foo1","2.3.4.5") and ("foo","12.3.4.5") yield same hash 269adda7ef0550b38e446729413cebaee4f45065cd608b2b5eb7a1cbd5d12ac8; one actual negative test FAILED.
REACHABILITY: exact HEAD Repo Code Bridge 887 eligible text blob search `computeDeviceId` found only its definition; `safeEqual(` likewise only own definition (other hits are timingSafeEqual calls). Thus **no proven importer or runtime authentication exploitation**; do not assert session bypass. Active login/session device binding uses another crypto implementation in `packages/auth/device-binding.ts`, and 13 standalone cases passed. Recommend minimal helper correctness regression and migration/consumer proof before changing any live session format.
OTAC failure proof document: EVIDENCE/20261010-NEXY-EX018-OTAC-HELPERS-14-TESTS-3-RED.md.
NOT_FLAW: `r.eval()` in rate-limit.ts is Redis Lua ZSET command, NOT arbitrary JavaScript eval(). Date.now in rate limiting is wall-clock by design; do not assume a deterministic-core violation without checking scope. Rust `unwrap` and `panic` searches include test-only contexts; do not claim runtime crash without reachability.

## 4. Source-level contract and DB migrations (NOT runtime acceptance)
The twelve DOC-C canonical API route wrappers were fetched from exact HEAD and all twelve expected HTTP method exports matched (12/12 SOURCE_METHOD_MATCH ONLY, NOT E2E AUTH/RBAC/CSRF).
Prisma 28 migration.sql + 28 migration.down.sql + schema.prisma = 57 read/hashed; 28/28 migration directories include a down script; this proves down FILE EXISTENCE, not successful PostgreSQL round-trip. `canonical_user_ownership/migration.sql` explicitly rejects unverifiable ownership mapping in original SQL, source evidence of fail-closed condition only. DROP/CASCADE in down scripts not automatically faults; need disposable PostgreSQL E3 execution to verify data preservation, rollback and FK constraints.
Current HEAD GitHub Actions 4 workflow runs all concluded failure with sample jobs steps=[] and log fetch missing, so they do NOT furnish green current-head suite. Cause of runner failure not yet proven; don't blame code execution without logs.
DOC-E E01-E12 authentic receipts and E11 human signoff are NOT independently current-head verified by EX018.

## 5. Multi-system acceptance matrix (proof type separated from completion)
| System | Source observed | Verified subset | NOT VERIFIED / outstanding |
|---|---|---|---|
| Config defaults/error/state types | source exact SHA | independent Node 118-test suite includes relevant checks | all runtime consumers, override/race/DB |
| Core FSM/LAW/JUDGE | full canonical group text read | transition/guards subset real tests | persistent EventLog/primary+secondary incidents/Release policy end-to-end |
| Authentication OTAC/device/CSRF | source read | CSRF13, IP14, binding13, helper11 passes/3 fails | OTAC actual user/session DB and 3 helper defects |
| API surface | 12 canonical routes read | method export 12/12 static | HTTP auth/RBAC/CSRF/schema/status contracts real E2E |
| SWARM/agents/pipeline | source content read | none current-head runtime | adapter provider calls, timeouts/debate+verification |
| Queue/retry/workers | source content read | none real Redis worker | BullMQ/Race/replay/FAILED retry/current G3 |
| Vault/revisions | source content read | none live DB | SERIALIZABLE/atomic, consistency, durable revision and rollbacks |
| Storage/Prisma | 57/57 schema+migration sources read | 28/28 down files present | genuine PostgreSQL roundtrip, constraints and rollback |
| Observability/Audit | source content read | none runtime | alarm, log chain, incident trace/persistence |
| Rust/kernel | 41/41 .rs source read | no cargo executable runner | build, fixed128, WAL recovery and authoritative FSM tests |
| Web UI | 99/99 selected web files read | ModeGuard 42/42 | real browser 12 screens+14 component interactions/responsive/a11y |
| Security/Sandbox | selected source read, search pass | IP/CSRF helper tests | isolation, auth abuse, tenant/replay on real runtime |
| DOC-E Release | historical Product docs observed | no current-head release approval in EX018 | E1-E12 run receipts, owner E11 signoff |
| Phase-F and Experimental | additional repo paths exist, not part of above full reads | none from EX018 | exact applicability / actual tests not completed |
| Test suites and CI scripts | counted by Git tree and selected reads | only new 228 tests above | full original repository Vitest, Rust, browser CI |

## 6. Audit truth and next work
NUMERATORS: source full content read 300 distinct / total 889 tracked blobs; independent Node tests 225 pass / 228 executed (3 RED). API export checks 12/12. Migration up/down existence 28/28.
DENOMINATOR FOR FEATURE COMPLETION: NOT LOCKED; 614 DOC-C paragraphs are NOT 614 mandatory features and historical 143 checked positions are not exhaustive.
FULL SEMANTIC AUDIT COVERAGE = NOT_COMPUTABLE; PRODUCT COMPLETION% = NOT_COMPUTABLE; RELEASE READINESS = NOT_VERIFIED. Do not replace NOT_VERIFIED with 0% or 100%.
NEXT READY SAFE TASKS: 1. audit each remaining repo source/test/Phase-F/experimental file at exact HEAD; 2. perform reachable original full repo tests in truly authorized private checkout runner with Node+Rust; 3. test isolated PostgreSQL and Redis integration; 4. add actual OTAC helper negative tests and ask builder to patch safely on NEXY.ai; 5. browser E2E DOC-D; 6. atomic DOC-C requirement inventory; 7. DOC-E E1–E12 current-head receipts.
PRODUCT_MUTATION: NONE (read-only auditor). AI-CONTEXT only audit evidence write.
VERDICT: PARTIAL_AUDIT_WITH_REPRODUCIBLE_DEFECTS, NO CLAIM OF COMPLETION.
