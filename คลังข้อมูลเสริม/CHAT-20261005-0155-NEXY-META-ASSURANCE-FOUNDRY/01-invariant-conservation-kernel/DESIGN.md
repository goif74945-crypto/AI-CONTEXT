# Design — Invariant Conservation Kernel (ICK)

Classification: `AI_PROPOSED_CONCEPT / REFERENCE_IMPLEMENTATION`

## Problem
Complex AI/tool pipelines can accidentally create semantic privilege: authority rises because a later stage says so, uncertainty disappears without evidence, constraints vanish during rewriting, or capabilities widen after a transformation. Provenance tracking alone does not prove that protected semantic quantities were conserved.

## Core law
For every adjacent pipeline transition, certain properties are monotonic unless an explicit typed receipt authorizes the exception.

### Conserved / monotonic dimensions
- **Authority** may not increase without an authority grant receipt.
- **Evidence level** may not increase without evidence references.
- **Unknowns** may not disappear unless each removed unknown is explicitly resolved.
- **Constraints** may not disappear unless each removed constraint is explicitly waived.
- **Capabilities** may not grow unless each added capability is explicitly granted.
- **Declared side effects** must remain a subset of current capabilities.

Strengthening constraints, adding unknowns, dropping capabilities, or reducing authority/evidence is allowed because those changes do not silently widen power or certainty.

## Verdict
- `PASS`: every conservation law is satisfied.
- `FREEZE`: one or more laws are violated.

The output contains stable reason codes and a SHA-256 fingerprint of normalized input state.

## Integration proposal
Possible placement: between any two NEXY-compatible transformation stages that mutate a structured decision envelope. ICK must remain subordinate to NEXY LAW/CORE/JUDGE and cannot itself create authority.

## Non-goals
- provenance lineage validation;
- signature/cryptographic receipt verification;
- deciding whether a grant/waiver is authorized by real NEXY law;
- executing side effects;
- production integration.
