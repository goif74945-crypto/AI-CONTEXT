# NEXY.AI Closed-Loop Control Plane

## Status

P4.1–P4.16 control-plane artifacts are materialized in AI-CONTEXT and pass the recorded structural/policy checks. This index does not claim that the separate NEXY implementation runs them, that a scheduler is live, or that deployment evidence exists.

## Components

1. [Command Model](./command/INDEX.md) — materialized; structural/policy checked.
2. [Command Queue](./queue/INDEX.md) — materialized; structural/policy checked.
3. [Worker Registry](./workers/INDEX.md) — materialized; structural/policy checked.
4. [Claim / Lease](./claims/INDEX.md) — materialized; structural/policy checked.
5. [Expected-HEAD Guard](./head-guard/INDEX.md) — materialized; structural/policy checked.
6. [Supersession](./supersession/INDEX.md) — materialized; structural/policy checked.
7. [Result Package](./results/INDEX.md) — materialized by canonical handoff reuse; structural/policy checked.
8. [Heartbeat](./heartbeat/INDEX.md) — materialized; structural/policy checked.
9. [Retry / Backoff](./retry/INDEX.md) — materialized; structural/policy checked.
10. Dead Letter / Quarantine — materialized; structural/policy checked.
11. Scheduler — materialized; structural/policy checked.
12. Evidence Ingestion — materialized; structural/policy checked.
13. Convergence — materialized; structural/policy checked.
14. Oscillation Detector — materialized; structural/policy checked.
15. Human Escalation — materialized; structural/policy checked.
16. Resume / Recovery — materialized; structural/policy checked.

## Authority boundary

This control plane coordinates work descriptions and evidence. It cannot bypass governance, human gates, secrets policy, or NEXY implementation write authorization. “Materialized” means the AI-CONTEXT artifacts and their recorded structural/policy checks exist; it does not mean runtime execution or production deployment is verified.
