# AI-Proposed Integration Boundary for NEXY

**Status: NON-GOVERNING PROPOSAL. Not current NEXY build scope.**

## Proposed placement
A future NPRG-like component would sit between an already-authorized TASK GRAPH node and AGENT/SWARM dispatch. It consumes a resource envelope from CORE and returns one allocation proposal or `FREEZE`.

It must not sit above LAW, CORE or JUDGE.

## Minimum production contracts before adoption
1. Signed/versioned resource-policy object.
2. Provenance + freshness on provider price, latency, clearance and capability metadata.
3. Stable provider independence-domain definition.
4. Explicit treatment of locally hosted/private models.
5. Revocation/quarantine feed integration.
6. Exact task-token estimation policy and bounded underestimation behavior.
7. Resource reservations so a selected plan cannot exceed budget through race conditions.
8. Idempotent plan identity tied to task revision + policy revision + agent inventory revision.
9. Audit record for candidate eliminations and final ranking.
10. Re-plan trigger model for stale metadata or provider outage.

## Suggested immutable relation

`Legal(task, policy, inventory, plan) == true` must be proven before optimization score is evaluated.

Optimization should be a function only over legal plans:

`Selected = argmin_policy( LegalPlans )`

Never:

`Selected = best_score(AllPlans)` followed by exceptions that waive hard gates.

## UI behavior
The operator should see concise output:
- selected execution plan summary;
- resource envelope;
- verifier/independence requirement;
- proof status (`NOT_VERIFIED` until executed);
- explicit freeze reason if no legal plan exists.

Internal pair enumeration and scoring do not need to clutter the default surface, but remain inspectable in an audit/details view.
