# Design — NEXY EPC Constitutional Satisfiability & Contradiction Lab 20

Truth class: `AI_PROPOSED / NON_CANONICAL / ADVISORY_ONLY`

## Core design
Input is an explicit, validated boolean constraint AST. No natural-language constraint is silently interpreted as executable truth. Equivalent valid input is canonicalized and hashed deterministically. The solver compiles expressions to CNF using deterministic Tseitin variables and uses deterministic DPLL with unit propagation and stable variable/branch ordering.

Exact minimal UNSAT-core claims are permitted only inside the configured bounded search domain. Above that bound, the implementation fails closed instead of renaming a heuristic result "exact".

All quantitative project metrics use checked signed Q64.64 carried by BigInt under signed-i128 raw bounds. Overflow and division-by-zero fail closed.

## 20 systems
1. **Atom Registry Gate** — validates explicit stable atom identities.
2. **Canonical Expression Normalizer** — canonical expression ordering without semantic guessing.
3. **Canonical Bundle Fingerprinter** — SHA-256 identity for normalized constraint bundles.
4. **Direct Satisfiability Gate** — SAT/UNSAT result for explicit bounded constraints.
5. **Deterministic Model Witness Generator** — stable satisfying assignment witness.
6. **Exact Bounded Minimum UNSAT Core Extractor** — minimum-cardinality contradiction core within hard bound.
7. **Pairwise Contradiction Witness Detector** — finds explicit two-constraint conflicts.
8. **Implication Prover** — proves A => B by checking A AND NOT B is UNSAT.
9. **Equivalence Prover** — bidirectional implication proof.
10. **Redundant Constraint Detector** — proves a constraint follows from the remaining set.
11. **Tautology / Vacuity Detector** — detects formulas that add no restriction.
12. **Forced Atom / Dead-State Detector** — proves variables forced true/false under current theory.
13. **Assumption Stress Matrix** — deterministic effect matrix for explicit assumptions.
14. **Dependency Cone Calculator** — traces referenced atoms/constraint dependencies.
15. **Canon + Proposal Merge Gate** — advisory check of combined explicit theories.
16. **Delta Satisfiability Analyzer** — identifies whether the proposal changes feasibility.
17. **Proposal-Specific Conflict Attribution** — separates Canon-only contradiction from contradiction introduced by proposal.
18. **Q64.64 Conflict Density Metric** — exact fixed-point conflict-density evidence.
19. **Proof Capsule Compiler** — canonical advisory proof artifact with hashes/witnesses.
20. **Deterministic Court Consistency Dossier** — one canonical, replayable EPC-facing consistency report.

## Required behavior
- malformed critical input => error / insufficient evidence
- UNKNOWN evidence => INSUFFICIENT_EVIDENCE, never guessed SAT/UNSAT
- identical normalized input => byte-identical canonical output
- no hidden clock/RNG/network source in proof path
- no NEXY Core/JUDGE event emission
- no KEEP/CUT right consumption from merely running a proof
- no promotion authority

## Integration shape
Future NEXY integration, if formally authorized, should be adapter-only:
`proposal/spec explicit constraint capsule -> this lab -> signed/hash-bound advisory proof capsule -> authoritative existing verification/JUDGE process`.

This project intentionally contains no adapter that can mutate NEXY state.
