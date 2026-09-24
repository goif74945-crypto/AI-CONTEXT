# NEXY.AI Atomic Ontology Registry

## Status
**ATOMIC ONTOLOGY V1 — COMPLETE FOR MAJOR SOURCE DOMAINS**

Primary source:
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- parsed non-empty paragraph sequence: **10,979**

Compiled result:
- **518 entities**
- **865 typed relationships**
- **86 aliases**
- **46 entity types**
- parent graph: acyclic
- `REQUIRES` graph: acyclic

The earlier **215-system registry is a top-level tracking baseline, not the atomic object count**.

## Canonical files

- `entities.jsonl` — canonical source-derived entity registry.
- `relationships.jsonl` — typed architecture graph.
- `aliases.json` — legacy/current alias normalization.
- `entity-types.json` — entity taxonomy.
- `entity.schema.json` — machine validation schema for entity records.
- `relationship.schema.json` — machine validation schema for relationship records.
- `coverage.json` — counts, source revision, domain checkpoints and limitations.
- `validation-report.md` — structural integrity report.

Streaming source checkpoints are retained under `checkpoints/` so a future AI can audit/recompile without depending on one context window.

## Entity contract
Every entity contains at least:

`id`
`name`
`aliases`
`entity_type`
`parent_id`
`authority`
`scope`
`status`
`source_range`
`description`
`responsibilities`
`inputs`
`outputs`
`dependencies`
`dependents`
`contracts`
`invariants`
`states`
`failure_behavior`
`recovery`
`security_boundary`
`persistence`
`determinism`
`implementation_refs`
`test_refs`
`evidence_refs`
`supersedes`
`superseded_by`
`conflicts`

Empty arrays mean **not established/mapped yet**, not “does not exist.”

## Entity types
The ontology separates real object kinds instead of calling everything a “system,” including:
- SYSTEM / SUBSYSTEM / MODULE / ENGINE / LAYER
- KERNEL / FABRIC / PLANE / ZONE / RUNTIME
- LAW / INVARIANT / PROTOCOL / FSM / STATE / EVENT
- CONTRACT / SCHEMA / DATA_MODEL / MEMORY / STORAGE / LEDGER
- REGISTRY / QUEUE / ADAPTER / GATEWAY / CONTROLLER
- MONITOR / DETECTOR / FILTER / RESOLVER / AUDITOR / SYNTHESIZER / EXTRACTOR / ORCHESTRATOR
- UI_SURFACE / ROLE / SECURITY_BOUNDARY / HARDWARE_PATH / TOOLCHAIN / EVIDENCE_CLASS / CONFIG / ERROR / WORKFLOW / CONCEPT

## Status semantics
- `CURRENT_CANON` — current source-law/canonical object.
- `CURRENT_BUILD` — current DOC-C build object.
- `SOURCE_DESIGN` — source-defined design object; not runtime proof.
- `HISTORICAL` — retained for provenance.
- `CONFLICT` — source evolution unresolved at entity level.

Implementation/runtime status is intentionally **not** inferred here.

## Scope semantics
Current registry uses:
- `DOC_B_SYSTEM_LAW`
- `DOC_C_CURRENT_BUILD`
- `DOC_D_PRODUCT_DESIGN`
- `DOC_E_DEPLOYMENT_EVIDENCE`
- `CURRENT_ARCHITECTURE`
- `FUTURE_ARCHITECTURE`
- `HISTORICAL`

The later Scope Registry will make this more granular.

## Source ranges
`source_range` points to the local non-empty paragraph sequence of the exact source SHA above.

It is a provenance/navigation anchor, not a Word page number.

## Relationship semantics
Current typed graph includes:
- `PART_OF`
- `REQUIRES`
- `CALLS`
- `VALIDATES`
- `PERSISTS_TO`
- `PERSISTS`
- `EMITS`
- `CONSUMES`
- `GOVERNS`
- `OVERRIDES`
- `RECOVERS`
- `OBSERVES`
- `SECURES`
- `IMPLEMENTS`
- `FEEDS`
- `CONTAINS`

Important: `REQUIRES` was validated as acyclic so it can later feed task/dependency DAG construction. Authority/control edges are kept as semantic relations rather than fake build dependencies.

## Streaming capture checkpoints
1. **Core / Human / DOC-C / DOC-D / DOC-E** — 120 entities.
2. **Sovereign / Constitutional / Game / NCF / Capability Governance** — 145 entities.
3. **L1o / Lo3 / Lo2 / Robotics / Final Architecture** — 122 entities.
4. **Atomic gap pass** — 131 entities covering errors, API routes, UI internals/components, constitutional economy, capability classes, Trinity visualization/control objects and final-layer subcomponents.

Total: **518**.

## What this solves
AI no longer needs to interpret:

> “System 126 = L1o”

as one opaque object.

It can traverse concrete sub-objects such as:
`SYS-L1O → ICL / Constraint Engine / DGE / Atomic Node Expansion / MPG / EPE / RSA / Output Synthesizer / memories / BTS / Code-Brain ...`

The same applies to Lo3, Lo2, DOC-C, Sovereign Fabric, Game Fabric, NCF, Capability Governance and RCL.

## Critical boundary
This registry answers:

> **“What architecture objects does the source define, and how are they structurally related?”**

It does **not** yet answer:

> “Where is each object implemented in current code?”  
> “What requirement does each object satisfy?”  
> “Which test proves it?”  
> “Which evidence is current?”

Those mappings are intentionally reserved for the next registries:
Requirement Registry → Authority/Scope/Supersession → Dependency Graph → Implementation Map → Contract/FSM/Invariant → Test/Evidence.

## Omission repair
A later Event Registry cross-check found two DOC-C execution events absent from ontology v1: `cancel` and `timeout`. They were added as first-class EVENT entities; current count is 518.

## Validation
See `validation-report.md`.

Current structural result:
**PASS**.

Do not reinterpret that PASS as implementation/runtime/deployment PASS.
