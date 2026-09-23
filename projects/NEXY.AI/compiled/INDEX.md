# NEXY.AI Machine-readable Canon Packs

Task-oriented entry packs for low-context, high-precision AI work.

- `nexy-canon.json` — authority/scope/supersession/critical laws.
- `nexy-build-context.json` — build snapshot/defaults/order + registry pointers.
- `nexy-audit-context.json` — evidence/traceability/failure/regression entry.
- `nexy-runtime-context.json` — state/event/config/error/concurrency/runtime entry.
- `manifest.json` — routing and refresh rules.

## Design choice
These files deliberately **do not duplicate all 516 ontology entities / 262 requirements / large traceability registries**.

They are minimal machine-readable boot packs. AI follows exact pointers only for the task-relevant slice, reducing context pollution and stale duplicated truth.

**Source registries remain authoritative.**
