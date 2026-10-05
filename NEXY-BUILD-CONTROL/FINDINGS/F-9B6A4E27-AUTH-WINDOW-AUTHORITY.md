FINDING_ID: F-9B6A4E27-AUTH-WINDOW-AUTHORITY
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
TASK_ID: TASK-AUTH-OTAC-WINDOW-001
FROM: C-9B6A4E27
TO: MISSION-AUTH-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0
STATUS: OPEN
TYPE: REQUIREMENT_AUTHORITY_CONTAMINATION

## OBSERVED
The canonical requirement packet attributes a "bounded 32-slot scan" and TypeScript/Rust bounded-window parity to final DOC-C authority.

## PRIMARY-SOURCE CHECK
Locked spec SHA-256:
b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

Final Verdict:
- DOC-C = BUILD SPEC
- Build obligation comes from DOC-C only.

Final DOC-C §2.3 paragraphs 9910-9949 defines auth defaults:
- otac_length
- otac_ttl_ms
- otac_max_attempts
- otac_resend_cooldown_ms
- otac_lock_window_ms
- session_ttl_ms
- concurrent_sessions_per_user

It does not define session_slots / SESSION_SLOTS / 32-slot scan.

The requirement packet cites final DOC-C paragraphs 10071-10105 and 10853-10860. Those establish:
- verify-otac verifies a one-time code and creates a session
- AUTH_INVALID and AUTH_EXPIRED are canonical route errors
- OTAC is one-time use
- consumed replay => AUTH_INVALID + security audit

They do not establish a 32-slot scan width or Rust-ring equivalence.

A full paragraph-text search of the locked DOCX found no session_slots, SESSION_SLOTS, "32 slots", or "32-slot" build clause.

## SOURCE CHECK
packages/api/vnext-config.ts explicitly labels salt_bytes, token_bytes, and session_slots as:
"Internal crypto parameters (not part of DOC-C §2.3 canonical config)"
and sets session_slots = 32.

REQ-DOC-C-2-3-VNEXT-DEFAULTS independently states:
"Implementation-only extensions, if retained, are not attributed to DOC-C canonical authority."

## SUPPORTED REQUIREMENT CORE
FACT:
A newly issued valid non-expired unconsumed OTAC must remain verifiable; otherwise POST /api/auth/verify-otac fails its DOC-C purpose.

FACT:
Retained historical rows currently can starve newer rows because packages/api/auth.ts orders createdTick ascending and take=32.

## UNSUPPORTED ATTRIBUTION
The number 32 and the bounded-window implementation strategy are implementation hardening / architecture choices, not final DOC-C product obligations based on the inspected source.

Rust parity may still be required by Constitution V7 if the Rust gate and TypeScript route are proven to implement the same active behavior, but that relationship must be established separately; it cannot be smuggled into DOC-C citation.

## IMPACT
A test oracle that says "DOC-C requires exactly 32 slots" would be false authority.
The valid-code starvation defect can still be repaired, but the repair must distinguish:
1. DOC-C behavior: valid active OTAC is verifiable.
2. retained implementation hardening: fixed-width constant-time scan, if preserved.
3. parity obligation: only after confirming both implementations share the same active contract.

## REQUIRED ACTION
Correct REQ-DOC-C-AUTH-VERIFY-WINDOW-001 authority attribution before promoting it to VERIFIED.
Do not delete the 32-slot hardening merely because it is not DOC-C; preserve/constrain it unless evidence supports removal.
Do not use the 32 value itself as a DOC-C-derived oracle.
