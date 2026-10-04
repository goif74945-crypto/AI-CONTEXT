# Contradiction and Authority Engine

## Objective
Make conflicts explicit before execution. Agent systems fail dangerously when they merge incompatible instructions into a fictional compromise.

## Authority lattice
Use project-specific authority first. Generic fallback:
1. Current explicit user requirement
2. Authoritative project specification
3. Immutable project rules
4. Verified project state
5. Official external documentation
6. Direct tool observation
7. Derived engineering inference
8. Heuristic preference

Higher authority does not automatically erase a lower statement. Record supersession and scope.

## Conflict classes
C1 lexical: same term, different definitions.
C2 behavioral: mutually exclusive outputs for same trigger.
C3 scope: one statement includes what another excludes.
C4 temporal: old and new requirements disagree.
C5 evidence: sources assert incompatible facts.
C6 capability: requirement demands an unavailable operation.
C7 safety/integrity: requested action threatens an immutable invariant.

## Resolution protocol
- Identify exact statements.
- Normalize trigger/scope.
- Check whether conflict is real or contextual.
- Apply authority and recency only where authorized.
- Preserve losing statement as superseded provenance.
- If critical conflict remains, FREEZE affected mutation.
- Emit UNKNOWN rather than inventing reconciliation.

## Forbidden behavior
Never resolve a contradiction by silently reducing a MUST to SHOULD.
