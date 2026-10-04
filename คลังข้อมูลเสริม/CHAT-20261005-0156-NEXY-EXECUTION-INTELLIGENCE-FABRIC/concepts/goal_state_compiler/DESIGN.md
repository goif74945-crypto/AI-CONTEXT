# Goal-State Compiler — Design

**Classification:** `AI-PROPOSED / EXPERIMENTAL / NOT CANON`

## Problem
Long or multi-agent work often loses a crisp definition of “done.” A plan can look busy while required facts, outputs, or safety constraints are missing.

## Objective
Compile a goal specification into a normalized tamper-evident contract and evaluate observed state against it deterministically.

## Inputs
- required facts with exact expected values;
- forbidden facts with exact forbidden values;
- required capabilities;
- forbidden effects;
- required output keys.

## Outputs
- stable `goal:*` contract ID;
- `PASS | FAIL | NOT_VERIFIED | FREEZE` evaluation;
- exact missing/mismatch/violation list;
- stable evaluation ID.

## Invariants
- semantically set-like lists normalize/sort before hashing;
- contract hash mismatch is a contract error;
- forbidden state/effect outranks ordinary mismatch and freezes;
- missing required evidence is `NOT_VERIFIED`, never silently accepted.

## Failure model
Malformed contract → exception to caller/CLI fail-closed. Forbidden state → `FREEZE`. Mismatch → `FAIL`. Missing proof → `NOT_VERIFIED`.

## NEXY value
Allows RUN/JUDGE to ask “did the requested end state actually become true?” with a machine-checkable predicate instead of relying on agent narration.
