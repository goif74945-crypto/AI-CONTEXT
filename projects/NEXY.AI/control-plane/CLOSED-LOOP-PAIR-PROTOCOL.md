# NEXY Closed-Loop Auditor ↔ Builder Pair Protocol

## Identity
- PAIR_ID: `NEXY-CLOSED-LOOP-01`
- Builder: `BUILDER-01`
- Auditor: the active audit chat operating under the user's current authority
- Control/knowledge repository: `goif74945-crypto/AI-CONTEXT`
- Implementation repository: `goif74945-crypto/NEXY.AI-`

## Purpose
Run a deterministic repair loop where the Builder only executes verified Auditor commands and the Auditor independently verifies Builder evidence. When the Builder is still working and no Auditor action is required, the Auditor uses the idle interval to materialize NEXY Skills in AI-CONTEXT.

## Non-background truth
This protocol does not authorize claims of hidden or asynchronous execution. Each chat/session invocation must refresh canonical state from Git before acting. If no tool invocation/session is running, no work is claimed to be running.

## Canonical live state
- `projects/NEXY.AI/control-plane/live/queue.json`
- `projects/NEXY.AI/control-plane/live/workers.json`
- `projects/NEXY.AI/control-plane/live/claims.json`
- `projects/NEXY.AI/control-plane/live/pair-state.json`
- command instances: `projects/NEXY.AI/control-plane/live/commands/<COMMAND_ID>.json`
- Auditor→Builder handoffs: `projects/NEXY.AI/control-plane/live/handoffs/<HANDOFF_ID>.json`
- Builder→Auditor result packages: `projects/NEXY.AI/control-plane/live/results/<HANDOFF_ID>.json`

Schemas/policies under `projects/NEXY.AI/control-plane/` and `projects/NEXY.AI/handoff/` remain authoritative for structure and semantics. Live files do not expand mutation authority.

## Auditor loop
1. Refresh `AI-CONTEXT/main`.
2. Read live pair state, queue, workers, claims, latest command/handoff/result.
3. If Builder has a valid ACTIVE claim and no returned result:
   - inspect any newly persisted heartbeat/checkpoint/evidence;
   - do not invent progress;
   - if no immediate blocker is proven, enter **IDLE_SKILL_FORGE**.
4. IDLE_SKILL_FORGE:
   - build the next NEXY Skill strictly from `skills/nexy/MASTER-SPECIFICATION.md` and its authoritative sources;
   - write only to AI-CONTEXT unless a separate implementation command authorizes NEXY.AI- mutation;
   - mark new Skills MATERIALIZED until required behavior/security/integration/evidence gates are actually executed;
   - suspend skill-forge work immediately when a Builder result or critical control-plane change is observed.
5. If Builder returns a `BUILDER_TO_AUDITOR` package:
   - pin START_HEAD/END_HEAD and current branch HEAD;
   - validate package schema/freshness;
   - inspect changed files/diff;
   - verify scope, acceptance, required tests, negative tests, regression, security and evidence class;
   - re-run or independently verify applicable checks where tooling permits.
6. Verdict:
   - PASS with sufficient evidence → Auditor may ACCEPT/COMPLETE the command and release the claim according to policy.
   - FAIL/PARTIAL/NOT_VERIFIED caused by a proven correctable implementation defect → create a new schema-valid command + AUDITOR_TO_BUILDER handoff, usually superseding the prior command, enqueue READY only when dependencies and exact-head preconditions are satisfied.
   - STALE → do not execute old command; revalidate semantic change impact and issue a superseding command or block.
   - AUTHORITY/SECURITY/HUMAN-GATE conflict → BLOCK/FREEZE; never workaround.
7. Refresh queue and repeat on the next active invocation.

## Command-authoring law
A repair command is created only from a proven Auditor finding. It MUST include:
- exact `target_repo`, `target_branch`, `created_from_head`, `expected_head`;
- finding IDs and proof;
- exact allowed/forbidden change surfaces;
- objective and acceptance;
- required, negative, regression and security tests;
- rollback and expected evidence;
- stale and retry policy;
- supersession lineage.

No defect may be invented merely to keep the Builder busy.

## Communication policy
Routine progress, idle skill creation and normal cross-chat handoffs are persisted in AI-CONTEXT rather than narrated to the user. User-visible interruption is reserved for a genuinely required human gate, an unrecoverable authority conflict, missing authorization that cannot be resolved from canonical state, or another blocker that requires the user's decision.

## Priority
When both exist:
1. safety / human gate
2. returned Builder result requiring audit
3. active command integrity / stale-head / lease collision
4. Auditor command generation for proven failed verification
5. NEXY Skill materialization during idle wait

Skill creation must never delay verification of a Builder result.

## Status semantics
- `WAITING_FOR_BUILDER`: Builder has work; Auditor has no immediate intervention.
- `AUDITING_RESULT`: Builder returned evidence; Auditor is verifying.
- `COMMAND_REQUIRED`: audit proved a correctable defect and a new command must be issued.
- `IDLE_SKILL_FORGE`: no immediate Builder action is required; Auditor may build NEXY Skills.
- `HUMAN_GATE`: user decision/authorization required.
- `CLOSED`: no READY/VERIFYING work remains and current objective is accepted.

## Evidence rule
Cross-chat statements are not proof by themselves. Every material claim must resolve to current repository/runtime/source evidence. Examples and fixtures are never promoted to live control state.
