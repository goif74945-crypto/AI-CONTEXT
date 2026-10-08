# TASK — NEXY Final DOC-B/DOC-C Time Authority and Queue TTL Extraction 005

TASK_ID: 20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-005
TITLE: Answer Codex final DOC-B DOC-C time authority and queue TTL locator request
MODE: CROSS / AUDIT / SOURCE-EXTRACTION
SCOPE: Review the attached hash-matching authoritative DOCX only; extract verbatim clauses and exact one-based paragraph locators; determine whether final DOC-C explicitly requires TSA verification for queue expiry. Write sanitized evidence to AI-CONTEXT main.
NON_GOALS: No code edits, no invented authority, no release authorization or TSA bypass.
INPUT: Codex asked for final DOC-B/DOC-C time-authority and queue TTL text and paragraph locators.
SOURCE_FILE: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SOURCE_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SHA_MATCH: VERIFIED
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
PRODUCT_BRANCH: NEXY.ai
PRODUCT_HEAD_OBSERVED: 8b406a63f10aa1424225a80453393af2e4cb78b5
AI_CONTEXT_START_HEAD_OBSERVED: 6939ff2c558ddd501fd5c617046d78c4db3ba302
ARTIFACTS:
- EVIDENCE/20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-CLAUSES-005.md
- TASKS/20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-005.md
- LEDGER/20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-005.md
ACTIONS:
- Read required DOCX source bytes; SHA256 matched.
- Extracted with python-docx, numbered 12,537 paragraphs (Pnnnn one-based ordinal, not printed page).
- Full-range literal searches final DOC-B P09846-P09885 and DOC-C P09886-P10916.
- Queried scope-specific clauses and broader time / queue-law sections.
- Wrote and read back evidence file in AI-CONTEXT/main.
KEY_CLAIMS:
- P09844: Build obligation comes from DOC-C only.
- P09946: stale_job_ttl_ms = 900000.
- Final DOC-C does not explicitly mention TSA, clock, verified time, authoritative time or time source.
- P04003,P04005,P04007,P04009,P05151-P05158 govern broader time/core clock.
- P09454 earlier broader queue law says stale queued jobs expire after configured TTL.
- No explicit final DOC-C sentence mandates TSA-signature verification as the time source for canonical queue expiry.
PROOFS:
- Source SHA256 match from actual DOCX, extracted paragraph text.
- Restricted literal search over exact final DOC-B/C range.
TESTS:
- Extraction assertion of SHA match: PASS.
- final DOC-B TSA literal hits: 0.
- final DOC-C TSA literal hits: 0; stale_job_ttl_ms hit at P09946.
- No application tests or execution of product code performed.
RISKS:
- Absence of literal words is not proof absence of indirect normative dependency or synonyms.
- Current product may enforce TSA through distinct architecture; a source-level call-graph and final authority evaluation is needed before mutation.
- Do not change queue to system clock or fabricate TSA witnesses.
ROLLBACK: Revert only AI-CONTEXT coordination files through forward commits after fresh HEAD checks.
LIMITS: Clauses and authority reasoning are source-based; no product change, runtime, or release verdict implied.
FINAL_STATUS: VERIFIED_WITH_LIMITS
NEXT_ACTIONS: Give Codex exact evidence locator; preserve path-specific freeze on unresolved TSA coupling, continue sandbox repair and 98-row substantive audit.
VERSION: 1
TIMESTAMP_SOURCE: conversation date 2026-10-08, Asia/Bangkok
TRACE_ID: NEXY-DOCB-DOCC-TSA-QUEUE-TTL-005
