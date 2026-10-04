# AI-Proposed Future Ideas

All items are `PROPOSAL` / `HYPOTHESIS`, not NEXY requirements.

1. **Cross-language conformance arena:** independent Rust/Python/TypeScript/Go implementations must match bytes and hashes without shared implementation code.
2. **Canonicalization witness certificate:** non-authoritative record of format version, schema id, policy id, admission class, and canonical hash.
3. **Differential parser firewall:** compare approved pair/number semantics across parser upgrades and freeze on divergence.
4. **Unicode confusable policy:** keep visual-confusable detection separate from NFC canonical admission.
5. **Schema-bound canonical wire:** bind exact schema identity so unknown fields cannot disappear into generic maps.
6. **Streaming decoder equivalence proof:** bounded-memory decoder must accept/reject exactly the same language as reference decoder.
7. **Deterministic mutation algebra:** named truncate/length/tag/reorder/duplicate/Unicode/append operators with coverage accounting.
8. **Format-drift invalidation graph:** changing ordering/tag/hash rules automatically invalidates dependent vectors, hashes, replay, and conformance evidence.
9. **Hostile complexity budget:** derive limits from measured CPU/memory evidence rather than arbitrary defaults.
10. **Canonical diagnostic codes:** stable machine error codes while keeping human messages outside consensus semantics.
11. **Legacy migration quarantine:** never auto-rewrite persisted history; prove semantic equivalence before version migration.
