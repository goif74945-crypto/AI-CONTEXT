# P4.7 Result Package

## Decision
**REUSE, DO NOT DUPLICATE.**

The first-class result package is the existing handoff type:
`BUILDER_TO_AUDITOR`
under `projects/NEXY.AI/handoff/handoff.schema.json`.

It already carries:
- command/handoff reference;
- START_HEAD / END_HEAD;
- changed files + commits + actual actions;
- tests run + results;
- evidence;
- failures + residual risks + blockers;
- rollback state + status.

This directory is a control-plane integration profile, not a second schema.

## Files
- `result-package-profile.json`
- `validation-report.md`
