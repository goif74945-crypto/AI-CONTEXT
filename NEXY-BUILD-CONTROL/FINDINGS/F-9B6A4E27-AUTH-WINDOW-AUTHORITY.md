FINDING_ID: F-9B6A4E27-AUTH-WINDOW-AUTHORITY
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
TASK_ID: TASK-AUTH-OTAC-WINDOW-001
FROM: C-9B6A4E27
TO: MISSION-AUTH-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0
STATUS: RESOLVED_CONTROL_CORRECTION
TYPE: REQUIREMENT_AUTHORITY_CONTAMINATION

## OBSERVED
The initial requirement/task treated a bounded 32-slot scan and TypeScript/Rust bounded-window parity as final DOC-C authority.

## PRIMARY-SOURCE RESULT
- FINAL VERDICT makes DOC-C the BUILD SPEC and sole source of build obligation.
- final DOC-C auth defaults define OTAC/session parameters but not session_slots / SESSION_SLOTS / 32-slot scan.
- final DOC-C POST /api/auth/verify-otac requires verifying a one-time code and creating a session, with canonical AUTH_INVALID/AUTH_EXPIRED and related errors.
- the exact 32-slot width is implementation hardening in source, not a DOC-C product obligation.
- TypeScript/Rust parity is conditional on independently proving both implementations mirror the same active contract.
- raw paragraphs 10853-10860 are outside final DOC-C and may not be relabeled as final-DOC-C authority.

## RESOLUTION
REQ-DOC-C-AUTH-VERIFY-WINDOW-001 was corrected to preserve the valid-code reachability obligation while explicitly removing false 32-slot and unproven parity attribution.
TASK-AUTH-OTAC-WINDOW-001 was reconciled to the corrected authority.
FIND-AUTH-OTAC-WINDOW-001 was corrected so its spec evidence no longer cites post-DOC-C replay material as final DOC-C.

## REMAINING SOURCE GAP
The oldest-first bounded query still presents an evidence-backed P1 auth-availability defect at integration SHA 608426cb30398b1f3461866f7079d2a435c96b96. This finding closes only the control-authority contamination, not the source defect.

SOURCE_MUTATION: NONE
CONTROL_CORRECTION: APPLIED
