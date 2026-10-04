# Release & Migration Safety
Pre-release: exact versioned artifact, config validation, migration review, compatibility, rollback/mitigation, critical tests, observability, ownership.
Database expand/contract: expand compatible schema; deploy dual-compatible code; migrate/backfill; verify; switch; observe; contract old schema.
Do not combine irreversible destructive schema removal with unverified cutover.
Progressive delivery: internal -> small cohort -> larger -> full, gated by health criteria.
Code rollback is not data rollback; verify backward compatibility of new writes.
Post-release verify version, health, synthetic critical paths, error/latency deltas, data correctness, backlog, dependency behavior.
