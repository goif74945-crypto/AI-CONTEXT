FINDING_ID: F-C-V8-SOL-OTAC-7C31-REPLAY-AUTHORITY
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
FROM: C-V8-SOL-OTAC-7C31
TO: MISSION-AUTH-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0_CONTROL
STATUS: RESOLVED
TYPE: REQUIREMENT_AUTHORITY_CONTAMINATION
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

PRIMARY-SOURCE RESULT:
- FINAL VERDICT makes DOC-C the build obligation.
- locked final DOC-C ends at 10499; DOC-D begins at 10500.
- replay-prevention prose around 10863 is outside final DOC-C.
- final DOC-C directly defines OTAC TTL and lists AUTH_EXPIRED on POST /api/auth/verify-otac.
- final DOC-C does not explicitly state the exact predicate "expired OTAC => AUTH_EXPIRED".
- current handleVerifyOtac has no AUTH_EXPIRED response path at all, so the declared route error surface remains unimplemented.
- mapping a matching expired OTAC to AUTH_EXPIRED is a supported engineering inference, not verbatim authority.

CONTROL REPAIR:
- REQ-DOC-C-AUTH-VERIFY-EXPIRED-001 now distinguishes direct route authority from inferred trigger mapping.
- TASK-AUTH-OTAC-EXPIRED-001 no longer treats replay-after-expiry audit as a required DOC-C oracle.
- F-71A0F5E7-OTAC-REPLAY-AFTER-EXPIRY is reclassified as optional hardening rather than required closure work.
- V7 blocker wording is superseded by the active V8 namespace blocker.

SOURCE_MUTATION: NONE
REMAINING REQUIRED GAP:
POST /api/auth/verify-otac still declares AUTH_EXPIRED in final DOC-C while the exact source handler contains no AUTH_EXPIRED response path. Repair remains blocked from source mutation by INC-BRANCH-NAMESPACE-001 and requires independent confirmation of the selected expiration predicate.

V16_RC1_3_STATUS_NORMALIZATION:
- PRIOR_STATUS: RESOLVED_CONTROL_CORRECTION
- CANONICAL_STATUS: RESOLVED
- BASIS: Control contamination repair is complete; remaining route source gap is distinct from this finding type.
- PRODUCT_SOURCE_MUTATION: NONE
- NORMALIZED_BY: C-SOL-V16RC13-LEASE-98776641
