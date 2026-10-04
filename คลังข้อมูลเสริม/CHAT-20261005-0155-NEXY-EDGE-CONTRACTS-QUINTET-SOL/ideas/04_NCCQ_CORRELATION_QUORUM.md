# 04 — NCCQ: NEXY Correlation-Cut Quorum

**Status:** AI-PROPOSED CONCEPT.

## Problem
Five agreeing agents are not five independent witnesses when they share the same model family, retrieval source, runtime, parser or environment. Naive vote counting can turn one shared defect into "consensus".

## Design
Each witness declares failure-domain identifiers. NCCQ searches deterministically for a PASS quorum whose members have pairwise disjoint declared failure domains. If none exists, it returns the maximum independent subset plus repeated domains that explain the correlation bottleneck.

## Invariants
- witness target/hash mismatch => FREEZE;
- duplicate witness identity => FREEZE;
- FAIL witnesses never count toward PASS quorum;
- quorum exists only if declared failure domains are disjoint.

## NEXY integration hypothesis
Use before NEXY::JUDGE accepts cross-agent consensus for high-impact claims. The declaration itself must come from an authenticated provider/runtime registry in a real integration.
