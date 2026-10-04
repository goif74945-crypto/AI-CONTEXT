# Concept and Scope

## Classification
**AI-PROPOSED CONCEPT / ADVISORY ONLY / NOT CANONICAL NEXY LAW**

## Problem
A control system can preserve truth internally yet still fail users if the final surface is noisy, ambiguous, overexposes internal machinery, or hides why an action froze. NEXY's source-derived context explicitly favors a small human surface over a large hidden backbone and distinguishes UI from authority.

## Objective
Define and implement a deterministic reference boundary that:
1. accepts typed truth claims;
2. treats material unknown/conflict/unverified state as release blockers;
3. strips internal/sensitive claims from the public surface;
4. emits concise public facts/uncertainties/freeze reasons;
5. emits a deterministic receipt suitable for auditing/replay.

## In scope
- reference Python compiler;
- canonical JSON hashing;
- release/freeze policy prototype;
- visibility filtering;
- narrow text redaction;
- schemas and fixtures;
- unit/CLI tests;
- integration proposal only.

## Out of scope
- editing any NEXY.AI repository;
- claiming this is current NEXY architecture;
- validating that an evidence reference is true;
- replacing NEXY::LAW, CORE, JUDGE, RSEL, or Safety Kernel;
- UI implementation;
- production secret scanning/DLP;
- model-generated summarization;
- deployment.

## Key invariant
**Compression may remove detail, but must not upgrade truth.**

A claim marked UNKNOWN cannot become a public fact because the output needs to look clean. A material conflict must remain a blocker. Human-friendly formatting is subordinate to truth classification.
