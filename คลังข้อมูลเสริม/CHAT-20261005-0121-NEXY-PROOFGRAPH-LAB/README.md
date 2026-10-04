# NEXY ProofGraph Lab

> **AI-PROPOSED / EXPERIMENTAL / NOT CANON**  
> This package is an AI-proposed auxiliary tool stored in `AI-CONTEXT/คลังข้อมูลเสริม`. It does **not** modify the NEXY.AI implementation repository and does not promote itself into NEXY canon.

## Project map

- [Design](./DESIGN.md)
- [Requirement ledger](./REQUIREMENT-LEDGER.md)
- [Future AI-proposed concepts](./AI-PROPOSED-CONCEPTS.md)
- [Local index](./INDEX.md)
- [Executed local test evidence](./evidence/LOCAL-TEST-REPORT.md)

## Purpose

NEXY ProofGraph Lab is a deterministic, dependency-free Python tool for catching context-integrity failures before an AI turns stale or ambiguous context into confident output.

It focuses on five high-value failure modes:

1. stale authority/evidence via SHA-256 **truth locks**;
2. broken local context references;
3. misuse of the deprecated historical `215` registry as current NEXY truth;
4. conflicting current NEXY denominators (`837` normalized requirement rows and `773` Current Build rows);
5. impact analysis for context changes through reverse Markdown-reference traversal.

It also includes conservative credential-signature detection with redacted fingerprints and a rule that supplemental design prose must explicitly identify itself as experimental/proposed.

## Why it matters for NEXY

NEXY's source-derived principles separate design, implementation, runtime, deployment evidence, and authority. AI systems are particularly good at blurring those categories while sounding impressively certain. ProofGraph Lab provides deterministic checks that do not depend on model confidence.

## Commands

```bash
python -m nexy_proofgraph scan <AI_CONTEXT_ROOT> \
  --policy policy/nexy-context-policy.json \
  --fail-on ERROR

python -m nexy_proofgraph graph <AI_CONTEXT_ROOT> \
  --policy policy/nexy-context-policy.json \
  --out proofgraph.json

python -m nexy_proofgraph impact <AI_CONTEXT_ROOT> \
  --policy policy/nexy-context-policy.json \
  --changed projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md

python -m nexy_proofgraph lock <AI_CONTEXT_ROOT> \
  --paths projects/NEXY.AI/overview.md \
          projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md \
          rules/VERIFICATION.md \
  --out nexy-truth-lock.json

python -m nexy_proofgraph verify-lock <AI_CONTEXT_ROOT> --lock nexy-truth-lock.json
```

## Status model

The tool emits deterministic findings. It does not claim that a clean scan proves NEXY implementation/runtime/deployment correctness. A clean scan proves only the checks actually executed on the scanned corpus.

- Source/design claims remain source/design claims.
- Repository behavior still needs repository tests.
- Runtime behavior still needs runtime evidence.
- Deployment still needs exact-build deployment evidence.

## Scope lock

**IN SCOPE:** AI-CONTEXT integrity, local link graph, deterministic policy checks, truth-lock freshness, impact closure.  
**OUT OF SCOPE:** changing NEXY.AI code, asserting production readiness, replacing DOC-B/C/D/E authority, executing untrusted code from scanned files.
