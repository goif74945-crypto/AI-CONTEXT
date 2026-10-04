# C1 — Interpretation Convergence Gate (ICG)

Status: `AI_PROPOSED_CONCEPT`

## Objective
Reduce unnecessary clarification without guessing. If every **admissible** interpretation of an unresolved request yields the same canonical decision signature, ambiguity is operationally irrelevant and can be released to the existing authority path. If signatures differ, freeze.

## Inputs
- finite set of `Interpretation(id, variables)` supplied by an upstream authorized ambiguity enumerator;
- deterministic evaluator mapping each interpretation to `DecisionSignature(action, target, scope, effects, authority_epoch)`.

## Invariants
1. ICG never creates an interpretation.
2. ICG never decides which interpretation is “probably intended.”
3. RELEASE requires all evaluated signature hashes to be identical.
4. Duplicate interpretation identity, empty candidate set, or evaluator failure fails closed.
5. Scope/effect ordering is canonicalized so representation order cannot create false divergence.

## Output
- `RELEASE / ALL_ADMISSIBLE_INTERPRETATIONS_CONVERGE` with witness list; or
- `FREEZE / DECISION_RELEVANT_AMBIGUITY` with exact divergent decision fields; or
- fail-closed structural/evaluator reason.

## Failure model
- No interpretations → FREEZE.
- Duplicate IDs → FREEZE.
- Evaluator exception → FREEZE.
- Any signature divergence → FREEZE.

## Security / authority boundary
ICG must be downstream of interpretation admissibility and authority resolution. A malicious interpretation source could omit a relevant meaning; ICG does not compensate for that.

## NEXY value
It preserves the zero-guess law while avoiding questions whose answers provably cannot change action/target/scope/effect/authority epoch.
