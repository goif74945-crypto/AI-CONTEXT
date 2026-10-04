# NEXY PEPSA — Pre-Execution Partial-State Analyzer

**Status:** `AI-PROPOSED / EXPERIMENTAL / ADVISORY`  
**Current NEXY requirement:** `NO`  
**NEXY runtime integration:** `NOT_VERIFIED / NOT IMPLEMENTED`  
**Repository mutation:** this project is stored only in `AI-CONTEXT`; it does not modify NEXY.AI source.

## Why this exists

Agent systems often validate whether every individual step looks legal, then still fail disastrously when step 3 succeeds and step 4 fails. The result is a half-applied plan: a resource was deleted, a message was sent, a policy was changed, or a file was written, while the remaining steps never happened.

PEPSA moves one question earlier in the lifecycle:

> **If execution stops at every possible boundary, what state can be left behind?**

The tool consumes two explicit machine-readable inputs:

1. an `ExecutionPlan`, which declares the step DAG and mutation semantics; and
2. a separate `Policy`, which declares allowed boundaries and protected resources.

It produces one deterministic report with `READY` or `FREEZE`. It does **not** execute the plan.

## User-facing value if adopted later

A future NEXY control surface could show, before execution:

- exact deterministic execution order;
- which resources are touched;
- which mutation lacks rollback coverage;
- whether an external side effect is idempotent;
- whether an irreversible action has explicit approval;
- which failure boundary can leave residual state;
- a stable plan/policy/report identity hash.

This supports a UX where “Run” means the plan has survived a structural preflight rather than merely looking plausible.

## Core invariants

- Policy is a separate input from the plan. A plan cannot authorize itself.
- Protected-resource mutation freezes.
- Unknown boundaries freeze.
- Mutation without declared postcondition freezes when required by policy.
- Mutation without evidence requirement freezes when required by policy.
- External side effects without an idempotency key freeze when required by policy.
- Irreversible mutation requires explicit approval.
- Irreversible mutation before later steps freezes because a later failure can strand state.
- Reversible mutation must declare a rollback strategy.
- Dependency cycles and missing dependencies are invalid input, not “best effort.”
- Equivalent semantic plans receive the same plan hash even when input step-array order differs.
- Floating-point values are rejected from canonical hashed data.
- The analyzer never performs tool calls, file mutations, network requests, or external effects.

## Quick run

From this directory:

```bash
PYTHONPATH=src python3 -m nexy_pepsa.cli analyze \
  --plan examples/safe_plan.json \
  --policy examples/policy.json \
  --pretty
```

Exit codes:

- `0` = `READY`
- `2` = `FREEZE`
- `3` = invalid input / invalid plan structure

Run validation:

```bash
./scripts/run_validation.sh
```

## What PEPSA proves and does not prove

PEPSA can provide structural/static preflight evidence about the declared plan and policy. It does **not** prove that a declared rollback strategy actually works, that an approval ID is authentic, that an external provider honors idempotency, or that NEXY has integrated this design. Those need higher evidence classes and an authoritative integration contract.

## Relationship to existing NEXY concepts

PEPSA is deliberately narrower than Capability Registry admission, Evidence Graph work, Context Engine work, contract compilation, or release verification. Its unit of analysis is a **concrete proposed execution DAG and every failure boundary inside that DAG**.

It is intended as an optional future guard between “plan accepted” and “effects executed,” subject to explicit promotion by NEXY authority. Until then it remains advisory research.
