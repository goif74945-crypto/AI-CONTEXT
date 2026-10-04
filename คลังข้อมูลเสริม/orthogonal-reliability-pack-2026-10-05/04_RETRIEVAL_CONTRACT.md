# Retrieval Contract
Request fields: query, intent, project_namespace, allowed_sources, forbidden_sources, authority_floor, freshness_requirement, time_scope, entity_scope, version_scope, max_results, sensitivity_policy.
Result fields: chunk_id, source_id, canonical_locator, content_hash, version, observed_at, authority_rank, relevance_score, scope_match, freshness_status, contradiction_group, content.

## Invariants
R1 Namespace mismatch rejected before ranking.
R2 Forbidden sources never enter context.
R3 Stale evidence cannot silently satisfy fresh requirements.
R4 Duplicates collapse by canonical identity/content hash.
R5 Provenance survives retrieval and synthesis.
R6 Ranking cannot override access policy.
R7 Empty retrieval produces explicit NO_EVIDENCE, never filler.
R8 Conflicting high-authority evidence surfaces as conflict.

## Four-pass retrieval
Precision -> Recall -> Authority verification -> Contradiction scan.

## Metrics
precision@k; golden-question recall; authority-weighted precision; freshness violation rate; cross-namespace leakage; contradiction surfacing; unsupported-answer rate.
