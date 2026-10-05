# Independent Review — POST /api/directives contract

REVIEW_ID: RV-DOC-C4-DIRECTIVE-CREATE-C-2CFA8A5D
CHAT_ID: C-2CFA8A5D
TASK_ID: TASK-DOC-C4-DIRECTIVE-CREATE-CONTRACT-001
FINDING_ID: FINDING-DOC-C4-DIRECTIVE-CREATE-CONTRACT-001
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
ROLE: INDEPENDENT_SPEC_REVIEWER / RED_TEAM
RESULT: PARTIAL_CONFIRM_PARTIAL_AUTHORITY_CHALLENGE
SOURCE_MUTATION: NONE

CONFIRMED ACTIONABLE GAP:
- Final DOC-C paragraphs 10153-10202 explicitly require Audit: DIRECTIVE_CREATED for POST /api/directives.
- packages/api/directives.ts@608426cb persists EventLog.eventKind = DIRECTIVE_RECEIVED and AuditLog.action = DIRECTIVE_RECEIVED on accepted creation.
- Exact source search in the inspected handler finds no DIRECTIVE_CREATED implementation.
- This is a direct literal semantic mismatch independent of response-shape interpretation.
- Repair/test oracle should require DIRECTIVE_CREATED on accepted creation while preserving transactionality, idempotency binding and durable dispatch behavior.

AUTHORITY CHALLENGE:
- Final DOC-C success data shows directive_id, run_id and state:"RUNNING".
- Final DOC-C §4.1-§4.2 contains no rule that response object types are closed/exact and no clause forbidding additional response members.
- Therefore dispatch_status is a verified implementation field, but its mere presence has not yet been proven to be a SPEC_MISMATCH.
- The task clauses requiring an exact three-field response and tests rejecting every additional field exceed currently proven primary authority unless a separate active closed-response rule is located.

SAFE REPAIR SCOPE AFTER UNBLOCK:
1. Repair DIRECTIVE_RECEIVED -> DIRECTIVE_CREATED for the route-required accepted audit semantics.
2. Add focused tests proving both event/audit evidence and idempotent replay behavior.
3. Do not remove dispatch_status solely because it is not listed in the displayed response type until closed-response authority is proven.
4. Preserve CSRF, session/device binding, OWNER/OPERATOR RBAC, ownership, request fingerprinting, SERIALIZABLE persistence, durable dispatch and fail-closed dependency handling.

RELATED_AUTHORITY_FINDING:
F-2CFA8A5D-DOC-C4-EXACTNESS-AUTHORITY

VERDICT:
ACTIONABLE audit-name gap CONFIRMED.
Response-extra-field defect classification NOT YET VERIFIED.
