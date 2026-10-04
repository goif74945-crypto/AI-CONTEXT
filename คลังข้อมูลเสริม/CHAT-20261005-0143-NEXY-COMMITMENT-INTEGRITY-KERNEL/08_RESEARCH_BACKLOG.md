# 08 — Research Backlog

Priority order reflects engineering risk, not product commitment.

## P0 — Correctness and authority
1. Define authenticated execution-binding receipt format.
2. Specify atomic `create-task + accept-commitment` protocol.
3. Specify cancellation-vs-dispatch concurrency law.
4. Prove retry/crash does not duplicate external side effects.
5. Define authoritative time/trigger semantics without trusting model clocks.
6. Define provider/tool capability revocation behavior.

## P1 — Distributed reliability
7. Model-check commitment FSM with dispatch/cancel/retry interleavings.
8. Design durable event cursor for conditional watches.
9. Define regional replication and stale-read behavior.
10. Design recovery after scheduler metadata corruption.
11. Define commitment migration across scheduler versions.
12. Define handoff protocol between AI workers/providers.

## P2 — Product integrity
13. Study when users interpret assistant language as a promise.
14. Build promise-language conformance corpus.
15. Test whether a commitment dashboard improves trust without UI overload.
16. Define concise BLOCKED/FAILED wording that preserves exact cause.
17. Test accessibility equivalence for commitment states.
18. Test localization for modal certainty, deadlines, and conditional semantics.

## P3 — Privacy and governance
19. Minimize retained commitment metadata.
20. Define deletion/retention law for completed/cancelled obligations.
21. Prevent sensitive trigger conditions from leaking into telemetry.
22. Define export/audit format for user-owned commitment history.

## P4 — Scale and economics
23. Admission control for huge recurring-monitor sets.
24. Fair scheduling across users/tenants without weakening hard deadlines.
25. Cost attribution and budget limits for long-lived obligations.
26. Backpressure behavior when watch/scheduler capacity is degraded.

## P5 — Formalization
27. TLA+/PlusCal or equivalent model for transition/concurrency invariants.
28. Property-based generation of temporal/binding/evidence combinations.
29. Tamper-evident receipt anchoring options.
30. Formal non-interference between NCIK acceptance and upstream LAW denial.
