# OCC — Outcome Contract Compiler

`AI-PROPOSED / EXPERIMENTAL`

## Problem
Execution systems often know what action to perform but lack a machine-checkable statement of what **successful final state** means.

## Contract
OCC requires explicit objective ID/text, at least one criterion, strict operator semantics, hard/soft classification, optional regression guards, and forbidden effects. Unknown fields are rejected.

## Output
Canonical `nexy-oaf/1` contract plus SHA-256 content identity.

## Key invariant
OCC never invents missing acceptance criteria, thresholds, baselines, forbidden effects, or regression tolerance.

## User value
A task cannot be declared successful merely because its command/API/tool call returned success; it must be measured against an explicit outcome definition.
