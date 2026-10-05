FINDING_ID: F-2CFA8A5D-DOC-C4-EXACTNESS-AUTHORITY
TYPE: DERIVED_REQUIREMENT_AUTHORITY_GAP / FALSE_POSITIVE_REPAIR_RISK
SEVERITY: P1_CONTROL
STATUS: OPEN
REVIEWER_CHAT: C-2CFA8A5D
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
AFFECTED_RECORDS:
- REQ-DOC-C-4-2-ARTIFACT-REVISIONS
- FINDING-DOC-C4-ARTIFACT-REVISIONS-001
- TASK-DOC-C4-ARTIFACT-REVISIONS-001

FACT:
- FINAL VERDICT binds build obligation to final DOC-C.
- Final DOC-C §4.1-§4.2 is raw DOCX paragraphs 10027-10352.
- GET /api/artifacts/:id/revisions declares response fields revision_id, revision_no, created_at, created_by and optional next_cursor.
- The primary DOC-C text in §4.1-§4.2 contains no clause stating response objects are exact/closed, no `strict`, `exact`, `no extra`, `additional fields forbidden`, or equivalent rule for response members.
- Within §4.1-§4.2, `only` appears for specific authorization/audit clauses, not as a response-shape closure rule.
- packages/api/canonical.ts@608426cb emits additional fields on the artifact-revisions response. That source fact is real.
- The derived requirement currently upgrades the listed response members into an exact closed wire schema and forbids extra fields, but that prohibition is not present in its quoted SPEC_TEXT and was not located in the primary final-DOC-C section.

ASSUMPTION:
- Treating a TypeScript-shaped response declaration as a closed runtime object schema is an engineering interpretation unless the authoritative spec separately states closed/exact response semantics.

UNKNOWN:
- Whether another active final-DOC-C clause outside §4.1-§4.2 establishes a global closed-response rule. No such clause has yet been proven.

RISK:
Deleting implementation fields on the premise that the canonical response is closed may mutate behavior beyond proven build authority and can create avoidable UI/client regressions.

REQUIRED_ACTION:
- Freeze source deletion/narrowing whose sole authority is the unproven exact-response assumption.
- Locate explicit active DOC-C authority for closed response semantics, or reclassify the extra fields as not-yet-proven mismatches.
- Preserve independently proven route requirements: required fields, auth/RBAC, pagination, audit emission, and error behavior.

VERDICT:
The extra fields are VERIFIED SOURCE FACT. Their classification as SPEC_MISMATCH is NOT YET VERIFIED from primary final-DOC-C authority.
