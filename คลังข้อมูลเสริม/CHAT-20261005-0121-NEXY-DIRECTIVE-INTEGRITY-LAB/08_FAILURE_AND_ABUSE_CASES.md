# Failure and Abuse Case Catalog

Status: AI-PROPOSED TEST/THREAT CATALOG

## F1 — Scope smuggling
Parent permits `project:alpha`; child adds `repo:other`. Expected: `SCOPE_BROADENED` -> FREEZE unless exact `/scope_in` authorization exists.

## F2 — Safety exclusion loss
Parent says `repo:NEXY.AI-` is out of scope; child omits it. Expected: `SCOPE_EXCLUSION_REMOVED` -> FREEZE.

## F3 — Action substitution
Parent `ACTION_RUN`; child `ACTION_EXPORT`. Expected: `ACTION_CHANGED` -> FREEZE.

## F4 — Target alias drift
Action stays the same while target changes from project A to project B. Expected: `TARGET_CHANGED` -> FREEZE.

## F5 — Side-effect laundering
A read calculation gains `write:file` or external notification. Expected: `SIDE_EFFECT_ADDED` and likely mutation escalation -> FREEZE.

## F6 — Privilege/mutation escalation
READ_ONLY becomes REVERSIBLE_MUTATION or IRREVERSIBLE_MUTATION. Expected: `MUTATION_ESCALATED` -> FREEZE.

## F7 — Constraint evaporation
A token cap, deterministic requirement, explicit prohibition, or other normalized constraint disappears. Expected: `CONSTRAINT_DROPPED` -> FREEZE.

## F8 — Authority evaporation
A governing user directive or law reference disappears. Expected: `AUTHORITY_REF_REMOVED` -> FREEZE.

## F9 — Ambiguity laundering
OPEN becomes RESOLVED because a model guessed. Expected: `AMBIGUITY_RESOLVED_WITHOUT_CLARIFICATION` -> FREEZE.

## F10 — Risk washing
HIGH becomes LOW with no new assessment evidence. Expected: `IMPACT_DOWNGRADED_WITHOUT_EVIDENCE` -> FREEZE.

## F11 — Parent substitution/replay
Child points to an unrelated parent. Expected: `PARENT_DIGEST_MISMATCH` -> FREEZE.

## F12 — Shadow re-authorization conflict
Two grants target the same semantic path. Reference model rejects duplicate grant paths rather than picking one by ordering.

## F13 — Set-order nondeterminism
Identical semantic sets arrive in different insertion orders. Expected: same digest.

## F14 — Malformed/blank semantic items
Whitespace-only entries must be rejected before comparison.

## Research-only cases not solved here
Semantic equivalence of free-form text, cross-language intent equivalence, ontology aliasing, signed authorization provenance, stale authorization, capability hierarchies, policy conflicts, and semantic diff across schema migrations require separate authoritative design/evidence.
