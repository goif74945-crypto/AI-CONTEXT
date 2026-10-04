# Dormant Capability Quarantine
> AI-PROPOSED CONCEPT
Unused capabilities should not remain implicitly trusted forever.
## States
ACTIVE -> WATCH -> DORMANT -> QUARANTINED -> REVALIDATING -> ACTIVE, or QUARANTINED -> RETIRED.
## Triggers
No production use; stale dependency; missing owner; tests no longer exercise behavior; superseded authority/spec; expired security assumptions.
## Resurrection gate
Current spec mapping; dependency verification; security review; data compatibility; acceptance tests; observability confirmation.
Purpose: eliminate zombie features that execute but no longer satisfy current contracts.
