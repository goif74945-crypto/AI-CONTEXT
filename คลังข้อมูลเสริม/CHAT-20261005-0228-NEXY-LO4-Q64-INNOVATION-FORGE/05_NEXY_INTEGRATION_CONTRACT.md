# Proposed NEXY Integration Contract

Classification: `AI_PROPOSED_LO4_ONLY / NOT_INTEGRATED`

## Source-aligned facts
Current AI-CONTEXT describes NEXY as deterministic, evidence-first, freeze-on-ambiguity, with external AI workers below NEXY authority. It separates design, implementation, runtime, and deployment truth.

## Proposed adapter boundary
If formally adopted later, integration should be additive:
1. NEXY prepares an explicit, already-authorized typed payload.
2. An adapter maps only necessary quantitative fields to decimal-string Q64 inputs.
3. The Lo4 evaluator returns structured `PASS | FREEZE | REJECT`, reasons, Q64 values, and a deterministic digest.
4. NEXY validates the response schema and provenance.
5. NEXY LAW/JUDGE/Safety/Execution layers decide whether that evidence has any operational consequence.

## Forbidden integration behavior
- no direct database mutation from the Forge;
- no direct policy/law mutation;
- no implicit promotion of Lo4 code;
- no automatic release/deployment;
- no use of module score as a substitute for required evidence class;
- no fallback to float if Q64 parsing fails;
- no swallowing FREEZE into “best effort” PASS;
- no hidden conversion of missing data to defaults except explicit defaults in each concept contract.

## Suggested adoption gates
Before any concept enters NEXY implementation scope:
- map it to an explicit authoritative requirement;
- independent mathematical review of its formula and thresholds;
- domain-specific calibration evidence where scores imply real-world meaning;
- typed adapter/schema review;
- integration tests against exact NEXY revision;
- negative/fault tests proving FREEZE propagation;
- performance/load characterization at expected scale;
- security and data-minimization review;
- rollback/version migration contract;
- explicit human/project promotion decision.

## Compatibility note
The standalone engine has deliberately narrow inputs and outputs so a future TypeScript/Node adapter could integrate without requiring changes to the conceptual NEXY authority chain. This is design compatibility, not implementation proof.
