# Counterfactual Verification Engine
Status: PROPOSAL / AI-PROPOSED CONCEPT / NOT CURRENT BUILD REQUIREMENT

## Objective
Test whether a candidate decision remains legal and verified when one relevant premise changes.

## Perturbation classes
- authority source superseded
- proof artifact invalidated
- target commit/config drift
- provider/dependency failure
- adversarial but schema-valid input
- duplicate/reordered event
- explicit assumption becomes false
- observability source missing

## Output states
STABLE, NOT_VERIFIED, CONFLICT, FREEZE_REQUIRED, ALTERNATE_EVIDENCE_REQUIRED.

## Contract
Counterfactual tests never replace executed verification. They identify fragility and missing proof obligations.

## Example
Candidate: provider integration release.
Perturb: timeout after external side effect, duplicate callback, schema-valid contradiction, provider version drift.
Expected artifact: exact status transition and affected proof dependencies, not a vague robustness score.

## Guardrails
- finite scenario coverage never proves universal robustness
- generated failures are scenarios, not observed facts
- model creativity has no authority
- combinatorial growth must be bounded by criticality and dependency graph

## Future evidence
Unit: deterministic perturbation expansion.
Integration: evidence invalidation propagation.
E2E: decision + perturbation -> expected legal status.
Abuse: perturbation cannot fabricate evidence or elevate authority.
