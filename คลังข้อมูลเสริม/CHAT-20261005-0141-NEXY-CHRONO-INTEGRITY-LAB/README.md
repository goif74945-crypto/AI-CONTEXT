# NEXY Chrono Integrity Lab

**Status:** AI-PROPOSED CONCEPT + VERIFIED STANDALONE REFERENCE PROTOTYPE  
**Authority:** Supplemental/advisory only. Not DOC-B, not DOC-C, not current NEXY implementation, and not deployment evidence.  
**Workstream ID:** `CHAT-20261005-0141-NEXY-CHRONO-INTEGRITY-LAB`  
**Platform chat ID:** `UNKNOWN` because the platform identifier is not exposed to this execution context.  
**Repository boundary:** This workstream lives only in `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/`. It must not mutate any repository whose name contains `NEXY.AI`.

## Executive summary

NEXY has or may have time-sensitive controls such as authentication-code TTLs, sessions, rate windows, authority leases, replay/idempotency windows, queue deadlines, evidence freshness, cancellation grace periods, and retry budgets. A civil wall clock is unsafe as the sole lifetime authority because wall time can step forward, step backward, be corrected, or change independently of elapsed execution time.

This project proposes a deterministic low-level primitive:

- **monotonic time** decides elapsed lifetime and exact activation/expiration boundaries;
- **wall time** is cross-checked against monotonic elapsed time to detect suspicious divergence;
- clock identity, monotonic epoch, rollback, or excessive divergence failures become explicit `FREEZE`;
- child deadline budgets can only narrow a parent deadline;
- serialized envelopes are strict, canonical, and fingerprinted for lineage;
- identical envelope + identical sample produces an identical decision without hidden I/O or model behavior.

The reference prototype is dependency-free Python and intentionally standalone. It does not modify or integrate with NEXY.AI.

## Distinction from existing supplemental work

This workstream was selected after inspecting the current supplemental inventory and comparing nearby concepts.

- **Temporal Truth and Validity** concerns whether a proposition remains admissible based on authority, dependency identity, validity interval, supersession, and knowledge time.
- **NEXY::LEASE** concerns bounded execution authority tied to a concrete plan and finite delegated budget.
- **Chrono Integrity** concerns only whether an elapsed-time decision is safe under clock-continuity constraints.

Chrono Integrity therefore does not replace either system. It can be a future primitive beneath them.

## Verified standalone evidence

- E1 compile/static syntax: `PASS`.
- E2 behavior suite: `PASS`, 42/42 tests.
- E2 example: `PASS`.
- Randomized invariant corpus: 1,000 within-skew cases + 500 above-skew freeze cases.
- E3 NEXY integration: `NOT_VERIFIED`.
- E4 end-to-end NEXY flow: `NOT_VERIFIED`.
- E5 target-runtime clock fault qualification: `NOT_VERIFIED`.
- E6 deployment: `NOT_VERIFIED`.

---

# 1. Task Contract

## Objective

Create a novel, useful, non-duplicative supplemental engineering project that could be integrated with NEXY in the future while never modifying any repository whose name contains `NEXY.AI`.

## Target

`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0141-NEXY-CHRONO-INTEGRITY-LAB`

## Authorized scope

- additive files under the target folder only;
- standalone clock/deadline integrity reference kernel;
- local static and unit/property-style tests against exact publish content;
- explicit evidence and limitations;
- future integration ideas labeled as proposals.

## Protected scope

- every repository whose name contains `NEXY.AI`;
- existing supplemental workstreams outside this folder;
- canonical NEXY law/spec files;
- secrets and credentials.

## Authority sources

1. Current explicit user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. `projects/NEXY.AI/overview.md` and the current source-normalization boundary.
5. Existing supplemental artifacts for collision detection only.

## Success invariants

1. No mutation to any NEXY.AI repository.
2. Work remains explicitly supplemental and AI-proposed.
3. Wall time alone never decides a TTL.
4. Monotonic rollback, epoch mismatch, clock-ID mismatch, or excessive wall/monotonic divergence cannot produce executable `VALID`.
5. Exact expiry semantics are deterministic: `elapsed >= timeout => EXPIRED`.
6. Child deadline cannot exceed parent remaining lifetime.
7. Same envelope + same sample yields the same decision.
8. Serialized envelopes reject unknown/missing/type-invalid fields.
9. Published executable files must be byte-identical to the locally tested set.

## Forbidden behavior

