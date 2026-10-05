REVIEW_ID: REVIEW-DOC-C4-ARTIFACT-REVISIONS-C-6D91A4F2
CHAT_ID: C-6D91A4F2
TASK_ID: TASK-DOC-C4-ARTIFACT-REVISIONS-001
REQ_ID: REQ-DOC-C-4-2-ARTIFACT-REVISIONS
ROLE: INDEPENDENT_SHADOW_REVIEW / RED_TEAM
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
TARGET_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_BLOB_CANONICAL_API: 1664d8d6a7da32245578addc26596f8fd4d55954
TEST_BLOB_CANONICAL_API: edc26665c768f31f27bee89c8b8578ad5c59ee1a
VERDICT: CHANGES_REQUIRED_TO_ACCEPTANCE_BEFORE_IMPLEMENTATION

FACTS:
- Final DOC-C §4.2 raw paragraphs 10302-10330 define GET /api/artifacts/:id/revisions.
- Canonical response data is items[{revision_id, revision_no, created_at, created_by}] plus optional next_cursor.
- Current handler emits additional item fields content_hash, commit_count, status, actions and data-level viewer_role.
- Current test line-equivalent assertions intentionally preserve the expanded item shape while naming the behavior canonical.
- Existing task acceptance correctly requires removal/isolation of those response-shape extensions from the canonical route.
- Final DOC-C query declaration is cursor?: string and limit?: number // max 100.
- Current PaginationQuerySchema additionally requires cursor length 1..512 and coerced limit integer >=1 <=100.
- Final DOC-C §4.1 Global API Law inspected at raw paragraphs 10027-10037 does not add cursor length, integer, or minimum-limit restrictions.

AUTHORITY_CLASSIFICATION:
- RESPONSE_WIRE_SHAPE: CONFIRMED_SPEC_MISMATCH.
- PAGINATION_MINIMUM_INTEGER_AND_CURSOR_LENGTH: UNRESOLVED_AUTHORITY_GAP / POSSIBLE_CONTRACT_NARROWING.
- Do not silently remove these guards as a "fix" because their security/runtime rationale is not established by this review.
- Do not silently preserve them as exact DOC-C behavior either because no active DOC-C authority for the extra restrictions was found.

REQUIRED_ACCEPTANCE_EXTENSION:
- Before implementation, explicitly resolve whether cursor min/max length and limit integer/minimum constraints have separate active build authority.
- If no active authority exists, classify the extra rejection domain as contract narrowing and repair/test it under the same requirement or a linked requirement.
- If separate authority exists, cite it and test the distinction between canonical DOC-C typing and implementation security validation.
- Add an exact-key assertion for canonical revision item and data shapes so unsupported fields cannot reappear through toMatchObject-style tests.
- Preserve ARTIFACT_HISTORY_VIEWED for AUDITOR and the explicit max-100 boundary.
- Preserve existing authorization/error behavior unless primary authority requires a change.

TEST_ORACLE_REVIEW:
- Existing test at the target blob proves 101 is rejected and 100 is accepted.
- Existing test proves a malformed opaque cursor is rejected.
- It does not prove the authority status of 0, negative, fractional limit values, empty cursor, or long cursor values.
- Existing toMatchObject pagination checks are insufficient as an exact canonical-shape oracle.

SOURCE_MUTATION: NONE
UPSTREAM_MUTATION: NONE
BLOCKER: INC-BRANCH-NAMESPACE-001
NEXT_EXACT_STEP: After worker namespace becomes Git-valid, implement only after pagination authority is resolved; then run focused canonical-api contract tests plus exact-shape drift tests on the exact candidate SHA.
