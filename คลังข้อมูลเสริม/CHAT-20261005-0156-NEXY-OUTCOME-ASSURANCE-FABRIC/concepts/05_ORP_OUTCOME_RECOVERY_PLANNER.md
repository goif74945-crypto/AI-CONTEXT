# ORP — Outcome Recovery Planner

`AI-PROPOSED / EXPERIMENTAL`

## Problem
After a failed outcome, blindly retrying the original action can repeat damage or waste resources. Recovery should target the unsatisfied end state.

## Behavior
ORP exactly enumerates a bounded candidate repair set, rejects irreversible actions when required, rejects conflicting effects, applies cost/risk budgets, simulates the resulting end state, and selects the lexicographically minimum valid full-PASS plan.

Ranking: `total cost -> combined risk -> action count -> stable action IDs`.

## Safety boundary
ORP does not execute. It emits a proposal for a future NEXY authority/effect layer to approve or reject.

## User value
Recovery becomes goal-directed and minimally invasive rather than “retry until green.”
