# FAILURE — NEXY release external blockers A93C7809

- FAILURE_ID: NEXY-RELEASE-EXTERNAL-BLOCKERS-A93C7809
- trace_id: NEXY-A93C7809-8EB145B3-20261002
- context: exact-head software validation is fresh and successful at `a93c780972ed7464bfc5f182d54129c54d0393cc`.
- cause: required release evidence depends on external/provider/human/physical proof not available in the current execution authority.
- final_status: ACTIVE_BLOCKER

## Failed / blocked paths
- E10: no authoritative exact-campaign provider receipt binding both deploy and rollback command identities.
- E11: no authorized engineering/security/migration human signoff. AI approval is forbidden.
- E12: no exact-current rollback execution receipt plus health/smoke/monitoring proof; available Railway connector exposes no rollback mutation action.
- External host/hardware/anchor/TSA/public/robotics proofs are incomplete or absent.
- Detailed 837-row and 935-record source workbooks are unavailable, blocking exhaustive row-level convergence.
- GitHub provider-side branch prevention is not verified; branch reports unprotected.

## Failed approach recorded
A Railway `redeploy` on the branch validation service reused an old `ab616cd…` snapshot. Source identity correctly rejected it. Prevention: trigger a new deploy from current branch source when exact source rebinding is required.

A no-op pre-deploy removal experiment did not fix the separate `nexy-validation` deployment failure and was reverted.

## Recovery boundary
Do not weaken tests, assertions, source-identity gates, evidence schemas, or release contracts. Resolve only by supplying real external evidence/authority and re-running on unchanged exact HEAD.
