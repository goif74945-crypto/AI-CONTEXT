# 08 — AI-Proposed Idea Backlog

Everything here is **AI-PROPOSED**, not current NEXY requirement.

## A. Effect Receipt
Bind lease ID, action index, provider resource ID, request/result hashes, logical tick, budget delta, and audit correlation after each effect.

## B. Reversible Write Escrow
Stage reversible mutation and deterministic diff before final commit. Separate staging authority from commit authority.

## C. Authority Difference Compiler
On plan change, compute the smallest authority delta instead of asking the operator to reread the whole plan.

## D. Provider Scope Proof Adapters
Each provider supplies deterministic `canonical_resource_id()` and `prove_subset(child,parent)` with adversarial conformance tests.

## E. Lease Simulation Mode
Run plan through the guard without side effects and report predicted authorization blocks before expensive work.

## F. Revocation Epoch
Embed a monotonic revocation/config epoch so stale workers can detect an old authority view. Requires distributed-systems proof.

## G. Proof-Carrying Delegation
Child derivation returns a machine-verifiable narrowing proof for every scope dimension.

## H. Authority Budget UX
Expose consequence ceilings such as no external sends, at most two reversible writes, no deletes, only Project Alpha, expires at task end.

## I. Lease-Aware Planner
Planner sees remaining authority and must fit the plan or return a structured authorization delta. Planner must never grant authority.

## J. Friction Evals
Compare plan-bound authorization against per-action confirmation on security and usability. A safe control users habitually ignore is still a product failure.
