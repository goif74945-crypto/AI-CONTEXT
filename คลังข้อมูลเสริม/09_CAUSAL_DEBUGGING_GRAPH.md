# Causal Debugging Graph
Status: PROPOSAL / AI-PROPOSED CONCEPT
Authority: ADVISORY ONLY

## Objective
Replace “search logs until something looks suspicious” with an evidence-preserving causal graph for failures.

## Node types
ObservedFailure
Symptom
Invariant
Requirement
Input
SourceChange
Configuration
Environment
Dependency
Execution
Artifact
Assertion
Hypothesis
Experiment
Counterexample
RootCause
Fix
RegressionTest

## Edge examples
FAILURE -> VIOLATES -> INVARIANT
CHANGE -> MAY_CAUSE -> FAILURE
HYPOTHESIS -> PREDICTS -> OBSERVATION
EXPERIMENT -> FALSIFIES -> HYPOTHESIS
ROOT_CAUSE -> EXPLAINS -> FAILURE
FIX -> ADDRESSES -> ROOT_CAUSE
TEST -> GUARDS -> INVARIANT

## Hypothesis discipline
Every hypothesis must include:
- predicted observation if true
- predicted observation if false
- cheapest discriminating experiment
- evidence source
- confidence label
- scope

Never promote correlation to root cause merely because the last changed file is nearby.

## Delta debugging
For deterministic failures:
- minimize input
- minimize source/config delta
- hold environment identity fixed
- bisect causal candidates
- preserve minimized reproducer

For nondeterministic failures:
- first enumerate uncontrolled variables
- capture scheduler/time/random/network/cache state where possible
- determine whether nondeterminism itself violates contract
- avoid averaging failures into invisibility

## Counterfactual test
A root-cause claim is stronger when:
“If cause C were absent while relevant conditions remain, failure F would not occur.”
Practical approximation:
- reproduce F
- remove/neutralize C
- observe F disappears
- reintroduce C where safe
- observe F returns
- run adjacent regressions

## Multi-cause failures
Support AND/OR causal sets:
C1 AND C2 -> F
C1 OR C2 -> F
Do not force one root cause when the system requires a conjunction.

## Stop conditions
FREEZE causal conclusion when:
- reproducer cannot be established
- evidence conflicts
- experiment changes multiple critical variables
- source identity is unknown
- proposed root cause does not explain all required observations

## Output contract
A completed causal investigation should yield:
- minimal reproducer
- violated invariant
- root-cause graph
- rejected hypotheses with evidence
- fix rationale
- regression test
- remaining uncertainty

This format is intentionally reusable by humans and agents.
