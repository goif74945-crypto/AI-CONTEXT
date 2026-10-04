# Decision Stability Lab — Design

> **STATUS: AI-PROPOSED SUPPLEMENTAL CONCEPT.** This is not current NEXY.AI law, not evidence of current NEXY.AI implementation, and not deployment evidence.

## Objective
Test the stability of a deterministic decision oracle under controlled evidence perturbations. The lab is deliberately outside the NEXY.AI implementation repository and is designed as a possible future adapter layer.

## Five concepts

### 1. MONO — Decision Monotonicity Verifier
For domains explicitly declared monotone, adding SUPPORT evidence must not worsen a decision and adding BLOCK evidence must not improve it. A violation identifies an unstable or incorrectly classified decision surface.

### 2. IRIS — Irrelevance Invariance Scanner
Declared irrelevant CONTEXT and evidence ordering should not alter the decision. This exposes accidental coupling to presentation/order/noise.

### 3. EDGE — Decision Boundary Cartographer
Perform bounded finite search over add/remove evidence perturbations and return the nearest observed decision flip. 'truncated=true' means the search budget prevents an exhaustiveness claim.

### 4. MDE — Minimal Decisive Evidence Extractor
Find a minimum-cardinality subset that reproduces the baseline decision under the same oracle and state. This is explanatory evidence only. It does not authorize deletion of omitted evidence or audit records.

### 5. DAMP — Temporal Decision Flicker Guard
Use the local reference order REJECT < FREEZE < RELEASE. Any worsening decision applies immediately. An improvement requires a configurable dwell and, by default, an unchanged evidence fingerprint across the dwell window.

## Shared invariants
- Duplicate evidence IDs with semantically different payloads are rejected.
- Canonical serialization is deterministic and order-independent where order is not semantically meaningful.
- NaN/Infinity are forbidden in canonical evidence values.
- Search budget exhaustion is explicit, never silently promoted to exhaustive proof.
- Oracle outputs outside the Decision enum are rejected.
- DAMP never delays a safety regression.
- The suite does not infer authority or evidence polarity.

## Failure semantics
Contract violation -> exception / fail closed.
Observed stability violation -> structured report with PASS=false.
Bounded search exhaustion -> structured result with truncated=true.
Insufficient or ambiguous NEXY adapter mapping -> integration must FREEZE rather than guess.

## Non-goals
This is not a theorem prover, not a policy engine, not a replacement for NEXY::JUDGE, not a production wire protocol, and not proof of NEXY runtime/deployment behavior.
