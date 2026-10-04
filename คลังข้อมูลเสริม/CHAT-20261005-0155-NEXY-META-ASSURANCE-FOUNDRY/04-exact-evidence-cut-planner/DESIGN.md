# Design — Exact Evidence Cut Planner (EECP)

Classification: `AI_PROPOSED_CONCEPT / REFERENCE_IMPLEMENTATION`

## Problem
A proof graph can contain many alternative evidence routes. A system needs two exact answers:
1. What is the smallest additional evidence set that can prove a target claim?
2. Which smallest evidence losses would make every proof route impossible?

Counting evidence or ranking nodes by centrality is not enough because AND/OR structure and shared dependencies matter.

## Model
- `Evidence` leaf: stable ID + positive integer acquisition cost.
- `Claim` node: `AND` or `OR` over child node IDs.
- Graph must be finite and acyclic.

## Exact proof frontier
EECP recursively constructs all subset-minimal evidence sets capable of proving each node:
- Evidence leaf -> `{leaf}`.
- AND -> Cartesian union of child frontiers.
- OR -> union of child frontiers.
- Supersets are pruned because they can never be a minimal proof.

For an acquisition plan, already-proven evidence is removed from each required set. The chosen plan minimizes lexicographically:
1. total integer cost;
2. number of new evidence items;
3. sorted evidence-ID tuple.

## Exact fragility cutsets
Given the complete minimal proof frontier, a cutset is a set of evidence leaves that intersects every possible proof set. EECP enumerates bounded combinations and returns subset-minimal exact hitting sets. These are the smallest evidence losses that invalidate all proof routes.

## Fail-closed bounds
Frontier/cutset enumeration has explicit caps. Hitting a cap is a planning failure, never an approximate PASS.

## Integration proposal
Useful to prioritize evidence acquisition, expose proof fragility, and avoid collecting redundant evidence. It is advisory until NEXY authority explicitly adopts its graph contract.
