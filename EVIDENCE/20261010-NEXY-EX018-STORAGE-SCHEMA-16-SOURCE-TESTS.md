# EX018 DOC-D Storage Law independent static assertions 2026-10-10

MODE: READ_ONLY_PRODUCT / INDEPENDENT AUDIT
PRODUCT_HEAD: 58b1200bd61b867e917057d0019eea78ea9f6b2a
AUTHORITATIVE_DOCX_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SCOPE: original DOCX P10723-10746, 7 uniqueness constraints and required RESTRICT foreign keys.
EXECUTION: Actual Floot VM Node.js v22.23.2, custom Node.js node:test; source fetched from private GitHub connector, tests compare source/migration text against DOCX assertions.
SOURCE_1: prisma/schema.prisma git blob be1cbe1481829a2c95b6599929abc86829f37667
SOURCE_2: prisma/migrations/20260921000000_current_schema_baseline/migration.sql git blob 553a55f4409261cca0dbbc6d78c8e06709b456b5
SOURCE_3: prisma/migrations/20260922201000_canonical_user_ownership/migration.sql git blob ba1e85a5ca9b8dd585ce789c1af39df3e3c693e1
TEST_RESULT: 16 of 16 static source assertions PASS, exit=0, elapsed 48.594225 ms
TESTED: User emailHash uniqueness (hashed/normalized identity, requires separate semantic equivalence), Session primary key, DirectiveRecord idempotency uniqueness, Commit idem uniqueness, Revision(artifactId,revisionNo), PipelineRun primary key, FreezeIncident pipelineRun unique, 6 Prisma onDelete Restrict clauses + baseline FreezeIncident FK SQL + corrected legacy Session FK and Project FK in later migration.
IMPORTANT: Baseline initial Session FK had ON DELETE SET NULL. 20260922201000_canonical_user_ownership/migration.sql explicitly drops/recreates it with ON DELETE RESTRICT and enforces non-null ownership after evidence-based backfill. Mark CURRENT-SOURCE CONSISTENT, not falsely report an unpatched mismatch.
LIMITS: These are static exact source tests. No actual isolated PostgreSQL service available for EX018, no migration apply/rollback/reversibility tested, no actual PostgreSQL catalog inspected, and not a claim that all 57 migrations applied successfully in a deployed environment. Also no proof User.emailHash faithfully enforces actual User.email normalization throughout all writers.
PRISMA_FULL_FILE_READ: exactly 57/57 current-head prisma/ files fetched and individual SHA matched, recorded in EVIDENCE/20261010-NEXY-EX018-PRISMA-READ-001.json to -005.json.
REVIEW: Combined original DOCX and current file bytes only; does not rely on AI-CONTEXT prior claims as proof.
VERDICT: VERIFIED_SOURCE_ONLY_FOR_16_PREDICATES; DB_RUNTIME_NOT_VERIFIED.
