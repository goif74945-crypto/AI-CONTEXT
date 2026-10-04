# Architecture

## Authority plane
All persistent domain types carry an authority class. The highest status emitted by this prototype is `ELIGIBLE_FOR_HUMAN_REVIEW` or a review decision. There is no `CANON` enum value exposed by the experimental modules.

## Data flow
1. `BehaviorContract` encodes behavioral identity.
2. `lo4_flight_chamber.py::novelty_report` computes normalized weighted similarity and SHA-256 contract fingerprints.
3. `lo4_flight_chamber.py::discover_invariants/challenge_invariants` derive candidates and record counterexamples.
4. `lo4_flight_chamber.py::minimize_integration_surface` resolves dependency closure and freezes on protected/missing/cyclic capabilities.
5. `lo4_flight_chamber.py::distill_guard` searches a bounded predicate space for the smallest safe counterexample separator.
6. `lo4_flight_chamber.py::run_tournament` filters candidates by hard constraints/evidence, ranks deterministically, and freezes ties.

## Determinism rules
- Sorted iteration for maps/sets before externally visible ordering.
- Stable SHA-256 fingerprints over canonical JSON.
- Lexicographic tie-breaking only for ordering, never for selecting equal-score winners.
- Unresolved equal top score -> FREEZE.

## Failure semantics
- Missing capability -> FREEZE.
- Protected capability -> FREEZE.
- Capability cycle -> FREEZE.
- No guard that separates good/bad cases -> FREEZE.
- Invariant counterexample -> remains EXPERIMENTAL.
- No tournament candidate satisfying hard/evidence requirements -> FREEZE.
- Equal top tournament score -> FREEZE.

## Security boundary
The reference implementation is pure/offline and performs no network, filesystem, shell, repository, or external tool mutation itself. Publication is performed separately by the execution workflow.
