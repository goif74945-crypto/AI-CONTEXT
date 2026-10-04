# NEXY Freeze Bridge Lab

> **AI-PROPOSED CONCEPT / REFERENCE IMPLEMENTATION / ADVISORY ONLY**
>
> This directory does not claim that NEXY.AI currently implements this system. It is an isolated supplemental research + executable reference project stored in AI-CONTEXT only.

## One-line idea

**Machine FREEZE in → deterministic human recovery card out, with no authority expansion.**

NEXY's strict freeze behavior protects correctness, but a user still needs to understand:
- what category of problem blocked progress;
- what information is genuinely missing;
- who owns recovery;
- which actions are actually authorized;
- whether retry is legal;
- which evidence can be shown safely.

Freeze Bridge is designed as a presentation/control-boundary compiler. It does **not** decide truth, change Core state, resolve conflicts, grant permission, or manufacture recovery actions.

## Session identity

- Session code: `NEXY-FREEZE-BRIDGE-20261005-0121-ICT`
- Platform chat ID: **UNKNOWN** because the available tools do not expose it.
- Target namespace: `คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-FREEZE-BRIDGE-LAB/`
- NEXY.AI implementation repository mutations: **FORBIDDEN / NONE**

## Why this is distinct

Recent supplemental work already covers proof lineage, uncertainty debt, compatibility/evolution, knowledge decay, verification economy, causal debugging, replay/idempotency, privacy egress, preference sovereignty and resource governance.

This project instead concentrates on **human-safe recovery semantics after a correct freeze decision**.

## Reference implementation

Language: Python 3.11+  
Runtime dependencies: Python standard library only.

Key properties:
- strict input normalization;
- deterministic action ordering;
- reason-policy intersection with pre-authorized actions;
- unknown-reason fallback without cause invention;
- restricted-evidence suppression;
- security/integrity freezes cannot become retryable;
- Thai and English user-facing text;
- SHA-256 fingerprint bound to normalized input + policy output;
- CLI that reads JSON and emits JSON;
- JSON Schema contracts;
- negative-path tests;
- exhaustive policy matrix self-check.

## Local verification snapshot

- Unit/negative tests: **21/21 PASS**
- Production library line + branch coverage: **100%**
- Policy-matrix cases: **330 PASS**
- `compileall`: **PASS**
- CLI JSON round-trip: **PASS**
- Example benchmark: **~28.8k compile operations/sec** in the current sandbox, 50,000 iterations. This is environment-specific and is **not** a production SLA.

## Directory map

- `00_EXECUTION_STATE.md` — durable temporary execution memory.
- `01_PROJECT_CHARTER.md` — task contract and scope lock.
- `02_ARCHITECTURE.md` — module/data/authority architecture.
- `03_PROTOCOL_SPEC.md` — event and recovery-card protocol.
- `04_POLICY_MATRIX.md` — reason/action/failure policy.
- `05_SECURITY_THREAT_MODEL.md` — disclosure and misuse threats.
- `06_INTEGRATION_GUIDE.md` — future integration boundary.
- `07_ADOPTION_GATES.md` — conditions before any real promotion.
- `08_TEST_AND_BENCHMARK_REPORT.md` — evidence from this run.
- `09_FUTURE_IDEAS.md` — clearly marked AI proposals only.
- `freeze_bridge/` — executable reference package.
- `schema/` — JSON contracts.
- `fixtures/` — example/negative fixtures.
- `tests/` — unit + negative-path test suite.
- `tools/` — policy self-check and benchmark.
- `10_FINAL_AUDIT.md` — final verification boundary.

## Non-goals

This lab does not:
- mutate NEXY Core decisions;
- redefine DOC-B/C/D/E;
- alter current 837-row source scope;
- bypass freeze;
- grant permissions;
- implement deployment/runtime integration;
- claim UI completion;
- claim release readiness.

Promotion into real NEXY scope would require explicit authorization plus current build-spec mapping and matching implementation/runtime evidence.
