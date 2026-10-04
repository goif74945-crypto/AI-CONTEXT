# 02 — AEP: Absence Evidence Planner

**Status:** AI-PROPOSED / Lo4 / NON-CANONICAL

## Objective
Prevent a common audit error: converting “my search returned nothing” into “the thing does not exist.”

## Inputs
- target claim/entity;
- declared authoritative search surfaces;
- per-surface freshness policy;
- expected source/version binding;
- actual search observations and hits;
- scan cost used only to order unresolved follow-up work.

## Outputs
- `PASS`: no hit across every required authoritative, current, version-matched surface;
- `FAIL`: at least one valid surface observed a hit, so absence is refuted;
- `NOT_VERIFIED`: missing, stale or version-mismatched coverage;
- deterministic cheapest-first next scan plan for unresolved surfaces.

## Immutable rules
- Missing coverage is never absence evidence.
- Stale evidence is not current evidence.
- Wrong-version evidence cannot satisfy a current absence claim.
- One positive hit refutes the absence claim even if other surfaces remain unchecked.

## NEXY fit
Useful for repository audits, requirement audits, capability discovery and “feature absent” claims. It formalizes coverage before a negative conclusion reaches NEXY::JUDGE.

## Failure behavior
Malformed duplicate surfaces or empty targets are rejected. Unresolved surfaces yield `NOT_VERIFIED`, not guessed PASS.

## Acceptance evidence
E2 tests cover complete proof, missing coverage, positive hit and version mismatch; stress checks verify input-order independence across 100 permutations.
