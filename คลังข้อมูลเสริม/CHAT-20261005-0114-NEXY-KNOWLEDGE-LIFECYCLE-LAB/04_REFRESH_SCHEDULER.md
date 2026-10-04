# Evidence Refresh Scheduler
> Classification: AI-PROPOSED CONCEPT. Design only.

## Goal
Allocate verification effort by consequence and volatility rather than refreshing everything equally.

## Inputs
Criticality, volatility, evidence age, source authority, dependency fan-out, contradiction signals, verification cost, consumer activity.

## Priority
Priority rises with execution/safety/financial impact, age relative to policy, volatility, active dependents, contradictions, and recent access. It falls for archival low-impact knowledge and where trustworthy event-driven invalidation exists.

## Modes
TIME after TTL.
EVENT on dependency/source change.
ACCESS before reuse.
HYBRID event-driven plus maximum TTL.
MANUAL expert review required.

## Safe reuse gate
For a critical claim: state ACTIVE; evidence resolves; freshness policy passes; no unresolved HARD contradiction; critical upstream dependencies pass recursively. Any failure => fail closed and revalidate before executable use.

## Starvation protection
Reserve refresh capacity for critical tiers. Cap repeated retries against unavailable sources. Do not let large volumes of cheap low-impact checks starve a small set of expensive critical verifications.
