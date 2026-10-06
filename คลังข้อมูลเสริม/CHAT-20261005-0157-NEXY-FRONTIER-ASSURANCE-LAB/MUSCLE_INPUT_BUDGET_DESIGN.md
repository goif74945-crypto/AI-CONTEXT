# MUSCLE Input & Search-Budget Assurance — Design

**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION**

## Verified gap

Fresh execution showed the original experimental MUSCLE accepting
`NEQ("saef")` against domain `("safe", "fast")` and returning `SAT` with the
domain unchanged. Two semantically different constraint sets also produced the
same UNSAT result hash because the original output binds final domains and core
IDs, not the submitted constraint definitions. Finally, the existing
per-variable cap of 22 still permits a theoretical 4,194,303 non-empty subset
checks and exposes no caller-selectable work budget.

This continuation deepens MUSCLE; it does not add a sixth mission concept.

## Objective

Admit a bounded finite-domain solve only when:

1. domain names and values are non-empty exact strings;
2. domain collections are tuples with unique values;
3. the constraint collection is a finite built-in list/tuple and all entries
   are actual `Constraint` values with unique IDs;
4. every constraint value is a tuple of unique exact strings;
5. every constraint literal belongs to its declared variable domain;
6. total variables, domain values, constraints, and constraint values fit the
   declared deterministic budget; and
7. the conservative exact-search upper bound
   `sum(2^constraints_per_variable - 1)` fits the declared subset-check budget.

Malformed input raises `FreezeError`. Structurally valid input that exceeds a
resource budget returns `FREEZE` before invoking the original exact solver.
Admitted input is delegated to the original `ConstraintEngine`.

## Contracts

- `MuscleSearchBudget`: positive exact-integer ceilings for input and search.
- `MuscleInputAssurance.solve`: validates vocabulary, computes a conservative
  search certificate, binds normalized input bytes, and delegates to MUSCLE.

The adapter preserves original SAT/UNSAT semantics and does not interpret,
repair, rank, or authorize policy constraints.

## Determinism and evidence binding

Domains, constraints, constraint values, budget accounting, and gaps are
normalized into stable order. The output includes `input_hash`, which changes
when any admitted domain or constraint semantic changes, and a `result_hash`
over the complete assurance record.

## Non-duplication boundary

The supplemental tree contains broader SAT/UNSAT proof capsules, minimal
blocker certificates, and exact-search budget systems for other engines. The
inspected scope did not contain an adapter for this mission's finite-domain
MUSCLE that jointly enforces domain-literal membership, exact input types,
input-semantic hashing, and a pre-solve subset-search bound. This artifact owns
only that narrow admission boundary; it does not create another SAT language,
proof-capsule framework, or repair-set engine.

## Limits

- The subset-check value is a conservative upper bound, not measured runtime.
- Passing the budget does not establish that caller-authored policy semantics
  are correct or authoritative.
- This adapter inherits the original solver's finite-domain operators and
  minimum-core selection behavior.
- No canonical, production, deployment, or NEXY.AI implementation claim is
  made.
