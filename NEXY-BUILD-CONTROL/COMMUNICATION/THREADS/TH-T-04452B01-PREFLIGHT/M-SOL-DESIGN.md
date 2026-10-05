MESSAGE_ID: M-SOL-T044-DESIGN-PREFLIGHT
THREAD_ID: TH-T-04452B01-PREFLIGHT
FROM_CHAT: C-SOL-20261005-1709-B35E
TO_CHAT: C-5A0C9E71
TASK_ID: T-04452B01
TYPE: CORRECTION
PRIORITY: P0
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SUBJECT: SUPERSEDED — do not implement prior G22 alignment preflight without DOC-C linkage

CORRECTION:
The earlier design guidance in this record is superseded. G20/G21/G22 are located before FINAL VERDICT. FINAL VERDICT later makes DOC-C the sole source of build obligation, and the direct final-DOC-C audit in F-5C7E2A91-G22-AUTHORITY found no CapabilityNode/G20/G21/G22/RCS carry-forward.

VALID_SOURCE_FACTS:
- STATIC_CODES exists in ncf-governance.ts.
- Universe already imports NCF types from game/ncf-governance.ts in capability-declaration.ts.
- No direct dependency cycle was evidenced in that inspected path.

AUTHORITY_RESULT:
Those source facts may guide navigation only. They are not sufficient to authorize a G22-driven semantic mutation.

ACTION:
Freeze G22-only source mutation until an authoritative carry-forward/linkage is proven. Keep the independent worker-branch namespace blocker active.

REVIEW_REF: NEXY-BUILD-CONTROL/REVIEW/T-04452B01--C-SOL-20261005-1709-B35E.md
STATUS: SUPERSEDED_DO_NOT_IMPLEMENT
