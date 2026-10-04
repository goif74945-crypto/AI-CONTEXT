# Threat and Failure Model

## Shared threats
1. Malformed structure attempts to trigger undefined semantics.
2. Nondeterministic iteration order changes decisions.
3. Oversized combinatorial input causes resource exhaustion.
4. Advisory output is accidentally treated as Canon authority.
5. A port changes semantics while preserving function names.

## Controls in this reference
- Strict value/type/range validation where semantics matter.
- Sorted/canonicalized iteration before externally visible output.
- Explicit bound (`max_nodes`) on exact minimal-cut enumeration.
- Lo4 tournament hard-coded to recommendation-only and no promotion permission.
- Property tests compare independent formulations for minimal cuts/dominators.

## Residual risks
- Minimal transversal enumeration remains exponential inside the configured bound.
- Liveness snapshot analysis is not a temporal model checker and cannot prove future scheduling fairness.
- Dominators identify topological chokepoints, not operational risk magnitude.
- Symmetry reducer v1 is for non-relational JSON state; cross-entity references require a reference-aware canonicalizer before adoption.
- Tournament metrics are supplied facts/measurements; the engine does not prove that metric values are truthful.
- No production load, distributed runtime, or deployment evidence exists for this lab.
