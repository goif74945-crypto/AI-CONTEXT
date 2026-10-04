# Cross-Language Conformance Protocol — PROPOSAL ONLY

The Python compiler is an executable reference, not authority. Any future TypeScript/Rust implementation must replay `conformance/cases.json` and produce the exact structured output, including `capsule_id`, input commitment, reason codes, evidence selection, coverage, dissent and cost.

Locked scenarios: basic PASS; equal-authority material conflict -> FREEZE; stronger PASS with weaker FAIL -> PASS + dissent; stale evidence -> FREEZE; item-budget overflow -> FREEZE; multi-claim deterministic cover -> PASS.

A production promotion must additionally lock Unicode normalization, timestamp canonicalization, numeric domain and JSON canonicalization across languages. A mismatch is FAIL, not something to normalize away after the fact.
