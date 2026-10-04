# NEXY Compatibility / Future Integration Contract

## Current exact implementation evidence used

Read-only NEXY implementation observation was bound to:
- repository: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

Observed relevant surfaces:
- `packages/core/vnext-state-matrix.ts`: `boot`/`execute` owned by CORE, `agents_done` by SWARM, `verified`/`accepted`/`rejected` by JUDGE;
- `core-kernel/src/kernel/vnext_matrix.rs`: equivalent JUDGE ownership for verification/accept/reject path;
- `packages/phase-f/lo3/governor.ts`: signed Q64.64 carried by BigInt with explicit signed-i128 range checks and divide-by-zero rejection;
- `core-kernel/src/engine/fixed128_math.rs`: signed Q64.64 `i128` implementation with fail-closed component behavior on checked arithmetic failure.

## Adapter rule

A future authorized adapter may translate existing proposal/evidence records into SFRC inputs, execute SFRC out-of-band, and return the `PromotionSciencePacket` as additional evidence.

It must **not** wire `eligibleForJudgeReview` directly to a state transition. The field means only that the scientific-validity packet is sufficiently complete to be *submitted* to the existing authority path.

## Suggested future call shape

```text
NEXY proposal/evidence snapshot
  -> immutable adapter DTO
  -> SFRC scientific evaluation
  -> PromotionSciencePacket
  -> existing evidence store / review queue
  -> LAW/JUDGE/Human authorized promotion logic
```

## Required integration safeguards

- pin exact source/spec and NEXY implementation commit used for each chamber run;
- preserve the preregistration hash before treatment-result evidence becomes available;
- map actor identities to stable privacy-preserving hashes;
- ensure replicator independence is meaningful, not just a different string supplied by the same actor;
- persist append-only null result lineage in an authorized durable store;
- bind environment IDs to actual reproducible environment manifests;
- treat `FailClosedError` as a blocked experimental evaluation, not permission to continue;
- never reinterpret DEFER as CUT;
- rerun tests against the exact adapter/runtime revision before any promotion discussion.

## What this package does not prove

This package is locally executed standalone evidence. It does not establish E4/E5/E6 evidence for NEXY integration, runtime operations, deployment, production security, or physical systems. Those remain NOT_VERIFIED until an authorized future integration is actually built and tested.
