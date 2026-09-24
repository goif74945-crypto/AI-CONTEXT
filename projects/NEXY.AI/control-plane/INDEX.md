# NEXY.AI Closed-Loop Control Plane

## Status
Foundation under construction in dependency order. Each component is versioned, schema-bound, evidence-aware and does not grant authority over NEXY implementation.

## Components
1. [Command Model](./command/INDEX.md) — implemented.
2. [Command Queue](./queue/INDEX.md) — implemented.
3. [Worker Registry](./workers/INDEX.md) — implemented.
4. [Claim / Lease](./claims/INDEX.md) — implemented.
5. [Expected-HEAD Guard](./head-guard/INDEX.md) — implemented.
6. [Supersession](./supersession/INDEX.md) — implemented.
7. [Result Package](./results/INDEX.md) — implemented by canonical handoff reuse.
8. [Heartbeat](./heartbeat/INDEX.md) — implemented.
9. [Retry / Backoff](./retry/INDEX.md) — implemented.
10. Dead Letter / Quarantine — pending P4.10.
11. Scheduler — pending P4.11.
12. Evidence Ingestion — pending P4.12.
13. Convergence — pending P4.13.
14. Oscillation Detector — pending P4.14.
15. Human Escalation — pending P4.15.
16. Resume / Recovery — pending P4.16.

## Authority boundary
This control plane coordinates work descriptions and evidence. It cannot bypass governance, human gates, secrets policy, or NEXY implementation write authorization.
