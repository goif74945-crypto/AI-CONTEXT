# CASE
CASE_ID: NEXY-BUILD-01-CORE-CLOCK-PRECEDENCE-20261004
TASK_ID: NEXY-BUILD-01-CORE-20261004
CHAT_ID: NEXY-BUILD-01-CORE
HEAD: cde969ea2d16626a60ad5571e9308ea294289d15
DESIGN_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
STATUS: CONFLICT
SEVERITY: S5_CONSTITUTIONAL

## Evidence A — earlier Layer 9 runtime determinism lock
The authoritative parsed design states:
- Core cannot read system clock.
- Allowed: TSA-injected batch time only.
- Forbidden: Date.now, system_time, monotonic_clock.
- No OS scheduling dependency.
- No sleep-based authoritative logic.
- Transitions are event-driven.
- WAL replay must not depend on current time.

## Evidence B — later G19 hardware clock-source lock
The later authoritative source states:
- authoritative layer uses Invariant TSC only;
- no HPET;
- no wall clock;
- Tick = integer counter.

The same design also contains a temporal-truth rule that older canon is historical and latest canon is active, but the clock statements are not version-labelled in a way that proves whether G19 supersedes all Layer 9 clock restrictions or only specifies a hardware source beneath them.

## Current implementation
packages/core/tick.ts blob 92ce2ae30a74d767013b322dd0d7aceb3fedd8b0:
- process.hrtime.bigint() initializes and advances the TypeScript authoritative tick.
- persisted max tick ratchets the epoch after restart.

nexy-daemon/src/main.rs blob 2a965339e215d2ee9c93e98048927ef431d78804:
- a background thread sleeps 100 ms;
- each wake calls advance_tick(100_000_000);
- current_tick() is later used by latency escalation and anchor scheduling.

core-kernel/src/auth/gatekeeper.rs blob 1a50ac5c37ba903ee94e63e8aee59108c561f0af:
- GLOBAL_TICK is an integer AtomicU64 counter;
- advance_tick(delta) changes the counter;
- current_tick() reads it.

## Decision
PRECEDENCE: UNKNOWN_PRECEDENCE
PATH_STATE: FREEZE_FOR_MUTATION

Reason:
- blindly deleting hrtime/sleep would change TTL, ordering, latency and persistence semantics across many consumers;
- treating process.hrtime as equivalent to Invariant TSC is not proven;
- treating the sleep-driven counter as deterministic is not proven because OS wake scheduling controls when deltas are injected;
- current P0 explicitly prohibits selecting the easier interpretation when specification clauses conflict.

## Required resolution proof
A valid resolution must explicitly establish:
1. active clock authority for CORE-04;
2. whether authoritative tick is event-count logical time, TSA batch time, Invariant-TSC-derived time, or a defined composition;
3. replay rule for tick values;
4. restart ratchet rule;
5. separation, if any, between security TTL/performance timers and canonical mutation ordering;
6. whether OS scheduling can affect authoritative outcomes.

No source mutation in this path is legal until the above is proven.
