# UPA — Unknown Propagation Algebra

Status: `Lo4_AI_PROPOSAL_ONLY`

## Problem
Boolean pipelines often collapse missing or contradictory evidence into `false`, `null`, defaults or ad-hoc exceptions. That can launder uncertainty into apparently deterministic decisions.

## Mechanism
UPA uses four evidence states:
- TRUE = support present, refutation absent;
- FALSE = refutation present, support absent;
- UNKNOWN = neither established;
- CONFLICT = both support and refutation present.

The implementation uses a two-bit evidence representation and supplies NOT, AND, OR and knowledge-join operations while retaining provenance.

## Invariants
- only TRUE is `releaseable`;
- TRUE + FALSE via knowledge join becomes CONFLICT;
- UNKNOWN is not guessed into TRUE/FALSE without additional evidence;
- provenance survives composition.

## NEXY value
Makes zero-guess and conflict semantics executable data types rather than documentation conventions.
