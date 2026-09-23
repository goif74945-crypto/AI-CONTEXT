# WORKFLOW — DEBUGGING

## Goal
Find the actual root cause, not merely suppress the visible symptom.

## Pipeline
`OBSERVE → REPRODUCE → MINIMIZE → HYPOTHESES → DISCRIMINATING TESTS → ROOT CAUSE → FIX → REGRESSION`

## Procedure
1. Capture exact symptom/error/environment.
2. Reproduce on the correct version.
3. Minimize the failing path.
4. List plausible hypotheses with evidence for/against.
5. Run tests that distinguish hypotheses.
6. Trace data/state/control flow across boundaries.
7. Identify earliest incorrect state, not last visible failure.
8. Repair root cause.
9. Re-run original failure and adjacent regression.
10. Record failure pattern if reusable.

## Debugging law
Do not:
- random-walk patch;
- change many variables before measuring;
- “fix” a test by weakening the invariant;
- hide exceptions;
- assume the error message names the root cause.

## Useful capture
- exact stack/error;
- commit/version;
- environment;
- minimal reproduction;
- first bad state;
- root cause;
- repair;
- evidence.
