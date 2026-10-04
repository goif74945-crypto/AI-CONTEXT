# Transition Rules and Failure Codes

Status: AI-PROPOSED / EXECUTABLE IN REFERENCE MODEL

The verifier compares one parent snapshot with one child snapshot. It does not perform natural-language inference.

| Code | Trigger | Default |
|---|---|---|
| `PARENT_DIGEST_MISMATCH` | child binds to a different parent digest | FREEZE |
| `ACTION_CHANGED` | action identity differs | FREEZE |
| `TARGET_CHANGED` | target identity differs | FREEZE |
| `CONSTRAINT_DROPPED` | child removes a parent constraint | FREEZE |
| `SCOPE_BROADENED` | child adds in-scope resource | FREEZE |
| `SCOPE_EXCLUSION_REMOVED` | child removes an explicit exclusion | FREEZE |
| `SIDE_EFFECT_ADDED` | child adds a side effect | FREEZE |
| `AUTHORITY_REF_REMOVED` | child loses authority reference | FREEZE |
| `MUTATION_ESCALATED` | child mutation class is stronger | FREEZE |
| `IMPACT_DOWNGRADED_WITHOUT_EVIDENCE` | child impact class is lower with no reassessment reference | FREEZE |
| `AMBIGUITY_RESOLVED_WITHOUT_CLARIFICATION` | OPEN becomes RESOLVED with no clarification reference | FREEZE |

A violation may be discharged only by an explicit `AuthorizedDelta` for the exact path. The reference implementation intentionally treats a grant as test/demo evidence only; a future production design must define who may issue grants, binding to actor/parent/child digests, expiry, replay law, and audit persistence.

## Monotonicity rationale

The default model is intentionally asymmetric. Narrowing `scope_in`, adding exclusions, adding constraints, retaining or adding authority references, and keeping mutation strength equal/lower are generally safe semantic refinements. The opposite direction can increase authority or impact and therefore requires explicit evidence.

This is not universally correct for every domain. For example, adding a constraint could create a conflict, and narrowing scope could make a task impossible. Those are downstream validity questions. This verifier only protects against unauthorized expansion/loss of safety meaning.
