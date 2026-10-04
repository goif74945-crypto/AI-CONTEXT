# AI-PROPOSED Future Concepts

> **EXPERIMENTAL / NOT CANON / NOT IMPLEMENTED unless explicitly marked otherwise**

These are future ideas proposed by AI. They are intentionally separated from NEXY canon and from verified project state.

## C1 — Evidence Lease

Attach an expiry condition to evidence rather than only a timestamp. A lease becomes stale when any bound authority file hash, relevant implementation commit, environment identity, or test contract changes. This could prevent “fresh-looking but invalid” proof reuse.

**Status:** CONCEPT ONLY.

## C2 — Authority Diff Compiler

Given two AI-CONTEXT revisions, classify changes as LAW, BUILD_SPEC, PRODUCT_DESIGN, EVIDENCE, HISTORY, or EXPERIMENTAL, then compute which downstream claims must be revalidated.

**Status:** CONCEPT ONLY.

## C3 — Claim-to-Proof Bipartite Graph

Represent claims and evidence artifacts as distinct node classes. Reject completion if a critical claim has no edge to evidence of the required E0–E7 class at the same revision/environment.

**Status:** CONCEPT ONLY.

## C4 — Context Quarantine

Unknown/untrusted imported content lands in a quarantine namespace. It cannot become canonical/project-state context until provenance, authority, conflict, and secret checks pass.

**Status:** CONCEPT ONLY.

## C5 — Determinism Replay Bundle

Persist a normalized input/state/policy fingerprint plus expected structural result so future engines can replay deterministic decisions and identify semantic drift without retaining private model reasoning.

**Status:** CONCEPT ONLY.

## Implemented seed

NEXY ProofGraph Lab v0.1 implements the smallest reusable foundation shared by C1–C3: hashing, link graph, impact closure, deterministic policy findings, and truth-lock verification.
