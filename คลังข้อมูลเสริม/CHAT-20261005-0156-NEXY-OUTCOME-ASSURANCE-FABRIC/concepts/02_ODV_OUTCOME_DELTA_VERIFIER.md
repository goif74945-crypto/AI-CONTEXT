# ODV — Outcome Delta Verifier

`AI-PROPOSED / EXPERIMENTAL`

## Problem
Observed final state can be incomplete, malformed, partially successful, or actively contradictory to the desired result.

## Behavior
ODV evaluates every criterion and forbidden effect, emitting:
- `PASS`: all hard and soft criteria satisfied, no forbidden effect;
- `PARTIAL`: hard/forbidden constraints pass but one or more soft goals miss;
- `FAIL`: hard criterion or forbidden effect violated;
- `FREEZE`: material observation is missing or invalid.

## Critical distinction
`FREEZE` is not ordinary failure. A string where a trusted numeric observation is required is an evidence/input-integrity problem, not proof that the outcome itself failed.

## User value
Prevents both false success and false failure from low-quality telemetry.
