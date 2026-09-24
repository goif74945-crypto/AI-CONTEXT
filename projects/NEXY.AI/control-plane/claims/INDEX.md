# P4.4 Claim / Lease

## Purpose
Prevent duplicate execution and conflicting concurrent mutation without serializing unrelated work behind one global lock.

## Lease identity
Every claim binds `claim_id + command_id + worker_id + lease_epoch` with explicit lease start, heartbeat deadline and expiry.

## Collision model
Before mutation, compare canonical mutation-exclusive:
- path claims;
- resource claims;
- dependency-closure claims.

Unrelated closures may execute concurrently. Exact/ancestor/descendant path overlap is a collision.

## Recovery
Expired lease history is immutable. Recovery requires a new claim with a higher/new lease epoch after worker/HEAD/collision revalidation.

## Files
- `claim-registry.schema.json`
- `claim-policy.json`
- golden and negative examples
- `validation-report.md`
