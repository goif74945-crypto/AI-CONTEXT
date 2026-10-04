# Final Audit — NEXY Proof-Preserving Resource Governor Lab

Status: PASS for the bounded supplemental-lab acceptance criteria.
Original user duration requirement: NOT SATISFIABLE inside one synchronous chat turn and therefore not claimed.
Durable session code: CHAT-20261005-0122-NEXY-RESOURCE-GOVERNOR
Platform-native ChatGPT conversation ID: UNKNOWN_NOT_EXPOSED
Date: 2026-10-05 UTC+7

## Objective audited
Create a divergent, future-useful NEXY supplemental project in AI-CONTEXT only; explicitly mark proposed systems as AI proposals; implement real reference code; test/fix/retest it; preserve a temporary durable execution memory; and never mutate a repository whose name contains NEXY.AI.

## Result
PASS: the isolated NPRG reference lab is complete for its declared artifact/test scope.
NOT VERIFIED: NEXY.AI product integration, runtime behavior, deployment, real-provider metadata, or production performance.
NOT CLAIMED: tens of hours of continuous/background execution.

## Distinctness evidence
Prior/sibling supplemental work inspected included Experience Compiler, Human Authority Integrity, proof-carrying execution, context compilation, failure atlas, scope firewall, temporal compatibility, uncertainty debt, verification economy/proof scheduling, evidence graph, capability admission, survivability/degraded modes, epistemic economics, idempotency/replay, and compatibility evolution.

Repository commit searches returned no matching prior work for:
- resource budget governor
- token latency cost budget
- multi-agent orchestrator
- model routing
- quality budget
- cost latency quality

The NPRG scope is resource/model/worker/verifier allocation. Existing Verification Economy material schedules proof work. The two are adjacent but not the same system.

## Source authority used
The lab was grounded in AI-CONTEXT:
- AI-BOOTSTRAP.md
- INDEX.md
- AI-EXECUTION-KERNEL.md
- WORK-ROUTER.md
- rules/GLOBAL.md
- rules/VERIFICATION.md
- workflows/system-design.md
- workflows/implementation.md
- workflows/verification.md
- workflows/memory-update.md
- projects/NEXY.AI/overview.md
- projects/NEXY.AI/deep/human-control-surface.md
- projects/NEXY.AI/deep/constitutional-locks.md
- projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md

The current 837-row normalized requirement matrix remains untouched and is not expanded by this proposal.

## Artifact blob audit
The following Git blob SHAs were computed from the locally validated files and matched the corresponding AI-CONTEXT GitHub blob SHAs:

- README.md — 970c57e5c4a17f3cf25e3d6c297d5d0983192ae4
- 01_TASK_CONTRACT.md — ccd4398e1a94c154363aede3ea4a58fb8a03b24e
- 02_ARCHITECTURE.md — aacb6c2d66e3348f42bf33d3e9f6242b4292a829
- 03_REQUIREMENT_LEDGER.md — c6036e85b9fd56fa8468d6cfe9d106c6566cd385
- 04_CONTRACTS.md — 09494839360350a1b799eeea5aa5e0310eea566c
- 05_FAILURE_MODEL.md — 1524996e423125cbc5cddeeca577940ac5604c5a
- 06_INTEGRATION_PROPOSAL.md — 53672c2b4c676f5813077672b98cb69b47257db4
- 07_RESEARCH_BACKLOG.md — 70169c9ab4e6c84dd2b3892c8a898391393cf421
- 08_VALIDATION_REPORT.md — 8ae7a28ac5dd6a04af4d0c8f200558ff0abf4328
- contracts/resource-governor.schema.json — 75d30c225bceb69b1d6ffbcad97ff33623ac3301
- fixtures/scenarios.json — 3c3c495198518910cec6f20149c36b5cb5be0c8b
- src/models.py — 4235a8aec355c7b92cb582a5f012c14d5a9cac85
- src/governor.py — b23f920b4f57b2918425a31ef808d8ecfb7cca49
- src/serde.py — 1455f6a80d49ba7e1fd291992aced6e9f3abafa0
- src/__init__.py — 0c7a449087b0f89d73c78683552f33953e36ff4d
- tests/test_governor.py — 222e0c101e24b190f648533d68f150da0268a852
- tests/test_properties.py — e9e5157f470ed06fe366bb3943e83da01d577c44
- benchmarks/benchmark_governor.py — b7b37c38dd9edfaa0f734663351154d53f799e7c

