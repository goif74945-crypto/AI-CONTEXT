# Research Backlog

These are proposals only, not implementation claims.

1. **Atomic reservation protocol**: compare-and-swap on catalog version so two agents cannot both receive ALLOW from the same stale snapshot.
2. **Write-set granularity**: distinguish file, directory, glob, database keyspace, queue, environment, deployment target, and external service mutation domains.
3. **Semantic duplicate detection**: evaluate deterministic local embeddings or dual-model review only as an advisory signal, never as hard authority without reproducibility controls.
4. **Historical calibration**: replay completed AI-CONTEXT workstreams and measure how often lexical overlap predicts actual conceptual duplication.
5. **Conflict graph**: emit a graph of workstreams/resources instead of pairwise findings only.
6. **Lease handoff**: interoperate with Delegation Lease Lab without merging the two authority models. WOCF answers collision; lease logic answers delegated permission.
7. **Resource governor handoff**: after admission, a resource governor may select workers. WOCF must not choose workers itself.
8. **Human-readable differentiator compiler**: generate concise evidence-backed explanations of why two workstreams are distinct without letting prose override hard path/resource collisions.
9. **Catalog provenance**: sign or attest catalog snapshots so admission decisions can later be replayed against the exact registry state.
10. **Distributed fault injection**: test stale reads, concurrent reservations, partial writes, process crashes, and retry/idempotency behavior at E3/E5 levels.
