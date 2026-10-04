# PauseSafe Kernel — Design Contract

Status: AI_PROPOSAL / REFERENCE_IMPLEMENTATION / NOT_NEXY_CANON

## Objective
Determine whether an autonomous mission can be preempted and later resumed without silently duplicating or losing side effects.

## Inputs
Explicit `StepState` records: stable ID, status, idempotence, checkpoint state, and compensation availability.

## Outputs
`PREEMPT_SAFE`, `DRAIN_REQUIRED`, or `BLOCKED_UNSAFE_INFLIGHT`; safe checkpoints may produce a content-bound `ResumeToken`. Resume validation detects state/completion drift.

## Safety law
A running non-idempotent step with neither checkpoint nor compensation blocks preemption. Resume never trusts a token if the current state fingerprint changed.

## NEXY boundary
Future orchestrators could ask PauseSafe before operator pause/model swap/process maintenance. It does not perform the pause or side effect itself.

## Verification model
E1 compile; E2 focused and negative-path unit tests; E3-local composition through `integration/test_portfolio.py`. Production integration is NOT_VERIFIED.
