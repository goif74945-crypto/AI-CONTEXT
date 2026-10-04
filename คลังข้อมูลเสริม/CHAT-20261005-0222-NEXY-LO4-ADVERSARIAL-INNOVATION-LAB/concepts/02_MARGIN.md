# MARGIN — Decision Legality Margin Sentinel

Status: `Lo4_AI_PROPOSAL_ONLY`

## Problem
A binary rule check treats `risk=0.099 <= 0.1` as equally healthy as `risk=0.01 <= 0.1`. Those are not equally robust under measurement error, drift or delayed state updates.

## Mechanism
For each numeric constraint, compute signed slack and normalized margin. Result states:
- `VIOLATION` -> FREEZE;
- `FRAGILE_PASS` -> REVERIFY;
- `ROBUST_PASS` -> eligible for RELEASE.

## Invariants
- explicit operator and threshold;
- positive normalization scale;
- non-negative required margin;
- no release if any constraint violates;
- no normal release if any constraint is only a fragile pass.

## NEXY value
Adds a deterministic robustness notion to final adjudication without asking an AI to guess how close is "too close". The policy owner sets required margins.
