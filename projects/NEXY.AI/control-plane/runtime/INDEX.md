# NEXY.AI Executable Closed-Loop Runtime

## Purpose
This directory is the first executable runtime layer for the previously structural P4.1-P4.16 control plane.

The runtime closes the coordination loop:

`AUDIT → COMMAND → SCHEDULE → CLAIM → HEAD GUARD → BUILDER → RESULT → RE-AUDIT → VERDICT → NEXT COMMAND / CONVERGENCE`

It is intentionally provider-agnostic. The runtime does **not** pretend it can directly control a ChatGPT/Work session. External worker adapters exchange machine-readable packets through the filesystem spool or another explicitly implemented adapter.

## Files
- `loop_engine.py` — SQLite-backed deterministic scheduler/control loop.
- `runtime-envelope.schema.json` — runtime metadata wrapped around the canonical command record.
- `test_loop_engine.py` — executable regression tests for the control core.
- `examples/golden-command-envelope.json` — valid runtime command envelope.
- `validation-report.md` — exact local validation evidence for this revision.

## Runtime authority
SQLite is authoritative only for **dynamic coordination state**: queue, claims, leases, worker assignment, results, verification jobs, and event sequence.

Git/AI-CONTEXT remains authoritative for versioned definitions, laws, schemas, playbooks, and durable engineering evidence.

No runtime state can override governance, expected-HEAD checks, protected scope, human gates, or evidence requirements.

## Determinism
Scheduler order is:

1. priority rank;
2. enqueue sequence;
3. command ID lexical order.

Wall clock is used for lease expiry and polling only; it is not a tie breaker. No RNG/jitter is used.

## Concurrency
Dispatch requires:
- dependencies completed;
- exact target HEAD known and matching;
- eligible worker/capability/scope;
- no active path/resource/dependency claim collision;
- explicit human approval when required.

## Re-audit rule
A Builder PASS does **not** complete a command. It moves the command to `VERIFYING` and creates a verification job for an Auditor. Only an Auditor PASS with evidence can move the command to `COMPLETED`.

## 24/7 spool mode
Run:

```bash
python3 loop_engine.py --db /var/lib/nexy/control.sqlite --spool /var/lib/nexy/spool
```

The runtime watches:
- `inbox/heads/`
- `inbox/workers/`
- `inbox/commands/`
- `inbox/acks/`
- `inbox/heartbeats/`
- `inbox/results/`
- `inbox/approvals/`

and emits dispatch packets to:

`outbox/<worker_id>/`

Create a `STOP` file in the spool root for a clean loop stop.

## Safety boundary
This runtime does not contain credentials, does not invoke production actions itself, and does not grant NEXY implementation mutation authority. A real worker adapter must be separately authorized and tested before live autonomous execution is claimed.
