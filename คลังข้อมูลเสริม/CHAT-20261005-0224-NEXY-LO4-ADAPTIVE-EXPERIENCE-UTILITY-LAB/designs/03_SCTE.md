# SCTE — Structural Complexity Tax Engine

**Status:** `Lo4_AI_PROPOSAL_ONLY / NON_GOVERNING`

## Problem
Feature benefit is often discussed while maintenance, migration, public-contract and rollback burden are treated as somebody else's future problem. SCTE forces those costs into an explicit deterministic record.

## Change surface
Each changed surface declares Q64.64 values for:
- touch weight;
- persistence burden;
- migration burden;
- public-contract burden;
- rollback burden.

The four burden weights must sum exactly to one.

## Algorithm
`intrinsic = wp*persistence + wm*migration + wc*public_contract + wr*rollback`

`surface_tax = touch_weight * intrinsic`

`total_tax = sum(surface_tax)`

`normalized_tax = total_tax / sum(touch_weight)`

Reject when one surface or aggregate tax exceeds policy.

## Invariants
- duplicate surface IDs freeze;
- zero touch weight is invalid;
- no surfaces means zero tax and PASS;
- policy thresholds are explicit Q64.64 inputs;
- tax remains advisory and cannot replace functional/security verification.
