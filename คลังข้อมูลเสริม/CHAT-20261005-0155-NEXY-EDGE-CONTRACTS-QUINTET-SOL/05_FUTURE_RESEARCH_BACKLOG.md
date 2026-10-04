# Future Research Backlog

All items below are **AI-PROPOSED CONCEPTS ONLY**. They are not current NEXY law, requirements, implementation, or roadmap commitments.

## F1 — Approval Causal Chain
Extend NAES from one approval seal to a DAG of derived approvals, where every downstream authorization proves which parent authority, scope reduction and plan transformation produced it. Research question: can authority only stay equal or decrease through a derivation graph?

## F2 — Evidence Planner With Value-of-Information
Extend NECP so multiple legal evidence plans can be ranked by expected information gain without allowing probabilistic estimates to determine PASS. The probabilistic layer may choose what to test next; the deterministic verifier still decides whether evidence is sufficient.

## F3 — Adapter Proof Obligations
Have NSAC emit machine-checkable obligations beside every generated mapping: preserved fields, inserted defaults, widening operations and unresolved semantics. A separate verifier must discharge the obligations before use.

## F4 — Dynamic Failure-Domain Discovery
Extend NCCQ with runtime-observed correlation hints such as shared provider outage, parser lineage, retrieval source, environment or observation-time overlap. The discovered domain can only reduce claimed independence until explicitly cleared.

## F5 — Policy Boundary Fuzzer
Extend NPMA with deterministic boundary generation around policy thresholds and categorical transitions. Goal: find monotonicity inversions and discontinuities without relying on random sampling for PASS.

## F6 — Quintet Composition Model Checker
Model the five systems as one finite state machine and verify cross-gate invariants such as: no unapproved execution, no evidence upgrade by planning, no quorum bypass by duplicate lineage, and no generated adapter escaping its admitted contract.

## F7 — User-Visible Reason Compression
Generate a minimal human-facing explanation from deterministic reason codes while proving that omitted details cannot change the user's action choice. This is an explanation-layer research problem, not an authority layer.

## Promotion rule
A backlog item stays EXPERIMENTAL until it has an explicit task contract, non-duplication review, implementation, matching evidence and authorized promotion. Repetition in documentation is not promotion.
