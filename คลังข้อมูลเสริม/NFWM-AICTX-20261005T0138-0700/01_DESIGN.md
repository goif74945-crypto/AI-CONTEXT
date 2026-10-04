# NFWM Design

## 1. Status classification

### SOURCE_FACT
AI-CONTEXT currently records NEXY design/build rules involving deterministic state transitions, explicit FREEZE/STOP behavior, idempotency, incident linkage, structured errors/evidence, and no release through unresolved failure. The source context also requires evidence to match the claim type.

### AI_PROPOSAL
NFWM itself is an AI-proposed external diagnostic tool. It is not listed as a canonical NEXY subsystem and must not be represented as one.

### RUNTIME_EVIDENCE
Only NFWM's own local parser/analyzer/minimizer/CLI behavior is executed and verified here. NEXY.AI runtime compatibility remains `NOT_VERIFIED` because this work intentionally does not mutate or execute the NEXY.AI repository.

## 2. Problem

A failure may appear inside thousands or millions of event records. Copying the whole trace into a bug report creates four problems:

1. humans and AI must repeatedly inspect irrelevant events;
2. regression tests become bulky and difficult to reason about;
3. private or unrelated log material is unnecessarily propagated;
4. a failure description may drift because the exact minimal reproducer is unknown.

## 3. Core idea

NFWM defines a pure function around a configured profile:

`Analyze(profile, ordered_events) -> violation_set`

For one selected violation code, NFWM applies deterministic delta debugging and a final single-deletion closure:

`Minimize(events, predicate(code still present)) -> 1-minimal witness`

A witness is **1-minimal** when removing any single remaining event makes the selected violation class disappear.

This is deliberately weaker and more honest than claiming a globally minimum witness.

## 4. Architecture

```text
Trace JSON
   |
   v
Strict Schema Parser ------> ValidationError / exit 64
   |
   v
Profile Loader
   |
   v
Invariant Analyzer --------> PASS or sorted violations
   |
   +---- selected violation code
   v
Deterministic ddmin
   |
   v
Single-deletion closure
   |
   v
Canonical witness JSON
   |
   +--> SHA-256 witness hash
   +--> replay verifier
```

### Modules

- `model.py` — strict event/trace boundary.
- `profile.py` — profile parsing and transition contract.
- `analyzer.py` — deterministic invariant evaluation.
- `minimize.py` — ddmin + 1-minimality proof helper.
- `canonical.py` — canonical JSON + SHA-256.
- `io.py` — explicit UTF-8 file boundary.
- `cli.py` — stable process interface and exit codes.

## 5. State/data contract

Each event requires:

- `seq`
- `kind`
- `trace_id`
- `request_id`

Optional declared fields:

- `run_id`
- `idempotency_key`
- `state_from`
- `state_to`
- `incident_id`
- `metadata`

Unknown top-level event fields fail closed. Extensible content belongs under `metadata`.

## 6. Determinism invariants

- Input order is preserved.
- Violation ordering is sorted by `(code, event_seqs, message)`.
- Profile collections become immutable sets/tuples.
- JSON hashing is canonical.
- No wall-clock time enters output.
- No random selection enters minimization.
- Partitioning order and deletion order are stable.
- Same profile + same trace + same NFWM version produces the same witness bytes for implemented rules.

## 7. Failure semantics

NFWM separates four classes:

- input invalid → fail closed with exit `64`;
- input valid and no violation → PASS / exit `0`;
- input valid and violation exists → FAIL / exit `2` plus violations/witnesses;
- witness fails integrity/minimality replay → FAIL / exit `3`.

There is no fallback that silently drops malformed events.

## 8. Security boundary

- Runtime uses no network.
- No shell execution occurs in library code.
- No dynamic import from trace/profile content.
- No `eval`/`exec`.
- No credentials are needed.
- Unknown event fields fail rather than being interpreted as executable configuration.
- Evidence hashes detect witness-content drift, not malicious filesystem or interpreter compromise.

## 9. Complexity

For `n` events and an invariant evaluator approximately O(n), ddmin typically requires repeated linear scans over shrinking subsets. This v0.1 optimizes for deterministic correctness and debuggability over asymptotically optimal minimization.

Future streaming/index acceleration is proposed separately and is not falsely presented as implemented.

## 10. NEXY integration boundary

A future integration could export sanitized event bundles from NEXY observability into NFWM and import only the resulting witness as a debugging artifact. That integration is **proposal only**. NFWM currently has no direct NEXY API dependency and therefore cannot mutate NEXY state.
