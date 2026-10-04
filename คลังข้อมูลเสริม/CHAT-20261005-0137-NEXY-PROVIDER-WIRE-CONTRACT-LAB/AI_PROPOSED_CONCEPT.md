# AI-PROPOSED CONCEPT — NEXY Provider Wire Contract Lab

Status: **AI-PROPOSED CONCEPT — NOT CURRENT NEXY REQUIREMENT**

This lab proposes a deterministic provider-boundary protocol that converts provider-specific streaming output into a small canonical event language before any output is trusted by NEXY::CORE.

The concept is intentionally outside the NEXY.AI implementation repository. It is a standalone compatibility reference that may later be adopted, rejected, or revised by human/project authority.

## Why it exists
NEXY's documented direction includes hot-swapping external AI providers/models while keeping NEXY as the controlling authority. Capability negotiation and provider-substitution safety already exist as neighboring concepts in AI-CONTEXT. This lab targets a narrower unresolved layer: **wire-level event semantics**.

Equivalent-looking provider APIs can differ in streaming order, tool-call framing, error semantics, IDs, usage reporting, and termination behavior. Allowing those differences to leak directly into CORE creates accidental provider authority.

## Proposed invariant
**Provider-specific wire behavior stops at the adapter boundary. CORE receives only canonical, validated, replayable events or a freeze result.**
