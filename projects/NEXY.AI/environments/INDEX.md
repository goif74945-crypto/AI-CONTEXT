# NEXY.AI Environment Matrix

## Purpose
Make environment differences explicit so AI does not silently transfer assumptions/evidence between LOCAL/TEST/CI/STAGING/CANARY/PROD.

## Files
- `environment-matrix.json`
- `validation-report.md`

## Authority rule
STAGING/CANARY are useful operational stages, but their exact topology is not promoted to Canon unless an authoritative source defines it.

## Core invariant
Evidence from one environment does not automatically prove another environment.
Config differences must be explicit/versioned.
