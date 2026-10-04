# Novelty and Semantic Collision Audit

Audit pin before publication: AI-CONTEXT `7b3e350e84bb2997c6a8c0c9685a66b6019ebdb1`.

## Collision that forced the first pivot
The initial local Evidence Causality & Independence Fabric was not published as the final candidate because it collided with established supplemental work:
- NEIK, merge `267b67740f26dfa9544af8ce54a47abee520ea4b`: exact evidence-independence witness solver, lineage closure, cycle/staleness/self-verification gates.
- NEIK source commit `033a1cd9ff43d71bdc8636891f7d34c7b47f0e51`.
- Correlation Consensus Guard source commit `5dbd5fde02c0fc04550f25d0b00db75d4d55f305`.
- Epistemic Control Plane `03_COUNTERFACTUAL_VERIFICATION.md`, commit `af027f896e6ffab01b4fe245d222bb6426de7591`.
- Epistemic Control Plane `04_ANTI_CONSENSUS_CORRELATED_FAILURE.md`, commit `17ba2ac839307f2db8b782064e6c130650db8ef1`.
- Decision replay/causal audit proposal, commit `21ce912623c7dc2dedf54c6a91e094644aceb85e`.

Therefore that direction is `WIP / DEFERRED`, not CUT. No vote right is consumed by the pivot.

## PRFF semantic boundary
NEIK asks: **How many submitted witnesses are actually independent after lineage closure?**
PRFF asks: **How many graph failures are required to fracture the proof, which exact nodes/edges form the cut, and where are shared structural bottlenecks across claims?**

NEIK's primary executable algorithm is an exact bounded maximum independent-set search over correlation conflicts. PRFF's primary executable algorithms are directed integer max-flow/min-cut, node splitting, residual cut extraction, deterministic ablation enumeration and minimum-cut-family enumeration.

## Explicit overlap, not hidden
NEIK's future-ideas list proposes “counterfactual independence mutation testing: collapse one root deliberately”. The Epistemic Control Plane also proposes counterfactual evidence removal. PRFF C12–C14 overlap that *general testing idea*, but PRFF does not claim inventing counterfactual mutation. Its additional implementation contribution is an exact graph-resilience model with:
- root-and-edge-disjoint channels;
- evidence vertex connectivity;
- minimum evidence vertex cut certificates;
- edge connectivity and edge cut certificates;
- universal evidence dominators;
- fracture-node marginal impact;
- hard support bridges;
- bounded exact k-ablation threshold;
- full minimum disconnect-cut family enumeration in bounded domains;
- cut-family concentration;
- multi-claim shared bottlenecks;
- cross-claim cut overlap;
- deterministic repair priority.

## Commit-search probes
At the audit pin, AI-CONTEXT commit searches returned no hits for:
`proof resilience`, `minimal cut`, `min cut`, `cutset`, `dominator`, `articulation`, `vertex connectivity`, `edge connectivity`, `fracture topology`, `proof bottleneck`, `ablation threshold`, `shared bottleneck`.

Search absence is not a universal mathematical uniqueness proof. The defensible claim is narrower: no semantic collision was found in the inspected current corpus for the PRFF primary min-cut/fracture-topology invariant.

## “Better than other chats” interpretation
There is no authoritative scalar that proves universal superiority over every other subsystem. PRFF instead improves a currently underrepresented dimension and provides stronger executable evidence on that dimension: dual-toolchain builds, exhaustive small-domain cut oracles, bounded exact search, sanitizers, float exclusion and deterministic replay. Universal superiority remains `NOT_VERIFIED` rather than being fabricated.
