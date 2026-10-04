# INTEGRATION_CONTRACT

Status: proposal only. No NEXY.AI integration is authorized by this mission.

A future adapter MUST bind exact source/spec identities, reject stale schemas, preserve IDs/hashes/ticks, supply complete participant inventories for completeness claims, keep Q64.64 authoritative paths free of binary float, preserve evidence roots, and treat PASS only as this verifier's predicate.

Current-source adjacency at `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`:
- retry policy already exists; S04 adds ambiguous-effect safety evidence rather than replacing retry;
- OWNER cancellation/idempotent replay exists; S14/S17 add disclosure/propagation verification;
- audit hash chain exists; S16 audits correlation/sequence, not chain replacement;
- artifact export exists; S12 targets user-level ownership coverage;
- production secret provider exists; S11 is build/config defense in depth;
- release gate exists; S20 is proposal-only presentation precedence after authoritative failures exist.

Forbidden shortcuts: no NEXY.AI mutation, no PASS-to-release conversion, no float-to-Q64 silent bridge, no Canon mutation, no claim local tests equal deployed proof.
