# Failure → Fix Log

1. **CSEC slotted-dataclass serialization failure**: explicit field serialization replaced `__dict__`.
2. **CSEC migration-step mismatch**: normalized required-default migration to an explicit BACKFILL step.
3. **CSEC many-to-one rename ambiguity**: added effective-target collision rejection.
4. **CPES artificial idle reservation**: selection now considers feasible start before critical-path priority.
5. **CPES benchmark timeout**: O(n²) ready scanning replaced with per-resource pending/runnable heaps. Final 1,000-task/8-slot local median: ~73 ms.
6. **CDA REVIEW state mutation**: REVIEW is now state-preserving; only ALLOW advances the ledger.
7. **Adversarial fixture conflict**: a REVIEW test accidentally violated the stronger linkability rule; fixture corrected, engine unchanged.
8. **FCCP quadratic lineage**: copied full reason paths replaced by O(V) predecessor lineage with on-demand path reconstruction. 5,000-node hard-chain local median improved from ~8.69 s to ~84 ms and peak memory from ~290 MiB to ~4 MiB.

Performance numbers are environment-specific reference measurements, not production guarantees.
