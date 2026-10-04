# Integration Contract

## Integration posture
**ADVISORY / READ-ONLY / EXPORT-IMPORT ONLY**

NEXY-REFLEX is designed so NEXY can use it without granting it write access to NEXY.

## Producer contract
A NEXY-side adapter, build tool, or human-controlled export process may emit one JSON object matching `contracts/input.schema.json`.

Required semantic fields:
- target identity: stable logical ID + exact revision + optional content digest;
- explicit authority order;
- requirement claims with semantic key, source authority, build scope, accepted evidence classes and dependencies;
- evidence records bound to requirement ID and target revision/content.

## Consumer contract
REFLEX emits `contracts/output.schema.json` with:
- canonical verdict;
- advisory gate action;
- input digest;
- decision digest;
- effective requirement IDs;
- non-gating IDs;
- deterministic finding list.

## Safe calling pattern
1. NEXY or a controlled build process exports snapshot data.
2. REFLEX runs in an isolated process with no NEXY write credentials.
3. Exit code `0` means REFLEX verdict `PASS`.
4. Exit code `2` means REFLEX recommends freeze.
5. Exit code `4` means malformed/unsupported input.
6. NEXY remains the final authority over whether and how to consume the advisory result.

## CLI

```bash
PYTHONPATH=src python -m nexy_reflex.cli evaluate examples/pass.snapshot.json --output out.json
PYTHONPATH=src python -m nexy_reflex.cli replay examples/pass.snapshot.json --expect-digest sha256:...
PYTHONPATH=src python -m nexy_reflex.cli diff before.json after.json --output impact.json
```

## Compatibility guarantees of v0.1
- Python 3.11+.
- Standard library only at runtime.
- UTF-8 JSON.
- Snapshot contract version `1.0` only.
- SHA-256 deterministic digests.

## Explicitly not guaranteed
- NEXY internal API compatibility, because no current implementation API contract was inspected or mutated for this standalone task.
- Deployment integration.
- Runtime security beyond the pure local computation surface.
- Coverage of every NEXY requirement domain.

Those are intentionally left `NOT_VERIFIED` instead of being filled with decorative optimism.
