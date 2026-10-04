# CCC — Cancellation Closure Certifier

**Classification:** Lo4 AI proposal / non-Canon.

## Problem
“Cancel the job” is insufficient when the job spawned descendants or already materialized external effects.

## Input
A parent-linked job graph using NEXY-compatible queue states plus explicit `hasExternalEffect` and optional `compensationId`.

## Required behavior
- compute exactly the requested cancellation subtree;
- mark QUEUED/RUNNING nodes for cancellation;
- identify every materialized external effect regardless of job status;
- require an explicit compensation obligation for every materialized effect;
- unknown parents, cycles, duplicate nodes and duplicate compensation identities fail closed.

## NEXY value
Strengthens DOC-C's FREEZE/STOP cancellation law by making orphan side effects visible instead of equating queue state with world state.
