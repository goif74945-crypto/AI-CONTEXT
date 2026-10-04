# MCAE — Multimodal Claim Arbitration Engine

**Status:** AI_PROPOSAL / NON_GOVERNING

## Objective
Prevent NEXY from silently collapsing contradictory text/image/audio/tool/model claims into one confident answer. The engine converts heterogeneous observations into typed claims and applies deterministic authority/score rules.

## Non-goals
No OCR, speech recognition, image understanding, truth discovery, or semantic model inference. Upstream adapters must already emit normalized propositions/values.

## Contract
Input claim fields: `claim_id`, `proposition`, `value`, `modality`, `source_id`, `source_tier`, `confidence`.

Source tiers are explicit policy labels: `authoritative > verified > observed > generated`.

## Invariants
1. Claims about different propositions are never mixed.
2. Invalid confidence/tier freezes evaluation.
3. Repeated claims from the same source/proposition are deduplicated to the strongest observation so one source cannot manufacture consensus by repetition.
4. If the highest authority tier contains different values, status is `CONFLICT` regardless of lower-tier votes.
5. A winner requires configured minimum score and minimum margin; otherwise `FREEZE`.
6. Output includes supporting claim IDs and score map; no hidden reasoning is required.

## Failure semantics
Malformed input → `FREEZE`; top-tier disagreement → `CONFLICT`; insufficient support/margin → `FREEZE`; established winner → `ALLOW`.

## Integration boundary
Place after modality-specific extraction/normalization and before a high-impact decision or user-visible assertion. Existing NEXY authority/JUDGE policy remains superior.

## Verification target
E2 unit evidence for consensus, same-source deduplication, top-tier conflict, weak-margin freeze, and malformed confidence.
