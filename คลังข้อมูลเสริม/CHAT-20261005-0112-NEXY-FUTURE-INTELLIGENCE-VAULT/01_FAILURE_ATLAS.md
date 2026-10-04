# NEXY Future Failure Atlas

This catalog is architecture-neutral. It does not claim current NEXY.AI has these defects.

Severity: S0 cosmetic; S1 degraded; S2 incorrect recoverable; S3 authority/data breach; S4 irreversible/high-impact.

## Failure families
F01 Authority inversion [S4]: lower-authority content overrides explicit constraints. Oracle: governing authority resolved before action.
F02 Evidence laundering [S3]: inference becomes fact after summarization. Oracle: provenance class survives every handoff.
F03 Completion hallucination [S3]: COMPLETE without acceptance evidence. Oracle: criterion-to-evidence map is total.
F04 Scope creep [S2]: attractive but unrequested work is executed. Oracle: changed surface is subset of authorized scope.
F05 Requirement erosion [S4]: difficult immutable requirement disappears over long context. Oracle: immutable set is monotonic until authoritative change.
F06 Retry amplification [S3]: timeout triggers duplicate non-idempotent action. Oracle: reconcile state before retry.
F07 Stale-state mutation [S4]: write based on obsolete read. Oracle: version/SHA precondition where available.
F08 Partial-success ambiguity [S3]: multi-step workflow collapses partial state into binary success/failure. Oracle: per-step ledger.
F09 Context poisoning [S4]: retrieved data issues executable instructions. Oracle: data/instruction separation plus trust labels.
F10 Tool-result spoofing [S4]: prose masquerades as typed tool result. Oracle: only actual tool channel/result confers tool evidence.
F11 Temporal confusion [S2]: current-state claim uses stale clock/source. Oracle: explicit time basis and freshness.
F12 Target confusion [S4]: action hits near-identical repo/file/account. Oracle: canonical target + scope lock.
F13 Secret propagation [S4]: credentials leak into logs/context/artifacts. Oracle: secret-class material excluded from broad durable stores.
F14 Evaluation gaming [S3]: visible metric improves while hidden invariant breaks. Oracle: independent invariant gates.
F15 Recovery regression [S3]: fix breaks prior verified behavior. Oracle: affected regression suite rerun.
F16 Concurrent-head conflict [S2]: shared branch changes between read and commit. Oracle: 409 treated as stale state; re-read and append safely, never overwrite another actor.

Incident schema: failure_id, observed_at, target, authority_context, trigger, expected, observed, severity, blast_radius, evidence_refs, root_cause, correction, regression_tests, verification_status.
