# AI-Proposed Future Concepts

**STATUS OF EVERY ITEM IN THIS FILE: AI_PROPOSAL_CONCEPT_ONLY**

These are ideas, not current NEXY requirements, not implementation claims, and not authorization to modify NEXY.

## 1. Golden Replay Corpus
Store approved exported snapshots plus expected REFLEX digests. Release tooling can replay the corpus to detect accidental change in governance semantics.

Potential value: deterministic regression proof for authority/evidence policy behavior.

## 2. Authority Lattice Fuzzer
Generate bounded permutations of authority order, duplicate claims, missing sources and equal-rank contradictions to test that adapters always fail closed.

Potential value: catches “last write wins” bugs before they become governance bugs.

## 3. Evidence TTL Policy Layer
Optional policy rules could declare that some runtime evidence expires by time even when revision is unchanged.

Potential value: operational evidence can become stale due to environment drift without source changes.

Risk: time-based policy can make replay depend on wall-clock time. Any implementation should inject evaluation time explicitly to preserve determinism.

## 4. Signed Export Envelopes
Add detached signatures over canonical snapshot bytes and signer-role metadata.

Potential value: prevents evidence/authority snapshots from being altered between producer and verifier.

Risk: key management becomes a real security system and must not be improvised.

## 5. Cross-Model Decision Differential
Feed the same normalized snapshot summary to multiple reasoning models, but compare their explanatory analysis only. REFLEX's deterministic verdict remains the control reference.

Potential value: find confusing requirement language without allowing probabilistic models to become authority.

## 6. Vault Change Impact Map
Convert REFLEX impact output into a graph showing which Vault facts/evidence become stale after each change.

Potential value: reduces unnecessary revalidation while preserving exact invalidation lineage.

## 7. Chaos Invalidation Simulator
Randomly mutate non-secret snapshot copies, target identities and dependency edges to verify that expected evidence becomes invalidated and no stale PASS survives.

Potential value: high-confidence failure-path testing for the evidence model.

## 8. Human Freeze Explainer
Render a minimal user-facing explanation from deterministic finding codes without exposing internal chain-of-thought.

Potential value: preserves NEXY's small human surface while keeping failure states actionable.
