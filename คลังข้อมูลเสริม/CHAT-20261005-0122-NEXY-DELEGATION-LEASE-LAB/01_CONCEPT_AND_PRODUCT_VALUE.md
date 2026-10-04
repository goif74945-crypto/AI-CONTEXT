# 01 — Concept and Product Value

## Classification

- `SOURCE_FACT`: NEXY emphasizes USER LAW, deterministic control, explicit authority, FREEZE, auditability, and separation of visible/editable/executable capability.
- `SOURCE_FACT`: current DOC-C includes RBAC, owner controls, idempotency, observability, queue control, and freeze semantics.
- `AI_PROPOSAL`: NEXY::LEASE is not part of current DOC-C based on the context inspected for this workstream.
- `AI_HYPOTHESIS`: plan-bound temporary authority can reduce overreach while reducing repetitive confirmation friction.

## Problem

Authentication answers **who are you?**  
RBAC answers **what class of operation may your role perform?**  
A task plan answers **what is intended in this execution?**

These are different questions.

A role may legally possess broad write permission while a particular task should touch only one artifact. Likewise, an agent may start from an allowed plan and later change the target, destination, effect class, or cost because of newly generated intermediate reasoning. If authority automatically follows the new plan, the system has converted a plan change into a privilege change.

That is exactly the kind of implicit behavior NEXY's authority model is designed to avoid.

## Proposal

Introduce a **Reversible Authority Lease** as an additional restrictive execution control.

A lease is explicit, finite, scoped, plan-bound, policy-version-bound, revocable, non-escalating under delegation, fail-closed, and auditable.

The lease never grants more authority than upstream auth/RBAC/LAW already permit. Its only legal effect is to **further restrict** what may execute.

## Intent Drift Firewall

This proposal intentionally avoids “AI guesses what the user really meant.” Natural-language semantic inference would violate the zero-guess direction if treated as authority.

Instead, intent drift is defined structurally:
1. an authorized directive is compiled into a concrete action plan by an authorized planning path;
2. the canonical representation of that plan is hashed;
3. the lease binds to that hash;
4. execution uses the current plan hash plus exact action facets;
5. any material change in resource, verb, effect, destination, cost, or action count changes the fingerprint;
6. mismatch blocks execution and requires a newly authorized plan.

This is a **structural drift firewall**, not a mind-reading system.

## Product value

- Fewer useless confirmations: approve a bounded plan once instead of every harmless sub-step.
- Stronger trust: approval cannot silently widen because an agent changed its mind mid-run.
- Better explanations: a freeze can name the exact boundary that changed.
- Safer delegation: a parent can delegate only a narrower lease.
- Cleaner audit: a decision can be reconstructed from lease ID, plan hash, policy version, logical tick, action index, and result code.

## Non-goals

NEXY::LEASE does not replace authentication, RBAC, CSRF/session controls, LAW, JUDGE/release policy, Vault integrity, provider authorization, sandboxing, transaction/rollback infrastructure, or cryptographic operator approval.

It is not autonomous privilege acquisition. There is no legal auto-renewal or silent expansion path.

## Adoption principle

If future evidence shows that lease prompts increase friction without reducing meaningful risk, the concept should be rejected or narrowed. The idea is subordinate to evidence and NEXY law.
