# Failure / Recovery Library Validation

## Result
**PASS — source-defined and observed failures separated**

- records: **22**
- by kind: {"OBSERVED_CAMPAIGN_FAILURE":6,"SOURCE_RUNTIME_FAILURE":16}
- observed campaign blockers are explicitly distinguished from designed runtime failure modes.

## Rules
- Do not convert a SOURCE_RUNTIME_FAILURE into an observed historical incident unless evidence says it happened.
- Do not convert an OBSERVED_CAMPAIGN_FAILURE into a permanent architecture law.
- Every recovery must preserve governing invariants; recovery is not permission to bypass LAW/FSM/audit.
- Failed approaches are retained deliberately so future AI searches them before repeating a repair strategy.
