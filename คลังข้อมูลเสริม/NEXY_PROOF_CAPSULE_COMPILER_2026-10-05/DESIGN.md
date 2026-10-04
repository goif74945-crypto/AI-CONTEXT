# Design Contract — AI Proposal

Pipeline: `claims + evidence + policy + as_of -> validate -> filter -> authority -> conflict gate -> deterministic cover -> budget gate -> hash -> PASS/FREEZE`.

Invariants: every required claim needs admissible evidence; evidence class is exact, not numerically substitutable; target/version/freshness must match; strongest FAIL blocks weaker PASS; equal strongest material disagreement freezes; weaker dissent is disclosed; budget overflow freezes instead of truncating; input commitment binds claim semantics, evidence provenance/digest, policy and time; core has no hidden network/filesystem/environment/process I/O.

Selector: claim/evidence adjacency + incrementally updated heap. Tie-break is most uncovered claims, then lower display cost, then lexicographic evidence ID. This is deterministic greedy cover, not a claim of globally minimal set cover.

Digest boundary: the compiler validates canonical `sha256:<64 lowercase hex>` and commits it into identity, but ingestion must verify that digest against actual evidence bytes.

Adoption gate: authoritative spec adoption, canonical cross-language schema/serialization, real digest verification, TypeScript/Rust parity if chosen, integration/UX/adversarial/performance tests, migration/rollback law, and exact-head evidence.
