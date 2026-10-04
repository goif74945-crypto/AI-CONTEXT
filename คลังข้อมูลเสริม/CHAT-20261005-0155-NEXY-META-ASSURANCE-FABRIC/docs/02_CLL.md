# C2 — Conservation-Law Ledger (CLL)

**Classification:** PROPOSAL / standalone prototype

## Problem
Many failures are invalid net changes across transitions: budget appears from nowhere, quota disappears, ownership units duplicate, credits are lost, or capability counts increase without an authorized source.

## Contract
A `ConservationRule` declares a named set of integer state keys. `verify_transition` computes:

`residual = after_total - before_total - declared_external_delta`

PASS iff residual is exactly zero.

A sequence verifier checks every adjacent transition independently so an illegal transition cannot be hidden by a later compensating error.

## Critical invariants
- every conserved key must be present in both states;
- values and external delta are exact integers;
- external creation/destruction must be explicit;
- unrelated state does not silently become conserved.

## Failure model
Missing key, duplicate/empty rule key, non-integer conserved value, or bad external delta -> explicit error. Undeclared mint/burn -> FAIL with residual.

## Integration proposal
Potential uses: quota/budget accounting, capability-token counts, ownership/lease units, action budget, or other additive invariants. The rule itself must be authorized; CLL does not invent what must be conserved.

## Tests
Legal transfer; silent mint; external source; missing-key fail-closed; multi-transition sequence; deterministic transfer grid.

## Trade-offs
Strength: catches cross-step integrity defects that point checks miss.  
Risk: the wrong conserved domain can reject legal evolution.  
Mitigation: explicit rule authority and source/sink deltas.
