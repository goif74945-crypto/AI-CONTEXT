# Architecture — NEXY Lo4 Proof Compiler Lab

Status: `Lo4_AI_PROPOSAL_ONLY`

## Objective
Create a deterministic pre-release verification chain that helps a future NEXY implementation preserve human authority, contain uncertainty, spend verification effort efficiently, turn requirements into executable boundary witnesses, and prevent unsupported claims from reaching the user-facing view.

## Non-goals
- This is not NEXY Canon.
- This is not a replacement for NEXY::CORE, NEXY::LAW, NEXY::JUDGE, or NEXY::VIEW.
- It does not modify NEXY.AI.
- It does not prove production integration, deployment, provider correctness, or safety.
- It does not infer requirements from ambiguous prose.

## 1. APS — Authority Provenance Seal
### Problem
Multi-agent systems can accidentally copy an AI-generated proposal into a stronger authority context. Repetition is not promotion.

### Invariant
Authority roots must match a caller-controlled trusted-root registry. Authority may flow downward without a receipt. Authority may flow upward only with an explicit receipt anchored to a trusted authority reference whose level is sufficient for the promoted target.

### Failure behavior
Missing parent, cycle, duplicate identity, malformed receipt, or unauthorized escalation raises a deterministic error. No implicit repair.

### Future NEXY integration point
Between NEXY::LAW/context ingestion and any consumer that treats a claim as governing authority.

## 2. UCL — Uncertainty Containment Lattice
### Problem
Global freeze on any unresolved fact wastes valid results; ignoring uncertainty is unsafe.

### Invariant
Epistemic status propagates only across declared dependency edges. Independent claims remain independently releasable.

### Order used by reference prototype
`PASS < UNKNOWN < NOT_VERIFIED < CONFLICT < FAIL`.

This is a prototype ordering, not NEXY Canon.

### Failure behavior
Cycles or missing dependency identities are rejected.

### Future NEXY integration point
Claim graph between NEXY::CORE/JUDGE reasoning products and verification/release gating.

## 3. MPP — Minimum Proof Planner
### Problem
Running every test/provider/check on every claim is expensive and slow. Skipping required evidence is unacceptable.

### Invariant
Every claim must be covered by at least one available probe whose evidence class meets or exceeds the declared requirement. The solver minimizes total cost, then probe count, then lexicographic IDs for deterministic tie-breaking.

### Bounded exactness
The reference solver uses exact claim-mask dynamic programming up to `max_exact_claims` (default 18) and `max_candidate_probes` (default 512), with only correctness-preserving dominance pruning. Above declared bounds it fails closed rather than silently switching to an unproven heuristic.

### Future NEXY integration point
NEXY::RUN / verification scheduler before executing proof work.

## 4. RBWE — Requirement Boundary Witness Engine
### Problem
A prose requirement that never creates a negative test remains easy to misread or under-test.

### Invariant
Only an explicit small DSL is compiled. Supported operators are `eq`, `neq`, `min`, `max`, `in`. The engine does not guess hidden semantics.

### Output
Deterministic positive, negative, and (when required) missing-input witnesses, plus selected contradiction detection.

### Future NEXY integration point
Build/verification tooling that converts already-normalized requirements into concrete test cases.

## 5. PCOC — Proof-Carrying Output Compiler
### Problem
Even if proof exists somewhere in a system, a user-facing answer can still overstate what was actually verified.

### Invariant
Every released claim must have:
- an authority digest present in the caller-controlled trusted seal set;
- epistemic state `PASS`;
- evidence records bound to the same claim identity and target version;
- successful evidence class >= required evidence class;
- evidence reference when required evidence class > E0.

Any blocker yields one deterministic `FREEZE` envelope with blocker codes. No partially optimistic prose is emitted.

### Future NEXY integration point
Immediately before NEXY::VIEW/user-visible trusted output.

## Composition
The five systems form a layered path:

`APS -> UCL -> MPP -> RBWE -> PCOC`

They remain separately testable. No module uses network/provider state. All durable identity/digests use canonical JSON and SHA-256 where sealing is needed.

## Security/trust boundary
Inputs are untrusted data. No input string is executed. The prototype uses no dynamic imports, shell, eval, network, filesystem mutation, database, or credentials.

## Version/evolution law
Any future change that alters authority ordering, epistemic ordering, evidence-class semantics, solver optimality, witness DSL, or release conditions is a semantic contract change and requires new tests plus re-verification.
