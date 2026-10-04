# NEXY-REFLEX Design

## Status
**IMPLEMENTED STANDALONE SUPPLEMENT — NOT PART OF NEXY RUNTIME**

NEXY-REFLEX is intentionally external. It does not claim to be a NEXY subsystem and does not prove NEXY implementation/runtime correctness. It is a compatibility-oriented laboratory for validating exported control-plane facts before those facts are trusted elsewhere.

## Problem
NEXY separates design, implementation, runtime and deployment evidence. That separation is correct, but humans and tools routinely create a nasty class of failure: an evidence record survives after the thing it proved has changed, or two sources at the same authority level disagree while a downstream process quietly chooses one. Computers are very obedient about preserving yesterday's mistake.

NEXY-REFLEX addresses three narrow problems:

1. **Authority ambiguity** — find contradictory values at the highest active authority for a semantic requirement key.
2. **Evidence freshness** — bind proof to target revision/content identity and reject stale proof.
3. **Change impact** — calculate which requirements and evidence become suspect when requirements or target identity change.

## Architecture

```text
Exported Snapshot (JSON)
        │
        ▼
Strict Typed Parser
        │
        ▼
Structural Integrity Gate
        │
        ▼
Authority Resolver ──► conflict => FREEZE_RECOMMENDED
        │
        ▼
Dependency Graph Validator ──► missing/cycle => FREEZE_RECOMMENDED
        │
        ▼
Evidence Freshness + Class Matcher
        │
        ├─ stale/missing => NOT_VERIFIED + FREEZE_RECOMMENDED
        ├─ explicit fail => FAIL + FREEZE_RECOMMENDED
        ▼
Deterministic Decision + SHA-256 replay digest
```

A second path compares two snapshots:

```text
BEFORE + AFTER
     │
     ▼
Requirement identity diff
     │
     ▼
Reverse dependency closure
     │
     ▼
Evidence invalidation set
```

## Determinism contract
- Input JSON object key order is irrelevant.
- Requirement/evidence list order is irrelevant to decision digest.
- Findings are sorted deterministically.
- Hashes use canonical UTF-8 JSON and SHA-256.
- NaN and infinities are rejected rather than normalized differently across runtimes.

## Authority semantics
`authority_order` is supplied by the exporter. Earlier entries outrank later entries.

For a semantic requirement `key`:
- only the highest authority rank is allowed to decide the effective value;
- two highest-rank claims with different canonical values are a blocking `CONFLICT`;
- equal top-rank values collapse deterministically;
- lower-rank values are retained as traceable shadowed findings, never silently merged.

REFLEX does **not** invent NEXY's authority order. The exporter must provide it explicitly. This prevents a generic tool from smuggling its own governance into a system whose whole point is governance.

## Evidence semantics
Each requirement declares exact `accepted_evidence_classes` from E0–E7. REFLEX does not assume “higher number means better,” because the AI-CONTEXT verification law explicitly rejects that shortcut.

Evidence is current only when:
- `target_revision` equals the snapshot target revision; and
- when the snapshot has a content digest, evidence carries the same digest.

Current accepted `FAIL` evidence dominates absence of PASS and returns `FAIL`. Absence of current accepted PASS returns `NOT_VERIFIED`.

## Scope semantics
`EXCLUDED_CURRENT` and `DEFERRED_FUTURE` are preserved but non-gating. This matches the current NEXY matrix rule that deferred/excluded items remain traceable and are not current implementation defects.

## Failure model
REFLEX is deliberately fail-closed:
- malformed structure → input error or `BLOCKED`;
- unknown authority → `BLOCKED`;
- orphan evidence → `BLOCKED`;
- missing effective dependency → `BLOCKED`;
- dependency cycle → `BLOCKED`;
- top-authority disagreement → `CONFLICT`;
- stale/missing proof → `NOT_VERIFIED`;
- current accepted failing proof → `FAIL`.

Every non-PASS verdict maps to `FREEZE_RECOMMENDED`.

## Non-goals
- It is not a replacement for NEXY::JUDGE.
- It does not execute provider models or SWARM.
- It does not read secrets.
- It does not mutate Vault, code, policies, deployment or user law.
- It does not infer whether a NEXY feature is implemented.
- It does not convert the 837 normalized source rows into implementation truth.

## Why this is useful to NEXY
The value is in an independent, replayable boundary. A NEXY exporter can emit a snapshot before a release, migration, evidence import, or context refresh. REFLEX can then provide a deterministic second opinion that is cheap, inspectable and incapable of “helpfully” editing the system it is checking.
