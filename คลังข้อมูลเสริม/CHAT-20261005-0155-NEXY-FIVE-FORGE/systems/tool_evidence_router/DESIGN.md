# Tool Evidence Router — Design

STATUS: PROPOSED_BY_AI / STANDALONE PROTOTYPE

## Objective
Select a bounded combination of tools that can satisfy a required evidence class and capability set within reliability, latency and cost constraints.

## Core idea
Availability is not authority and a tool description is not evidence. TER makes the routing constraint explicit.

## Invariants
- every required capability is covered by at least one selected tool;
- at least one selected tool reaches the required evidence class;
- each selected tool meets minimum reliability;
- aggregate latency/cost stay within declared budgets;
- deterministic tie breaking chooses lower total penalty then lexicographic tool names;
- if no route exists, return FREEZE.

## Search
Enumerate combinations from size 1 to `max_tools` (default 3). This is intentionally bounded and exact over the bounded candidate set.

## Evidence target
E2 tests cover route selection, reliability gate, evidence-class gate and no-route freeze.
