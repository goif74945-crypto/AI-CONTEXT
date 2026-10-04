# Adoption Sequence — NEXY Edge Contracts Quintet

> Classification: **AI-PROPOSED / NON-CANONICAL / NOT INTEGRATED**.
> This document proposes a future evaluation order only. It does not change NEXY.AI requirements or implementation.

## Objective
Introduce the five reference systems only through evidence-gated stages, keeping the deterministic NEXY authority model intact.

## Proposed order

| Order | System | Proposed boundary | Why first/later | Promotion evidence |
|---:|---|---|---|---|
| 1 | NAES Approval Escrow Seal | NEXY::LAW / NEXY::RUN pre-execution authorization | Small interface, high protection against stale or widened approvals | E3 adapter integration + abuse cases + replay/expiry tests |
| 2 | NPMA Policy Monotonicity Auditor | NEXY::LAW policy CI / release gate | Offline verifier with no runtime authority; can detect unsafe policy inversions before release | E3 policy-pipeline integration + representative policy corpus |
| 3 | NECP Evidence Closure Planner | NEXY::JUDGE / verification planner | Optimizes verification work but must never replace evidence itself | E3 integration + optimality fixtures + bounded-search failure tests |
| 4 | NCCQ Correlation-Cut Quorum | NEXY::SWARM / NEXY::JUDGE | Useful only after witness lineage/failure domains can be populated reliably | E3 integration + correlated-failure simulations + lineage quality audit |
| 5 | NSAC Safe Adapter Compiler | NEXY::FORGE / compatibility boundary | Highest mutation-adjacent risk; generated adapters need strongest shadow and regression validation | E3 shadow integration + E4 representative flows + generated-adapter security review |

## Staging law
1. **Reference only** — standalone code, E1/E2 evidence.
2. **Shadow mode** — run beside current behavior; no authoritative writes.
3. **Adapter integration** — explicit typed bridge into the target NEXY surface.
4. **Adversarial verification** — abuse, stale state, malformed input, replay and limit exhaustion.
5. **Human/project authority review** — decide whether the concept is promoted at all.
6. **Canonical promotion** — only through the governing NEXY change process; never because this lab exists.

## Cross-system composition proposal
A future execution path could be:

`policy candidate -> NPMA -> evidence plan via NECP -> witness collection -> NCCQ -> plan authorization via NAES -> execution`

NSAC remains outside that hot path and is used to construct compatibility adapters before they are admitted.

## Integration invariants
- A planner never upgrades evidence status.
- A quorum never converts correlated witnesses into independence by counting them twice.
- An approval is bound to exact canonical plan semantics and cannot authorize a changed plan.
- Generated adapters have no authority of their own.
- Any UNKNOWN/CONFLICT/material mismatch freezes the affected promotion path.
- No stage may claim production readiness from E1/E2 evidence.

## Rollback / containment
Every initial integration should be removable as a sidecar or gate without rewriting canonical NEXY state. If a proposed integration cannot be disabled without data migration or authority ambiguity, promotion should FREEZE until a reversible design exists.
