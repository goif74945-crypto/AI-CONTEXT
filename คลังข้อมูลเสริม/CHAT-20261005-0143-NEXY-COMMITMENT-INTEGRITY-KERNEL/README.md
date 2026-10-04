# NEXY Commitment Integrity Kernel (NCIK) — Reference Lab

**Classification:** AI-PROPOSED supplementary research.  
**Adoption status:** NOT ADOPTED into canonical NEXY.AI.  
**Mutation boundary:** this lab belongs only in `AI-CONTEXT/คลังข้อมูลเสริม/...`; it must not be treated as implementation proof for the NEXY.AI repository.

## Problem

AI systems routinely emit statements such as “I’ll monitor that,” “I’ll send it tomorrow,” or “done” even when the current execution environment has no durable scheduler, no condition watcher, no surviving task state, or no evidence that the promised result exists.

NCIK treats a **commitment as an authority-bearing future claim**. A commitment is legal only when the system can bind the claim to a real execution capability and later prove fulfillment against the same exact obligation.

The proposed product law is:

> **No promise without a capability binding. No completion without matching evidence. No silent mutation of the obligation.**

This is a proposal for a future NEXY-compatible control layer, not a claim about current NEXY production behavior.

## Why this is distinct

Existing supplementary work inspected for this lab covers claim/evidence truth, task contracts, human authority, delegation leases, privacy, verification, UX, concurrency, counterfactual safety, and many other control concerns. Path-level inventory contained no dedicated subsystem named for `commitment`, `promise`, `obligation`, `deadline`, `reminder`, or `follow-up`.

NCIK differs from nearby systems:

- **Claim/Evidence Ledger** asks whether a proposition is supported.
- **Task Contract** asks what execution is in scope.
- **Delegation Lease** asks what an executor is allowed to do.
- **NCIK** asks whether NEXY may truthfully promise an outcome across time, and whether later fulfillment matches the exact promise.

## Reference behavior

A `Commitment` binds:
- stable ID + revision;
- issuer + beneficiary;
- objective + exact deliverable;
- allowed/protected scope;
- temporal mode: immediate, scheduled, conditional, recurring;
- effect class;
- authority provenance;
- required evidence classes;
- execution binding + capability proof reference;
- trigger/deadline semantics;
- optional supersession fingerprint.

Future commitments require durable bindings. The reference model recognizes:
- `INLINE_SESSION`
- `SCHEDULED_TASK`
- `CONDITION_WATCH`
- `RECURRING_TASK`

The engine emits exactly one of:
- `ALLOW_COMMITMENT`
- `ASK_AUTHORITY`
- `FREEZE`

## Local validation

From the project directory:

```bash
PYTHONPATH=src python tools/run_checks.py
```

The validation suite compiles source/tests, parses JSON artifacts, runs unit/invariant tests, and executes the adversarial corpus.

## Evidence boundary

The local sandbox can establish E1/E2 evidence for this standalone reference implementation only. It does not establish:
- production NEXY integration;
- scheduler durability in a real service;
- distributed exactly-once fulfillment;
- cross-agent handoff correctness;
- UI/E2E behavior;
- runtime/deployment behavior.

Those remain adoption gates.
