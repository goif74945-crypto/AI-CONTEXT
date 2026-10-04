# Concept 1 — Outcome Closure Engine
AI-PROPOSED / NON-GOVERNING

**Problem:** tests can pass while the user's actual required outcome remains partially unproven.

**Contract:** declare required predicates, forbidden predicates, and evidence requirements before evaluation. Runtime observations cannot invent new predicate IDs.

**Core invariant:** CLOSED is legal only when every required predicate is satisfied with adequate evidence and every forbidden predicate is explicitly shown absent with evidence.

**Why it can help NEXY:** it provides a supplemental definition of task-level done that can sit above individual test gates without altering NEXY's canonical release state.

**Implementation:** `src/outcome_closure.ts`.
**Tests:** `tests/outcome_closure.test.mjs`, relevant adversarial tests, integration test.
**Evidence:** RED traces plus final 33-test run.
