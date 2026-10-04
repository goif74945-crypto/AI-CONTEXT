# Migration Choreography
Status: PROPOSAL_AI

A migration is a distributed state transition, not merely a deployment.

## State model
PREPARED → DUAL_COMPATIBLE → MIGRATING → VERIFIED → CUTOVER → CLEANUP_ELIGIBLE → CLEANED.
Side states: ROLLBACK, BLOCKED, PARTIAL, UNKNOWN.

## Questions
What old/new representations coexist? Which readers/writers support each? Is downgrade possible after new writes? What is the point of no return? How is partial migration detected? Which invariant proves completion? Which evidence expires after cutover?

## Expand / migrate / contract
Expand backward-compatibly; migrate while both forms are accepted; verify population and behavior; cut over authoritative writer/reader; observe through rollback window; contract only after evidence and authorization.

## Dangerous shortcuts
Breaking schema+code in one irreversible step; trusting backfill exit code as completion; deleting old fields before all readers move; rollback that cannot read new data; unrelated refactor during migration.

## Evidence
Static schema/contracts, data invariants, compatibility tests, runtime health, recovery rehearsal, and exact revision/environment binding.
