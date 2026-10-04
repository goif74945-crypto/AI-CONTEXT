# Requirements Ledger and Integration Proposal

Status: AI-PROPOSED / NOT INTEGRATED.

## Requirement ledger
R1 Shared configured lineage must never count as independent.
Implementation: lineage closure + conflict graph.
Evidence: shared source/producer/oracle tests.

R2 Derived evidence inherits all ancestor lineages.
Implementation: DAG closure.
Evidence: ancestry test.

R3 Circular proof dependencies block release.
Implementation: deterministic cycle detector.
Evidence: cycle FREEZE test.

R4 Evidence must bind the exact target revision.
Implementation: stale-revision admissibility gate.
Evidence: stale evidence test.

R5 Evidence class cannot be silently promoted.
Implementation: E0-E7 ordered class gate.
Evidence: lower-class exclusion test.

R6 Self-verification can be disallowed unless it has a provenance-bearing external oracle.
Implementation: anti-self-verification gate.
Evidence: two self-verification negative-path tests.

R7 Blindness can be mandatory.
Implementation: policy gate.
Evidence: non-blind exclusion test.

R8 Current sufficient PASS/FAIL contradiction freezes.
Implementation: contradiction gate before quorum release.
Evidence: conflict FREEZE test.

R9 Quorum witness search must be exact within configured resource bounds.
Implementation: deterministic branch-and-bound.
Evidence: non-greedy chain test plus exhaustive comparison against brute force for every graph through five vertices.

R10 Duplicate proof artifacts cannot inflate quorum.
Implementation: intrinsic artifact_identity conflict dimension.
Evidence: duplicate artifact test.

R11 Search must not consume unbounded resources.
Implementation: max_solver_states.
Evidence: forced budget-exhaustion FREEZE test and bounded stress runs.

R12 NEXY.AI repositories must not be mutated.
Implementation: storage only in AI-CONTEXT supplemental folder.
Evidence: target commit tree is limited to AI-CONTEXT paths.

## Future authorized integration proposal
Possible placement:
candidate evidence -> provenance normalization -> NEIK -> proof-weighted consensus / JUDGE release boundary

Suggested adapter responsibilities:
- map claim ID and exact target revision;
- map evidence-capsule provenance to source, producer, oracle and artifact roots;
- require a genuinely external oracle lineage for claims about the verifier itself;
- persist NEIK decision SHA beside the evidence receipt;
- treat prompt/template identity, shared retrieval corpus and common toolchain as additional future correlation roots where NEXY authority approves them.

Do not integrate until NEXY authority defines which lineage dimensions are hard independence boundaries. Too weak permits correlated-consensus laundering; too strict creates unnecessary NOT_VERIFIED/FREEZE states.