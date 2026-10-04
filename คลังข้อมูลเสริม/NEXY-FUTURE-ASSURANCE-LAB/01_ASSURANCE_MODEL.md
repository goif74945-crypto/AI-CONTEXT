# Assurance Model

Status: AI-PROPOSED CONCEPT

## Source-aligned premise
SOURCE_FACT: NEXY separates design, implementation, runtime, and deployment truth. SOURCE_FACT: verification/freeze behavior is central to the project context.

## Proposal: Assurance Case Graph
Represent every important capability as:
`CLAIM -> INVARIANT -> THREAT -> CONTROL -> TEST -> EVIDENCE -> STATUS -> EXPIRY`.

A capability is not releasable when any required edge is absent.

### Claim states
DRAFT, TESTABLE, EVIDENCED, REJECTED, STALE, CONFLICT, FROZEN.

### Invariant classes
- Authority invariant: lower authority cannot override higher authority.
- Scope invariant: execution cannot escape authorized scope.
- Evidence invariant: PASS cannot exceed evidence class.
- State invariant: replay from equivalent relevant state must preserve structural decision.
- Provenance invariant: durable facts retain origin and freshness.
- Recovery invariant: interrupted work resumes from verified checkpoint, not reconstructed imagination.
- Isolation invariant: parallel agents cannot silently overwrite each other's authoritative state.

## Assurance debt
Track debt explicitly:
- missing oracle
- missing negative test
- stale evidence
- unbounded side effect
- ambiguous ownership
- irreversible migration
- provider-specific hidden dependency
- unproven recovery

Debt is not automatically a blocker. Each item must have severity, affected invariant, deadline/trigger, and owner.

## Promotion rule
No proposal becomes candidate architecture until:
1. authority owner is named;
2. input/output contract is explicit;
3. failure semantics are explicit;
4. abuse/negative paths exist;
5. minimum evidence class is assigned;
6. rollback/recovery exists;
7. compatibility impact is classified.
