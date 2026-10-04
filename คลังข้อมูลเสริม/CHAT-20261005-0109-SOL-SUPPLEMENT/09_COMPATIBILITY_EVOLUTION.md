# Compatibility & Evolution Strategy

Status: SUPPORTING_KNOWLEDGE

## Contract surfaces
Version API payloads, event schemas, persisted records, tool contracts, policy formats, model/provider adapters, evidence records and UI-consumed state whenever semantic interpretation may change.

## Change classes
1. additive compatible
2. behavior-changing but schema-compatible
3. schema-breaking
4. semantic-breaking
5. security-sensitive
6. irreversible data migration

Schema compatibility never proves semantic compatibility.

## Safe migration sequence
Map producers/consumers → define old/new invariants → add compatibility reader/adapter → migrate/backfill with measurable progress → verify old/new paths → cut over with explicit criteria → observe → remove legacy path only after rollback window.

## Rules
- Never silently reinterpret an existing field.
- Unknown enum/value behavior must be explicit.
- Durable records should carry schema/version when future decoding can differ.
- Provider adapters should expose capabilities explicitly.
- Evidence for version A becomes stale for changed semantics in version B.
- Dual-write requires reconciliation and authoritative winner rules.

## Rollback design
State whether rollback means code rollback, data restore, forward-fix or compatibility bridge. Lossy transforms are irreversible unless a separately verified source preserves the original.

## Verification
Compatibility PASS requires executable old/new consumer tests at the relevant boundary, not merely matching type signatures.
