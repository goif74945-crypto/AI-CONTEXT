# Collision / Novelty Audit

Status: **PASS_BOUNDED — repository-observed collision review, not proof of universal uniqueness.**

## Why this audit exists
A new filename is not innovation. The selected systems were required to differ from earlier supplemental labs by input contract, state transition, failure semantics, and evidence question rather than branding.

## Observed competing domains deliberately excluded
Recent AI-CONTEXT work already covered, among other themes:
- evidence freshness / invalidation;
- assumption planning;
- authority delegation and scoped authority leases;
- proof/evidence capsules and selective disclosure;
- semantic drift;
- counterfactual verification;
- resource allocation / resource governor;
- admission control and capacity economics;
- self-calibration, failure minimization, pause/resume safety, evidence genealogy;
- outcome closure, progress truth, reversible probe planning, benefit regression, adoption readiness;
- metamorphic verification, decision stability, assurance distillation, live-interaction integrity, and correlated consensus.

Those areas are not reimplemented here.

## Targeted negative searches
Repository commit search returned no matching prior commit messages for the exact concepts/phrases used to select this lab, including:
`deadlock`, `livelock`, `retry storm`, `retry budget`, `poison task`, `poison message`, `quarantine task`, `partial result`, `result salvage`, `salvage compiler`, `progress signature`, `thrash detector`, `stalled progress`, `wait-for graph`, `dependency cycle`, and `workflow cycle`.

A separate search did find prior work for `admission control` and `resource governor`; therefore this lab intentionally avoids generic capacity allocation and instead owns runtime failure topology.

## Distinctness matrix

| New system | Primary input | Primary state/output | Failure question | Why materially distinct |
|---|---|---|---|---|
| Deadlock Sentinel | wait-for edges | `CLEAR / DEADLOCK` + SCC cycles | Are actors structurally waiting in a cycle? | Not scheduling optimization, interleaving enumeration, or generic resource budgeting. |
| Livelock/Thrash Detector | ordered progress samples | `PROGRESSING / STALLED / LIVELOCK / FREEZE` | Is work changing state repeatedly without increasing declared progress? | Not deterministic replay or pause/resume safety; it analyzes no-progress cycle topology. |
| Retry Storm Governor | ordered attempt history + retry policy | retry/stop/quarantine/freeze decision | Is another retry legally and operationally bounded? | Does not allocate workers or plan admission; it preserves retryability/idempotency history. |
| Poison Task Quarantine | repeated task-run outcomes | `CLEAR / QUARANTINE` + revision-scoped key | Is the same input failing the same way on the same executor revision repeatedly? | Separates poison input/revision identity from global provider health or circuit breakers. |
| Partial-Result Salvage Compiler | result DAG | dependency-closed safe subset | Which already-proven outputs can survive a terminal failure? | It does not declare outcome closure and cannot mint task completion. |

## Limitation
GitHub commit search is not an exhaustive semantic index of every repository byte, and concurrent chats may add new work after this audit. Therefore the accurate claim is: **no direct collision was found in the inspected recent work and exact targeted searches at audit time.**
