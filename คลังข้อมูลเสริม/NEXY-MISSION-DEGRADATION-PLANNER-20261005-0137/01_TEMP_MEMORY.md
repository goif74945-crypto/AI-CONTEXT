# Temporary Working Memory — NMDP

work_id: NMDP-CHAT-SURROGATE-20261005T0137+07-01
status: TEMPORARY_CHECKPOINT
truth_class: REPO_WORK_STATE

## Locked decisions
- Project name: NEXY Mission Degradation Planner (NMDP).
- Artifact is AI-PROPOSED and NON-AUTHORITATIVE.
- It must be integration-ready but not integrated into NEXY.AI.
- Reference implementation language: Python 3 standard library only.
- Public result states: FULL, DEGRADED, FREEZE.
- Mandatory objective policy:
  - MUST cannot be dropped.
  - SHOULD/Could may be omitted only with explicit reason in result.
- Evidence is modeled as integer E0..E7, matching AI-CONTEXT evidence classes.
- Alternatives are filtered before scoring by capability availability, minimum evidence, and side-effect ceiling.
- Selection ordering must be deterministic with stable alternative_id tie-break.

## Core algorithm draft
For each objective:
1. validate objective and candidate alternatives;
2. filter candidates that violate hard policy;
3. compute deterministic utility for each feasible candidate;
4. select best candidate using score then lexical id;
5. if no candidate:
   - MUST => FREEZE;
   - SHOULD/COULD => record dropped objective;
6. after all objectives:
   - no drops/substitutions => FULL;
   - all MUST met but optional work changed/dropped => DEGRADED;
   - any MUST unmet => FREEZE.

## Utility model draft
score = quality*100 + evidence_level*10 - side_effect_cost*20 - degraded_capability_penalty

The exact formula is implementation detail and may be adjusted before freeze, but output determinism and hard constraints are immutable.

## Risks
- accidental overlap with existing resilience/degradation labs;
- overclaiming NEXY compatibility without real integration;
- tests run on local bytes but repository content later differs;
- hidden nondeterminism from unordered collections.

## Mitigations
- narrow focus to mission-value preservation under partial capability loss;
- label all integration material AI-PROPOSED;
- hash local tested files and compare with repository-fetched content;
- canonical sorting everywhere.

## Next action
Implement package + tests locally, execute until passing, then upload exact tested bytes and verify GitHub content identity.
