# Migration & Reversibility Law
> AI-PROPOSED CONCEPT.
1. Code rollback does not prove system reversibility.
2. Track read-old/write-old/read-new/write-new separately.
3. Prefer expand → dual-compatible → migrate → verify → contract.
4. Destructive contraction requires proof old consumers and rollback paths are retired.
5. Declare idempotency, partial failure, resume cursor, reconciliation, audit lineage.
6. Backfill completion is not correctness without invariant/count/referential proof.
7. If old code cannot interpret post-cutover data, rollback is BLOCKED.
8. Irreversible external effects require compensation semantics or explicit irreversibility.