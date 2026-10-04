# Future System Concepts

**All items below are AI-PROPOSED CONCEPTS, not NEXY requirements.**

## P-01 Protected Terminology Registry
Versioned registry of canonical state names, command strings, role labels, identifiers, and legal phrases, with ownership and localization policy per term.

## P-02 Translation Provenance Seal
Bind source text hash, source locale, target text hash, target locale, translator identity/tool class, glossary version, and integrity-policy version into a verifiable record.

## P-03 Structured Message First
Replace high-risk prose generation with typed message objects such as `{code, state, actor, amount, unit, action}` and localize only presentation templates. This reduces semantic attack surface.

## P-04 Semantic Diff UI
Human review surface that highlights only invariant-affecting differences: modality, negation, quantities, protected terms, identifiers, and missing placeholders.

## P-05 Locale Capability Lattice
Each language pair declares which semantic protections are PROVEN, PARTIAL, or UNSUPPORTED. Unsupported classes freeze instead of inheriting confidence from another pair.

## P-06 Dual-Path Review for High-Risk Copy
For destructive/recovery/security actions, require deterministic invariant PASS plus an independent human-language review before release.

## P-07 Unicode Security Normalizer
Detect bidi overrides, confusables, zero-width characters, homoglyphs, and normalization traps in protected terms and identifiers.

## P-08 Numeric Equivalence Contract
Allow explicitly authorized numeric formatting equivalence (`1,000` ↔ `1000`) without permitting value changes. Separate display normalization from quantity meaning.

## P-09 Unit Conversion Contract
Permit conversions such as `1000 ms` ↔ `1 s` only when an exact, policy-authorized conversion proves equality. The current lab deliberately rejects such conversions.

## P-10 Localization Regression Ledger
Every discovered translation-semantic incident becomes a permanent fixture with source/target, invariant violated, root cause, expected decision, and policy revision.

## P-11 Accessibility Semantic Parity
Apply the same integrity law to visible labels, ARIA text, screen-reader copy, keyboard command descriptions, and mobile condensed states.

## P-12 Release-Critical Copy Compiler
Compile authoritative message definitions into locale bundles while checking missing keys, unexpected keys, placeholder compatibility, protected literals, and semantic-class constraints before packaging.

## P-13 Language-Pack Attestation
Treat a locale bundle like a release artifact with content hash, policy hash, source revision, test evidence, and rollback target.

## P-14 Mixed-Language Boundary Detector
Detect when canonical control tokens are embedded in localized prose and verify that surrounding grammar cannot invert their operational meaning.

## P-15 Human Feedback Without Authority Drift
Allow users to report awkward or unclear translations, but route suggestions through proposal/review rather than silently changing authoritative copy.
