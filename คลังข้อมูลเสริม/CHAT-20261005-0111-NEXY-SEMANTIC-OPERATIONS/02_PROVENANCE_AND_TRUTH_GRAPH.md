# Provenance and Truth Graph
## Problem
Flat memory mixes source text, repository/runtime observations, inference, tool output, cache, and directives into plausible ambiguity.
## Claim node
claim_id; subject; predicate; value; truth_class; authority_rank; source_ref; observed_at; valid_from; valid_until; scope; sensitivity; verification_status; supersedes; content_hash.
## Edge types
DERIVED_FROM, VERIFIED_BY, CONTRADICTS, SUPERSEDES, SUMMARIZES, TRANSFORMS, DEPENDS_ON, AUTHORIZED_BY, OBSERVED_IN, INVALIDATED_BY.
## Truth classes
SOURCE_FACT, REPO_FACT, RUNTIME_FACT, EXTERNAL_FACT, INFERENCE, ASSUMPTION, UNKNOWN, CONFLICT, NOT_VERIFIED.
Promotion never overwrites provenance. It adds a claim or verification edge.
## Conflict resolution
Group semantic peers; enforce scope/validity; compare authority/recency/evidence; honor explicit supersession; otherwise preserve CONFLICT. Block mutations whose correctness depends on unresolved conflict.
## Invalidation
When a source claim becomes invalid, traverse DERIVED_FROM/DEPENDS_ON and mark downstream conclusions dirty.
## Cache rule
Cache = materialized view, not fact. Bind it to source revision + derivation revision + expiry + scope. Dependency revision changes invalidate it even before TTL.
## Audit queries
Why believe X? Who authorized X? What changed X? Which outputs depend on invalid evidence? Which claims lack verification? Which conflicts remain?
## Privacy
Prefer protected source handles over duplicating sensitive payloads.
