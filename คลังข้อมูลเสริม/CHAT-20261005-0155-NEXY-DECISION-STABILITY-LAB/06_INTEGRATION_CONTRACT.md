# NEXY Compatibility / Integration Contract

**Classification: AI-PROPOSED supplemental concept. No NEXY.AI repository mutation is authorized or performed by this lab.**

## Adapter boundary
A future adapter may provide:
- a deterministic NEXY decision oracle;
- evidence objects with stable identity/provenance;
- an explicit mapping from NEXY outcome states to the lab-local REJECT/FREEZE/RELEASE order;
- explicit evidence polarity for MONO;
- explicit declarations of irrelevant CONTEXT for IRIS.

## Forbidden adapter behavior
- Do not infer SUPPORT/BLOCK/CONTEXT from sentiment or model confidence.
- Do not classify unknown context as irrelevant.
- Do not treat MDE omission as authorization to delete source/audit evidence.
- Do not treat EDGE truncated=false beyond the exact finite universe/budget supplied.
- Do not delay a worsening safety decision through DAMP.
- Do not mutate NEXY law, policy, repository state, or runtime state from a lab result.
- Do not convert this reference Decision ordering into canonical NEXY law without explicit authority.

## Freeze rule
If outcome mapping, evidence polarity, identity, provenance, or state snapshot is ambiguous, the adapter must fail closed / FREEZE instead of guessing.

## Evidence boundary
Local E1/E2/E3 proof for this lab does not prove NEXY runtime integration, UI flow, provider behavior, production security, or deployment. Those remain NOT_VERIFIED until tested against the exact NEXY revision/environment.
