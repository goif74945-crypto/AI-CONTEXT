# NEXY.AI Integration Notes

STATUS: PROPOSAL ONLY / NOT INTEGRATED

## Principle
These systems should sit beside NEXY control flow as optional deterministic services. They must not become hidden authorities.

## Suggested interfaces
- CBO: NEXY::CORE or task router supplies candidate context records; CBO returns selected IDs + omitted reasons + freeze status.
- TER: NEXY::JUDGE or verification planner supplies required evidence/capabilities; TER returns a bounded tool route or FREEZE.
- RRD: post-incident/evaluation pipeline supplies verified failure episodes; RRD emits candidate recipes into a reviewable Vault area.
- SKC: successful execution ledger supplies traces; SKC emits candidate skill manifests that remain untrusted until explicitly admitted.
- ABP: pre-execution planner supplies ASSUMPTION/UNKNOWN objects; ABP returns validation probes that must run before protected mutation.

## Integration invariants
1. NEXY remains the authority; these modules only propose deterministic outputs.
2. Any module may return FREEZE rather than fabricate a route/recipe/skill/plan.
3. IDs and evidence references must be stable and auditable.
4. User Law and protected-scope rules dominate every optimization score.
5. Production adoption requires NEXY-specific E3/E4 evidence at an exact commit.

## Compatibility strategy
Each prototype accepts plain Python data structures and returns immutable-ish dataclass results. A later adapter can map them to NEXY TypeScript/Zod contracts without embedding model-specific behavior.
