# Read-Only NEXY Compatibility Boundary

Status: COMPATIBILITY_PROPOSAL / NOT_INTEGRATED
NEXY repository: `goif74945-crypto/NEXY.AI-`
Observed branch: `NEXY.ai`
Observed snapshot SHA: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
Mutation authority used: NONE

## Observed source contracts
The following were inspected read-only at the observed branch:

- `packages/contracts/directive.ts`
  - directive request carries stable IDs, mode, priority, bounded input, constraint fields, operator/role metadata, schema version, and idempotency key.
- `packages/contracts/evidence.ts`
  - evidence items include source, source type, content, 64-hex hash, confidence, verified flag, collection identity, anchors, contradiction indicator, and normalization version.
- `packages/contracts/state.ts`
  - canonical SystemState is `INIT | READY | RUNNING | VERIFYING | CONSENSUS | STABLE | FREEZE | STOP`.
- `packages/contracts/envelope.ts`
  - canonical wire envelope carries status/state/request/trace/version and optional actor, freeze reason, warnings, integrity, data, and error.
- `packages/contracts/release-policy.ts`
  - release result contains pass flag, reasons, and threshold snapshot.
- root `package.json`
  - TypeScript/Vitest tooling and contract/integration/typecheck verification scripts exist.

## Proposed adapter relationship
NOCM is intentionally **outside** these contracts.

1. Outcome Closure evidence IDs may point to NEXY evidence records through a future adapter, but NOCM must not replace or weaken `EvidenceItemSchema`.
2. Progress Truth is a supplemental project/task aggregate. It must not masquerade as or overwrite canonical SystemState.
3. Reversible Probe Planner can produce a *proposal* for evidence acquisition. A future adapter may translate an authorized safe probe into a directive only after NEXY's own authority, constraints, idempotency, and release rules approve it.
4. Benefit Regression is pre-adoption R&D evidence. It is not ReleasePolicy and cannot alter release thresholds.
5. Adoption Readiness's strongest output is `READY_FOR_HUMAN_REVIEW`, intentionally below canonical promotion/release authority.

## Compatibility invariants
- NEXY contracts remain authoritative.
- NOCM never writes into NEXY state or evidence stores directly.
- NOCM fingerprints are not substitutes for NEXY cryptographic evidence hashes.
- NOCM cannot interpret README orientation as permission to change canonical law.
- Future integration requires an explicit adapter and fresh tests against the then-current NEXY exact SHA.

## Compatibility result for this lab
`PASS` means only: the reference proposal can be kept isolated and an adapter boundary can be described without changing the observed contract files. It does **not** mean production integration has been executed or verified.