This establishes exact content identity for the validated core artifact set, not merely path presence.

## E1 evidence
PASS:
- Python compilation for source, tests and benchmark harness.
- JSON syntax for schema and fixture corpus.
- JSON Schema Draft 2020-12 check_schema using jsonschema 4.26.0.
- All 4 positive fixture task/agent payloads validated against the schema.
- Negative payload with zero worker input + zero worker output tokens was rejected, aligning schema with the Python TaskProfile invariant.

## E2 evidence
PASS:
- 16 unit/adversarial tests.
- 0 failures.
- 0 errors.
- fixed-seed property-style regression over 300 generated task/inventory cases.
- input-order determinism checked.
- selected-plan capability, clearance, context, quality, evidence, independence and budget invariants checked.
- self-verification rejection checked.
- duplicate identity rejection checked.
- budget exhaustion confirmed to FREEZE rather than suppress required verification.
- every PLAN_READY result remains verification_status=NOT_VERIFIED.

## Synthetic performance evidence
Python 3.13.5, current execution container, 5 repeats:
- 50×50 = 2,500 pairs: median 4.402 ms
- 100×100 = 10,000 pairs: median 17.575 ms
- 250×250 = 62,500 pairs: median 107.020 ms
- 500×500 = 250,000 pairs: median 423.918 ms

This is an environment-specific synthetic measurement, not a production SLA.
The reference planner is O(W×V) in verifier-required time and streams the best candidate instead of retaining all feasible plans.

## Boundary audit
PASS: every mutation performed in goif74945-crypto/AI-CONTEXT.
PASS: every project artifact mutation performed under the isolated namespace:
`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-RESOURCE-GOVERNOR/`
PASS: no repository whose name contains NEXY.AI was mutated.
PASS: canonical NEXY AI-CONTEXT source/context files were read only.
PASS: sibling supplemental folders were not overwritten.
PASS: no force push, reset, rebase, merge, branch rewrite or destructive delete was used.
PASS: no secret/credential material was intentionally persisted.

## Concurrency/failure recovery
A concurrent writer changed main during a validation-report update, producing GitHub HTTP 409.
Recovery:
1. retain the already-successful ledger update;
2. refetch the current target file/blob;
3. recompute the intended isolated-file replacement;
4. retry only that file;
5. succeed without force mutation or touching sibling work.

This failure is preserved because conflict recovery is part of the evidence, not an embarrassment to hide under the rug.

## Defects found and corrected during the run
1. Initial planner retained every feasible pair: changed to streaming best-candidate selection to reduce feasible-plan working storage.
2. Self-verification loophole: closed by always forbidding worker == verifier.
3. Monolithic source organization: split into models/governor/serde modules and reran regression.
4. Requirement ledger referenced pre-refactor helper `_pair_reasons`: corrected to `_candidate_reasons`.
5. JSON Schema permitted zero worker input + zero worker output although Python contract rejected it: schema tightened and negative validation added.
6. README artifact index omitted contract/property-test files: corrected.

## Known limitations
- Agent capability, price, quality and latency metadata are trusted inputs in this reference; production provenance/freshness remains research work.
- Provider-domain inequality is only a coarse independence model.
- Pair enumeration is exhaustive O(W×V); production optimization must prove selection equivalence before replacing it.
- No E3 integration, E4 end-to-end, E5 operational/runtime, E6 deployment or E7 physical evidence exists.
- No claim is made that the NEXY.AI implementation contains NPRG.
- The user's literal request for many tens of hours of continuous execution cannot be truthfully fulfilled by a single synchronous turn. No background work is claimed.

## Final acceptance
Artifact completeness: PASS.
Exact committed-content identity for core validated files: PASS.
E1 static/schema evidence: PASS.
E2 unit/adversarial/property evidence: PASS.
Proposal labeling/non-canonical boundary: PASS.
NEXY.AI mutation boundary: PASS.
Current NEXY product implementation/runtime/deployment: NOT_VERIFIED.
Literal multi-tens-of-hours duration requirement: NOT COMPLETED / platform execution-mode limitation.
