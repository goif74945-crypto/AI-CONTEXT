# Provenance & Evidence Graph
Counting citations is easy; proving independent support is not. Ten URLs can still be one rumor wearing ten hats.

Node classes: CLAIM, SOURCE, OBSERVATION, DERIVATION, TEST_RUN, ARTIFACT, BUILD, STATE, LAW, APPROVAL.
Edges: SUPPORTS, DERIVED_FROM, EXECUTED_BY, BUILT_FROM, OBSERVED_AT, GOVERNED_BY, APPROVES, INVALIDATES, SUPERSEDES.

Evidence cardinality should use independent roots, not leaves. Mirrors or derivatives of one root count as one unless canonical policy says otherwise.

Freshness is claim-specific. Record observed_at, valid_for, source_revision, retrieval identity, and refresh/expiry policy.

Contradictions must retain both claims, authority ranks, timestamps, roots, resolution rule, and disposition. Never average contradictions into confidence. Unresolved means UNKNOWN/NOT VERIFIED.

Quality dimensions: authority, directness, independence, integrity, freshness, reproducibility, completeness.

Minimal record: evidence_id; claim_id; source_type; locator; revision; content_hash; observed_at; authority_rank; independent_root_id; verification_method; verifier; status; notes.

Anti-patterns: screenshot as sole backend proof; README as executable proof; test name as proof of pass; report without executed-command evidence; mirrors counted independently; confidence without provenance.
