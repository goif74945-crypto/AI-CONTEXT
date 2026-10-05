# Independent Review — TASK-DOC-C4-READ-AUDIT-ACTOR-BINDING-001

REVIEWER_CHAT: C-SOL-20261005-1923-V8
TASK_ID: TASK-DOC-C4-READ-AUDIT-ACTOR-BINDING-001
FINDING_ID: FIND-DOC-C4-READ-AUDIT-ACTOR-ROLE-COLLAPSE-001
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
VERDICT: FINDING_NOT_PROVEN_BY_ACTIVE_BUILD_AUTHORITY
SOURCE_MUTATION: NONE

## Verified source fact

At the pinned integration SHA, `recordCanonicalRead` in `packages/api/directives.ts` receives an enum-like actor value and writes it into both `AuditLog.actor` and `AuditLog.role`. Several canonical read callers pass OWNER/AUDITOR role values instead of an authenticated user identifier. The source observation in the finding is therefore real.

## Authority review

The finding's decisive actor-vs-role authority is not final DOC-C:

- Final DOC-C ends at raw DOCX paragraph 10499.
- Paragraph 10500 starts `6) DOC-D — FINAL PRODUCT DESIGN PACK`.
- The cited AuditTable actor/role columns are raw paragraphs 10607-10616, inside DOC-D.
- The cited `AuditLog(actor_id, request_id, incident_id, created_at)` index is raw paragraph 10825, also inside DOC-D.
- Final DOC-C itself contains route-specific required audit event names and at 10499 says recovery emits AuditLog + EventLog, but no final DOC-C clause found in 9886-10499 requires AuditLog.actor to be principal/userId or forbids role-as-actor.

Per AUTHORITY_MAP and FINAL_DOC_C_PRIMARY_INDEX, build obligation comes from DOC-C only. DOC-D must not be silently promoted to equal build authority.

## Result

The source design may be undesirable for forensic identity, but under the active locked build authority it is not yet an evidence-proven SPEC_MISMATCH / AUTHORITY_VIOLATION.

Required disposition:
1. Do not implement this P1 repair solely from the cited DOC-D paragraphs.
2. Reclassify the task/finding to SPEC_AUTHORITY_GAP / UNPROVEN unless a valid DOC-C incorporation path or other active build authority is produced.
3. Preserve the source observation as raw evidence; do not promote it to verified actionable code gap.
4. If active authority is later established, re-open independent review before source mutation.

BLOCKER: INC-BRANCH-NAMESPACE-001 still independently blocks compliant source mutation even if authority is later established.
