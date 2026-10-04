# COMET — Concept Overlap Marginal-Erosion Table

**Status:** `Lo4_AI_PROPOSAL_ONLY / NON_GOVERNING`

## Problem
A new proposal can look valuable in isolation while mostly duplicating work already funded by another lab. Counting full standalone value repeatedly inflates the apparent portfolio benefit.

## Contract
Every relevant pair requires explicit `OverlapEvidence(left_id, right_id, overlap, basis_id)` with Q64.64 overlap in `[0,1]`.

## Algorithm
For candidate `c` against selected set `S`:
- find explicit overlap for every `(c,s)`;
- use the maximum overlap as conservative redundancy exposure;
- retention = `1 - max_overlap`;
- marginal value = `base_value * retention`.

If pair evidence is missing: `FREEZE`.
If duplicate pair evidence conflicts in score or basis: `FREEZE`.
If max overlap exceeds explicit policy limit: `COLLISION`.

## Invariants
- missing evidence is not zero overlap;
- same pair is symmetric;
- candidate cannot be compared against itself as an external selected item;
- ordering does not change fingerprint.

## Non-goals
COMET does not infer semantic similarity from embeddings or model judgment. Upstream evidence creation is a separate responsibility.
