# UMC — Uncertainty Mass Conservation Compiler

## Objective
Prevent a pipeline from converting unresolved uncertainty into apparent certainty merely by transforming or summarizing state.

## Contract
For each ordered stage:
`incoming + introduced = outgoing + resolved`

All quantities are non-negative Q64.64. If `resolved > 0`, at least one evidence receipt ID is mandatory. The next stage's `incoming` must exactly equal the previous stage's `outgoing`.

## Quantization boundary
When decimal values are independently converted to Q64.64, mathematically equivalent decimal expressions can differ by one raw fixed-point unit. UMC therefore accepts only `abs(left.raw-right.raw) <= 1`. Two raw units or more freeze. This is a representation-level bound with a precise denominator `2^64`, not an arbitrary epsilon.

## Failure semantics
- no stages -> FREEZE;
- duplicate stage ID -> FREEZE;
- unsupported resolution -> FREEZE;
- chain mismatch -> FREEZE;
- mass residual >1 ULP -> FREEZE;
- conserved chain -> PASS.

## NEXY boundary
Candidate placement: between decomposition/transformation stages and final verification. UMC reports conservation only; it cannot decide whether evidence is authoritative enough. Receipt validity remains owned by an upstream evidence authority.
