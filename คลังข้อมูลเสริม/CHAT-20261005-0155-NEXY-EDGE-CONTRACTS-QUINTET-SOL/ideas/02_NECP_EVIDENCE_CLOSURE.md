# 02 — NECP: NEXY Evidence Closure Planner

**Status:** AI-PROPOSED CONCEPT.

## Problem
NEXY's evidence discipline says which evidence class is required, but large tasks can have many possible verification actions. Re-running everything wastes time and resources; running too little creates false confidence.

## Design
NECP models claims, evidence levels, prerequisite claims and candidate evidence actions. It performs exact deterministic lowest-cost search over evidence states using cost, risk, action count and lexical order as stable tie-breakers.

## Invariants
- impossible closure => FREEZE;
- cyclic claim prerequisites => FREEZE;
- exploration cap exhausted => FREEZE, never PASS;
- target PASS only when every target and prerequisite reaches required evidence level.

## NEXY integration hypothesis
Use after Task Contract creation to generate the minimum evidence work plan before verification and again after failures to recompute only the remaining closure.
