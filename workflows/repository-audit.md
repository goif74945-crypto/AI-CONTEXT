# WORKFLOW — REPOSITORY AUDIT

## Goal
Compare authoritative requirements with real repository state and produce evidence-backed findings without guessing.

## Pipeline
`AUTHORITY → INVENTORY → REQUIREMENT LEDGER → IMPLEMENTATION MAP → EVIDENCE MAP → GAP GRAPH → VERDICT`

## 1. Lock target
Record repository, branch/ref, HEAD and protected scopes.

## 2. Resolve authority
Identify current governing spec/law/requirements.
Do not mix vision, deprecated design and current build spec as equal authority.

## 3. Inventory
Map relevant:
- modules;
- entry points;
- contracts;
- schemas;
- state machines;
- persistence;
- security;
- tests;
- CI;
- deployment evidence.

## 4. Requirement ledger
For each requirement:
- ID/name;
- authority;
- expected behavior;
- implementation path;
- evidence;
- status;
- notes/conflicts.

## 5. Search discipline
Absence from one search != missing.
Before MISSING:
- try exact and semantic variants;
- inspect expected directories;
- trace imports/call paths;
- check generated/configured behavior when relevant.

## 6. Status discipline
- MATCH/PASS only with required evidence.
- PARTIAL for incomplete semantics.
- MISSING when required object/behavior is proven absent.
- CONFLICT when implementation contradicts authority.
- SCOPE when implementation exists but authorization/governance differs.
- NOT_VERIFIED when execution proof is missing.

## 7. Semantic audit
Audit more than file presence:
- authority;
- state transitions;
- failure behavior;
- ordering;
- idempotency;
- isolation;
- persistence;
- evidence;
- bypass paths.

## 8. Contradiction audit
Search for:
- duplicate constants;
- conflicting enums;
- inconsistent timeouts;
- multiple authorities;
- UI/backend disagreement;
- docs/code divergence;
- stale tests;
- bypass/force paths.

## 9. Gap graph
Group findings by shared root cause and dependency.

## 10. Verdict
Report:
- proven clean areas;
- proven findings;
- not-verified areas;
- blockers;
- exact evidence limits.

Never convert “not found” into “does not exist” without sufficient search coverage.
