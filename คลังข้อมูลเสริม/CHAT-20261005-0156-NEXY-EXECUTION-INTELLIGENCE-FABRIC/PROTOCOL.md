# Integration Protocol v1

**Status:** AI-proposed experimental adapter, not canonical NEXY API law.

## Boundary
EIF exchanges JSON-like objects only. It does not call providers, execute tools, write repositories, or mutate external state.

## Input sections
- `goal_spec`: required/forbidden facts, required capabilities, forbidden effects, required outputs.
- `observed`: current facts/capabilities/effects/outputs.
- `uncertainty`: blocked requirements, known facts, and available probes/questions.
- `assurance`: evidence dimensions, independent-domain counts, validator metadata, optional cost budget.
- `actions`: action dependency graph with reversibility/compensation metadata.
- `input_schema` + `valid_case`: source contract for negative-vector synthesis.

## Output
`NEXY_EXECUTION_INTELLIGENCE_FABRIC_V1` returns:
- `status`: `READY | ASK | FREEZE`;
- `decision_id`: stable SHA-256-derived structural identity;
- goal evaluation;
- selected unknown-resolution probes/questions;
- selected assurance validators;
- execution/rollback plan and point of no return;
- counterexample suite identity/count.

## Suggested NEXY placement
A future integration could invoke EIF between task normalization and RUN/JUDGE execution:

`REQUEST → LAW/Task Contract → EIF → {ASK | FREEZE | READY} → RUN → existing verification/JUDGE`

EIF never outranks USER LAW, NEXY LAW, JUDGE, or verified runtime evidence.
