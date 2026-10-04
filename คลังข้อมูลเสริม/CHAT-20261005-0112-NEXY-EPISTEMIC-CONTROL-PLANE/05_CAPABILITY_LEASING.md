# Capability Leasing & Revocation
Agents should receive temporary capabilities rather than ambient permanent authority.
Lease: principal, action classes, target scope, read/write distinction, limits, start/expiry, preconditions, revocation triggers, required evidence, rollback expectation, human approval boundary.
Laws: expiry deny-by-default; read never implies write; no implicit inheritance; delegation cannot exceed held authority; scope changes invalidate lease.
Revocation triggers include head change, authority conflict, stale evidence, anomalous tool behavior, budget exceedance, user-law change.
Status: DESIGN PROPOSAL.