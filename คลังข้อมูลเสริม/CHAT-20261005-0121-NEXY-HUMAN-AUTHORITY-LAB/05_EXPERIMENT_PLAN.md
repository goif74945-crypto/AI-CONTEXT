# Experiment Plan

**Status: AI_PROPOSED_CONCEPT / HYPOTHESES NOT VERIFIED**

## Research question

Can an explicit human-authority preflight contract reduce unnecessary interaction while preserving or improving scope fidelity and freeze truth?

## Hypothesis H1 — Aggregated questions reduce friction

Compare:
- baseline: one question per missing field;
- proposal: one aggregated question containing every currently known material blocker.

Primary measure:
- median interruptions per successfully resolvable task.

Hard safety measure:
- rate of actions executed with a still-missing material field must remain zero.

Falsification:
- aggregation materially decreases comprehension or increases unresolved execution attempts.

## Hypothesis H2 — Explicit outcome IDs reduce scope drift

Inject mutation proposals that:
- support a required outcome;
- support only an unrelated outcome;
- claim no outcome relationship.

Measure:
- drift rejection recall;
- false rejection rate for legitimate declared work.

Important limitation:
This tests declared contract integrity, not natural-language semantic correctness.

## Hypothesis H3 — Exact consent binding prevents stale destructive confirmation

Generate consent records for:
- exact contract/action;
- prior contract;
- different action;
- non-explicit consent;
- wrong grantor role.

Hard gate:
Only exact authorized binding may pass.

## Hypothesis H4 — Progressive disclosure reduces control confusion

Evaluate role/state combinations:
- OWNER/OPERATOR/AUDITOR;
- VIEW/RUN/FORGE;
- READY/FREEZE/STOP.

Critical constraints:
- FREEZE/STOP notice never disappears;
- unauthorized controls never appear;
- hidden UI never becomes backend authorization.

## Hypothesis H5 — Evidence-bearing acceptance improves completion calibration

Compare interface interpretations when a required criterion is:
- PASS with evidence;
- PASS without evidence;
- NOT_VERIFIED;
- FAIL.

Expected proposal behavior:
Only PASS with evidence allows acceptance status PASS.

## Adversarial families

1. role forgery;
2. protected scope disguised as allowed scope;
3. namespace wildcard edge cases;
4. external action with external flag mismatch;
5. outcome tag injection;
6. stale consent replay;
7. malformed contract;
8. interruption flooding;
9. success presentation after freeze;
10. control visibility escalation;
11. STOP-state action attempts;
12. recoverability mismatch;
13. hash canonicalization vectors;
14. very large contract resource bounds;
15. Unicode normalization ambiguity.

The current implementation covers a subset. Unicode normalization and large-input resource limits remain future research.

## Stop conditions

Stop an experiment if:
- it requires changing canonical NEXY authority without authorization;
- a critical violation is hidden by an aggregate score;
- user-friction optimization causes a truth/authority regression;
- the experiment requires production mutation;
- evidence cannot be bound to the exact tested revision.
