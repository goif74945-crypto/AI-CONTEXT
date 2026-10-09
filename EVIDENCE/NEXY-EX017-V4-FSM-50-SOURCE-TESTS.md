# EX017 V4 FSM source-fenced real Vitest proof
ROLE=BUILDER_ONLY; AUDITOR_VERDICT=PENDING.
PRODUCT_REPO=goif74945-crypto/NEXY.AI-; PRODUCT_BRANCH=NEXY.ai; HEAD=ce340f29cf2c101e4229ef31b8513a2f6d0895fc
DOCX_SHA256=b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (original actual 12537-paragraph DOCX).
FSM_SOURCE=packages/core/vnext-state-matrix.ts; exact Git blob 27e1281fba330784cc3bf2c30e9e1e82f951479b.
GITHUB_TEST_BLOBS:
 tests/contract/state-matrix.test.ts=9459dbee70b75631b1d0204110116aa2e4be6239
 tests/contract/fatal-state-law.test.ts=04a1b683e84b66b99d960247f99bc82e47b3f7cc
 tests/coverage/core-state-matrix.test.ts=180be159a30642d8d73675a1736432b14b8f4dde
RELATED_SOURCE_BLOBS=packages/law/prerelease.ts 696acae9428a347e91eb32a26b692f6d913f1bf0; packages/api/vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b.
RUNNER=isolated connected Higgsfield Linux, Node22.16.0 via npx node@22, Vitest4.1.11 via Yarn, zod via Yarn; exported GitHub files only; NO private git credentials, NO database connections.
COMMAND=node node_modules/vitest/vitest.mjs run tests/contract/state-matrix.test.ts tests/contract/fatal-state-law.test.ts tests/coverage/core-state-matrix.test.ts --reporter=dot
ACTUAL_EXIT=0; RESULTS=3 test files passed; 50 tests passed, 0 failed.
ACTUAL_LOG_SHA256=4b9d258ee9e4b28a464011497b942245473d452dac7d368b1a821737424a4cb0.
SOURCE_GIT_HASH_VERIFICATION=all source and test Git blobs matched observed remote GitHub (fatal-state-law initially got extra newline on export and was corrected BEFORE final 50/50 run).
ASSERTION_SCOPE=static/pure state matrix transitions, owners, guard/fatal/recovery rules, prerelease gate interactions. This is actual unit/contract Vitest on exact module sources; NOT an execution of the full Product repo checkout/CI.
NO_PRODUCT_MUTATION_THIS_CYCLE: correct source preserved.
UNVERIFIED=DOC-C P10496-P10499 persisted EventLog, primary/secondary incidents, transactional recovery AuditLog+EventLog, full DB and queue worker concurrency, remote production readiness and DOC-E signoff. Source inspection of packages/orch-core/system-state.ts blob1883414a3d8b2034d06ef30e039b537319e2e0f1 found SERIALIZABLE transition, eventLog.create, freezeIncident, auditLog.create, secondary links: source evidence only, NOT runtime proof.
INDEPENDENT_AUDITOR=NOT_YET; BUILD_COMPLETION=NOT_COMPUTABLE; all historic 143 acceptance rows await independent per-atomic review.
NEXT_READY=fetch packages/contracts/state.ts, errors.ts, test canonical 4 status 8 states 29 errors via actual Vitest; inspect persistent FSM hooks against spec with DB-safe tests when runner available.
