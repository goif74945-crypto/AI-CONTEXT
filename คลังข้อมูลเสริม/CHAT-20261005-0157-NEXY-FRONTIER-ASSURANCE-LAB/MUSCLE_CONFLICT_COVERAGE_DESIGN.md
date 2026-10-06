# MUSCLE Exhaustive Conflict Coverage — Experimental Design

Status: **AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT DEPLOYED / NOT A NEXY.AI IMPLEMENTATION**

## Problem

The hardened MUSCLE input and work-budget adapter proves satisfiability or returns one deterministic minimum-cardinality unsatisfiable core. That result is correct but incomplete when either:

1. multiple variables are independently unsatisfiable; or
2. one variable has multiple alternate minimum-cardinality cores.

The existing engine deliberately selects the lexicographically first member of the globally smallest core set. Its `final_domains` reveals every empty variable, but its certificate explains only one. A repair based solely on that core can therefore leave a second independent contradiction or an alternate minimum conflict undiscovered.

Fresh reproduction at the inherited revision used two independent variables. Both final domains were empty, but the original result reported only variable `a` and core `a-fast, a-safe`.

## Proposed assurance boundary

`MuscleConflictCoverageAssurance` composes the existing `MuscleInputAssurance`; it does not replace the constraint semantics.

- The existing adapter remains the input validator and exact-search admission gate.
- SAT and input/search-budget FREEZE results are preserved.
- For admitted UNSAT inputs, constraints are partitioned by variable.
- For every empty variable, subsets are enumerated in increasing cardinality and canonical constraint-ID order.
- Enumeration stops after the first cardinality containing conflicts, while retaining every conflict at that cardinality.
- Every emitted core includes a witness for removing each member. Each witness must leave a non-empty remaining domain.
- The original MUSCLE-selected core must consequently be a member of the corresponding certified family.

This is exhaustive coverage of **minimum-cardinality cores**, not every inclusion-minimal core of larger cardinality. That boundary is intentional and stated in the result reason `EXHAUSTIVE_MINIMUM_CONFLICT_COVERAGE`.

## Fail-closed resource contract

`ConflictCoverageContract` requires positive exact-integer limits:

- `max_cores_per_variable`
- `max_total_cores`

The inherited `MuscleSearchBudget.max_subset_checks` already bounds subset evaluation. The additional contract bounds certificate cardinality. If either output bound is exceeded, the adapter returns `FREEZE / CONFLICT_COVERAGE_BUDGET_EXCEEDED`, an empty `conflict_families` object, and explicit gaps. It never labels a truncated family exhaustive.

## Determinism and binding

Inputs are normalized by the existing adapter. Variables, constraints, subsets, cores, deletion witnesses, and gaps use canonical ordering. The result binds:

- the inherited input hash and complete base result;
- the conflict-coverage contract hash;
- all unsatisfiable variables and certified conflict families;
- subset checks executed and discovered core count; and
- a final result hash over the complete record.

Changing only the coverage contract changes the result certificate even when the discovered family is unchanged.

## Composed-pipeline behavior

The composed experimental pipeline now uses this coverage adapter as its MUSCLE gate. A certified UNSAT family still freezes with `UNSAT_CONSTRAINTS`. Certificate-cardinality exhaustion freezes distinctly with `MUSCLE_CONFLICT_COVERAGE_BUDGET_EXCEEDED`. Later gates remain unexecuted in both cases.

## Verification strategy

- Positive: all independently unsatisfiable variables, alternate minimum cores, deletion witnesses, SAT empty coverage.
- Negative: boolean limits, foreign contracts, and malformed base inputs.
- Adversarial: per-variable and total core explosion, 100 input permutations, contract-only certificate changes.
- Integration: original-core membership, direct reproduction/closure of the hidden-conflict gap, and composed-pipeline fail-closed behavior.

## Non-claims and residual limits

- This prototype does not establish repository canon, production deployment, or NEXY.AI adoption.
- It supports the existing separable, single-variable MUSCLE constraint model only.
- It does not enumerate larger inclusion-minimal cores once a smaller cardinality exists.
- It does not optimize the exponential exact search beyond deterministic hard bounds.
- Deletion witnesses prove irreducibility under the existing monotone finite-domain constraint semantics; they are not general SAT proof objects.
