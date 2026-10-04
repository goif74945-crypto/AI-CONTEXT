# NEXY Supplemental Collision Guard

**Durable work ID:** `CHAT-20261005-0122-NEXY-SUPPLEMENTAL-COLLISION-GUARD`

Status: `AI_PROPOSED_SUPPLEMENTAL_TOOLING`

This project adds a deterministic, explainable preflight guard for the `AI-CONTEXT/คลังข้อมูลเสริม` workspace. Its job is narrow: before a new supplemental project is created, compare the proposed responsibility against existing sibling work and surface likely duplicate or high-overlap workstreams.

It does **not** modify NEXY.AI, decide canonical NEXY requirements, or claim semantic equivalence from lexical similarity. It is a coordination aid for humans and agents working concurrently in AI-CONTEXT.

## Why this exists

On 2026-10-05, multiple independent chat workstreams were observed creating new supplemental projects in the same AI-CONTEXT folder within the same time window. Existing NEXY context already covers context routing, proof, reuse, privacy, reliability, and other subsystems. A new workstream therefore needs a cheap, reproducible way to ask: **"Is this project actually new, or am I rebuilding a sibling project under a different name?"**

The guard answers that question conservatively with four signals:

- `DISTINCT`
- `RELATED`
- `HIGH_OVERLAP`
- `LIKELY_DUPLICATE`

These are lexical coordination signals, not proof of semantic identity.

## Properties

- Python standard library only.
- Deterministic ordering and scoring for the same filesystem snapshot.
- Read-only scanning by default.
- Explicit output files only when requested.
- Explainable top matches with shared terms and domain tags.
- CI policy gate through `--fail-at`.
- Bounded reads: at most 80 supported text files per project and 32,000 bytes per file.
- Generated/cache directories are ignored to prevent self-referential fingerprint drift.
- Symlinked project directories and symlinked files are ignored to prevent scanning outside the intended project boundary.
- Invalid or non-discriminating candidate descriptions fail closed.

## Quick use

```bash
python src/collision_guard.py scan \
  --root /path/to/AI-CONTEXT/คลังข้อมูลเสริม \
  --output generated/catalog.json
```

```bash
python src/collision_guard.py check \
  --root /path/to/AI-CONTEXT/คลังข้อมูลเสริม \
  --title "NEXY Supplemental Collision Guard" \
  --summary "detect duplicate parallel supplemental projects and explain overlap" \
  --fail-at HIGH_OVERLAP
```

Exit code `2` means the configured overlap policy threshold was reached or the CLI rejected invalid input. Exit code `0` means the command completed and the configured threshold was not reached.

## Scoring model

For each existing project:

```text
score = 0.60 * candidate-term-containment
      + 0.25 * term-jaccard
      + 0.15 * tag-jaccard
```

Thresholds:

| Score | Classification |
|---:|---|
| `>= 0.93` | `LIKELY_DUPLICATE` |
| `>= 0.62` | `HIGH_OVERLAP` |
| `>= 0.38` | `RELATED` |
| `< 0.38` | `DISTINCT` |

The high duplicate threshold is intentional. A large existing project often contains many terms from a smaller candidate brief, so containment alone must not be promoted into an identity claim.

## Files

- `00_SESSION_MEMORY.md` — resumable mission state.
- `01_PROJECT_SPEC.md` — authority, scope, contracts, architecture, failure semantics.
- `02_IMPLEMENTATION_PLAN.md` — executed TDD plan and verification gates.
- `03_AI_PROPOSED_FUTURES.md` — future ideas, explicitly not current requirements or implemented behavior.
- `04_REQUIREMENT_EVIDENCE_LEDGER.md` — requirement-to-evidence mapping.
- `05_VALIDATION_REPORT.md` — local verification and remediation history.
- `PROJECT-MANIFEST.json` — SHA-256 integrity manifest for immutable project payload.
- `schema/collision-report.schema.json` — report contract.
- `src/collision_guard.py` — reference implementation and CLI.
- `tests/test_collision_guard.py` — unit, policy, determinism, and security-boundary tests.

## Non-goals

This v1 does not use embeddings, LLM judges, vector databases, source-code semantics, or automatic project deletion/merging. It never mutates a sibling supplemental project. Those choices are deliberate: the preflight guard should remain cheap, inspectable, offline-capable, and unable to turn a fuzzy similarity guess into a destructive action.
