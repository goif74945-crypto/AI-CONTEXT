# SCARM-20 NEXY Integration Contract

## Purpose
Define how a future NEXY/EPC adapter could consume SCARM without granting SCARM authority it does not have.

## Inputs
- immutable candidate snapshots;
- normalized semantic atoms with provenance;
- revision lineage;
- explicit logical ticks;
- explicit provenance clusters where identity-sensitive checks are requested;
- external KEEP/CUT entitlement snapshot;
- evidence stance and dossier inclusion records;
- ranking snapshots produced by the authoritative evaluation path.

## Outputs
- one `Finding` per mechanism with `CLEAR | FLAGGED | UNKNOWN`;
- Q64.64 risk metric where quantitative;
- hard/soft review classification;
- `MANIPGATE64` disposition: `ALLOW_REVIEW | DEFER_REVIEW | BLOCK_REVIEW`.

## Forbidden output semantics
SCARM output must never be interpreted as:
- JUDGE verdict;
- LAW authorization;
- Core state transition;
- KEEP or CUT vote;
- Canon promotion;
- physical deletion instruction;
- proof of hidden identity or collusion intent.

## Recommended adapter placement
`EPC evidence normalization -> SCARM advisory checks -> dossier attachment -> existing verification/JUDGE/LAW/Core path`

The adapter should attach exact input hashes and SCARM version/commit to the dossier. It should not call SCARM from a path that can directly mutate NEXY state.

## Fail-closed rules
- Missing explicit provenance for provenance-sensitive checks -> UNKNOWN.
- Missing required mechanism finding before MANIPGATE64 -> DEFER_REVIEW.
- Hard finding -> BLOCK_REVIEW, not automatic rejection/CUT.
- Q64 overflow/divide-by-zero -> execution failure requiring freeze/defer at the adapter boundary.
- Target NEXY commit drift -> stale compatibility evidence; re-inspection required.

## Compatibility evidence used for this design
Read-only NEXY head inspected: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
Relevant observed surfaces:
- `packages/phase-f/lo3/governor.ts`: checked bigint Q64.64 proposal-governance arithmetic.
- `packages/core/vnext-state-matrix.ts`: JUDGE owns verified/accepted/rejected; SWARM owns agents_done.
- `packages/human/dialog-sandbox.ts`: no direct Core mutation authority.
- `packages/phase-f/game/numeric-law.ts`: confirms Q64.64 usage while also demonstrating that overflow policy is scope-specific, so SCARM does not claim a global policy rewrite.
