# Gap Analysis and Provenance

Status: SOURCE-GROUNDED ANALYSIS + AI-PROPOSED GAP

## Source facts used

AI-CONTEXT records NEXY as a deterministic control/orchestration hub where models are workers rather than final authority, and where a legal verified output is released or the system freezes. The current source-normalization denominator is 837 normalized requirement rows; the historical 215-entry registry is deprecated for current enumeration.

The human/control deep context describes CIRL as resolving explicit intent without inventing missing material facts, exposes `USER_INTENT_TRACK`, and states that dangerous actions require an explicit confirmation/authority path. DOC-C defines a Directive contract, `AMBIGUOUS_INPUT`, runtime validation boundaries, release policy, FSM, idempotency, and freeze behavior.

Read-only implementation inspection observed:
- `packages/intelligence/cirl.ts`: explicit-marker intent resolution; missing/conflicting intent remains unresolved rather than guessed.
- `packages/intelligence/cle.ts`: validates CIRL objects and compiles explicit constraint laws; unresolved/unsupported authority fails closed.
- `packages/contracts/directive.ts`: structured CreateDirective request with constraints and metadata.
- `tests/contract/intelligence-layer-contract.test.ts`: negative tests for ambiguity, malformed inputs, uncertainty propagation, and explicit constraints.
- Search evidence showed canonical request hashing/idempotency and a prompt-law boundary in current implementation sources.

Existing supplemental work also already contains an Execution Transaction Model with authorization, pre-state, side effects, idempotency, reversibility, compensation, and postcondition verification.

## Gap hypothesis

**AI-PROPOSED HYPOTHESIS:** these controls still leave a distinct cross-representation question:

> When representation A and representation B are intentionally not byte-identical, what proves that B did not silently alter the authorized semantics of A?

Examples include:
- `read project A` becoming `read project A and repo B`;
- `do not touch NEXY.AI-` disappearing from downstream scope exclusions;
- a read-only action acquiring a write side effect;
- a HIGH-impact operation becoming LOW-impact without a risk re-evaluation reference;
- ambiguity becoming RESOLVED without a user clarification reference;
- a target identifier changing while the action label stays the same.

A canonical request hash is excellent for replay/idempotency identity of a particular payload. It is not a semantic-equivalence proof across two intentionally transformed payloads.

## Non-claim

This file does **not** claim the current NEXY implementation is vulnerable to these transitions. No end-to-end defect reproduction was performed. The lab is a defensive design proposal and evaluation surface.
