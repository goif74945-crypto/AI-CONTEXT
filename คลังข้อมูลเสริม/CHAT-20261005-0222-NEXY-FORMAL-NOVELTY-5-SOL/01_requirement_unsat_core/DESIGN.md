# 01 — RUC: Requirement Unsat Core

**Status:** AI-PROPOSED / Lo4 / NON-CANONICAL

## Objective
When requirements cannot all be true, return a small reproducible conflict witness rather than a generic conflict flag.

## Inputs
- finite variable domains;
- uniquely identified requirements;
- rules: equality, inequality, membership, non-membership, same/different variable, implication;
- explicit maximum assignment budget.

## Outputs
- satisfiable + concrete witness assignment; or
- unsatisfiable + an **irreducible** conflicting requirement ID set.

## Immutable rules
- Never guess values outside declared domains.
- Never claim minimum-cardinality core; the algorithm guarantees deletion-irreducibility only.
- Exceeding verification budget raises `ModelTooLargeError` and fails closed.
- Duplicate requirement IDs or unknown variables are invalid input.

## Architecture
Finite-domain exhaustive verifier → deletion-based irreducible-core reducer.

This reference design favors correctness transparency over scalability. A future production version could delegate bounded SAT/SMT solving to a verified backend while preserving the same external contract.

## Failure behavior
- Empty domains: reject.
- Unknown variables: reject.
- State space beyond configured cap: explicit failure, no guessed verdict.
- Contradiction: return core; do not select a preferred requirement.

## NEXY fit
Potential pre-judge or spec-compiler utility. It can explain exactly which subset of structured requirements makes a task impossible before workers waste execution budget.

## Non-goals
- Natural-language theorem proving.
- Automatic authority resolution.
- Canonical policy override.
- Large-scale SAT performance in this prototype.

## Acceptance evidence
E1 compile + E2 tests for satisfiable witness, unary contradiction, cross-variable implication conflict and fail-closed size limit.
