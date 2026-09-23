# NEXY.AI Fuzz / Chaos Catalog

## Purpose
Systematic attack/fault catalog for current testing and future deterministic ChaosUniverse work.

## Modes
- `DETERMINISTIC_CHAOS_UNIVERSE` — future G25 isolated deterministic fork.
- `CURRENT_TEST_INJECTION` — current DOC-C fault/negative-path testing.
- `ADVERSARIAL_INPUT` — model/input security testing.
- `FAILURE_INJECTION` — reasoning/runtime fault cases.
- `HIL_OR_SIMULATION_FAULT` — robotics; physical claims still require physical/HIL evidence.

## Files
- `catalog.jsonl` — 22 scenarios.
- `validation-report.md`

## Rule
Chaos state never becomes production state.
A scenario definition is not proof that the system survives it.
