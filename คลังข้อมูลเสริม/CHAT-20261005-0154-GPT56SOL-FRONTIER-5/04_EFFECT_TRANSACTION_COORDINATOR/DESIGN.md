# Effect Transaction Coordinator (ETC) — Design

## Problem
An AI task can mutate several external systems. If action 3 fails after actions 1 and 2 succeed, the user may be left in a partially-mutated world. “Retry” can make it worse.

## Objective
Provide deterministic PREPARE → COMMIT → COMPENSATE semantics for side-effect plans. Reversible effects carry compensation. Irreversible effects require explicit approval receipts before prepare succeeds.

## Invariants
- Duplicate idempotency keys are invalid.
- Nothing commits until the whole plan prepares.
- Irreversible action without matching approval => FREEZE.
- On commit failure, committed reversible actions compensate in reverse order.
- Uncompensated partial effects => FREEZE with exact residue.

## Scope
This implementation is a deterministic simulator/state machine. Actual connector execution adapters are future integration work.
