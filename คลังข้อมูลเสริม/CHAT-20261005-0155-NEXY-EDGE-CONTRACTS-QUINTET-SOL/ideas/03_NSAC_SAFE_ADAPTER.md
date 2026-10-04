# 03 — NSAC: NEXY Safe Adapter Compiler

**Status:** AI-PROPOSED CONCEPT.

## Problem
Detecting provider/tool contract drift is useful but incomplete. Humans still have to decide whether a compatibility adapter is safe. Model-generated adapters can silently rename critical fields or coerce incompatible types.

## Design
NSAC compiles a deterministic adapter only from explicit field contracts. It accepts exact mappings, explicit unambiguous aliases for non-critical fields, safe integer-to-number widening and validated explicit defaults. Critical fields require exact name and exact type.

## Invariants
- ambiguous source candidates => FREEZE;
- missing required field => FREEZE;
- incompatible type => FREEZE;
- critical rename/type change/default => FREEZE;
- compiled adapter has a stable hash.

## NEXY integration hypothesis
Use as a repair proposal stage after a tool-contract drift detector. Only generated plans that pass this deterministic compiler can proceed to shadow integration testing.
