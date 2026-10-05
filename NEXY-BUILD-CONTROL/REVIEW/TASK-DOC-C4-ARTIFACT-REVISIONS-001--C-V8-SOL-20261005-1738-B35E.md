TASK_ID: TASK-DOC-C4-ARTIFACT-REVISIONS-001
REVIEWER_CHAT: C-V8-SOL-20261005-1738-B35E
ROLE: INDEPENDENT_SPEC_CONTRACT_REVIEWER
STATUS: REVIEW_CONFIRMS_ACTIONABLE_GAP
PRIORITY: P1
RISK: MEDIUM
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_AUTHORITY: final DOC-C §4.2 GET /api/artifacts/:id/revisions, primary DOCX paragraphs 10302-10330

FACT:
- Final DOC-C requires session auth and OWNER / OPERATOR / AUDITOR RBAC.
- Query contract is cursor?: string and limit?: number with max 100.
- AUDITOR reads emit ARTIFACT_HISTORY_VIEWED.
- Canonical response data is { items: Array<{ revision_id, revision_no, created_at, created_by }>, next_cursor?: string }.
- packages/api/canonical.ts blob 1664d8d6a7da32245578addc26596f8fd4d55954 emits additional canonical-wire fields content_hash, commit_count, status, actions in each item and viewer_role at data level.
- tests/contract/canonical-api.test.ts blob edc26665c768f31f27bee89c8b8578ad5c59ee1 explicitly expects those extra item fields, so the test currently preserves the drift instead of detecting it.
- Cursor validation, max limit 100, ownership scoping, and AUDITOR history audit behavior are present and should be preserved.

OBSERVED:
Canonical route emits fields not declared by final DOC-C and the contract test accepts/locks them.

EXPECTED:
Canonical response must match final DOC-C wire shape exactly. Legitimate storage/UI metadata may remain internal or be exposed by separately authorized non-canonical surfaces, but must not silently widen this canonical route.

CLASSIFICATION:
SPEC_MISMATCH + CONTRACT_DRIFT + TEST_ORACLE_DEFECT.

ASSUMPTION:
None required.

UNKNOWN:
Exact-candidate runtime tests remain pending because compliant source mutation is blocked by INC-BRANCH-NAMESPACE-001 and exact-head hosted CI is currently EXECUTION_INFRA_FAILURE.

VERDICT:
ACTIONABLE_CODE_GAP CONFIRMED. Minimal repair scope in the task is appropriate; no source mutation performed by reviewer.
