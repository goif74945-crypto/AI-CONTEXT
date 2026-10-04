# NEXY Five-Axis Assurance Lab — Design Contract

Status: EXPERIMENTAL / PROPOSAL
Authority: advisory only; never overrides NEXY Canon/DOC-C/DOC-D/JUDGE/LAW.
Protected scope: every repository whose name contains `NEXY.AI` is read-only.

## Goal

Build five deterministic, model-agnostic reference modules that close assurance gaps visible in the current NEXY conceptual architecture without duplicating the recently inspected supplemental labs.

## Shared invariants

1. Same canonical input must produce the same canonical output identity.
2. Core logic uses no wall clock, randomness, network, subprocess, hidden environment input or floating-point assurance arithmetic.
3. Invalid structure is explicit `ValidationError`; unsafe/legal-nonclosure becomes `FREEZE`, never hidden success.
4. All durable identities are SHA-256 over canonical UTF-8 JSON.
5. The implementation is advisory and has no mutation capability against NEXY.AI.
6. Integer assurance scores are structural policy metrics, not scientific probability claims.
7. Experimental resource ceilings fail closed before unbounded work: derivation fan-in 1,024; impact nodes 10,000 / edges 50,000; FSM machines 2,048 / transitions 50,000 / bridges 50,000; context records 10,000; swarm agents 20 with selected count <= 6. These are FAAL implementation defaults, not NEXY constitutional limits.

## C1 — Uncertainty Propagation Kernel (UPK)

Purpose: preserve uncertainty/truth-state through derived claims.

Contract:
- each claim has truth status, uncertainty in integer parts-per-million, evidence IDs and dependencies;
- derived uncertainty cannot be lower than the strongest input floor unless a bounded evidence-reduction permit and new evidence are explicitly supplied;
- conflict/refuted/unknown/stale states propagate by deterministic severity rules;
- release is policy-gated by allowed status and maximum uncertainty threshold.

Failure model:
- malformed ppm, duplicate claim IDs, illegal evidence reduction -> ValidationError/FREEZE as appropriate;
- disallowed status or threshold exceedance -> FREEZE.

## C2 — Change Impact Frontier (CIF)

Purpose: compute the exact deterministic reverse dependency closure after a change and identify stale evidence, required tests and affected claims.

Contract:
- graph nodes are typed: REQUIREMENT, SOURCE, MODULE, TEST, EVIDENCE, CLAIM;
- edge `A -> B` means B depends on A;
- graph must be a DAG;
- changed nodes create deterministic impact paths;
- impacted TEST/EVIDENCE/CLAIM nodes are separated in the report.

Failure model:
- unknown nodes, self edges or cycles -> ValidationError.

## C3 — Swarm Independence Planner (SIP)

Purpose: reduce false consensus by measuring structural correlation among candidate verifier agents and selecting a bounded subset with required capabilities.

Structural score only, 0..100:
- same provider: +30
- same model family: +20
- same context shard: +20
- toolchain overlap: up to +15
- data-source overlap: up to +15

The score is not a probability of shared failure.

Planner objective, lexicographically:
1. satisfy capability coverage and minimum provider diversity;
2. minimize maximum pairwise score;
3. minimize total pairwise score;
4. deterministic tie-break by sorted agent IDs.

No legal subset under policy -> FREEZE.

## C4 — FSM Composition Guard (FCG)

Purpose: preserve separation among multiple state machines while validating explicit event bridges.

Contract:
- each FSM owns its own states and transitions;
- a bridge may emit a target event but may never directly mutate another machine's state;
- bridge references must exist;
- event-bridge cycles are detected and FREEZE composition;
- runtime simulation uses a bounded deterministic FIFO event queue.

Failure model:
- malformed/deterministically ambiguous machine -> ValidationError;
- bridge cycle or event budget overflow -> FREEZE.

## C5 — Provenance-Preserving Context Compressor (PPCC)

Purpose: reduce duplicate structured context while preserving decision-critical information.

Contract:
- only exact semantic/content/status duplicates are merge candidates;
- unresolved truth states and declared conflicts are never merged away;
- strongest authority record becomes the representative of a safe duplicate group;
- requirement coverage, dependency references and provenance are union-preserved;
- same semantic key with different content hashes requires explicit conflict linkage or compression FREEZEs.

Cost metrics are caller-supplied integer content-cost units; they are not tokenizer-accurate unless the caller supplied tokenizer-derived values.

## Integrated assurance flow

`CHANGE -> CIF -> UPK -> SIP -> FCG -> PPCC -> FINAL ADVISORY VERDICT`

The integrated report is canonicalized and hashed. PASS means only that these five experimental contracts passed for the provided bundle. It is not NEXY runtime/deployment proof.
