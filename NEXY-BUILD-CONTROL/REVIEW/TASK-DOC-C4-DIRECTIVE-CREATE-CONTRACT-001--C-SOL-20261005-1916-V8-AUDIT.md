# Second Independent Review — TASK-DOC-C4-DIRECTIVE-CREATE-CONTRACT-001

REVIEW_ID: RVW-DOC-C4-DIRECTIVE-CREATE-C-SOL-20261005-1916-V8-AUDIT
TASK_ID: TASK-DOC-C4-DIRECTIVE-CREATE-CONTRACT-001
FINDING_ID: FINDING-DOC-C4-DIRECTIVE-CREATE-CONTRACT-001
REVIEWER_CHAT: C-SOL-20261005-1916-V8-AUDIT
ROLE: INDEPENDENT_SPEC_REVIEWER / RED_TEAM
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_MUTATION: NONE

## PRIMARY AUTHORITY
Final DOC-C raw 10153-10202:
- session required
- OWNER / OPERATOR
- idempotency required
- same key returns same accepted run
- Audit: DIRECTIVE_CREATED
- success response declares directive_id, run_id, state:"RUNNING"

## EXACT-HEAD SOURCE FACTS
packages/api/directives.ts blob 8cd214c87e5aa55561e52347802ec8172feadc36:
- accepted transaction writes EventLog.eventKind = DIRECTIVE_RECEIVED
- accepted transaction writes AuditLog.action = DIRECTIVE_RECEIVED
- idempotent replay is bound to the same session and canonical request hash
- successful new and replay responses include directive_id, run_id, state:"RUNNING", and dispatch_status

## VERDICT
DIRECTIVE_CREATED_AUDIT_MISMATCH: CONFIRMED_ACTIONABLE_P1
IDEMPOTENCY_BINDING: PRESENT
SUCCESS_DECLARED_FIELDS: PRESENT
DISPATCH_STATUS_EXTRA_FIELD_DEFECT: NOT_VERIFIED
REVIEW_RESULT: CONFIRM_CORE_GAP_WITH_SCOPE_NARROWING

The audit name is a direct literal mismatch and needs repair plus focused evidence. By contrast, final DOC-C provides a TypeScript response shape but no separately proven closed-object/no-extra-members law. Removing dispatch_status solely because it is unlisted would add an unproven constraint. Preserve it unless active authority establishes exact/closed wire semantics.

## SAFE REPAIR AFTER UNBLOCK
1. Change accepted route audit/event semantics to DIRECTIVE_CREATED.
2. Prove new submission and same-key replay still preserve idempotency and durable dispatch.
3. Add focused negative oracle for the audit-name mismatch.
4. Treat response exactness as a separate authority question; do not bundle an unproven field removal.
5. Do not touch the separate state/event matrix repair scope.

GLOBAL_BLOCKER: INC-BRANCH-NAMESPACE-001 prevents Constitution-compliant isolated source mutation.
