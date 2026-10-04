# Verification Evidence — Directive Epoch Firewall Reference

Date: 2026-10-05
Environment:
- Python 3.13.5
- Debian GNU/Linux 13 (trixie)
- Linux kernel 6.18.44 x86_64
- Reference project: local isolated build staged for `goif74945-crypto/AI-CONTEXT`

## E1 — Static / syntax
Command:
`PYTHONPATH=src python scripts/run_validation.py`

Observed:
- `compileall` return code: 0
- JSON fixture/schema parse check: 4/4 PASS

Status: **PASS**

## E2 — Unit behavior
Executed `python -m unittest discover -s tests -v` through the validation runner.

Observed:
- 16 tests executed
- 16 passed
- 0 failed
- 0 errors

Covered negative/critical paths:
- duplicate event ID with changed content -> FREEZE;
- duplicate identical event -> idempotent;
- expected epoch mismatch -> FREEZE;
- failed directive attempt preserved in journal and replay;
- commit-induced FREEZE reproduced by full journal replay;
- irreversible action requires exact approval binding;
- journal tamper detected;
- NARROW cannot expand scope;
- NARROW invalidates old prepared action;
- out-of-scope preparation rejected;
- recovery creates new replacement epoch and old action stays invalid;
- REPLACE invalidates old action;
- deterministic replay;
- REVOKE blocks prepared action;
- payload tamper -> FREEZE;
- valid current reversible action -> ALLOW.

Status: **PASS**

## E3 — Fixture-driven protocol flow
Scenario:
1. NEW directive alpha permits READ + REVERSIBLE_WRITE.
2. Prepare reversible action under alpha/epoch 1.
3. REPLACE with beta/epoch 2, read-only.
4. Attempt old write commit.

Observed:
- decision: `FREEZE`
- code: `STALE_DIRECTIVE_EPOCH`
- final epoch: 2
- final status: `FROZEN`
- final state hash: `81a8d26f10f8938399bee8399fc4c77a2895d2e1c37e83825badbe7ab0d2c563`
- directive hash: `1c4b74a6ba58c7d8496d86b980dfe9fc67f8d89f88f8c880ba30e4b1fa48a989`
- lineage hash: `6b2826ede4b7aa7913ff657a7c4ca66fc9fcfc8da690e30878cbb2d5670f9786`

Status: **PASS**

## Deterministic adversarial stress
Command:
`PYTHONPATH=src python scripts/adversarial_validation.py`

Fixed seed: `20261005`
Trials: `5000`
Observed:
- stale attempts: 3743
- current attempts: 1257
- no stale attempt reached ALLOW
- journal replay state/head equality asserted on every trial

Output:
`PASS adversarial trials=5000 seed=20261005 stale_attempts=3743 current_attempts=1257`

Status: **PASS**

## Local benchmark observation
Command:
`PYTHONPATH=src python benchmarks/benchmark.py`

Observed on this container:
- events: 20,001
- build: 1.500952 seconds
- replay: 1.655925 seconds
- build throughput: 13,325.55 events/s
- replay throughput: 12,078.44 events/s
- journal records: 20,001
- final replay match: PASS

Status: **PASS as local benchmark observation only**.
This is not an SLO, production capacity claim, distributed throughput claim, or deployment evidence.

## Defect found and corrected during verification
Initial implementation journaled directive transitions but not commit attempts. A stale commit could move the live state to FROZEN while directive-only replay reconstructed ACTIVE state. That violated replay determinism.

Correction:
- introduced a hash-chained protocol journal;
- journaled DIRECTIVE, COMMIT and RECOVERY attempts;
- replay verifies index, previous hash, outcome, resulting state and record hash;
- added regression tests for commit-induced FREEZE and failed directive attempts.

Reverification after correction: 16/16 unit tests PASS + 5,000 adversarial trials PASS.

## Evidence limitations
NOT_VERIFIED:
- production NEXY integration;
- real database/queue transaction atomicity;
- cross-process/distributed consensus;
- cryptographic operator identity/signatures;
- deployment/runtime E5/E6 proof;
- physical or robotics integration.
