# C4 — Behavioral Fingerprint Kernel (BFK)

**Classification:** PROPOSAL / standalone prototype

## Problem
Source diffs are a poor proxy for behavior. Large refactors may preserve behavior while one-line changes alter a critical result. BFK fingerprints canonical scenario→outcome records so compatibility review focuses on observed semantics.

## Contract
Each `ScenarioRecord` contains:
- stable scenario ID;
- canonical input payload;
- outcome status;
- canonical output payload;
- ordered side-effect labels.

BFK produces per-scenario SHA-256 digests, one aggregate digest over sorted scenario IDs, and added/removed/changed/unchanged diffs.

## Canonicality law
Allowed primitives: null, string, integer, boolean, mappings with string keys, ordered sequences. Floats are rejected because cross-runtime serialization/rounding can create accidental drift. Production use should specify a decimal/rational canonical form.

## Failure model
Duplicate or empty scenario IDs, empty status, unsupported payload types, and floats -> explicit error.

## Integration proposal
Use in compatibility/regression workflows. Scenario corpus remains authority-controlled. BFK identifies which behavior changed; it does not decide whether the change is allowed.

## Tests
Mapping-key canonicalization; exact semantic diff; scenario-order stability; duplicate ID rejection; float rejection; all 24 permutations of four scenarios produce one aggregate digest.

## Trade-offs
Strength: compact deterministic semantic-drift signal.  
Risk: strength is limited by scenario corpus coverage.  
Mitigation: pair with coverage contracts and never equate unchanged fingerprint with universal equivalence.
