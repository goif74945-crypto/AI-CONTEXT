# Compatibility & Evolution

## Dimensions
API shape; semantics; persistence schema; events; configuration; auth; client behavior; model/prompt behavior; operations.

## Breaking Change Test
potentially breaking หาก consumer เดิมอาจ fail, misinterpret, silently change behavior, lose data, gain/lose permission, retry differently หรือ cache incorrectly.

## Migration
inventory consumers -> define old/new contracts -> compatibility bridge -> backfill with verification -> observe divergence -> migrate consumers -> remove bridge after evidence -> retain rollback according to risk.

## Feature Flags
ต้องมี owner, default, rollout plan, telemetry, kill switch, cleanup condition.

## Data Migration
preflight invariants; bounded batches; resume; idempotency; progress visibility; reconciliation; rollback/forward-fix.

## AI Evolution
prompt/model/tool change อาจ breaking แม้ API เดิม. เก็บ eval corpus, critical invariants, model/tool version และ comparative evidence.
