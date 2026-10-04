# Knowledge Lifecycle
Knowledge states: CAPTURED, VALIDATED, ACTIVE, STALE, SUPERSEDED, RETIRED.
Metadata: owner/domain, source authority, created_at, last_verified_at, freshness policy, supersedes/superseded_by, applicability scope.
Retrieval should prefer ACTIVE validated knowledge but preserve access to historical states for diagnosis.
Never delete contradictory historical evidence merely to make retrieval cleaner; mark lifecycle and precedence explicitly.
Periodic revalidation should be driven by freshness class and usage criticality.
