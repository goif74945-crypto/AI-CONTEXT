# Design Contract

## Status and authority

Everything in this folder is **AI-proposed Lo4 experimental material**. It may be useful to future NEXY engineering, but it has zero authority to change USER LAW, NEXY::LAW, NEXY::CORE, NEXY::JUDGE, DOC-B, DOC-C, or the current source-normalized build matrix unless an authorized promotion process separately adopts it.

## Shared invariants

- deterministic canonical fingerprints for semantically equivalent set-like inputs;
- malformed IDs, cycles, identity collisions, alias ambiguity, unsupported evidence classes, and invalid numeric values fail explicitly;
- `UNKNOWN`, `CONFLICT`, `NOT_VERIFIED`, `BLOCKED`, and `FREEZE` are not coerced to `PASS`;
- no model/network/provider dependency exists in the reference core;
- authority rank is supplied by the caller/adaptor and is never inferred by the library;
- no system writes NEXY state;
- outputs are advisory until NEXY-owned adjudication adopts them.

## 1. BKR — Bitemporal Knowledge Reconstructor

### Problem
Ordinary “latest value” stores conflate world time with knowledge time. That makes late-arriving evidence look as if it was always known, corrupting historical replay and postmortems.

### Contract
Each fact version has a valid interval, `known_at`, source, caller-supplied authority rank, and optional explicit supersession edges. A query receives `valid_time` and `known_time` separately.

### Failure semantics
- no eligible fact → `UNKNOWN`;
- equal top-authority surviving values disagree → `CONFLICT`;
- supersession cycle/unknown target → exception/fail closed;
- recency alone never silently overwrites another fact.

### NEXY boundary
A future Vault adapter could encode verified project state changes and later corrections, enabling “what did NEXY know when it made decision D?” audits. Current integration: `NOT_VERIFIED`.

## 2. CEML — Concurrent Epistemic Merge Lattice

### Problem
Parallel agents can author context concurrently. Last-writer-wins is convenient and epistemically terrible: it destroys evidence and creates order-dependent truth.

### Contract
Claims and retractions are immutable identity-bearing events. Replica merge is set-union-like, idempotent, commutative, and deterministic. Same claim ID with different content is an identity collision and fails. Retractions are append-only tombstones.

### Resolution semantics
For each `(subject, predicate, scope)` key, only caller-defined top-authority active claims participate in semantic resolution. Equal top-authority differing values remain `CONFLICT`.

### NEXY boundary
Could sit between SWARM worker outputs and a NEXY-owned adjudicator/Vault commit stage. It cannot authorize a Vault write by itself.

## 3. CUVL — Causal User Value Ledger

### Problem
Novel systems can be technically impressive while creating no measurable user benefit. Lo4 needs a mechanism for turning “cool idea” into a falsifiable value contract.

### Contract
A proposal declares mechanism, user outcome, primary metric/direction/minimum effect, guard metric with its own direction/maximum regression, and falsifier. Guard direction is explicit because a regression may mean an increase (for latency/error rate) or a decrease (for safety-success/availability). Experiment evidence declares sample count and evidence class.

### Statuses
- insufficient sample/evidence → `NOT_VERIFIED`;
- falsifier or guard regression breach → `FALSIFIED`;
- effect below threshold → `NO_SUPPORTED_BENEFIT`;
- all declared thresholds pass → `BENEFIT_SUPPORTED` (still advisory).

### NEXY boundary
Could help prioritize which Lo4 proposals deserve expensive promotion work. It cannot promote a feature.

## 4. STCE — Scoped Terminology Contract Engine

### Problem
Large projects reuse words such as “matrix”, “state”, “law”, “verified”, or “agent” across layers. A model that resolves such terms by intuition violates zero-guess behavior.

### Contract
Definitions are explicit `(term, scope, definition, aliases)` records. Resolution selects the most specific scope prefix. Exact same-scope conflicting definitions, ambiguous aliases, alias/canonical collisions, and alias cycles fail closed.

### NEXY boundary
Could guard requirement parsing, document ingestion, and agent handoff by requiring explicit scoped term resolution before semantic actions.

## 5. FSA — Failure Semantics Algebra

### Problem
When multiple subsystems return statuses, ad hoc `if` chains can accidentally hide `UNKNOWN`, `CONFLICT`, or missing proof under a locally successful step.

### Contract
The default safe precedence is explicit and inspectable:

`PASS < PARTIAL < NOT_VERIFIED < UNKNOWN < BLOCKED < FREEZE < FAIL < CONFLICT`

The join is deterministic, commutative and idempotent. A locally `PASS` node with any required non-PASS dependency becomes at least `BLOCKED`, preserving the stronger upstream state when applicable.

### NEXY boundary
Could be used as a narrow status-composition primitive below NEXY-owned policy. The ranking is a proposal, not Canon.

## Integration sketch

```text
NEXY-owned source/context
  -> STCE term resolution
  -> BKR time-correct reconstruction
  -> CEML concurrent context reconciliation
  -> NEXY-owned JUDGE/LAW gate
  -> optional CUVL innovation evaluation
  -> FSA explicit status composition
  -> NEXY-owned final output/freeze
```

No arrow grants authority to the Lo4 modules.
