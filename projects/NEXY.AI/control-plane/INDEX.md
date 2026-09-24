# NEXY.AI Closed-Loop Control Plane

## Status
All P4.1-P4.16 control-plane foundation components are present and structurally validated. Runtime orchestration is the next layer and remains NOT_VERIFIED until executable loop tests and an authorized worker adapter prove end-to-end behavior.

## Components
1. [Command Model](./command/INDEX.md) — structural PASS.
2. [Command Queue](./queue/INDEX.md) — structural PASS.
3. [Worker Registry](./workers/INDEX.md) — structural PASS.
4. [Claim / Lease](./claims/INDEX.md) — structural PASS.
5. [Expected-HEAD Guard](./head-guard/INDEX.md) — structural PASS.
6. [Supersession](./supersession/INDEX.md) — structural PASS.
7. [Result Package](./results/INDEX.md) — structural PASS via canonical handoff reuse.
8. [Heartbeat](./heartbeat/INDEX.md) — structural PASS.
9. [Retry / Backoff](./retry/INDEX.md) — structural PASS.
10. [Dead Letter / Quarantine](./dead-letter/INDEX.md) — structural PASS.
11. [Scheduler](./scheduler/INDEX.md) — structural PASS.
12. [Evidence Ingestion](./evidence-ingestion/INDEX.md) — structural PASS.
13. [Convergence](./convergence/INDEX.md) — structural PASS.
14. [Oscillation Detector](./oscillation/INDEX.md) — structural PASS.
15. [Human Escalation](./human-escalation/INDEX.md) — structural PASS.
16. [Resume / Recovery](./resume-recovery/INDEX.md) — structural PASS.

## Runtime layer
Runtime execution belongs under `runtime/` and must prove the closed loop:

`AUDIT → COMMAND → SCHEDULE → CLAIM → HEAD GUARD → EXECUTE → RESULT → EVIDENCE → RE-AUDIT → CONVERGENCE`

The runtime may coordinate authorized work, but it cannot grant implementation write authority, bypass human gates, accept stale evidence, or turn structural validation into runtime PASS.

## Authority boundary
This control plane coordinates work descriptions, claims, results, and evidence. It cannot bypass governance, human gates, secrets policy, or NEXY implementation write authorization.
