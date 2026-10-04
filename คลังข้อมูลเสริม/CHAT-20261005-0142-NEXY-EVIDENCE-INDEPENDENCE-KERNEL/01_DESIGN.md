# NEIK Design

Classification: AI-PROPOSED CONCEPT + REFERENCE IMPLEMENTATION.
Authority: advisory only. It does not override NEXY law, specification, or implementation truth.

## Problem
Agreement count is not evidence independence. Different agents can reuse one source, one producer lineage, one oracle implementation, or one copied artifact. Derived proofs can be counted twice. A system can even indirectly verify itself. Those patterns can inflate a consensus score without adding new epistemic support.

## Core invariant
A quorum is admissible only when an exact witness set exists whose members:
1. bind to the required target revision;
2. meet the required evidence class;
3. carry the required verdict;
4. satisfy blindness policy when enabled;
5. are not prohibited self-verification;
6. form an acyclic derived_from graph;
7. are pairwise disjoint across every configured independence dimension after ancestor-lineage closure;
8. do not reuse the same artifact hash.

## Pipeline
JSON envelope
-> strict parser
-> evidence dependency DAG
-> cycle detection
-> ancestry lineage closure
-> admissibility filtering
-> verdict contradiction gate
-> correlation/conflict graph
-> exact bounded maximum-independent-set search
-> canonical deterministic decision capsule
-> SHA-256 seal

## Independence dimensions
Configurable hard dimensions:
- source_lineage
- producer_lineage
- oracle_lineage

Intrinsic non-disableable dimension:
- artifact_identity, derived from artifact_hash

Evidence inherits all ancestor lineage roots through derived_from. Therefore transforming or aggregating another proof does not create a fresh independent confirmation.

## Exact solver
A greedy solver can return a smaller witness than actually exists, so NEIK uses deterministic branch-and-bound on the conflict graph. Inputs are bounded by max_evidence_nodes and exact search is bounded by max_solver_states. If the exact search cannot finish inside the declared deterministic budget, NEIK returns FREEZE instead of approximating PASS.

## Failure semantics
- dependency cycle -> FREEZE
- sufficient-class current PASS and FAIL simultaneously -> FREEZE
- admissible FAIL -> FREEZE
- exact solver budget exhausted -> FREEZE
- valid but insufficient independent quorum -> NOT_VERIFIED
- valid exact quorum and no blocker -> PASS
- invalid contract -> INVALID_INPUT at CLI boundary

## Determinism
The core uses no clock, randomness, network, environment-based policy, hidden model call, or filesystem discovery. Input collections and decision structures are normalized before output hashing.

## Security boundary
NEIK treats submitted lineage metadata as claims. It does not authenticate producer identity, oracle identity, source identity, or artifact origin. A future production integration requires trusted provenance capture or signed attestations upstream.

## NEXY compatibility
The system follows NEXY's architectural direction: exact revision binding, explicit evidence classes, explicit conflict/freeze semantics, deterministic behavior, untrusted external evidence, provenance awareness, and no hidden fallback. It is not wired into NEXY.AI in this task.