- treating this proposal as current NEXY law or implementation;
- changing NEXY.AI repositories, settings, branches, issues, PRs, workflows, or files;
- claiming E3-E6 proof from local unit tests;
- hidden provider/network dependencies;
- guessing malformed serialized fields;
- silently comparing monotonic timestamps across unknown epochs.

---

# 2. Architecture

## 2.1 Clock authority split

```text
issue TimeSample
  wall_ns --------------------┐
  monotonic_ns ----┐          │
                   v          v
             DeadlineEnvelope
                   |
                   v
current sample -> integrity checks -> monotonic elapsed -> lifetime state
                    |                         |
                    | unsafe                  | safe
                    v                         v
                  FREEZE     NOT_YET_VALID / VALID / EXPIRED
```

- `monotonic_ns` is authoritative for elapsed lifetime inside one monotonic epoch.
- `wall_ns` is cross-check evidence, not TTL authority.
- `clock_id` prevents accidental cross-provider comparison.
- `monotonic_epoch` prevents comparison across an unknown restart/boot/process continuity boundary.

## 2.2 Data contracts

### TimeSample

- non-negative `wall_ns`;
- non-negative `monotonic_ns`;
- non-empty `clock_id`;
- non-empty `monotonic_epoch`.

### DeadlineEnvelope

Immutable fields bind:

- envelope identity;
- clock identity and monotonic epoch;
- wall and monotonic issue observations;
- activation delay;
- finite timeout;
- maximum tolerated wall-vs-monotonic elapsed divergence;
- policy version;
- purpose;
- optional parent envelope identity.

The canonical JSON form is SHA-256 fingerprinted. The fingerprint is lineage metadata, not caller authentication.

### ChronoDecision

States:

- `VALID`
- `NOT_YET_VALID`
- `EXPIRED`
- `FREEZE`

Reason codes make failure explicit, including clock-ID mismatch, monotonic epoch mismatch, rollback, wall/monotonic divergence, invalid parent, and exhausted child budget.

## 2.3 Evaluation order

1. clock identity must match;
2. monotonic epoch must match;
3. monotonic elapsed must not be negative;
4. wall/monotonic elapsed divergence must be within policy;
5. activation boundary is evaluated;
6. exact timeout boundary is evaluated;
7. otherwise the envelope is valid.

Clock integrity is checked before ordinary lifetime state so an invalid clock cannot masquerade as a normal expiration.

## 2.4 Boundary law

- `elapsed < activate_after => NOT_YET_VALID`
- `activate_after <= elapsed < timeout => VALID`
- `elapsed >= timeout => EXPIRED`

## 2.5 Child deadline propagation

`child_timeout = min(requested_timeout, parent_remaining)`

If the parent is not `VALID`, no child is emitted. A child can narrow but never amplify its parent's remaining time budget.

## 2.6 Determinism boundary

The evaluator performs no network access, filesystem access, model call, randomness, or system-clock read. System clock acquisition is deliberately separated from the pure decision function.

---

# 3. Requirement Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| CHR-001 | TTL uses monotonic elapsed | `evaluate` | boundary tests | PASS E2 |
| CHR-002 | wall clock is cross-check only | delta check | drift tests | PASS E2 |
| CHR-003 | clock ID mismatch freezes | `evaluate` | negative test | PASS E2 |
| CHR-004 | epoch mismatch freezes | `evaluate` | negative test | PASS E2 |
| CHR-005 | monotonic rollback freezes | `evaluate` | negative test | PASS E2 |
| CHR-006 | excessive divergence freezes | `evaluate` | drift tests | PASS E2 |
| CHR-007 | exact timeout edge expires | closed timeout | exact + 1ns-before tests | PASS E2 |
| CHR-008 | activation edge deterministic | activation branch | boundary tests | PASS E2 |
| CHR-009 | child cannot outlive parent | `derive_child` | cap tests | PASS E2 |
| CHR-010 | invalid parent emits no child | `derive_child` | negative tests | PASS E2 |
| CHR-011 | canonical serialization stable | canonical JSON | key-order test | PASS E2 |
| CHR-012 | malformed shapes rejected | strict parser | shape/type tests | PASS E2 |
| CHR-013 | same input deterministic | pure evaluator | replay test | PASS E2 |
| CHR-014 | package has no runtime deps | package/code | compile + inspection | PASS E1 |
| CHR-015 | target-runtime clock semantics proven | future harness | none | NOT_VERIFIED |
| CHR-016 | actual NEXY integration proven | future task | none | NOT_VERIFIED |

---

# 4. Failure and Threat Model

## Wall clock rollback

