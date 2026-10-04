# Architecture — Minimal Blocker Core / Freeze Explanation Engine

**Status:** `AI-PROPOSED / EXPERIMENTAL / ADVISORY ONLY`

## 1. Problem

Composite verification gates often degrade into an opaque Boolean: pass or no pass. For a verify-or-freeze architecture, that is insufficient. A frozen gate should expose a deterministic, reviewable explanation without weakening the gate.

The engine therefore answers:

> Given an explicit monotone gate and explicit evidence states, what is the current gate status, why is it not passing, and what inclusion-minimal modeled sets of obligations would need to become PASS for the gate to pass?

## 2. Trust boundary

The engine trusts **structure**, not truth.

It validates its JSON shape and evidence metadata, but it cannot prove that a caller truthfully labeled a test PASS or supplied an authentic revision. Upstream attestation/provenance systems remain responsible for evidence authenticity.

No input text is executed. Remediation strings and metadata are inert data.

## 3. Modules

### Evidence normalizer

Inputs one record per evidence obligation.

Effective-status rule:

1. non-PASS declared status remains unchanged;
2. declared PASS with missing required evidence class -> `NOT_VERIFIED`;
3. declared PASS with observed evidence class below required class -> `NOT_VERIFIED`;
4. declared PASS with required target revision but missing observed revision -> `NOT_VERIFIED`;
5. declared PASS with observed revision different from target -> `NOT_VERIFIED`.

### Gate evaluator

Supported monotone operators:

- `leaf(E)`
- `all_of(children)`
- `any_of(children)`
- `at_least(k, children)`

No NOT/XOR/implication operator is accepted in v0.1.0. This keeps repair-set semantics monotone: making more leaves PASS cannot make a passing gate fail.

### Minimal repair-set engine

For each node, the engine computes a family of evidence-ID sets sufficient to make that node PASS if those leaves become PASS while other leaf results stay fixed.

Rules:

- PASS leaf -> `{}`
- non-PASS leaf -> `{leaf}`
- ALL -> Cartesian union of child repair families
- ANY -> union of child repair families
- AT_LEAST(k) -> choose k children, combine one repair set from each, then minimize

After generation, strict supersets are removed. The remaining sets are **inclusion-minimal**, not necessarily minimal in time, risk, money, or engineering effort.

### Cost ranker

`repair_cost` is an explicit caller-supplied non-negative number. Default is `1`. The engine ranks inclusion-minimal repair sets by:

1. summed declared repair cost;
2. cardinality;
3. lexicographic evidence IDs.

Cost is advisory. It has no authority over project law or release requirements.

### Explanation/certificate layer

Output includes:

- root status and ALLOW/FREEZE decision;
- status counts;
- unsatisfied leaves and downgrade reasons;
- minimal repair sets;
- primary blocker core;
- structured explanation tree;
- truncation disclosure;
- deterministic certificate hash.

## 4. Status semantics

Status is not a replacement for the explicit explanation tree.

- Leaf: effective evidence status.
- ALL: PASS only if all pass; otherwise strongest blocking status by engine precedence.
- ANY: PASS if any pass. If all alternatives are FAIL, FAIL. If some alternative remains unresolved, known failed alternatives do not force the whole OR gate to FAIL; status is derived from viable unresolved alternatives.
- AT_LEAST: PASS if threshold is already met. FAIL if the number of known FAIL children makes the threshold impossible without repairing a hard failure. Otherwise derive status from unresolved viable children.

Current precedence among unresolved blockers is:
`CONFLICT > FAIL > BLOCKED > NOT_VERIFIED > UNKNOWN > PASS`.

The explanation tree is the authoritative diagnostic surface; precedence is only a compact summary.

## 5. Determinism invariants

D1. Evidence map insertion order does not affect output hash.  
D2. Gate child order may affect explanation-tree order, because ordered input is semantically preserved.  
D3. Minimal-set ordering is deterministic.  
D4. No wall-clock time is injected.  
D5. Canonical JSON uses sorted object keys and compact separators for hashing.  
D6. Engine version participates in the certificate body.  
D7. The hash excludes only the `certificate_sha256` field itself.

## 6. Bounded execution

To avoid unbounded combinatorial behavior:

- max gate depth: 64;
- max visited nodes: 10,000;
- caller-selected repair-set retention: 1..4096, default 256;
- AT_LEAST intermediate candidates are bounded before final minimization.

If repair enumeration truncates, the engine marks `repair_sets_truncated=true` and downgrades the recommendation guarantee to `PARTIAL_DUE_TO_REPAIR_SET_TRUNCATION`.

## 7. Failure model

Malformed JSON, unsupported schema version, unknown evidence reference, invalid evidence class/status, invalid threshold, negative/non-finite cost, excessive depth/node count, or I/O failure are explicit errors.

CLI exits `64` for invalid input. It does not guess defaults for materially invalid fields.

A valid gate that freezes is not an execution error. CLI exits `2` so automation can distinguish “valid but frozen” from malformed input.

## 8. Security model

- standard-library only;
- no network access;
- no dynamic imports from input;
- no shell execution from input;
- remediation/metadata are inert strings/JSON;
- bounded recursion/node/search limits;
- no secret storage requirement.

## 9. Complexity

Basic gate evaluation is O(nodes). Repair-set enumeration can be exponential in the number of alternatives, which is inherent to enumerating minimal satisfying sets for general monotone formulas. v0.1.0 contains explicit caps and honesty flags rather than hiding this fact behind a cheerful progress bar.

## 10. Integration shape if ever promoted

Potential future call chain:

`evidence registry -> blocker-core input adapter -> engine -> freeze certificate -> human/JUDGE review surface`

This is only a proposed integration shape. Current NEXY implementation integration status is `NOT_VERIFIED / NOT_IMPLEMENTED_BY_THIS_TASK`.
