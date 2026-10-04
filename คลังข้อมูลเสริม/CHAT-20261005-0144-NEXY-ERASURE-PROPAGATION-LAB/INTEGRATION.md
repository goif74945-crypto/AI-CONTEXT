# NEXY Integration Contract

Status: PROPOSED FUTURE INTEGRATION. No NEXY.AI code was modified.

## Read-only compatibility anchor

Repository: goif74945-crypto/NEXY.AI-
Branch: NEXY.ai
Commit: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43

Observed blobs:
- package.json: 972cd03ed7878ff6eb0cb4813e459cb0c29cd1e7
- vault/repository.ts: 197698c5514da02af251640aa51ad80597710c8f
- prisma/schema.prisma: be1cbe1481829a2c95b6599929abc86829f37667

## Observed facts at that snapshot

- TypeScript/Node is already part of the stack.
- Project and Artifact expose soft-delete state through deletedTick.
- Artifact exposes hardDeletedTick.
- ArtifactStorageState exposes lifecycle state and blobAccessRevoked.
- Revision and Commit are documented as immutable and use restrictive relationships.
- AuditLog is append-only and must not be updated/deleted.
- Vault commit paths emit immutable event/audit evidence.

## Proposed mapping

CANONICAL_ARTIFACT -> Project/Artifact control-plane identity
BLOB -> ArtifactBlobLocation / physical storage adapter
DERIVED -> derived artifacts with single-principal provenance
SHARED_DERIVED -> outputs whose provenance references multiple principals
CACHE -> Redis/application cache projections
INDEX -> search/index projections
AUDIT_LOG -> append-only AuditLog/EventLog identity
EXTERNAL_EXPORT -> third-party export/adaptor record

## Integration gates before production use

1. Define authoritative provenance edges for every derived/cache/index/export path.
2. Define trusted executor adapters and idempotency keys per action.
3. Define a receipt schema whose evidenceHash is backed by adapter-specific evidence.
4. Bind retention/legal hold policy to an authoritative policy engine.
5. Implement external erasure adapters and retry/reconciliation.
6. Ensure audit tombstones carry no erased payload.
7. Add crash/replay/concurrency tests around partial execution.
8. Add backup/replica propagation semantics.
9. Add deployment evidence proving physical erase and projection cleanup.

Until those gates exist, this project remains advisory and must not be used to claim production deletion completion.
