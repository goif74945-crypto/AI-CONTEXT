# NEXY.AI Known-Good Baselines

## Purpose
Preserve exact proven historical recovery points without accidentally treating them as current truth.

## Files
- `baselines.jsonl` — 18 baseline records.
- `validation-report.md`

## Baseline classes
- `HISTORICAL_COMPONENT_RECOVERY`: exact historical repair/proof point.
- `CURRENT_CONTEXT_STRUCTURE`: current AI-CONTEXT registry validation only.

## Absolute rule
A historical green commit/workflow is **not** a current NEXY runtime baseline.

Before using a baseline:
1. compare target HEAD;
2. identify changed impact surface;
3. rerun required regression/evidence;
4. promote current status only from fresh proof.
