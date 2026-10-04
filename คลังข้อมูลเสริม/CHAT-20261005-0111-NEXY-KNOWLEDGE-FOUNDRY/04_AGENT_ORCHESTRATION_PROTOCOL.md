# Agent Orchestration Protocol

## Objective
Make multi-agent execution auditable and resistant to scope drift.

## Roles
Planner decomposes without mutating scope. Researcher gathers evidence. Builder produces scoped artifacts. Verifier independently checks acceptance criteria. Adversary searches for hidden failure and regression. Integrator resolves verified outputs.

One agent may hold several roles, but Builder self-report alone cannot satisfy critical independent verification.

## Work packet
Each packet contains objective, authority, inputs, scope, forbidden actions, dependencies, acceptance criteria, evidence requirements, output schema, and stop conditions.

## Handoff
A valid handoff includes completed items, unresolved items, exact evidence locators, changed assumptions, risks, and next safe action.

## Concurrency
Parallelize only independent packets. Shared mutable state requires ownership or serialization. Never silently overwrite another agent's canonical artifact.

## Stop conditions
STOP on authority conflict, unavailable critical evidence, ambiguous destructive scope, or repeated verification failure without a new hypothesis.

## Completion
DONE = acceptance criteria plus evidence. Implemented without verification = BUILT_NOT_VERIFIED.
