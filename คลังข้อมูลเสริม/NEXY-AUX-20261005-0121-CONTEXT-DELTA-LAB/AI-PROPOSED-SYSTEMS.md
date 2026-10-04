# AI-Proposed Future Systems

Everything in this file is a proposal, not current NEXY scope.

## Proposal A — Context Delta Sentinel
Continuously compare approved context snapshots at explicit checkpoints and block reuse of stale verification when governing inputs changed.

Promotion gate: prove false-positive/false-negative behavior on historical context changes; define ownership of snapshot creation; never monitor or mutate silently.

## Proposal B — Evidence Expiry Router
Consume a delta report and map impacted records to exact evidence jobs. It should invalidate only evidence whose claim inputs changed, while preserving unrelated proof.

Promotion gate: must integrate with an authoritative evidence registry and prove that selective invalidation cannot suppress mandatory gates.

## Proposal C — Authority Migration Review
When a record moves between DOC-B/DOC-C/DOC-D/DOC-E or current/future scopes, produce a human-review packet that shows semantic and authority impact separately.

Promotion gate: require canonical authority owners and conflict handling before any automated status transition.

## Proposal D — Drift Budget Dashboard
Measure how many current-build records changed between releases, how much verification was invalidated, and where review cost concentrates.

Promotion gate: metrics must never become a reason to skip required verification. Optimization follows proof integrity, not vice versa.
