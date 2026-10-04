# Collision and Novelty Audit

## Scope of the audit

The current `คลังข้อมูลเสริม` top-level inventory was inspected before design. It contained 153 top-level entries and many parallel labs covering evidence, epistemics, context, reliability, privacy, authority, UX compilation, concurrency, model conformance, side effects, provenance and shadow verification.

This audit does **not** claim formal semantic uniqueness across every byte of every sibling project. It establishes a bounded novelty case from:

- current top-level project names;
- NEXY overview/product/control context;
- selected task contracts for the most likely collisions;
- explicit responsibility deltas below.

Global semantic uniqueness remains a stronger claim than this evidence can prove.

## Concepts deliberately rejected because of collision risk

The design phase rejected generic variants of:

- attention/notification optimization, because `NEXY Experience Compiler Lab` already includes interruption/notification economics;
- experiment design/evaluation, because `NEXY Product Evidence Lab` already compiles and evaluates controlled experiments;
- generic decision intelligence, because `NEXY Decision Intelligence` already owns option-space/counterfactual/reversibility reasoning;
- semantic directive drift, because `NEXY Directive Integrity Lab` already owns adjacent representation drift;
- duplicate work admission, because `NEXY Orthogonal Work Admission` and `Supplemental Collision Guard` already own that space;
- commitment tracking, because `NEXY Commitment Integrity Kernel` already owns future promise/obligation integrity;
- context/provenance/shadow-execution work, because dedicated sibling labs already exist.

Creating yet another engine in those areas would be bureaucracy wearing a new acronym.

## Novelty delta by selected concept

### 1. Goal Contribution Graph (GCG)

**Responsibility:** prove that every planned work item contributes to an explicit acceptance criterion and that every criterion is covered, while rejecting orphan work, forbidden scope, bad dependencies and cycles.

**Nearest siblings:** Directive Integrity Lab, Orthogonal Work Admission, Commitment Integrity Kernel.

**Delta:**
- Directive Integrity checks semantic drift between representations of a directive.
- Orthogonal Work Admission checks duplication/overlap before work begins.
- Commitment Integrity governs outward promises and completion evidence.
- GCG instead checks **objective-to-work value traceability inside a plan**. It asks: “Why does this work item exist, and which acceptance criterion does it earn?”

### 2. Verified Capability Composer (VCC)

**Responsibility:** compose a deterministic chain of currently AVAILABLE capability manifests whose typed inputs/outputs and policy envelopes can reach a requested target under risk/cost/permission/data constraints.

**Nearest existing NEXY structures:** capability registry, deterministic scheduler; nearest supplemental sibling: Shadow Integration Twin.

**Delta:**
- Capability Registry records capability status.
- Scheduler dispatches already-eligible commands.
- Shadow Integration Twin verifies candidate adapter behavior against a profile.
- VCC performs **policy-bounded capability composition planning** before dispatch, without executing any capability.

### 3. Artifact Consumer Fitness Gate (ACFG)

**Responsibility:** verify that a produced artifact package is actually consumable by a declared downstream consumer profile: required files, media types, metadata, size budget, classifications and content hashes.

**Nearest siblings:** Product Evidence Lab, TASC/PRISM/truth-surface projects.

**Delta:**
- Product Evidence Lab evaluates product experiments.
- TASC/PRISM compile authoritative state into user-facing plans.
- ACFG checks **deliverable usability at the consumer boundary**. A factually correct artifact can still fail if the receiving tool/human cannot safely consume it.

### 4. Supply-Chain Trust Gate (SCTG)

**Responsibility:** admit or freeze dependencies/plugins/tools based on pinned identity, SHA-256 presence, source, signature state, declared permission envelope and network-domain policy.

**Nearest siblings:** Tool Contract Drift Lab, Provenance Taint Lattice, Agentic Security.

**Delta:**
- Tool Contract Drift detects interface/contract drift.
- Provenance Taint Lattice tracks trust through transformed information lineage.
- Agentic Security covers broader agent/security boundaries.
- SCTG is a narrow **software/tool artifact admission gate** before a dependency enters a trusted workflow.

### 5. Mastery Path Compiler (MPC)

**Responsibility:** compile a minimal prerequisite-respecting onboarding/mastery path from an explicit skill graph and user-declared known skills. It never infers hidden competence and freezes on missing/cyclic definitions or step-budget overflow.

**Nearest siblings:** Experience Compiler, PRISM UX Compiler; nearest canonical product material: first-session walkthrough.

**Delta:**
- Experience/PRISM optimize presentation and cognitive load of system state.
- DOC-D defines a fixed first-session walkthrough.
- MPC compiles **goal-specific prerequisite paths** from declared knowledge and explicit skill dependencies. It is a training/onboarding planner, not a truth-surface compiler.

## Novelty status

- Path/name collision with these five responsibilities in the inspected top-level inventory: **NOT OBSERVED**.
- Responsibility collision against selected nearest siblings: **DISTINCT WITH RELATED BOUNDARIES**.
- Formal exhaustive semantic uniqueness across all sibling content: **NOT_VERIFIED**.
