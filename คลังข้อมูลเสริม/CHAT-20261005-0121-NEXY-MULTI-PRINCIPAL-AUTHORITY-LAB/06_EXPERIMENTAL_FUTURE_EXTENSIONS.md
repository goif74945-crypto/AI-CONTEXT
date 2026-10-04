# AI-Proposed Future Extensions

Everything in this file is **EXPERIMENTAL / AI-PROPOSED / NOT CURRENT NEXY SCOPE** unless future authoritative specification explicitly promotes it.

## X1 — Signed Authority Receipts
Canonical signed receipts with signer identity, policy identity/version, request hash, decision, validity window, nonce, and audit linkage.

## X2 — Conflict-of-Interest Graph
Structural separation constraints such as requester/approver independence, organizational-domain diversity, and finance-recipient conflict escalation. This must be policy, not model judgment.

## X3 — Revocation Snapshot Binding
Bind evaluation to an explicit roster/revocation snapshot identity.

## X4 — Workspace / Tenant Authority Domains
Ensure `OWNER` in workspace A has no authority in workspace B without an explicit cross-workspace grant.

## X5 — Break-Glass Path
An emergency rule could reduce normal quorum only under explicitly proven conditions, stronger authentication, bounded TTL/scope, mandatory incident creation, and retrospective review. Default should be absent.

## X6 — Authority Diff Compiler
Semantic diff between policy versions: gained/lost authority, quorum/veto/self-approval changes, domain/action changes, and evidence invalidation.

## X7 — Approval Explanation Surface
Non-authoritative projection of counted approvals, ignored reasons, missing thresholds, veto sources, and fingerprints. UI must not alter the decision.

## X8 — Property / Model Checking Expansion
Automatically check no-ALLOW-below-quorum, veto dominance, self-approval prohibition, order invariance, revocation monotonicity, and cross-domain isolation.

## X9 — NEXY::LAW Compilation Target
If ever promoted, declarative MPAL policy should compile into the authoritative LAW/Core path rather than execute as an independent authority sidecar.

## X10 — Human-Friendly Pending Plans
For `PENDING`, expose the smallest legal completion gap, e.g. “Security: 1 missing; Operations: 1 missing,” without AI choosing who should approve.

## Promotion gate
Promotion requires authoritative requirement approval, conflict check, threat model, implementation contract, test/evidence plan, migration/rollback design, and exact runtime verification.
