# Test Plan

## Static / E1
- strict TypeScript compilation;
- no-float/random/wall-clock token scan of authoritative `src/`;
- package dry-run;
- common credential/private-key pattern scan.

## Unit / E2
- exact Q64 anchors, multiplication/division, overflow, zero division, unit bounds;
- each major court failure mode: source dependence, collusion, strong minority proof, conflict evidence, monoculture concentration, physical deletion, evidence-dropping archive, sham reconsideration, unexplained precedent divergence, missing dissent, proof deadlock, missing explanation, assumption contamination, future evidence, invalid burden policy;
- adapter target pin validation and no-mutation authority flags.

## Determinism / property-style
- exhaustive Q64 monotonicity across denominators 1..128;
- additional ratio repeatability through denominator 512;
- five evidence-order rotations;
- 1,000 deterministic presentation/order perturbations inside test suite;
- independent 1,000-run canonical replay proof.

## Integration-like local boundary / E3-reference
`examples/integration_example.mjs` builds a full `CourtCase`, evaluates all 20 organs, asserts `READY_FOR_EXTERNAL_JUDGE`, and asserts all mutation/promotion capability flags are false.

## Explicitly not proven
- NEXY process/runtime wiring;
- database/queue/API integration;
- deployment;
- production operational behavior;
- physical systems.
