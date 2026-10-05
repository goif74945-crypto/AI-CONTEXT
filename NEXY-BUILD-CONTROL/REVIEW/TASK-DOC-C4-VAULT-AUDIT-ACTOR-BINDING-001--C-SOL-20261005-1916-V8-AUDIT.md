# Independent Review — TASK-DOC-C4-VAULT-AUDIT-ACTOR-BINDING-001

REVIEW_ID: RVW-DOC-C4-VAULT-ACTOR-C-SOL-20261005-1916-V8-AUDIT
TASK_ID: TASK-DOC-C4-VAULT-AUDIT-ACTOR-BINDING-001
FINDING_ID: FIND-DOC-C4-VAULT-AUDIT-ACTOR-SPOOF-001
REVIEWER_CHAT: C-SOL-20261005-1916-V8-AUDIT
ROLE: SHADOW_REVIEW / SPEC_AUDIT / RED_TEAM
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_MUTATION: NONE

## VERIFIED SOURCE FACTS
- packages/api/canonical.ts authenticates a session/role, then forwards parsed.data.metadata.created_by as internalRequest.authorId.
- vault/repository.ts uses req.authorId in computeAuditChain(...) and persists AuditLog.actor=req.authorId with AuditLog.role=req.authorRole.
- tests/contract/canonical-api.test.ts accepts authenticated userId USER0000000000000000000001 while metadata.created_by is "owner" and expects authorId "owner".

## VERIFIED FINAL DOC-C FACTS
- Raw 10030: mutating routes require secure session + CSRF except OTAC request/verify.
- Raw 10273-10276: POST /api/vault/commit requires session; RBAC OWNER / SYSTEM.
- Raw 10281-10282: audit emission is VAULT_COMMIT_CREATED.
- Raw 10283-10295: canonical request includes metadata.created_by, metadata.timestamp, metadata.idempotency_key.
- Within final DOC-C raw 9886-10499, no inspected clause defines AuditLog.actor identity mapping, states actor must equal session userId, or states metadata.created_by is non-authoritative provenance only.

## AUTHORITY CHALLENGE
The observed caller-controlled created_by -> authorId -> AuditLog.actor dataflow is real. However, the proposed EXPECTED behavior in the finding is not yet derivable from final DOC-C alone. Final DOC-C explicitly requires both authenticated session/RBAC and a created_by request field, but does not define their identity relationship. Older pre-final audit/accountability text cannot silently become DOC-C build obligation.

## VERDICT
OBSERVED_SOURCE_DATAFLOW: CONFIRMED
SECURITY_DEFECT_CLASSIFICATION: NOT_VERIFIED
AUTHORITY_VIOLATION_CLASSIFICATION: NOT_VERIFIED
DATA_INTEGRITY_DEFECT_CLASSIFICATION: NOT_VERIFIED
TEST_ORACLE_DEFECT_CLASSIFICATION: NOT_VERIFIED
IMPLEMENTATION_AUTHORITY: INSUFFICIENT
REVIEW_RESULT: CHANGES_REQUESTED_BEFORE_IMPLEMENTATION

## REQUIRED RESOLUTION
Before implementing actor binding, identify a valid final-DOC-C incorporation path defining actor identity semantics, or record a SPEC_GAP/SPEC_CONFLICT and freeze only this semantic sub-scope. Do not infer actor=session-user merely from general security preference.

GLOBAL_BLOCKER: INC-BRANCH-NAMESPACE-001 remains independently applicable to all source mutation.
