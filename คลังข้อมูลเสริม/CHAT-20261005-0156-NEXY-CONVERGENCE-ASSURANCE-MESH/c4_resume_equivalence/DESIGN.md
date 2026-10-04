# C4 — Resumption Equivalence Capsule (REC)

Status: `AI_PROPOSED_CONCEPT`

## Objective
Prove that a reconstructed execution state after handoff/restart is equivalent in the parts that matter to continuation and yields the same next legal action.

## State split
`ResumeState` separates:
- **resume-critical:** task ID, authority epoch, target identity, declared critical payload;
- **ephemeral:** UI/session/debug fields intentionally excluded from continuation identity.

## Capsule
The compiler stores:
- canonical critical state;
- critical-state SHA-256;
- next action;
- next-action SHA-256;
- capsule integrity hash.

## Verification order
1. required fields present;
2. capsule integrity hash valid;
3. schema supported;
4. reconstructed critical-state hash identical;
5. next-action function executes;
6. next-action hash identical.

## Invariants
- Ephemeral change alone does not invalidate resume.
- Critical drift freezes.
- Tampering fails.
- A changed next-action rule freezes even if the critical payload is unchanged.
- Mapping insertion order does not affect capsule identity.

## Integration note
REC complements existing freshness/HEAD/claim/lease revalidation. It does not replace those checks and must never revive expired authority.
