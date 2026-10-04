# Future Proposals — AI-Generated, Not Current NEXY Requirements

Every item in this file is **an AI-proposed concept only**. None is current NEXY.AI law, requirement, implementation, or verified capability. Promotion requires explicit human/project authority and its own design/implementation/evidence cycle.

## P1 — Merkle Rehydration Vault

Replace the flat dropped-ledger root with a Merkle tree so a consumer can request and prove only the missing atoms needed for a task without loading the entire source bundle. Useful for very large Vault histories and low-bandwidth agents.

Proof obligations before promotion:
- deterministic tree construction;
- inclusion/non-inclusion proofs;
- stable canonical leaf encoding;
- corruption and replay tests;
- migration/version rules.

## P2 — Multi-Tier Context Lattice

Produce related capsules at several information budgets:
- L0: immutable law + conflict/unknown only;
- L1: high-authority facts + evidence;
- L2: operational working context;
- L3: broader exploratory context.

Each tier must have its own commitment and be provably monotonic: lower tiers cannot contain an atom absent from the corresponding higher-authority source.

## P3 — Semantic Candidate Layer Above LBCC

Allow an LLM to propose paraphrased synthetic atoms, but never place those directly into the integrity capsule. Each synthetic atom would need:
- source atom IDs;
- explicit `INFERENCE` status until proven;
- entailment/adversarial verification;
- a reversible link to exact source;
- a fail-closed path when semantic equivalence cannot be established.

LBCC remains the non-generative ground-truth boundary.

## P4 — Delta Capsule Protocol

For evolving projects, store `base_commitment + added atoms + removed atom refs + changed atom refs` instead of repeatedly emitting full snapshots. This could reduce long-horizon storage and replay cost while preserving exact history.

Required controls:
- chain verification;
- checkpoint compaction;
- fork/conflict detection;
- bounded replay depth;
- deterministic merge rules or explicit CONFLICT.

## P5 — Tokenizer Budget Adapters

Keep LBCC core byte-based and provider-independent, but add optional adapters that estimate model-specific token cost. Adapter output is advisory unless backed by the exact tokenizer/version used at runtime. The core must not treat token estimates as canonical truth.

## P6 — Context Pressure Governor

A higher-level controller could choose shard size, codec budget, and retrieval depth based on current runtime limits. It must never weaken protected-record policy automatically. Pressure response should be:

`reduce optional context -> shard -> retrieve on demand -> FREEZE`

not `drop law/conflict/unknown`.

## P7 — Cross-Agent Context Partition Proofs

For SWARM-style work, issue different agents deterministic capsule subsets plus a common law capsule. Record exactly which atoms each agent saw. This would make later disagreements diagnosable as context divergence rather than vaguely blaming “model behavior.”

## P8 — Provenance-Aware Deduplication

Current LBCC does not merge semantically similar records. A future exact-dedup layer could deduplicate only when content and authority/provenance contracts prove equivalence. Near-duplicate semantic merging must remain separate from exact integrity compression.
