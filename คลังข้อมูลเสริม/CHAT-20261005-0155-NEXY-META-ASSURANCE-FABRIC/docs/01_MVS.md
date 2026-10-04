# C1 — Metamorphic Verification Synthesizer (MVS)

**Classification:** PROPOSAL / standalone prototype  
**Not authority:** This document does not add a NEXY.AI requirement.

## Problem
Some systems cannot cheaply provide a complete expected output for every input. A naive verifier then either trusts the output, compares against another model, or freezes everything. Metamorphic testing provides a third path: when an authoritative relation is known, transform the input and verify the corresponding relation between outputs.

## Contract
Input:
- a callable subject;
- a base input;
- an explicit `MetamorphicRelation` containing a named transform and expectation.

Output:
- base output;
- transformed input/output;
- deterministic PASS/FAIL relation result;
- human-readable reason.

Supported prototype transforms: identity, integer shift, integer scale, sequence reverse, sequence sort.  
Supported expectations: equality, integer delta, integer scale, nondecreasing, same multiset.

## Critical invariant
A metamorphic relation is **not generated truth**. In a real NEXY integration, provenance/authority must be resolved before use.

## Failure model
- unknown transform/expectation -> explicit exception / freeze-equivalent;
- wrong type -> explicit exception;
- subject failure -> propagated, never converted to PASS;
- relation violated -> structured FAIL, no fallback.

## Determinism
No randomness, clock, I/O, global mutable state, or unordered output iteration.

## Integration proposal
Potential location: pre-release or judge-adjacent verification worker. NEXY would supply only authority-approved relations. MVS returns evidence; it does not make the final decision.

## Tests
Identity; affine shift; intentionally false relation; unknown transform; sequence multiset; deterministic grid of 451 affine cases.

## Trade-offs
Strength: useful when exact oracle is unavailable.  
Risk: a wrong relation can create misleading evidence.  
Mitigation: relation provenance, independent negative tests, and never treating MVS alone as complete correctness proof.
