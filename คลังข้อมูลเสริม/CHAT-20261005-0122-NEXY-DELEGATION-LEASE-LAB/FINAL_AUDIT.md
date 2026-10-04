# FINAL AUDIT — NEXY Delegation Lease Lab

Workstream: `CHAT-20261005-0122-NEXY-DELEGATION-LEASE-LAB`
Audit time context: 2026-10-05 +07
Scope: supplemental reference artifact in `goif74945-crypto/AI-CONTEXT` only.

## Status

**PASS — reference artifact integrity and executed local behavior evidence.**

This PASS does not mean NEXY production integration, deployment, or canonical adoption.

## Delivery lineage

- Main documentation/reference merge: PR #12, merge commit `50455d6d8624cfe26ff37cd40ffda60a53279c6c`.
- Exact tested-byte/final evidence correction: PR #19, merge commit `a9682b9cd4d60ec473dcb37937c6d33d2b3f0ae3`.
- Repository main observed during final re-read: `7abc88dad097ab822029c133f35e676cf7335247`.

## Executed evidence

Local reference package:
- compile: PASS;
- unit suite: 21/21 PASS;
- schemas parse as JSON: PASS;
- exact demo allowed path: PASS.

The first journal test failure was retained in `evidence/TEST-EVIDENCE.md`; root cause was a slotted dataclass being accessed through `__dict__`, corrected using `dataclasses.replace`.

## Main-branch byte identity

GitHub `main` was re-read after the correction merge. All expected Git blob SHA values matched:

| Artifact | Blob SHA | Match |
|---|---|---|
| model.py | `1cf018d963361f36a1528a01c2b205ecd5a234a7` | PASS |
| canonical.py | `3dad124e335f23f5ebcc336d23c97a8688fa5640` | PASS |
| policy.py | `61e13678a4d1ff7d076ebd3f3e0984248e43bec3` | PASS |
| journal.py | `10f36b96388fbaafc7bfc118c7c8c80ecb03f203` | PASS |
| __init__.py | `d13bf4e676cb56eced96851fa307f38ed2b5ff11` | PASS |
| test_policy.py | `4b24a593c09051202eb8392fee26f5aaf5568384` | PASS |
| reference README | `777d70b7ff81ae44686fe23f48472035410d37ff` | PASS |
| action-plan schema | `8677a380ee4537f848fb6cd3da8ea46cbfda8357` | PASS |
| authority-lease schema | `5bb4d1047c7f5ccd5539568430c693f52c1bd6ce` | PASS |
| demo.py | `30f6af16f6dfb4c9228b46563c90af24f5c2ea2a` | PASS |
| pyproject.toml | `a3b0193f29a9dc3cde32050e522f076346c6fd4b` | PASS |
| 00_EXECUTION_STATE.md | `4e39ee48bdb108b931e1c8db49f7ac924bc8fcb8` | PASS |
| TEST-EVIDENCE.md | `72814c530f556c37fe283af59b1dea742930754b` | PASS |

## Protected-scope audit

No repository whose name contains `NEXY.AI` was mutated by this workstream.

All durable writes were directed to `goif74945-crypto/AI-CONTEXT`, primarily the dedicated path:
`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-DELEGATION-LEASE-LAB/**`.

Concurrent writes by other sessions caused 409/non-fast-forward/base-modified errors. No force update was used. Dedicated branches and PR merges preserved concurrent main history.

## Truth boundary

**FACT:** the standalone reference policy behavior listed in the executed suite passed and the tested artifacts were byte-matched to main.

**AI-PROPOSED:** NEXY::LEASE architecture, UX, promotion path, effect vocabulary, and future backlog.

**NOT_VERIFIED:** NEXY integration, distributed revocation, production concurrency atomicity, cryptographic attribution, provider resource identity, deployment, performance, usability benefit, and full JSON Schema meta-validation.

## Stop condition

Do not treat this lab as canonical NEXY law. Any integration requires explicit authorization, specification promotion, and the evidence gates defined in `06_INTEGRATION_AND_PROMOTION_GATE.md`.
