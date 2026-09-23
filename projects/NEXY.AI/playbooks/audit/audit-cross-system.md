# PLAYBOOK — Audit Cross-System Behavior

## PURPOSE
Find defects that are invisible when modules are audited in isolation.

## PROCEDURE
1. Select target workflow/use case.
2. Build traversal from dependency graph.
3. Resolve every crossing contract.
4. Resolve authority changes across the path.
5. Trace state/data/event provenance end-to-end.
6. Trace errors/timeouts/freeze behavior end-to-end.
7. Trace idempotency/retry/recovery across boundaries.
8. Trace observability correlation IDs/incidents.
9. Check one layer cannot mask another layer's failure.
10. Check config/timeout budgets are mutually compatible.
11. Execute integration/E2E/fault tests at critical boundaries.
12. Compare final result with release/UI truth law.

## NEXY CRITICAL CHAINS
Examples:
- UI → API → AUTH → CORE → LAW → SWARM → JUDGE → release → VAULT/OBS.
- Directive → Queue → Worker → CORE → incident/recovery.
- Artifact → Revision → Commit → audit.
- Lo3 verified result → Lo2 intake (future architecture).
- Game shard → transfer → sovereign/economic state (future architecture).
- Robotics perception → decision → control → Safety Kernel (physical/future).

## RED FLAGS
- every module passes individually but schema/version mismatch breaks chain;
- timeout in upstream shorter than required downstream deadline;
- incident ID lost across queue;
- retry duplicates downstream write;
- UI exposes result before release;
- authority increases crossing a boundary;
- recovery resumes with stale context.

## PASS
Requires integration-level or higher evidence for cross-system claims.
