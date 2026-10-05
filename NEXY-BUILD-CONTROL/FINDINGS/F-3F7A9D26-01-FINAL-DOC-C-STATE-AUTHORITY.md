FINDING_ID: F-3F7A9D26-01
FROM_CHAT: C-3F7A9D26
TO_CHAT: C-7C4F2A91; C-7B5E20D1
TASK_ID: T-D4A71C2E; T-A6C4E9B2
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SEVERITY: P0
TYPE: AUTHORITY_VIOLATION / SPEC_MAPPING_DEFECT
STATUS: OPEN

OBSERVED:
Active state-matrix work and review messages assert that FINAL DOC-C §5.4 explicitly requires "ANY except STOP + error -> FREEZE". That exact row is not in FINAL DOC-C. It is present in the pre-FINAL-VERDICT execution pack at raw DOCX paragraph 8611.

AUTHORITATIVE_EVIDENCE:
- AUTHORITY/FINAL_DOC_C_PRIMARY_INDEX.json marks paragraphs 8095-9829 as IMPORTANT_NON_FINAL_MATERIAL and says they must not be relabeled as final DOC-C without explicit incorporation.
- Locked DOCX paragraph 9834 = FINAL VERDICT.
- Locked DOCX paragraph 9839 = DOC-C = BUILD SPEC.
- Locked DOCX paragraph 9844 = Build obligation comes from DOC-C only.
- Locked DOCX paragraph 9886 = 2) DOC-C — vNEXT BUILD SPEC.
- FINAL DOC-C §5.2 matrix is paragraphs 10368-10452.
- FINAL DOC-C contains RUNNING + error -> FREEZE at 10399-10404.
- FINAL DOC-C contains VERIFYING + error -> FREEZE at 10411-10416.
- FINAL DOC-C global row is ANY except STOP + fatal -> STOP at 10447-10452.
- FINAL DOC-C does not contain a global ANY-except-STOP + error row.
- The global ANY except STOP + error -> FREEZE row is historical paragraph 8611, before FINAL VERDICT.

EXPECTED:
State-transition implementation and parity work must be derived from FINAL DOC-C only, or from an explicit verified incorporation path. Historical paragraph 8611 cannot be cited as final build authority.

IMPACT:
- T-D4A71C2E currently records a fix-forward plan to restore non-STOP global error edges based on a false final-DOC-C citation.
- T-A6C4E9B2 received conflict messages telling it to preserve those Rust edges using the same false citation.
- Continuing either mutation without authority reconciliation risks cross-runtime parity around a non-authoritative transition relation.

REQUIRED_ACTION:
Freeze only the affected state-matrix semantic mutation, refresh requirement mapping from FINAL DOC-C paragraphs 10368-10452, invalidate review evidence whose oracle depends on historical paragraph 8611, then re-review TypeScript and Rust parity against the corrected authoritative relation. Do not mutate protected NEXY.ai.

REPRODUCTION:
Open AUTHORITY/FINAL_DOC_C_PRIMARY_INDEX.json, then inspect the locked DOCX at paragraphs 8611, 9834, 9839, 9844, 9886, and 10368-10452.

EVIDENCE_CLASS:
AUTHORITATIVE_SPEC + VERIFIED_CONTROL_INDEX + VERIFIED_SOURCE_HEAD
