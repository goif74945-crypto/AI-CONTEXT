# 02 — Epistemic Debt & Evidence Decay Ledger (EDEL)

**Class:** `Lo4_AI_PROPOSAL_ONLY`

## Purpose
Convert “tests once passed” into a version-bound evidence model. When code/spec/data subjects change, prior proof can become stale. EDEL identifies direct evidence debt, propagates invalidity to dependent claims, and emits a re-verification frontier.

## Core idea
Evidence has:
- explicit evidence class E0..E7;
- claims it supports;
- exact subject versions it observed.

Claims have:
- required evidence class;
- criticality weight;
- subject identities;
- dependency claims.

An artifact is usable only when its evidence class is sufficient and all bound claim subjects match current versions.

## Debt propagation
Direct debt: no usable evidence, stale evidence, or insufficient class. Dependent claims become debt when a prerequisite claim is invalid. Dependency cycles are rejected because circular proof graphs obscure root evidence authority.

## Re-verification frontier
The reference frontier contains direct-invalid root claims not downstream of another direct-invalid claim. Re-proving those roots is the first evidence repair boundary, not a promise that all dependents automatically pass afterward.

## Invariants
- E1 cannot satisfy an E3 requirement;
- changed subject version invalidates evidence bound to the old version;
- dependency invalidity propagates deterministically;
- evidence order cannot alter the report.

## Complexity
O(claims + evidence bindings + dependency edges + subject comparisons), excluding serialization.

## Code/Test
- code: `src/nexy_lo4_frontier/edel.py`
- tests: `tests/test_edel.py`
