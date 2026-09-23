# PLAYBOOK — Audit Persistence

## PURPOSE
Verify state ownership, durability, lineage, versioning, deletion and consistency semantics.

## PROCEDURE
1. Load state ownership + persistence map.
2. Identify authoritative writer/readers.
3. Resolve data/storage contracts and requirements.
4. Inspect identity/key/version fields.
5. Inspect transaction boundaries.
6. Inspect OCC/idempotency semantics.
7. Inspect blob/metadata hash linkage.
8. Inspect append-only/immutable records.
9. Inspect FK/delete/restore/hard-delete behavior.
10. Inspect retention/redaction.
11. Inspect migration/rollback.
12. Test partial writes/concurrent writers/stale versions.
13. Verify audit trail survives legal mutation/deletion rules.
14. Check recovery and persistence semantics agree.

## RED FLAGS
- overwrite of immutable revision/history;
- multiple canonical writers;
- hard delete without required authority/audit;
- restore when lineage/blob is missing;
- metadata commit without verified blob or vice versa;
- stale previous_version accepted;
- redaction rewriting canonical audit history;
- migration without tested rollback.

## PASS
Requires DB/storage integration evidence appropriate to the claim; schema presence alone is E0/E1 only.
