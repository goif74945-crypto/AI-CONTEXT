# LBCC Design Specification

## Classification

**AI-PROPOSED CONCEPT.** This document is a future integration proposal and standalone implementation, not current NEXY.AI system law and not proof of NEXY.AI runtime behavior.

## 1. Objective

Transform a `ContextBundle` into a smaller `ContextCapsule` while making all information loss explicit, bounded, deterministic, and auditable.

The codec does **not** attempt semantic paraphrase. That omission is deliberate. A generative summarizer can be useful above this layer, but it must not be trusted as the integrity boundary.

## 2. Non-goals

- no edits to NEXY.AI;
- no claim of token-optimal compression;
- no semantic equivalence proof for paraphrased text;
- no encryption or secret storage;
- no network calls;
- no provider-specific tokenization;
- no silent conflict resolution.

## 3. Actors and authority

1. Caller defines `CodecPolicy`.
2. Codec validates and applies deterministic selection.
3. Verifier independently recomputes commitments against source.
4. Optional future NEXY adapter may decide whether a `PASS` capsule is admissible. LBCC itself never overrides NEXY LAW/JUDGE.

## 4. Data model

### ContextAtom

A smallest independently traceable context unit:

- `atom_id`: stable unique ID.
- `text`: exact payload.
- `truth_class`: SOURCE_FACT / REPO_FACT / RUNTIME_FACT / EXTERNAL_FACT / INFERENCE / ASSUMPTION / UNKNOWN / CONFLICT / NOT_VERIFIED.
- `authority_rank`: integer 0..100, caller-owned meaning.
- `provenance`: source references.
- `evidence`: evidence references.
- `immutable`: hard retain flag.
- `tags`, `valid_from`, `valid_to`, `metadata`.

### ContextBundle

- `bundle_id`
- ordered-unimportant collection of atoms; canonicalization sorts by `atom_id`.

### CodecPolicy

- `max_capsule_bytes`: exact canonical serialized byte ceiling.
- `max_loss_ppm`: max dropped importance / total importance, 0..1,000,000.
- `protect_unknown_conflict`: default true.
- `protected_authority_rank`: atoms at/above this rank cannot be dropped; default 95.
- `allow_sensitive`: default false.

### CodecResult

- status `PASS` or `FREEZE`.
- capsule on PASS.
- full `loss_ledger` outside the constrained capsule.
- reason and metrics.

## 5. Importance model

No floating point is used. Each atom receives deterministic integer importance:

`truth_weight + authority_rank*1000 + evidence_bonus + provenance_bonus`, capped at 1,000,000.

Immutable/protected atoms are not droppable regardless of weight.

The default truth weights intentionally prioritize `CONFLICT`, `RUNTIME_FACT`, `SOURCE_FACT`, and `UNKNOWN` over inference/assumption. These weights are project-local defaults, not NEXY canonical law.

## 6. Selection algorithm

1. Validate bundle and policy.
2. Scan for likely secrets; FREEZE unless policy explicitly allows them.
3. Compute source bundle commitment from canonical JSON.
4. Partition atoms into protected and optional.
5. Build minimal capsule containing protected atoms and a dropped-set commitment summary.
6. If protected-only capsule exceeds byte limit, FREEZE.
7. Rank optional atoms by `importance / canonical_atom_bytes`, then importance, then ID. Integer cross-multiplication is used instead of floating point.
8. Add optional atoms when the resulting canonical capsule remains within the byte ceiling.
9. Compute full loss ledger for all omitted atoms.
10. Compute `loss_ppm`. If it exceeds policy, FREEZE.
11. Emit PASS capsule + separate loss ledger.

This is deterministic greedy utility-density selection, not an exact knapsack solver. The choice favors predictable runtime and reproducibility.

## 7. Cryptographic commitments

- `source_commitment_sha256`: canonical full source bundle.
- each dropped entry: canonical atom SHA-256.
- `dropped_commitment_sha256`: canonical ordered list of dropped references.

These commitments detect accidental or malicious mismatch. They are integrity commitments, not signatures and not authorization.

## 8. Freeze conditions

- malformed input;
- duplicate atom ID;
- invalid truth class / authority / policy range;
- likely secret with `allow_sensitive=false`;
- protected-only capsule cannot fit;
- computed information loss exceeds policy;
- verifier detects source commitment mismatch;
- verifier detects altered retained atom or loss ledger.

## 9. Determinism invariant

Given identical canonical input bundle, policy, and codec version, `canonical_json(result)` must be byte-identical.

No timestamps, randomness, environment-derived values, locale-sensitive sorting, or floating-point ranking participate in the core result.

## 10. Concurrency and state

Core functions are pure with respect to caller-visible state. No global mutable state, network, filesystem, clock, or environment is required. Multiple executions can run concurrently without shared state.

## 11. Security boundary

LBCC is not a secret manager. It detects several high-signal credential shapes and freezes. The scanner is a guardrail, not proof that content is non-sensitive. Integration should still enforce upstream data classification.

## 12. Future integration shape

Suggested, not implemented in NEXY.AI:

`VAULT/context atoms -> LBCC compact -> verifier -> NEXY admission/judge -> bounded context surface`

Potential uses:
- long-running project handoff;
- agent context sharding;
- low-RAM mode;
- evidence-preserving history condensation;
- deterministic context snapshots for replay.

## 13. Acceptance

Standalone acceptance requires E1 compilation, E2 tests including negative paths, and E3 CLI compact→verify execution. No claim about NEXY.AI integration is PASS until integrated and tested in that repository/runtime under separate authorization.
