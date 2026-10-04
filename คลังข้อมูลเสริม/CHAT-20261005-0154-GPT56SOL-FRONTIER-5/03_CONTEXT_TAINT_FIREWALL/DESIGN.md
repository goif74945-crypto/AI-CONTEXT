# Context Taint Firewall (CTF) — Design

## Problem
Webpages, tool output, model output, documents and logs can contain instructions that look authoritative. Without provenance propagation, untrusted text can contaminate policy or leak secrets downstream.

## Objective
Represent context as a provenance graph with inherited taints and evaluate whether a node may flow into sensitive sinks.

## Taints
`UNTRUSTED_EXTERNAL`, `MODEL_GENERATED`, `SECRET`, `VERIFIED_EVIDENCE`, `AUTHORITY_SOURCE`.

## Invariants
- Untrusted/model-generated content may not flow to an authority sink without an explicit verification transform.
- SECRET may never flow to EXTERNAL_EGRESS.
- Verification adds evidence lineage; it does not erase SECRET.
- Parent taints propagate deterministically.
- Missing verification evidence freezes authority promotion.
