# Reversibility & Blast-Radius Architecture

## Core model
Before durable mutation compute a Mutation Envelope:
`E = {target, authority, write_set, read_set, external_effects, reversibility, rollback, concurrency_risk, evidence_plan}`.

## Reversibility classes
R0 read-only.
R1 trivially reversible local change.
R2 reversible with known prior state.
R3 reversible only through backup/transaction.
R4 externally visible or costly to reverse.
R5 effectively irreversible.

## Rules
- R0-R2 may be autonomous when authorized.
- R3 requires verified rollback material before execution.
- R4 requires explicit scope plus confirmation when impact is material.
- R5 freezes unless the user explicitly authorizes that exact irreversible effect.
- Never infer authorization for adjacent resources.

## Blast radius
Estimate across data, users, services, repositories, credentials, billing, external communication, and future agents consuming corrupted context.

## Two-phase mutation
PREPARE: resolve target identity, fetch current state, validate preconditions, produce intended diff/effect.
COMMIT: execute smallest authorized mutation.
VERIFY: re-read target and test effect.
ROLLBACK: if invariant fails and rollback is safe, restore known-good state and verify restoration.

## Concurrency
Use current SHA/version/etag where available. A stale precondition is not a nuisance to bulldoze through; it is evidence another actor changed reality.
