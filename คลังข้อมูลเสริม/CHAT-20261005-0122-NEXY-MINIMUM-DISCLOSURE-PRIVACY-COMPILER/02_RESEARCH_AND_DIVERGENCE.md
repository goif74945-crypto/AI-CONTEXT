# Research and Divergence Record

## SOURCE_FACT — NEXY grounding
Current NEXY context describes a deterministic AI control hub where user authority, verification, freeze-on-material-ambiguity, server-side secrets, private-by-default direction, and minimal user-facing complexity are design principles. The current normalized source matrix has 837 requirement rows, but this lab is not part of that matrix and does not claim current-build authority.

AI-CONTEXT security law also requires data minimization: external models/services should receive only the minimum context required, and credentials/secrets must not be persisted into context artifacts.

## EXTERNAL_FACT — non-governing research support
NIST's Privacy Framework is a voluntary tool for identifying/managing privacy risk, and NIST frames privacy risk across the lifecycle of data actions from collection through disposal. NIST AI RMF materials list privacy-enhancement among AI trustworthiness characteristics and note that data-minimizing methods such as de-identification/aggregation can support privacy-enhanced AI systems.

References:
- https://www.nist.gov/privacy-framework
- https://www.nist.gov/privacy-framework/getting-started-0
- https://www.nist.gov/itl/ai-risk-management-framework
- https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/

These references inform research framing only. They do not change NEXY authority.

## Divergence scan
Existing supplemental work already covers generic agentic security/trust boundaries, evidence architecture, reliability, failure taxonomies, counterfactual verification/impact, proof debt, causal debugging, compatibility evolution, knowledge decay, capacity economics, experience compilation, and human authority/interaction integrity.

NMDPC intentionally targets a narrower but actionable gap:

> Before NEXY sends task context to a model/processor, deterministically compute the minimum necessary disclosure bundle and fail closed on unresolved purpose/recipient/sensitivity/consent conditions.

## Hypotheses requiring future product experiments
- H1: a deterministic disclosure preflight can reduce accidental data over-sharing without materially increasing task abandonment.
- H2: showing a compact privacy receipt for high-sensitivity tasks can improve user trust without exposing internal system complexity.
- H3: brokered credentials plus recipient-scoped context bundles reduce blast radius compared with constructing one large shared prompt/context.

All three are HYPOTHESIS, not current product facts.
