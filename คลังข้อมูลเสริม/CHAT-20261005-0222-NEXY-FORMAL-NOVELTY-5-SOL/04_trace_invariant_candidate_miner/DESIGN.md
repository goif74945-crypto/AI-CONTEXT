# 04 — TICM: Trace Invariant Candidate Miner

**Status:** AI-PROPOSED / Lo4 / NON-CANONICAL

## Objective
Extract useful regularities from runtime/test traces without committing the classic error “it happened repeatedly, therefore it is law.”

## Candidate types in reference prototype
- constant field;
- observed numeric range;
- nondecreasing numeric sequence;
- small observed categorical allowed set.

## Authority rule
Every output is one of:
- `CANDIDATE_NOT_VERIFIED`;
- `SUPPORTED_BY_HOLDOUT`;
- `REFUTED_BY_HOLDOUT`.

There is deliberately **no `CANONICAL` state** in this engine.

## Immutable rules
- Fewer than two training records is insufficient.
- Holdout violations refute a candidate.
- Holdout support does not promote a candidate to NEXY law.
- Identical traces produce identical candidate order and content.

## NEXY fit
Can turn real traces into hypotheses for later formalization, regression tests or operator review. This helps discover undocumented behavior while keeping evidence and authority separate.

## Failure behavior
Insufficient training data raises an explicit error. Fields absent from holdout remain unverified rather than treated as supported.

## Acceptance evidence
E2 tests cover candidate mining, holdout refutation, holdout support and minimum-data failure. Stress processes 10,000 records twice and verifies byte-equivalent logical output objects.
