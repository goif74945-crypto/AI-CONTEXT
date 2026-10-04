# Freeze Communication Protocol

**Classification:** AI-PROPOSED protocol derived from source UX laws.

## Problem
A strict system can still lose user trust if it freezes with vague copy, hides the cause, or presents an action the user cannot legally take. The opposite failure is worse: a polished UI can visually imply success while the backend is blocked.

## Protocol
When authoritative status or state is FREEZE:

1. Render FREEZE visibly and unambiguously.
2. Hide any candidate result even if a stale/internal payload exists.
3. Surface, when supplied:
   - incident code;
   - trigger;
   - blocking layer;
   - recoverable true/false;
   - request/trace identity.
4. Do not reinterpret unknown incident codes.
5. OWNER + recoverable=true may see `Recover` as a **request action** requiring confirmation and backend authorization.
6. Non-owner roles must not receive a Recover affordance from this reference layer.
7. Always retain a read/trace route when available.

## STOP protocol
STOP is not rendered as FREEZE-with-a-retry-button.

Reference behavior:
- headline: System stopped;
- block result;
- no automatic Recover action;
- expose trace/incident path;
- defer intervention to the explicit administrative procedure outside this UI compiler.

## HOLD protocol
HOLD exists only at presentation level when the system claims STABLE but the envelope supplied to the UI lacks sufficient release proof.

This avoids a dangerous inference:
`STABLE -> therefore user may see final output`.

Instead:
`STABLE + release proof -> RESULT`
`STABLE - release proof -> HOLD`

HOLD does not mutate or relabel the backend system state.

## Copy law
Reference copy avoids probabilistic softening such as:
- maybe;
- probably;
- try again and see;
- looks successful.

Unknowns are shown as unknown identifiers or generic blocked state. User-facing warmth may be added later, but not by changing the semantic result.
