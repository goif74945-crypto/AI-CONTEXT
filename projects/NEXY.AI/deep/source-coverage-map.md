# NEXY.AI — Full Source Coverage Map

## Source
Uploaded design document:
`แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`

Parsed capture used for this pass:
- 293 pages
- 10,979 extracted non-empty paragraph records

Paragraph numbers below refer to the local extraction sequence used during this capture. They are resume/navigation anchors, not permanent source line IDs.

## Coverage

### 1–3219 — Identity / Human / Canon / UX evolution
Covered primarily by:
- `human-control-surface.md`
- existing `overview.md`
- existing `architecture.md`

Contains repeated/evolving:
- Human Gravity;
- identity/naming;
- CORE/LAW/JUDGE/SWARM;
- VIEW/RUN/FORGE;
- FRONT/PULSE/DIALOG/GUARD/COMPANION;
- mental model;
- trust/UI/UX;
- final/absolute canon variants.

Important: many sections repeat with later corrections. Deep context records conflicts instead of treating every duplicate as separate current law.

### 3220–4054 — Sovereign / Universe / Host / Recovery
Covered by:
- `sovereign-fabric.md`

Contains:
- local vs public/sovereign execution;
- isolation planes;
- HSP;
- deterministic resurrection;
- HSR-A;
- auto restart;
- memory governance;
- consolidated sovereign fabric;
- anchor/TSA/quorum;
- cross-universe permission.

### 4055–5154 — Creator + Constitutional layers
Covered by:
- `sovereign-fabric.md`
- `constitutional-locks.md`

Contains:
- Creator universe;
- publication;
- resource/economy containment;
- constitutional locks;
- FSM;
- economic;
- catastrophic continuity;
- version/evolution;
- sandbox tiers;
- reproducible implementation;
- runtime determinism;
- crash/recovery;
- storage/I/O;
- human/operational determinism.

### 5155–6530 — AAAA Game + NCF
Covered by:
- `game-aaaa-ncf.md`

Contains:
- G1–G12;
- G14–G19;
- drift vs fork;
- deterministic multiplayer;
- toolchain/numeric/world/AI/network/hardware laws;
- NCF;
- ArtifactSpec/CIR/seal;
- capability composition.

Note: source registry has no named G13 in this mapping.

### 6530–7102 — Capability governance / public registry / chaos
Covered by:
- `capability-registry-chaos.md`

Contains:
- G20 registry;
- G21 admission;
- G22 RCS;
- G23 public view;
- G25 chaos.

Note: source mapping has no named G24 in this sequence.

### 7103–8297 — vNEXT.1 Execution Pack
Covered by:
- `doc-c-vnext-build-spec.md`

Contains:
- canonical type system;
- runtime contracts;
- module architecture;
- FSM;
- pipeline;
- APIs;
- auth;
- storage;
- RBAC;
- observability;
- config;
- queue;
- retention;
- tests;
- UI truth;
- build order.

### 8298–8957 — Merged DOC-B/DOC-C canonical pack
Covered by:
- `doc-c-vnext-build-spec.md`
- `human-control-surface.md`

Contains:
- document authority hierarchy;
- later canonical defaults;
- route-level API pack;
- exact state/error/auth semantics;
- merged gap closure.

Later canonical values supersede conflicting earlier draft defaults where explicitly stated.

### 8958–9371 — DOC-D / storage / auth hardening
Covered by:
- `doc-d-product-design.md`

Contains:
- screens/components;
- product flow;
- permission visibility;
- loading truth;
- onboarding/trust;
- migration-ready storage rules;
- auth-hardening pack.

### 9372–9471 — DOC-E Deployment Evidence Pack
Covered by:
- `doc-e-deployment-evidence.md`

Contains:
- E1–E12;
- evidence metadata;
- deployment runbook;
- signoff;
- queue/monitor/incident/migration proof.

### 9472–10337 — L1o / Lo3 / Lo2 vision + L600
Covered by:
- `intelligence-trinity.md`

Contains:
- early hyper-deep vision;
- bounded-truth correction;
- L1o 7-layer L600;
- Lo3 8-layer L600;
- Lo2 9-layer L600;
- memory/evolution/security;
- user-scale intelligence flywheel;
- vision-vs-governance conflicts.

### 10338–10814 — Robotics / RCL / hardware stack
Covered by:
- `robotics-rcl.md`

Contains:
- risks of direct L1o+Lo3 robotics;
- RCL-L600;
- dual brain;
- sensor fusion;
- decision/control;
- Safety Kernel;
- mini swarm;
- physical stack;
- ROS2/MCUs;
- safety loops/build phases.

### 10815–10979 — Final Absolute Architecture
Covered by:
- `final-architecture-cross-system.md`

Contains:
- final 10-layer system;
- IRL/CIRL/CLE/L1o/Lo3/DSL/RSEL/ECL/Safety/Lo2;
- uncertainty propagation;
- time-bounded intelligence;
- no-single-point trust;
- fail-safe dominance;
- final 5-state risk model;
- bounded intelligence;
- final conceptual equation/failure classes.

# Completeness rule
This coverage means the **major architecture domains and late-source governing specifications have been captured**.

It does not mean:
- every repeated sentence was copied;
- every older discarded proposal remains authoritative;
- implementation was audited;
- runtime was verified.

Future work should use the deep context as a normalized map, then return to the original source only when exact wording/older evolution history is needed.

# Resume protocol
If a future model needs to continue source extraction:
1. read `deep/README.md`;
2. read this coverage map;
3. read the domain-specific deep file;
4. compare against latest relevant source range;
5. append conflict/status, never silently overwrite governance history.
