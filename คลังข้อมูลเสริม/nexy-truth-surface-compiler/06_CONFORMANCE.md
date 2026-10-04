# Cross-Implementation Conformance Contract

## Classification
**AI-PROPOSED / EXPERIMENTAL / ADVISORY ONLY**

The long-term value of a truth-surface boundary depends on different implementations agreeing on semantics. A TypeScript or Rust port must not turn the same input into a different RELEASE/FREEZE decision merely because JSON iteration order or library behavior differs.

## Required conformance dimensions
A conforming implementation must reproduce, for every golden vector:
- the same normalized-input SHA-256;
- the same decision;
- the same freeze reason codes and ordering;
- the same visibility filtering;
- the same public evidence reference ordering;
- the same canonical capsule structure;
- the same output SHA-256.

## Current golden fixtures
- `fixtures/release.json`
- `fixtures/freeze-unknown.json`
- `fixtures/freeze-conflict.json`
- generated contract: `fixtures/golden-vectors.json`

The generator is `tools/generate_golden_vectors.py`. A port must consume the checked-in golden vectors rather than silently regenerating them to match itself.

## Evolution rule
Any intentional semantic change requires:
1. version increment;
2. explicit rationale;
3. new/updated golden vectors;
4. migration note describing which outputs change and why;
5. compatibility review before replacing an older version.
