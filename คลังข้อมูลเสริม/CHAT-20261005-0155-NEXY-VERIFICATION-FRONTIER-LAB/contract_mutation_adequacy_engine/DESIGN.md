# Contract Mutation Adequacy Engine (CMAE) — Design

Status: **AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL**

## Objective
Measure whether a verification oracle is actually sensitive to meaningful perturbations of a structured contract. A green validator that also accepts broken near-neighbors is weak evidence, even when its terminal output is attractively green.

## Authority and scope
CMAE evaluates **test/oracle adequacy**, not contract correctness. Mutants are synthetic adversarial probes. They MUST NOT be promoted into requirements or written into production state.

## Inputs and outputs
Input: JSON-like contract plus an oracle that returns truthy when a candidate is accepted.
Output: `MutationReport` with total mutants, killed/survived counts, score, and stable mutant IDs.

## Mutation operators
- delete mapping key;
- delete list item;
- flip boolean;
- integer boundary minus/plus one;
- replace string with a sentinel.

Mutants are canonicalized and deduplicated. IDs are deterministic SHA-256-derived identifiers over path/operator/content.

## Invariants
1. Baseline contract MUST pass before mutation score is meaningful.
2. Equivalent canonical mutants are removed.
3. Generation order and IDs are deterministic.
4. Oracle exception on a mutant counts as rejection/killed, matching strict validator semantics.
5. Score describes only the generated mutation operator set.

## Failure model
- Baseline rejected or raises: `ValueError`; no score is fabricated.
- Non-JSON-serializable values may fail canonicalization; this v0.1 deliberately does not hide that mismatch.
- Mutant generation is capped by `max_mutants`.

## NEXY integration proposal
CMAE could evaluate requirement validators, schema gates, evidence adjudicators, or policy tests in an isolated build/verification environment. It must never mutate production contracts. Surviving mutants become review findings, not automatic fixes.

## Evidence plan
E2 tests prove deterministic unique generation, demonstrate surviving mutants under a deliberately weak oracle, show complete kill under exact equality oracle, and enforce baseline validity.

## Known limitations
- Operator set is intentionally small and generic.
- A score of 1.0 means all **generated** mutants were killed, not that the oracle is complete.
- Equivalent mutants are filtered syntactically/canonically, not by deep semantic equivalence.
