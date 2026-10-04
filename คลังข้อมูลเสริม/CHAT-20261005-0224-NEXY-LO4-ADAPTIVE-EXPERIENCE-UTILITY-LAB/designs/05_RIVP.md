# RIVP — Reversible Information-Value Pilot Planner

**Status:** `Lo4_AI_PROPOSAL_ONLY / NON_GOVERNING`

## Problem
After selecting an interesting idea, the next best step may be a bounded experiment rather than adoption. A pilot should buy information while preserving rollback and a control holdout.

## Allowed effects
Only:
- `VIEW_ONLY`;
- `REVERSIBLE_STATE`.

Irreversible effects fail contract construction.

## Option-value model
All terms are Q64.64:

`option_value = information_gain * rollback_confidence - risk_weight*risk - blast_weight*blast_radius - cost_weight*pilot_cost`

Hard gates independently constrain:
- minimum information gain;
- maximum risk;
- maximum blast radius;
- minimum rollback confidence;
- maximum sample budget;
- minimum option value;
- maximum treatment fraction.

## Treatment/control allocation
A conservative treatment fraction is derived from information gain divided by `1 + risk + blast + pilot_cost`, capped by policy. At least one control sample is mandatory.

## Output
- `PLAN`: includes treatment/control budgets, rollback procedure ID and stop-rule ID;
- `HOLD`: economic information option too weak;
- `REJECT`: safety/reversibility/budget gate failed.

## Non-goals
RIVP does not run the experiment, approve user exposure, produce consent, or promote successful pilots into Canon.
