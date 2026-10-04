# Adoption Map

Status: **AI-PROPOSED**

HCAS should only be adopted after project authority explicitly approves it.

## Safe staged adoption
1. Documentation-only: use manifest format to review owner controls and freeze surfaces.
2. Non-blocking CI: run HCAS and collect findings without release gating.
3. Targeted gate: gate only high-impact control manifests after false-positive review.
4. E2E binding: map each manifest action to Playwright/API tests and evidence IDs.
5. Release binding: require current exact-revision HCAS + E3/E4 proofs.

## Required promotion evidence
- mapping from HCAS rules to authoritative NEXY requirements;
- false-positive/false-negative review on real surfaces;
- owner/operator usability review;
- proof that manifests cannot substitute for backend auth;
- regression tests tying manifest actions to runtime behavior;
- explicit decision record approving which profile is binding.

## Rollback
Because HCAS is advisory metadata/tooling, initial adoption should be reversible by removing the release gate while preserving historical reports. It must not mutate canonical state.
