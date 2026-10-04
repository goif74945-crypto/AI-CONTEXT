# 05 — NPMA: NEXY Policy Monotonicity Auditor

**Status:** AI-PROPOSED CONCEPT.

## Problem
Threshold-heavy policies can contain paradoxes: a slightly riskier request can fall into a different branch and receive a less restrictive decision. Unit tests at a few points often miss this global ordering bug.

## Design
NPMA accepts finite policy points, an ordered decision severity map and a direction for each risk dimension. It compares all comparable pairs and emits exact witnesses whenever a riskier point is ranked less restrictive than a safer point.

## Invariants
- invalid dimension shapes or decisions => FREEZE;
- any monotonicity violation => FREEZE with witness pair;
- PASS means only that the provided finite policy surface is monotone under the declared ordering.

## NEXY integration hypothesis
Run in CI against deterministic policy tables and generated boundary grids for auth, rate limits, safety gates, resource governors and risk decisions.
