# Model Drift Sentinel (MDS) — Design

## Problem
NEXY intends to hot-swap AI providers/models, but a provider can change behavior without changing the client integration. A syntactically valid adapter can therefore become semantically stale.

## Objective
Given a fixed probe catalog, a trusted baseline observation set, and a candidate observation set, produce a deterministic drift report. Critical probe drift freezes provider admission.

## Core invariants
- A probe ID is unique.
- Critical probe missing or changed => FREEZE.
- Unknown candidate probes never silently become accepted baseline behavior.
- Fingerprints are canonical SHA-256 over normalized structural observations.
- No model call is made by this library; it evaluates recorded observations only.

## Inputs / Outputs
Input: Probe definitions + baseline observations + candidate observations.
Output: PASS / DRIFT / FREEZE, per-probe differences, canonical fingerprints.

## Failure behavior
Malformed or duplicate probes raise validation errors. Missing critical evidence returns FREEZE, not optimistic PASS.

## Evidence model
E2 proves comparison behavior. It does not prove a live provider is stable; that would require live probe collection and operational evidence.
