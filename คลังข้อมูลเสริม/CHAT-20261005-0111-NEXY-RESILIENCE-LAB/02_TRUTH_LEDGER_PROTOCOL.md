# Truth Ledger Protocol

## Problem
An agent can be locally correct and globally wrong when claims from different times, authorities, or evidence classes collapse into one undifferentiated context.

## Claim tuple
Represent material claims as:
`<claim_id, proposition, truth_class, authority, observed_at, valid_from, valid_until, scope, evidence_ref, dependencies, status>`.

Truth classes inherit AI-CONTEXT: SOURCE_FACT, REPO_FACT, RUNTIME_FACT, EXTERNAL_FACT, INFERENCE, ASSUMPTION, UNKNOWN, CONFLICT, NOT_VERIFIED.

## Laws
1. No claim promotion without evidence.
2. A newer observation does not automatically outrank a stronger authority.
3. Runtime proves behavior at an observed state, not eternal correctness.
4. Absence of evidence is UNKNOWN unless an exhaustive negative test establishes absence.
5. Derived claims must retain dependency edges.
6. When a dependency expires, descendants become STALE_PENDING_REVALIDATION.
7. Contradictions are stored, not averaged away.

## Temporal invalidation
Invalidate claims when commit, deployment, configuration, schema, dependency version, external source, or policy authority changes.

## Negative knowledge
Record disproven paths as first-class artifacts:
- attempted action
- preconditions
- observed failure
- evidence
- safe retry conditions
This prevents future agents from paying the same failure cost repeatedly.

## Acceptance tests
A truth ledger passes only when every completion-critical claim has a matching evidence class, timestamp/scope, and no unresolved stronger contradiction.
