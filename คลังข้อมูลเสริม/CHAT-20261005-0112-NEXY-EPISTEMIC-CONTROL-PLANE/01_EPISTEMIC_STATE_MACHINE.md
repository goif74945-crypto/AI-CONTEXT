# Epistemic State Machine
Purpose: model knowledge as state, not boolean.
States: UNSEEN → CLAIMED → SOURCED → CORROBORATED → VERIFIED; side states STALE, CONTESTED, SUPERSEDED, REVOKED, UNVERIFIABLE, SCOPE_BOUND.
A claim record should include claim_id, proposition, scope, validity interval, observation/verification times, source version, evidence class, dependencies, contradictions, verification method, status, revocation reason.
Invariants: VERIFIED is not immortal; newer is not automatically higher authority; contradictions remain queryable; derived claims inherit freshness limits; scope expansion requires re-verification; agent confidence never upgrades evidence class.
NEXY fit: conceptual control between VAULT provenance and JUDGE.
Status: DESIGN PROPOSAL.