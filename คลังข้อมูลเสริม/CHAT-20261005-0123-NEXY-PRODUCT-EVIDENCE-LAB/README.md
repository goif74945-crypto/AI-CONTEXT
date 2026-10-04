# NEXY Product Evidence Lab (NPEL)

> **AI-PROPOSED / NON-GOVERNING R&D ARTIFACT**
>
> This project is a supplemental reference implementation. It is not canonical NEXY architecture, not part of the 837-row current-build matrix, and not evidence that NEXY.AI implements these behaviors.

NPEL turns product ideas into explicit, falsifiable experiment contracts and evaluates completed evidence without silently guessing missing facts or auto-authorizing product changes.

## Why this exists

A product team can easily optimize for activity rather than user value. NPEL forces a proposal to state the population, primary metric, baseline, minimum detectable effect (MDE), confidence level, power, guardrails, duration, and risk flags before it can become an experiment contract.

The reference engine then:

1. validates the proposal;
2. freezes prohibited or materially underspecified experiments;
3. computes deterministic per-arm sample-size planning;
4. emits a canonical JSON contract with SHA-256 identity;
5. validates analytics event contracts without allowing common secret-bearing fields;
6. evaluates exact-contract evidence as `SUPPORTED`, `REJECTED`, `INCONCLUSIVE`, or `FREEZE`;
7. always marks the final product decision as human-owned.

## NEXY alignment

The lab intentionally mirrors NEXY principles documented in AI-CONTEXT: human authority, zero-guess behavior, explicit uncertainty, evidence-bound output, deterministic control logic, and freeze rather than unsafe continuation.

## Reference scope

Reference v1 requires a 50/50 control/treatment allocation. Unequal allocation is rejected rather than approximated silently.

Supported primary metric families:

- binary/proportion metrics;
- continuous/mean metrics with an explicit planning standard deviation.

The engine uses normal-approximation planning/evaluation. It does not claim to replace a production experimentation platform, sequential testing framework, causal inference system, or domain-specific safety review.

## Run locally

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Example

```bash
PYTHONPATH=src python -m nexy_product_evidence.cli compile examples/proposal.json
```

The output includes a canonical contract and `contract_hash`. Any later evaluation must provide that exact hash.

## Status

See `11_VALIDATION_REPORT.md` and `13_FINAL_AUDIT.md`. File presence is not proof of PASS.
