# TRACEWEIGHT — Agent Influence Dominance Auditor

Status: `Lo4_AI_PROPOSAL_ONLY`

## Problem
A five-agent result can look independent while four agents actually inherit most reasoning from one upstream agent. Counting agents or votes alone can create pseudo-consensus.

## Mechanism
TRACEWEIGHT models a derivation DAG. Weighted parent influence is recursively propagated back to agent-source nodes. It reports:
- normalized source influence;
- dominant source and dominance ratio;
- effective source count using inverse concentration;
- influence attributable to unverified source agents;
- PASS/FREEZE reasons.

## Invariants
- source agents have no parents;
- every non-source ancestry edge points to an existing node;
- edge weights are positive and finite;
- cycles are rejected;
- source influence normalizes to one.

## NEXY value
Provides a causal complement to consensus logic: not merely "how many agents agreed?" but "how many independent upstream agents materially caused this decision?"
