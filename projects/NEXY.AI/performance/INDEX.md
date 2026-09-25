# NEXY.AI Performance Budget Registry

## Purpose
Centralize source-backed timing/concurrency/coverage/resource budgets so AI does not re-derive numbers from prose.

## Files
- `budgets.jsonl` — 18 registered source-backed budgets.
- `robotics-latency-domains.json` — path-separated robotics latency registry (`sensor_to_actuator`, `mcu_fast_path`, `lo3_cycle`) with unresolved values preserved instead of collapsed.
- `validation-report.md`

## Status semantics
- `CANONICAL_BUILD_DEFAULT` = current DOC-C build default.
- `SOURCE_REQUIREMENT` = explicit source requirement, implementation/enforcement proof separate.
- `SOURCE_DESIGN_TARGET` / `SOURCE_DESIGN_RECOMMENDATION` = future/design target, not production guarantee.
- `SOURCE_DESIGN_VARIANT` = one of multiple source values; conflict must remain visible.

## Critical unresolved item
Robotics Safe Path / critical-loop latency remains unresolved:
`CONFLICT-RCL-LATENCY-001`.

Do not select 50–200ms, 50–500ms, <100ms, ~5ms, ~10ms, or ~100ms as one universal production truth. Use the path-separated registry and keep `authoritative_value_ms=null` until target-domain profiling + authoritative contract resolves each metric.

## Rule
No budget without a source pointer. Unknown throughput/memory/cost values remain unknown rather than invented.
