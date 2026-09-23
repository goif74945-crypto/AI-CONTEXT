# NEXY.AI Contract Registry

Pinned implementation snapshot:
- repo: `goif74945-crypto/NEXY.AI-`
- branch: `codex/spec-audit-20260919-78df350`
- HEAD: `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`

## Structure
- `registry.json` — compiled counts/defaults/snapshot.
- `contract.schema.json` — machine validation schema.
- `api/contracts.jsonl`
- `events/contracts.jsonl`
- `schemas/contracts.jsonl`
- `storage/contracts.jsonl`
- `modules/contracts.jsonl`
- `errors/contracts.jsonl`

## Semantics
A contract record binds source authority to observed code references without claiming runtime PASS.

Contract fields cover producer, consumer, input/output schema, pre/postconditions, errors, timeout, idempotency, authorization, version and source/code references.

## Boundary
`IMPLEMENTATION_PRESENT_E0` means contract-bearing code is present at the pinned HEAD. Acceptance/Test Matrix and Evidence Registry determine whether behavior is proven.
