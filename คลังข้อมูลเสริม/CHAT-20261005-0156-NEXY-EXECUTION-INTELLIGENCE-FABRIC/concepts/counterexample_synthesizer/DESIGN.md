# Counterexample Synthesizer — Design

**Classification:** `AI-PROPOSED / EXPERIMENTAL / NOT CANON`

## Problem
Positive tests prove too little. Contract boundaries routinely fail because missing, wrong-type, below-minimum, above-maximum and invalid-enum paths were never exercised.

## Objective
Generate deterministic single-field counterexamples from a compact field contract, then validate that every emitted vector is actually rejected by the same validator.

## Supported field types
- integer with min/max;
- string with length bounds;
- boolean;
- enum;
- required/optional presence.

## Outputs
- suite ID;
- invalid vectors with mutation IDs and expected errors;
- `FREEZE` if the alleged base-valid case is itself invalid.

## Invariants
No emitted counterexample may validate successfully. Deduplication is canonical-byte based. Field ordering does not affect suite identity.

## NEXY value
Can automatically turn a normalized tool/API/task contract into a negative-test seed set before admitting it into a verified execution path.
