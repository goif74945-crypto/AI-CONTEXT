# NFWM Task Contract

## Identity

- Work ID: `AICTX-NFWM-20261005T0138+0700`
- Platform conversation/chat ID: `UNKNOWN` — no authoritative platform chat identifier is exposed to this execution environment.
- Target repository: `goif74945-crypto/AI-CONTEXT`
- Target area: `คลังข้อมูลเสริม/<isolated NFWM folder>`
- Protected repository: every repository whose name contains `NEXY.AI`, including `NEXY.AI-`

## Objective

Design, implement, test, and preserve an AI-proposed external tool that converts a failing NEXY-style event trace into a deterministic, replayable, 1-minimal failure witness while remaining completely outside the NEXY.AI implementation repository.

## Authority sources

1. Current user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. Current NEXY project context under `projects/NEXY.AI/`.
5. Executed local test evidence for NFWM claims.

## Authorized scope

- Add a new isolated project under `AI-CONTEXT/คลังข้อมูลเสริม/`.
- Add design, requirements, code, fixtures, tests, evidence, and resumption state for this project.
- Read NEXY context from AI-CONTEXT to derive an external compatibility profile.
- Execute NFWM code/tests in an isolated local environment.

## Protected scope

- No write, branch, merge, commit, push, workflow, setting, issue, PR, rename, delete, or file mutation in any repository containing `NEXY.AI`.
- No claim that NFWM is canonical NEXY law or deployed runtime behavior.
- No credentials or secrets persisted.
- No silent expansion into unrelated AI-CONTEXT systems.

## Success invariants

- Source code exists and imports using Python 3.11+.
- Runtime dependency set is empty outside the Python standard library.
- Valid trace returns PASS.
- Invalid trace returns deterministic reason codes.
- Release-after-freeze fixture minimizes to a 2-event 1-minimal witness.
- Duplicate-idempotency fixture minimizes to a 2-event 1-minimal witness.
- Witness replay detects hash tampering.
- Canonical hashing is independent of dictionary key insertion order.
- Design clearly separates SOURCE_FACT, AI_PROPOSAL, and RUNTIME_EVIDENCE.
- `NEXY.AI-` receives zero mutations from this work.

## Required evidence

- E1: `python -m compileall -q src tests`.
- E2: `PYTHONPATH=src python -m unittest discover -s tests -v`.
- E2: executed CLI PASS/FAIL paths.
- E2: executed witness replay verification.
- Presence/hash inventory of committed project files.

## Stop conditions

Freeze mutation if:

- target repo identity becomes ambiguous;
- the destination would touch a repository containing `NEXY.AI`;
- an authoritative source conflicts materially with the design;
- current destination path collides with unrelated existing work;
- verification fails and cannot be repaired within the authorized project scope.
