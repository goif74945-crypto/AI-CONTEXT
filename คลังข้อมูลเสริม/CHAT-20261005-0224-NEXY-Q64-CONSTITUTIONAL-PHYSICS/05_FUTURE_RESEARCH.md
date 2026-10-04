# Future Research — AI-Proposed, Not Canon

These are deliberately unimplemented research directions. They require separate authority and evidence.

1. **Interval-Q64 backend for DRC**: support nonlinear monotone transforms and certified interval propagation without floating point.
2. **SMT witness backend**: generate a concrete perturbation counterexample when DRC freezes, allowing a verifier to inspect the exact decision-flip witness.
3. **Sparse accumulator VBR**: O(d) atomic reservation checks using per-dimension committed/reserved counters plus monotonic reservation epochs.
4. **Evidence-backed RHL calibration**: learn decay parameters only from signed operational recovery observations while retaining an explicit conservative policy floor.
5. **Consequence ontology for EDB**: versioned consequence IDs with transformation proofs so UI previews and executable plans share the same semantic schema.
6. **Q64 differential oracle**: compare Python reference arithmetic against a second implementation (Rust/C with checked 128-bit intermediates or big-int oracle) over boundary/property vectors.
7. **Proof-carrying quantitative envelope**: bundle raw Q64 inputs, policy digest, output, and compact reproducibility witness for NEXY::JUDGE review.

None of these items should be implemented inside NEXY merely because they appear here.
