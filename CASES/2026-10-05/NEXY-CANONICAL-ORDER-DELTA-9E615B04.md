CASE_ID: NEXY-CANONICAL-ORDER-DELTA-9E615B04
head: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
status: PARTIAL_IMPROVED

resolved_static_targets:
- Phase-F economy constitutional ordering
- G20/G25 governance/chaos ordering
- L1o L600 support ordering
- Lo2 federation tie-break ordering
- Lo3 governor/L600 ordering
- Sovereign canon seal/global anchor/versioning ordering
- Universe capability/cross-app/web-app ordering

mechanism:
- new packages/core/canonical-order.ts compareCanonicalText compares Unicode scalar values independent of host locale.
- tests cover ASCII, Thai, mixed-script, composed/decomposed forms and replay/reversed inputs.

remaining_risk:
- packages/obs/incident-priority.ts canonicalSecondary() still uses localeCompare in deterministic multiple-failure arbitration.
- packages/obs is classified BOUNDARY and is outside scanner blocking roots.
- do not declare repository-wide canonical ordering complete.