A wall-only TTL could unintentionally extend a credential/session. This kernel uses monotonic elapsed lifetime; excessive divergence becomes `FREEZE`.

## Wall clock jump forward

A wall-only lifetime could expire work prematurely. Monotonic lifetime remains authoritative; excessive divergence freezes.

## Monotonic rollback

A negative monotonic elapsed value indicates broken continuity, stale/fabricated input, or an invalid source. It freezes.

## Restart/epoch discontinuity

Process/boot-local monotonic readings from unrelated epochs are not comparable. An epoch mismatch freezes.

## Different clock providers

Equal numeric values do not guarantee equal semantics. Clock-ID mismatch freezes.

## Deadline amplification

Nested work could incorrectly receive a fresh full TTL and outlive its parent authority. Child budget is capped at parent remaining budget.

## Serialization smuggling

Permissive deserialization can silently add semantics. Exact keys are required; unknown/missing/type-invalid fields are rejected.

## Host compromise

A hostile host can fabricate both wall and monotonic clocks. This prototype does not claim trusted time under host compromise. Such a claim needs an external trust design and matching runtime/deployment evidence.

## Suspend/resume and VM snapshot semantics

Python unit tests do not prove platform-specific behavior under sleep, hibernation, migration, or snapshot restore. These remain promotion-gate obligations.

---

# 5. Future NEXY Integration Contract

This section is **AI_PROPOSAL**, not current scope.

A future adapter should expose only stable operations equivalent to:

- sample an authorized dual-clock provider;
- issue a deadline envelope under a named policy;
- evaluate an envelope;
- derive a narrower child envelope;
- record reason codes, lineage, and fingerprints.

The generic kernel should remain policy-neutral. Authentication/session/queue/lease components should own their own policy values.

## Promotion gate

Do not promote this project into canonical NEXY until an independently authorized task proves:

1. real implementation language/runtime compatibility;
2. platform-specific monotonic semantics;
3. persistence/restart behavior for existing envelopes;
4. distributed/multi-node behavior if envelopes cross nodes;
5. observability mapping;
6. compatibility with current auth/session/queue/lease semantics;
7. abuse and negative testing;
8. E3/E4/E5 evidence appropriate to the claim.

No standalone Python test substitutes for those proofs.

---

# 6. Verification Plan

## E1

`PYTHONPATH=src python -m compileall -q src tests examples`

## E2

`PYTHONPATH=src python -m unittest discover -s tests -v`

`PYTHONPATH=src python examples/demo.py`

The suite includes 42 deterministic/boundary/negative tests and randomized corpora.

## E0 publication

After publication:

- enumerate target folder;
- fetch critical files;
- compare Git blob IDs against locally computed exact bytes;
- record commit/presence evidence.

---

# 7. AI-Proposed Future Research

The ideas below are proposals only.

### Restart continuity ticket
Explore an authority-bound restart artifact that can prove whether an old envelope may be reconstructed after monotonic epoch change. Default remains fail-closed.

### Time-source quorum
For higher assurance distributed flows, compare independent time signals and freeze on material disagreement.

### Deadline algebra
Define deterministic `min(parent, user, policy, dependency)` propagation with proof lineage.

### Clock fault observability
Aggregate divergence values and freeze reason codes to surface host/VM timing faults.

### Temporal chaos qualification
Inject clock steps, slews, suspend/resume, restart, VM restore, and multi-node skew in the real target runtime to earn E5 evidence.

### Auth policy profile
If canonical NEXY authority later approves adoption, map current DOC-C authentication/session values through an adapter rather than hard-coding product policy into this generic kernel.

---

# 8. Repository Layout

- `README.md` — task contract, architecture, ledger, failure model, promotion gate, ideas.
- `EXECUTION_STATE.md` — final resumable state and publication proof.
- `src/nexy_chrono_integrity.py` — reference implementation.
- `tests/test_chrono_integrity.py` — 42-test suite.
- `examples/demo.py` — deterministic example.
- `evidence/TEST-EVIDENCE.md` — test commands, results, hash boundary.
- `memory/TEMP_WORKING_MEMORY.md` — resumption checkpoint.
- `pyproject.toml` — package metadata.

# 9. Audit Boundary

Standalone reference semantics are verified at E1/E2 only. Actual NEXY integration, end-to-end behavior, target-runtime clock fault tolerance, and deployment remain `NOT_VERIFIED`.

Repository publication is not considered complete until `EXECUTION_STATE.md` records the post-publication fetch-back verification.
