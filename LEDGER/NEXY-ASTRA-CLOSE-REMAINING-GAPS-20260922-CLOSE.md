# LEDGER

LEDGER_ID: NEXY-ASTRA-CLOSE-REMAINING-GAPS-20260922-CLOSE
source_revision: 9eaeec9b830471907f2f1f19ca5d76371caf22cb
final_head: 9c9befd9fe255b0f9271e6e2b8c4bb2443a08089
claim_1: Canonical vault/incident/audit RBAC, canonical revision/audit pagination, exact read audit events, and logout 422 are present in source.
proof_1: packages/api/canonical.ts; packages/api/directives.ts; packages/api/auth.ts; contract/integration test sources.
status_1: SOURCE_VERIFIED_EXECUTION_BLOCKED

claim_2: Baseline fingerprint flake was caused by a potentially no-op fixed 00 seed-prefix mutation.
proof_2: baseline push run 35621268711 plus guaranteed-different prefix logic in tests/integration/game-runtime-deterministic.spec.ts.
status_2: ROOT_CAUSE_PROVEN_SOURCE_FIX_PRESENT_EXECUTION_BLOCKED

claim_3: Prior CI-only LAW-pass fixture was not policy-valid because equal confidences hit ambiguity freeze and duplicate evidence collapsed below evidence_min=2.
proof_3: swarm emitOrFreeze tie rule; JUDGE evidence Set; DOC-C release thresholds.
status_3: DEFECT_PROVEN_FIXED_IN_SOURCE

claim_4: Current fixture supplies deterministic unequal confidences and distinct per-agent evidence hashes while preserving SWARM -> JUDGE -> LAW worker path.
proof_4: packages/swarm/pipeline.ts and packages/queue/workers.ts.
status_4: SOURCE_VERIFIED_EXECUTION_BLOCKED

claim_5: DOC-D revision history now has desktop table/mobile cards and browser acceptance includes sticky freeze, one-column mobile, and <=2-column desktop checks.
proof_5: vault page; globals.css; tests/browser/critical-flows.spec.mjs.
status_5: SOURCE_VERIFIED_EXECUTION_BLOCKED

claim_6: Final current Actions do not execute test commands.
proof_6: runs 35693191309, 35693196053, and 35692777192 attempt 2 report critical jobs with steps=null.
status_6: VERIFIED

claim_7: Production deployment was not performed; PR #8 is open, draft, and unmerged.
proof_7: PR metadata and skipped Deploy jobs.
status_7: VERIFIED

claim_8: Protected branch was not touched by repository operations in this campaign.
proof_8: all NEXY repository reads/writes targeted the authorized work branch or commit SHAs on its ancestry; no protected-branch repository operation was issued.
status_8: VERIFIED

claim_9: The current complete repository tree exposes no hard-delete/delete/purge API route.
proof_9: final recursive tree reports truncated=false; API route list contains no such route.
status_9: VERIFIED_ROUTE_ABSENCE; IMPLEMENTATION_REMAINS_AUTHORITY_GAP

final_verdict: PARTIAL
confidence: 0.99 for recorded source and Actions state; executable correctness remains unverified
freshness: current through GitHub Actions metadata 2026-09-22T06:05Z
protected_branch_touched: false
