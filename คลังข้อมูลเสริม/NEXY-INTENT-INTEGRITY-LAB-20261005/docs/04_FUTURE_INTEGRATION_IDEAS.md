# 04 — Future Integration Ideas

**Every item in this file is an AI-PROPOSED CONCEPT. None is a current NEXY.AI requirement.**

## Idea A — Intent Seal at orchestration boundaries

Before NEXY::SWARM delegates work, emit a compact contract digest plus requirement IDs. Each worker returns the digest it actually used. NEXY::JUDGE rejects results evaluated under a stale or different contract.

**Potential benefit:** detects hidden context loss across agent handoffs.  
**Trade-off:** every contract revision creates explicit migration overhead.

## Idea B — Human-visible semantic diff

When a model proposes changing objective/scope/requirements, present exact change IDs and a concise semantic diff to the user before authorization.

**Potential benefit:** makes “AI quietly changed the plan” visible.  
**Trade-off:** too many low-value diffs could create approval fatigue.

## Idea C — Approval capability tokens

Convert an exact approved change ID into a short-lived, single-use capability bound to:

- base contract digest;
- candidate digest;
- repository identity;
- actor/workflow ID;
- expiry;
- nonce.

**Potential benefit:** prevents approval reuse outside the intended transition.  
**Trade-off:** adds cryptographic key management and failure modes.

## Idea D — Drift budget for non-authoritative exploration

Exploratory agents could receive a sandbox-only “drift budget” allowing suggestions outside current scope, while the execution path remains frozen unless a human promotes the suggestion into the authoritative contract.

**Potential benefit:** creativity without authority leakage.  
**Trade-off:** UI must distinguish suggestions from executable intent with zero ambiguity.

## Idea E — Requirement coverage heatmap

NEXY::VIEW could display which mandatory requirements have implementation evidence, verification evidence, both, or neither.

**Potential benefit:** exposes partial completion before the user sees a false “done” state.  
**Trade-off:** requires strong evidence-to-requirement linkage.

## Idea F — Contract-aware memory write gate

Durable memory writes could be checked against the active intent contract. New “facts” unsupported by the current evidence envelope would remain experimental/unknown rather than being promoted into durable truth.

**Potential benefit:** reduces context corruption over long project histories.  
**Trade-off:** may block useful provisional notes unless the memory model supports explicit uncertainty tiers.

## Idea G — Cross-model intent conformance tournament

Give multiple models the same contract and ask each to generate an execution proposal. Score only structural conformance first, quality second.

**Potential benefit:** separates “best answer” from “most obedient to authority.”  
**Trade-off:** extra compute and possible convergence on formally compliant but low-quality plans.

## Promotion rule

No idea above should move into NEXY.AI implementation merely because it exists here. Promotion requires an authoritative user/spec decision, compatibility analysis, threat modeling, implementation design, and evidence plan.
