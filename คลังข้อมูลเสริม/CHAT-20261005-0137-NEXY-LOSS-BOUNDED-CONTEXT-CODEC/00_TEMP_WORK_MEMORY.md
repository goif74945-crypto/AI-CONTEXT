# Temporary Work Memory — LBCC

Status: PUBLICATION_VERIFIED
Session work ID: CHAT-20261005-0137-NEXY-LBCC
Target repository: goif74945-crypto/AI-CONTEXT only
Target path: คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-LOSS-BOUNDED-CONTEXT-CODEC
Protected scope: every GitHub repository whose name contains NEXY.AI; no mutation authorized or performed.

## Objective
Build a standalone, deterministic, model-agnostic Loss-Bounded Context Codec (LBCC) that can later integrate with NEXY.AI through JSON/file contracts without modifying NEXY.AI.

## Canonical constraints observed
- zero-guess / evidence-first / freeze on unresolved material uncertainty;
- preserve truth classes and provenance;
- deterministic execution is a design target;
- persistent memory should be explicit, scoped, provenance-aware;
- design is not implementation evidence;
- completion requires matching test evidence.

## Design decisions
- Python stdlib only to reduce supply-chain risk.
- No LLM summarization in the integrity codec.
- Exact retained atoms; omitted atoms are committed into a loss ledger.
- Capsule carries deterministic source commitment + dropped-set commitment.
- Protected atoms: immutable plus UNKNOWN/CONFLICT by default plus configurable high-authority threshold.
- Sensitive-token scanner freezes by default, including metadata.
- Serialized capsule byte budget is exact canonical UTF-8 bytes.
- Loss is deterministic integer ppm.
- Metadata is recursively frozen; non-string keys and floats are rejected to avoid mutable/cross-language canonicality ambiguity.

## Failure / repair history
1. Test run 1: 21/22 passed. `test_rehydrate_roundtrip` errored because the test attempted to hash a dataclass containing dict metadata. Root cause was test strategy. Fixed by deterministic tuple comparison and reran full suite successfully.
2. Initial benchmark: 250 atoms median ~1.24 s; 1000 atoms exceeded 45 s. Root cause was repeated full ledger construction + full capsule serialization per candidate, near O(n²). Replaced with precomputed cost/importance, exact scalar size accounting, Fraction ranking, single final ledger construction.
3. Post-repair benchmark: sub-second through 5000 synthetic atoms in this container.
4. Integrity hardening: deep-freeze metadata, scan metadata for secret patterns, verify result metrics, strict nested unknown-field checks.

## Final local verification
- compileall: PASS
- unittest: PASS, 29 tests
- CLI compact -> verify: PASS
- randomized invariant suite: PASS
- benchmark artifacts captured

## Publication verification
- First complete publication PR: #56
- Merge commit: f81c711b45e4f50ac5cbffd5103d57799e53d251
- Remote branch verified: main
- Remote file count: 30 files
- Source, tests, evidence, examples, tools, and top-level design files were re-listed from GitHub after merge.
- Remote blob identities match the prepared final subtree for all 30 files.
- No repository whose name contains NEXY.AI was mutated.

## Remaining action
None for the standalone LBCC deliverable. Actual NEXY.AI integration remains intentionally out of scope and NOT_VERIFIED.
