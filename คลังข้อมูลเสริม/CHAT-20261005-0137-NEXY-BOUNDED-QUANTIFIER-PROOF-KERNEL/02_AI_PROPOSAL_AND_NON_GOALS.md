# AI-PROPOSED Concept — BQPK

**Classification: PROPOSAL_AI / EXPERIMENTAL / NON_AUTHORITATIVE**

BQPK is a proposed guard between evidence aggregation and final claim release.

## Problem
AI systems routinely over-promote weak observations:
- "I searched and found none" becomes "none exist".
- "These sampled tests passed" becomes "all tests pass".
- "The files I saw are valid" becomes "the entire project is valid".
- stale evidence is reused after revision changes.

BQPK makes the quantifier itself executable policy.

## Core idea
A quantified claim is represented by:
1. an explicit predicate;
2. a population/domain;
3. enumeration provenance and whether the domain is complete;
4. member-level evidence bound to a target revision;
5. a quantifier and optional threshold.

The evaluator computes a conservative lower bound and upper bound for how many members can satisfy the predicate.

For incomplete enumeration the upper bound is intentionally unbounded. This permits logically sufficient one-sided conclusions, such as refuting ALL with a known counterexample or proving AT_LEAST 3 with three proven matches, while blocking conclusions that require a closed world.

## Anti-vacuity law
An empty domain is rejected instead of treating ALL/NONE as vacuously true. Operational AI claims should not gain a PASS from an accidentally empty inventory.

## Non-goals
- proving that an evidence artifact is itself truthful;
- replacing NEXY::JUDGE, NEXY::LAW, Vault, or evidence sealing;
- searching repositories;
- deciding user authority;
- running tests;
- mutating project state.

BQPK consumes already-collected evidence metadata and decides only whether that metadata logically entails the quantified claim.
