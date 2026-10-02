# FAILURE — NEXY DIALOG convergence and E11 external blocker

- FAILURE_ID: NEXY-DIALOG-CONVERGENCE-E54ABD31-E11
- trace_id: NEXY-E54ABD31-3F9C4730-20261002
- final_status: ACTIVE_EXTERNAL_BLOCKER
- timestamp_source: Railway logs at 2026-10-02T15:00:12.355896441Z

## Repaired failures
1. UI type narrowing regression → repaired by stable local union narrowing and typed DialogMessage entries.
2. Active API → experimental Phase-F import → repaired by promoting the sandbox to canonical `packages/human`; boundary test remained unchanged.
3. API branch coverage 83.91% < 85% → repaired with 10 direct API fail-closed tests; threshold remained unchanged.
4. E10 receipt identity mismatch → repaired using a real current-head deployment plus provider rollback execution and exact SHA/tree receipt rebinding.

## Active blocker
E11 authorized human release signoff is absent. AI approval is forbidden by `scripts/doc-e/e11-signoff-verify.ts`.

## Failed/blocked paths
- Railway Agent rollback path hit connector usage limit; alternate authorized browser path completed the exact rollback and Railway API/logs verified the result.
- Generic user continuation commands were not interpreted as engineering/security/migration approval.

## Recovery boundary
Do not weaken E11 validation or invent actors/evidence. Resolution requires genuine authorized human signoff and one unchanged-head rerun.
