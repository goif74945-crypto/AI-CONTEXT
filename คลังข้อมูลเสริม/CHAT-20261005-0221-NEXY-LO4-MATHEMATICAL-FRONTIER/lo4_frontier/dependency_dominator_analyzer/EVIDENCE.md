# Evidence — DDA

Unit tests verify standard diamond-shaped graphs, shared chokepoints and unreachable-node exclusion.

An independent property test enumerates all simple root-to-node paths for a non-trivial DAG and checks that the implementation dominator set equals the intersection of nodes on every enumerated path. Additional tests reject unknown starts/unreachable targets.
