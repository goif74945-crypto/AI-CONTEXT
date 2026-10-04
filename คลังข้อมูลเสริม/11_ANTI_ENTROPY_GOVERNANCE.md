# Anti-Entropy Governance for Long-Lived AI Context
Status: PROPOSAL / AI-PROPOSED CONCEPT
Authority: ADVISORY ONLY

## Threat
Long-lived context repositories decay even when every individual edit looks reasonable. Duplicate summaries diverge, advisory text gains accidental authority, stale claims survive, and AI-generated documents recursively cite other AI-generated documents.

Call this context entropy.

## Entropy signals
- duplicate claim with different wording and no shared identity
- orphan document with no authority/source link
- advisory claim copied into authoritative-looking location
- missing supersession edge
- contradictory status labels
- stale repository SHA
- generated summary citing another summary instead of primary evidence
- requirement with multiple incompatible interpretations
- unresolved UNKNOWN silently disappearing from later docs

## Anti-entropy cycle
DISCOVER -> NORMALIZE -> LINK -> COMPARE -> INVALIDATE -> ARCHIVE -> VERIFY

## Claim identity
PROPOSAL: important claims receive stable IDs independent of prose.
A claim record points to:
- canonical statement
- authority
- scope
- sources
- derivations
- dependents
- contradictions
- status
- supersession

Documents may render claims, but prose copies do not become independent truth.

## Source-distance rule
For authority-sensitive decisions, prefer shortest provenance path to primary authority. Each summarization hop increases transformation risk.

## Compaction rule
Compaction may reduce tokens but must preserve:
- MUST/SHALL/NEVER semantics
- thresholds
- exclusions
- authority
- uncertainty
- contradictions
- identifiers
- evidence pointers

If loss cannot be bounded, keep the original and mark the summary non-authoritative.

## Garbage collection
Eligible for archive, not silent deletion:
- superseded advisory proposals
- duplicate generated summaries
- stale snapshots whose historical value remains
- invalidated hypotheses

Never garbage-collect the evidence needed to reconstruct why a past decision was made.

## Entropy audit
Periodically ask:
1. Which claims have no primary source?
2. Which claims have conflicting active variants?
3. Which sources are stale?
4. Which UNKNOWNs vanished without resolution evidence?
5. Which AI proposals are being treated as project facts?
6. Which documents cannot name their authority tier?

## Metric proposals
orphan_claim_rate
contradiction_density
mean_provenance_hops
stale_dependency_rate
unlabeled_generated_content_rate
unknown_disappearance_rate
supersession_completeness

Metrics diagnose; they do not become authority.
