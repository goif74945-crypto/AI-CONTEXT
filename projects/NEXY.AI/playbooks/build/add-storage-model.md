# PLAYBOOK — Add Storage Model

## PRECONDITIONS
- Authoritative owner/writer/readers identified.
- Durability/retention/deletion semantics known.
- New model does not break lineage/audit invariants.

## REQUIRED CONTEXT
- state ownership + persistence map;
- storage contracts;
- Vault requirements;
- data models;
- retention/redaction;
- security/permission map;
- migrations;
- evidence/test matrix.

## IMPLEMENTATION SEQUENCE
1. Define identity/key strategy.
2. Define owner/writer/readers.
3. Define schema and constraints.
4. Define immutable vs mutable fields.
5. Define revision/version semantics.
6. Define FK/delete/restore behavior.
7. Define transaction/atomicity.
8. Define content/hash/blob linkage where applicable.
9. Define migration and rollback.
10. Define audit/event emissions.
11. Implement persistence layer.
12. Add migration/integration/constraint tests.
13. Test rollback and corrupted/partial-write behavior where critical.

## NEGATIVE TESTS
- duplicate identity;
- stale previous_version/OCC;
- broken FK/lineage;
- unauthorized write/delete;
- partial blob/metadata commit;
- restore with broken parent/blob;
- rollback failure.

## DONE
Migration, persistence semantics, lineage, authorization, rollback and required evidence are proven.
