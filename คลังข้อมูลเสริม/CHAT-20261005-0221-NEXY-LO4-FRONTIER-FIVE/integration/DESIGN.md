# Frontier Five Integration Gate

The integration gate is intentionally conservative:

- CAWT != PASS → `COUNTERFACTUAL_AUTHORITY_RISK`
- EDEL != PASS → `EVIDENCE_DEBT_PRESENT`
- CCF != PASS → `CAPABILITY_COMPOSITION_RISK`
- DRCDO != PASS → `REPLAY_DIVERGENCE`
- SIMF falsifications/survivors are advisories because the miner has no Canon authority.

Any blocker → FREEZE.

Even when all blockers are clear, output carries:
- `Lo4_AI_PROPOSAL_ONLY`
- `CANON_PROMOTION_REQUIRES_FORMAL_AUTHORITY`

This prevents a local prototype PASS from becoming an accidental architecture promotion.
