# NEXY Consensus Independence Firewall (NCIF)

**Classification:** EXPERIMENTAL / AI-PROPOSED / NON-GOVERNING REFERENCE LAB

NCIF is a deterministic reference system for detecting pseudo-consensus in multi-agent workflows. It asks a narrower question than “how many agents agree?”:

> How many materially independent evidence lineages support or oppose the claim?

The prototype collapses correlated votes into connected independence groups using evidence ancestry, root source identity, and caller-declared correlation keys. It fails closed on malformed provenance, cycles, unsupported evidence claims, independently evidenced opposition beyond policy, and optional single-root fragility.

## Authority boundary

NCIF is **not** NEXY.AI law, is not integrated into NEXY.AI, and does not replace CORE or JUDGE. A `CONSENSUS_CANDIDATE` result means only that the supplied provenance contract satisfies this prototype's independence policy. It is not a truth verdict, release authorization, or deployment proof.

## Why it exists

NEXY context requires multi-model work, adversarial review, cross-verification, proof-weighted consensus, provider/model independence, and final adjudication. Agent-count consensus can be misleading when agents share the same upstream source, copied evidence, context snapshot, dataset, tool output, or hidden lineage. NCIF makes that correlation explicit enough to test.

## Quick local verification

```bash
python scripts/verify.py
```

The verifier runs compile checks, the unit/adversarial suite, a bounded deterministic audit, a structural stress audit, positive/negative CLI checks, and JSON parsing.

## Reference CLI

```bash
PYTHONPATH=src python -m ncif.cli fixtures/independent_consensus.json --min-support-groups 2
PYTHONPATH=src python -m ncif.cli fixtures/correlated_false_consensus.json --min-support-groups 2
```

Expected decisions are `CONSENSUS_CANDIDATE` and `FREEZE`, respectively.

## Repository safety

This lab is designed to live only under AI-CONTEXT. Nothing in this artifact authorizes mutation of a repository whose name contains `NEXY.AI`.
