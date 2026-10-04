# HCAS Rule Catalog

All rules below are HCAS advisory controls. Their provenance and promotion status must not be confused with current NEXY build law.

| Rule | Purpose | Default severity |
|---|---|---|
| HCAS-001..006 | root/schema/action structure | ERROR/WARNING |
| HCAS-010..011 | stable unique action identity | ERROR |
| HCAS-020..022 | side-effect/mutation consistency | ERROR |
| HCAS-030 | mutating action declares backend authorization | ERROR |
| HCAS-040..042 | confirmation policy; strict-future dual approval | ERROR |
| HCAS-050 | mutating action has audit event | ERROR |
| HCAS-060 | explicit fail-closed failure mode | ERROR |
| HCAS-070 | one defined structural action result | ERROR |
| HCAS-080..081 | evidence class is explicit/sane | ERROR/WARNING |
| HCAS-090..091 | user can see success/block/failure-or-freeze outcomes | ERROR |
| HCAS-100..101 | backend role and UI visibility role are separately explicit | ERROR |
| HCAS-110..111 | FREEZE surface visible, sticky, authoritative, unmaskable | ERROR |
| HCAS-120..122 | pending/loading is not evidence or success | ERROR |
| HCAS-130..131 | action and accessibility names exist | ERROR |
| HCAS-140..142 | reversibility/rollback/irreversible warning explicit | ERROR |

## Provenance mapping
Directly motivated by current project context:
- role hiding != backend authorization;
- dangerous action confirmation;
- FREEZE visibility and sticky mobile banner;
- pending animation != evidence;
- explicit real-state UI.

AI-proposed normalization:
- exact JSON field names;
- exact rule identifiers;
- `strict_future` profile;
- evidence requirement field per action;
- exact visible-outcome set;
- rollback metadata shape.
