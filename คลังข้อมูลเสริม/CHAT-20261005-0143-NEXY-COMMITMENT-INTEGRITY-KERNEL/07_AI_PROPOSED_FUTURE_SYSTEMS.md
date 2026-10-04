# 07 — AI-PROPOSED Future Systems

Everything in this file is **proposal**, not NEXY law or current implementation truth.

## 1. Commitment-to-Automation Compiler

Compile an authorized structured commitment directly into a durable scheduler/watch object, then return a cryptographic or server-authenticated binding receipt. Acceptance and task creation should be one transaction or have compensating rollback.

**Value:** eliminates the gap between “I promise” and “a task actually exists.”

## 2. User Commitment Dashboard

A compact VIEW surface showing only real commitments:
- active;
- waiting on condition;
- blocked;
- fulfilled with proof;
- failed/cancelled/expired;
- superseded.

The dashboard should expose edit/cancel where authority permits and never infer completion from elapsed time.

## 3. Commitment Debt Budget

Track accepted obligations that remain unresolved. Prevent the system from accumulating an unbounded tail of low-value promises, especially recurring monitors and follow-ups.

**Risk:** a scalar debt score must never cancel a safety-critical or legally required obligation automatically.

## 4. Cross-Agent Commitment Capsule

When work transfers between agents/providers, transfer a signed/verified capsule containing exact commitment fingerprint, revision, authority refs, execution binding, current state and required evidence.

**Value:** prevents “handoff amnesia.”

## 5. Promise Language Linter

A deterministic semantic-copy checker that flags phrases implying future persistence unless the response carries an accepted commitment reference.

Examples of semantic classes to detect:
- future delivery;
- monitoring;
- recurring action;
- delayed notification;
- guaranteed completion.

This should classify meaning, not police brand voice.

## 6. Capability Lease Coupling

Bind commitments not only to a task ID but also to a capability lease/health epoch. If the provider/tool capability disappears, the commitment transitions to BLOCKED or FAILED with explicit user-visible reason instead of vanishing.

## 7. Obligation Conflict Resolver

Detect incompatible commitments to the same resource or deadline, such as “never publish externally” versus a later scheduled external publish. Authority conflict must freeze before either obligation executes.

## 8. Fulfillment Proof Capsule

Bundle the minimal evidence needed to prove one commitment fulfilled, including target fingerprint, revision, execution receipt, evidence classes, artifact refs, and limitations.

## 9. Commitment Migration Protocol

When scheduler infrastructure changes, migrate obligations with two-sided proof:
- source commitment disabled or fenced;
- destination commitment active;
- no duplicate effect window;
- same obligation identity/revision lineage.

## 10. Commitment SLOs

Define metrics for the obligation system itself:
- unbacked-promise escape rate;
- fulfillment-evidence gap rate;
- forgotten active commitment rate;
- duplicate fulfillment rate;
- cancellation race escape rate;
- stale-binding rate;
- user correction rate after acceptance.

No target value is canonical in this proposal.
