# NCIF Concept and Novelty Boundary

**Classification:** EXPERIMENTAL / AI-PROPOSED / NON-GOVERNING

## Problem

A multi-agent system can produce the appearance of strong consensus while all participants ultimately depend on one causal source. Examples include:

- three models summarizing the same document;
- two agents querying the same cached tool output;
- multiple copied evidence records with different IDs;
- derived evidence whose parents converge on the same root;
- different roots known by the caller to share one dataset/vendor/experiment;
- a chain of correlation where A shares with B and B shares with C.

Counting votes in these cases inflates epistemic independence.

## Proposal

NCIF converts evidence provenance + votes into **independence groups**. Within a stance, votes are connected when they share any propagated correlation token. Connected components, not raw votes, are the counting unit.

```text
Evidence DAG + declared source identities/correlation keys
                    ↓
             lineage validation
                    ↓
            root/key propagation
                    ↓
       per-vote provenance token set
                    ↓
   transitive connected-component collapse
                    ↓
 SUPPORT groups / OPPOSE groups / resilience
                    ↓
        CONSENSUS_CANDIDATE | FREEZE
```

## Why this is useful to future NEXY work

NEXY context already expects multiple AI/model slots, parallel debate, bounded adversarial review, cross-verification, proof-weighted consensus and final adjudication. NCIF addresses a narrow integrity gap: **cross-verification is weak when cross-verifiers share the same evidence root.**

## Distinctness from observed sibling labs

### Proof-Preserving Resource Governor (NPRG)
NPRG selects feasible worker/verifier allocations under resources, capabilities, privacy and provider-domain independence. NCIF does not select agents or optimize resources. It evaluates evidence-lineage independence after outputs exist.

### Intent Integrity Lab
Intent Integrity protects objective/scope/requirement/evidence-contract drift. NCIF assumes a claim contract is already chosen and examines provenance dependence among votes.

### Proof / evidence graphs
Graph-shaped evidence can record lineage. NCIF's novel focus is a deterministic **independence-counting/firewall policy over that lineage**, including anti-clone source identity, transitive vote clustering and single-root removal stress.

### Human-control / UX labs
NCIF has no UI authority and does not change visibility/permission behavior.

## Non-goals

NCIF does not:

- determine whether a source is factually correct;
- discover undeclared hidden causal dependence automatically;
- prove actors are organizationally or economically independent;
- authenticate source identity;
- replace JUDGE/CORE;
- make model output trustworthy merely because roots differ;
- infer correlation from prose similarity;
- guarantee Sybil resistance;
- claim production-scale denial-of-service resistance.

## Promotion law

Presence in AI-CONTEXT is not adoption. Any future NEXY integration requires explicit authority, mapping to current build contracts, real integration tests, policy review, abuse testing, and revision-bound evidence.
