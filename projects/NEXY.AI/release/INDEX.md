# NEXY.AI Release Gate Matrix

## Purpose
Machine-readable release progression and exact current release truth.

## Files
- `gates.json` — DEV → TEST → STAGING → CANARY → PROD operational gate definitions.
- `current-gate-state.json` — current target/evidence verdict.
- `validation-report.md`.

## Authority distinction
DOC-E defines production evidence obligations.

DEV/TEST/STAGING/CANARY stage grouping is **AI-CONTEXT operational structure** used to organize those obligations. It must not be cited as if the source explicitly canonized those stage names/topology.

## Absolute rule
No stage can promote because a file exists.
Required evidence must be executed, current, target-matching and successful.

## Current truth
Target HEAD:
`9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`

Current DOC-E evidence:
- PASS: 0
- BLOCKED: 12
- exact-current-HEAD: 0

Verdict:
**NON_DEPLOYABLE / NOT_VERIFIED**
