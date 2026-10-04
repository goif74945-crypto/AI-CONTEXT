# Design — Artifact Referential Integrity Guard (ARIG)

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Objective
Prevent release evidence from becoming a decorative pile of files whose references are broken, hashes are stale, or artifacts are unreachable from requirements.

## NEXY value
Evidence-first systems need graph integrity, not just file presence. ARIG validates a compact manifest connecting requirements, tests, evidence, and other artifacts.

## Core contract
- Node fields: stable `id`, `kind`, list of `refs`, optional `sha256`.
- Detect duplicate/empty IDs.
- Detect missing references.
- Verify supplied blob content against declared SHA-256.
- Detect reference cycles.
- Compute reachability from `requirement` roots.
- Report orphan nodes deterministically.
- Empty manifest -> `NOT_VERIFIED`.
- Errors -> `FAIL`; only orphan warnings -> `PARTIAL`; clean graph -> `PASS`.

## Failure semantics
A missing blob for a declared hash is an error, not an assumed match. A hash mismatch is `STALE_HASH`. The engine never repairs references automatically because silent repair would change proof semantics.

## Complexity
Reference validation and reachability are O(V+E), plus O(total hashed content).
