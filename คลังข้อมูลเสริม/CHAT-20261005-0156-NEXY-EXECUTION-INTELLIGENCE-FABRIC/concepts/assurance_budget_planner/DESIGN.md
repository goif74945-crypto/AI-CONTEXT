# Assurance Budget Planner — Design

**Classification:** `AI-PROPOSED / EXPERIMENTAL / NOT CANON`

## Problem
Multi-agent verification can become expensive and slow if every task invokes every validator. Cheap validation can also be fake-safe if all validators share one failure domain.

## Objective
Choose the lowest-cost validator subset that meets required evidence dimensions and minimum independent-domain counts.

## Algorithm
Exact bounded subset search (≤20 validators). Candidate score:
`total cost → maximum parallel latency → validator count → lexicographic IDs`.

Coverage counts **distinct domains**, not number of validators, preventing two validators from one provider/domain from faking independence.

## Outputs
- `PLAN` with selected validators, cost, latency ceiling and domain coverage;
- `FREEZE` if independent assurance is impossible;
- `FREEZE` if the cheapest sufficient plan exceeds explicit budget.

## NEXY value
Provides a deterministic “minimum sufficient verification” planner for SWARM/JUDGE-style pipelines, potentially reducing latency/cost without weakening declared assurance requirements.
