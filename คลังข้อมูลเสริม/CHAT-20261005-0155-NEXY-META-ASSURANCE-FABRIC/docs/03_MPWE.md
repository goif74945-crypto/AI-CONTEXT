# C3 — Minimal Proof Witness Extractor (MPWE)

**Classification:** PROPOSAL / standalone prototype

## Problem
Evidence-first systems can become unusable if every decision carries every log, artifact and citation. Aggressive summarization is worse if it drops the only evidence supporting a requirement.

MPWE treats evidence selection as weighted set cover: choose the deterministic minimum-cost evidence subset covering every declared requirement.

## Contract
Input:
- finite requirement IDs;
- `EvidenceItem(id, covers, cost)`.

Objective order:
1. minimum total cost;
2. minimum number of evidence items;
3. lexicographically stable evidence-ID tuple.

Output:
- selected evidence IDs;
- total cost;
- covered and uncovered requirements;
- exact coverage flag.

## Algorithm
Requirements map to bits; deterministic dynamic programming explores reachable coverage masks.

Weighted set cover is NP-hard in general. This implementation is a correctness/reference prototype and bounded optimizer, not a claim of cheap large-scale optimization.

## Failure model
Empty requirements, duplicate evidence IDs, unknown requirement references, and invalid costs -> explicit errors. Impossible full coverage -> explicit `uncovered`, never false PASS.

## Integration proposal
Use after evidence validation, as an evidence presentation/compiler stage. MPWE must never delete canonical evidence; it chooses a witness for a specific claim contract.

## Tests
Weighted optimum; stable tie break; uncovered requirement; unknown reference; duplicate evidence ID; brute-force optimality cross-check.

## Trade-offs
Strength: reduces proof payload without reducing declared coverage.  
Risk: weights influence which proof is shown and exact solving can be expensive.  
Mitigation: policy-defined costs, preserved canonical evidence, bounded/partitioned production solving with explicit optimality status.
