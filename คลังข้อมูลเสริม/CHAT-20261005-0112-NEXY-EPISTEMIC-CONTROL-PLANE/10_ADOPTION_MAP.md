# Adoption Map
VAULT: claim states, freshness, negative knowledge, replay packets.
JUDGE: epistemic transitions, counterfactual checks, correlation-aware evidence.
SWARM: independence vectors, anti-herding, leases.
RUN: lease enforcement and action-risk tiers.
VIEW/PULSE: expose STALE/CONTESTED/NOT_VERIFIED cleanly.
Potential sequence when authorized: contracts → read-only analyzers → judge integration → lease enforcement → replay harness → telemetry.
Non-goal: no current NEXY.AI implementation mutation.