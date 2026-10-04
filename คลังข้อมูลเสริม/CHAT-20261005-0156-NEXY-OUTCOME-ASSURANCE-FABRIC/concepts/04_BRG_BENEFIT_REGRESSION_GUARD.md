# BRG — Benefit Regression Guard

`AI-PROPOSED / EXPERIMENTAL`

## Problem
A candidate can improve its aggregate score while worsening a user benefit that must not regress. Metric gaming loves averages because averages are excellent places to hide damage.

## Behavior
Each protected criterion is evaluated directly against baseline with explicit directional tolerance. A protected regression causes BRG `FAIL` even if other metrics improve enough to keep the candidate outcome `PASS`.

## Key invariant
Aggregate gain never overrides an explicit regression guard.

## User value
Protects continuity of user value across optimizations, upgrades, model swaps, and performance work.
