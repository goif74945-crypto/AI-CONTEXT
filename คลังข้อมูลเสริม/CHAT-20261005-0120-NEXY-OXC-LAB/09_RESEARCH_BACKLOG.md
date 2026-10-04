# OXC Research Backlog

Classification: **EXPERIMENTAL / AI-PROPOSED**

These items are intentionally unresolved. Do not convert them into NEXY requirements without authority.

## P0 — authority/schema alignment

1. Resolve human-facing role model:
   - current product context includes OWNER/OPERATOR/AUDITOR/SYSTEM;
   - OXC reference introduces VIEWER for explicit read-only presentation;
   - decide whether VIEWER maps to anonymous/read-only capability or should be removed.

2. Determine canonical action-risk ownership.
   - Is risk computed by LAW/Core?
   - Is it static metadata?
   - Is a UI minimum-friction table permitted?
   - What component can raise/lower risk?

3. Add snapshot freshness/version contract.
   - OXC v1 cannot detect stale state.
   - production integration needs versioned re-authorization.

## P1 — UX effectiveness without truth compromise

4. Measure task completion time with MINIMAL/STANDARD/DIAGNOSTIC disclosure.
5. Measure operator error rate around FREEZE/recovery.
6. Test whether disabled-reason visibility improves comprehension.
7. Determine when hiding denied actions causes confusion versus safely reducing clutter.
8. Validate first-session behavior against DOC-D “I-Don’t-Know Mode.”

## P1 — accessibility

9. Define accessibility signal contract independent of “density” preference.
10. Prove critical state is perceivable without color.
11. Test keyboard-only dangerous-action confirmation.
12. Test screen-reader ordering for mandatory signals.

## P1 — localization

13. Replace authoritative-looking free-form labels with stable message keys.
14. Define critical-control translation review workflow.
15. Test right-to-left layouts without hiding state.
16. Prove translated text cannot be parsed back into permission decisions.

## P1 — race and stale state

17. Render READY then transition to FREEZE before click.
18. Change role after render.
19. Revoke backend permission after render.
20. Change artifact/project version after render.
21. Replay an old SurfacePlan.

Expected invariant: backend rejects stale/unauthorized mutation regardless of UI state.

## P2 — formal methods

22. Model action eligibility as a lattice and prove preference non-interference.
23. Property-test all enum/state combinations.
24. Add mutation testing for denial rules.
25. Consider lightweight TLA+/Alloy model for stale-plan race semantics if integration complexity justifies it.

## P2 — privacy

26. Define maximum preference retention.
27. Decide whether preferences may sync across devices.
28. Verify preference telemetry cannot become behavioral profiling.
29. Test deletion/export if preferences become durable.

## P2 — performance

30. Establish target plan size and compile latency only after real UI integration exists.
31. Benchmark large action sets.
32. Ensure diagnostic disclosure does not create dashboard sprawl or low-RAM regressions.

## Stop rule

Research results are evidence, not automatic product law. Promotion requires current NEXY authority.
