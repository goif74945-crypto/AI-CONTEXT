# NEXY Proposal Forge

Status: **IMPLEMENTED SUPPLEMENTAL TOOL / AI-PROPOSED CONCEPT / NON-AUTHORITATIVE**

NEXY Proposal Forge is a deterministic, fail-closed sandbox for evaluating ideas proposed by AI sessions before those ideas are allowed anywhere near canonical NEXY requirements.

It exists because parallel AI work creates a predictable mess: plausible ideas are easy to generate, but proving that they are new, useful, non-conflicting, and properly evidenced is the hard part. This tool makes that review explicit.

## Authority boundary

This project does **not** modify or define NEXY.AI. It cannot promote a candidate into DOC-B, DOC-C, DOC-D, DOC-E, a build obligation, or a release decision. Every candidate must carry the literal status `AI_PROPOSED_CONCEPT`, and every evaluator output sets:

- `advisory_only = true`
- `authoritative = false`
- `deterministic = true`

The strongest positive recommendation is `PROMOTE_FOR_HUMAN_REVIEW`, not `IMPLEMENT` and not `APPROVED`.

## What it does

1. Validates a strict candidate capsule.
2. Produces a canonical SHA-256 fingerprint.
3. Compares a proposal with an existing proposal catalog.
4. Detects exact-title and near-duplicate overlap using deterministic integer scoring.
5. Checks a minimum evidence contract.
6. Fails closed on unresolved authority conflict.
7. Emits one advisory recommendation:
   - `PROMOTE_FOR_HUMAN_REVIEW`
   - `MERGE_WITH_EXISTING`
   - `NEEDS_EVIDENCE`
   - `REJECT_DUPLICATE`
   - `FREEZE_CONFLICT`
8. Compares active work manifests and reports write-scope or proposal-ID collisions before parallel sessions touch the same area.

## Design constraints

- Python standard library only.
- No network calls.
- No model calls.
- No floating-point values in canonical proposal data.
- Integer similarity scores in basis points (`0..10000`).
- Same input + same catalog => same canonical result.
- No hidden promotion path.
- Missing evidence never becomes positive authority.

## Usage

From this directory:

```bash
PYTHONPATH=src python -m nexy_proposal_forge validate examples/proposal-forge-self.json
PYTHONPATH=src python -m nexy_proposal_forge fingerprint examples/proposal-forge-self.json
PYTHONPATH=src python -m nexy_proposal_forge evaluate examples/proposal-forge-self.json --catalog examples/catalog.synthetic.json
PYTHONPATH=src python -m nexy_proposal_forge collide examples/work-manifest.current.json --catalog examples/work-manifests.synthetic.json
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/benchmark_catalog.py
```

## Important limitation

Text overlap is intentionally deterministic and dependency-free. It is not semantic omniscience. Two ideas with very different wording can still be conceptually duplicated. A low overlap score is therefore **not proof of novelty**; it is one evidence input for human/project review.
