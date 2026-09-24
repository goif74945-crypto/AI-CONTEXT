# NEXY.AI Change Impact Engine Data

## Purpose
Per-entity derived impact data consumed by the canonical `change-impact/` facade.

## Files
- `system-impact.jsonl` — **518** entity impact records.
- `impact.schema.json`
- `validation-report.md`

## Reconciliation
The ontology additions `EVENT-EXEC-CANCEL` and `EVENT-EXEC-TIMEOUT` are now included. Both are CURRENT_BUILD EVENTs, PART_OF `FSM-EXECUTION`, with the established EVENT regression class `STATIC + STATE_TRANSITION`.

## Canonical query boundary
Do not answer impact questions from this dataset alone; use `projects/NEXY.AI/change-impact/`.

## Staleness
Implementation/test/evidence refs inherit their source revision pins and must be refreshed when target HEAD changes.
