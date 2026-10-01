# NEXY — COMPLETE SYSTEM INVENTORY

## AI AUTHORITY NOTICE

ระบบทั้งหมดของ NEXY ที่ถอดจาก `NEXY_FULL_PROJECT_SYSTEM_FEATURE_PERCENT_MATRIX.xlsx` อยู่ในเอกสาร inventory นี้แล้ว

AI MUST:
- ใช้เอกสารนี้เป็น COMPLETE SYSTEM INVENTORY สำหรับชื่อระบบและขอบเขตระบบของ NEXY
- ตรวจรายการนี้ก่อนสรุปว่า NEXY มีหรือไม่มีระบบใด
- ห้ามเดาหรือสร้างชื่อระบบเพิ่มโดยไม่มี authoritative evidence
- หากข้อมูลขัดกับ authoritative specification ที่ใหม่กว่า ให้ FREEZE ข้อสรุปส่วนนั้นและตรวจ source ก่อน
- ห้ามใช้หรือเติมค่าเปอร์เซ็นต์ใน inventory นี้

Source workbook contained 74 system groups and 935 requirement/system-feature records. Percentage fields are intentionally omitted.

## COMPLETE SYSTEM LIST

### DOC-B
- DOC-B System Law — governing system law; no normalized audit controls in source matrix.

### DOC-C
- Auth hardening — current build; DOC-C BUILD SPEC.
- Build Order — current build; DOC-C BUILD SPEC.
- Canonical API — current build; DOC-C BUILD SPEC.
- Canonical config — current build; DOC-C BUILD SPEC.
- Canonical contracts — current build; DOC-C BUILD SPEC.
- Configuration — current build; DOC-C BUILD SPEC.
- FSM / state control — current build; DOC-C BUILD SPEC.
- Module architecture — current build; DOC-C BUILD SPEC.
- Observability — current build; DOC-C BUILD SPEC.
- Queue — current build; DOC-C BUILD SPEC.
- RBAC — current build; DOC-C BUILD SPEC.
- Reference stack — current build; DOC-C BUILD SPEC.
- Retention / redaction — current build; DOC-C BUILD SPEC.
- Runtime enforcement — current build; DOC-C BUILD SPEC.
- Scope fence — current build; DOC-C BUILD SPEC.
- SWARM / JUDGE / LAW — current build; DOC-C BUILD SPEC.
- System baseline — current build; DOC-C BUILD SPEC.
- Test / CI gate — current build; DOC-C BUILD SPEC.
- UI truth layer — current build; DOC-C BUILD SPEC.
- Vault / storage — current build; DOC-C BUILD SPEC.

### DOC-D
- Product screens — supported product design; DOC-D PRODUCT DESIGN.
- UX contract — supported product design; DOC-D PRODUCT DESIGN.

### DOC-E
- Exact-head deployment evidence — deployment evidence; DOC-E DEPLOYMENT EVIDENCE.

### SOURCE-DESIGN SYSTEMS

Unless explicitly overridden below, source-design classification must be read from the authoritative source evidence and must not be guessed.

### CURRENT REQUIRED FULL-PROJECT SCOPE — OVERRIDE

The following systems are **CURRENT REQUIRED FULL-PROJECT SCOPE**. AI MUST NOT label, classify, defer, exclude, or describe them as Future, Extension, optional future work, or out-of-current-project scope:

- Game Fabric, including G1–G10 and its required supporting game/runtime fabric.
- Universe, including Universe isolation and required cross-universe capability/permission mechanisms.
- Robotics, including Fast Brain, Safe Brain, sensor/control/safety integration and required robotics runtime components.
- Sovereign systems, including Sovereign continuity and the required constitutional/authority/continuity mechanisms.
- Lo2, including verified learning, Logic Quantum provenance, governed law synthesis/evolution, USL ledger and federation-law mechanisms.

This scope classification is authoritative for project planning and completeness evaluation. **Required does not mean implemented or verified.** Implementation/verification status still requires repository artifacts, tests, logs, or reproducible evidence.

Other source-design systems listed below retain their source-evidence classification unless separately overridden by authoritative project instructions.

- Auto recovery — playbook controller.
- Build reproducibility — compiler/container/locale/path/build-environment reproducibility lock.
- Builder Engine — AppSpec registry + canonical spec hash.
- CIRL — explicit intent/constraints/risk/ambiguity resolution.
- CLE — logical/resource/safety/temporal law classes.
- Constitutional Fabric — kernel authority / Vault / Canon / recovery backbone.
- Crash/recovery — guardian final seal + WAL flush; pre-death/pre-kill tamper-evident snapshot.
- Cross-universe permissions — signed PermissionGrant with scope/rate/expiry/dual signatures.
- Deployment direction — Web/PWA/mobile delivery / edge-friendly UI.
- Detection model — immutable core signature/Merkle/hash continuity detection.
- DSL — one deterministic action from scored internal candidates.
- ECL — Fast/Safe/Timeout-fallback execution modes.
- Economic layer — CSU/LAL append-only ledger; deterministic escrow; immutable revenue share; deterministic minting constraint; dispute resolution; degraded settlement; DoS bond/fee floor; finalized-anchor ledger finality.
- G12 Cross-shard transfer — hash-bound export/import + replay protection.
- G14 Toolchain — deterministic build spec/artifact hashes.
- G15 Numeric law — Q64.64 fixed-point authoritative numeric operations.
- G16 Crowd budget — deterministic shard quota/overflow.
- G16 World topology — integer/BigInt world partition.
- G17 AI/crowd determinism — crowd/AI deterministic controls.
- G18 Networking — canonical packet schema/tick delay/order hashing.
- G19 Hardware determinism — architecture whitelist/target triple; microcode/firmware/binary boot attestation; ECC/physical power/clock/bitflip enforcement.
- G1–G10 Game Fabric — GameSpec/state/runtime/firewall/base fabric.
- G20 Capability registry — versioned immutable capability nodes.
- G21 Admission — static verifier + human quorum model.
- G22 Rejection codes — R001–R010 / R101–R110.
- G23 Public registry view — sanitized public registry snapshot.
- G25 Chaos — A001–A012 deterministic isolated attack-vector simulation.
- Global Anchor — fixed 5-region 3/5 authority; TSA/chain time witness model; anchor publication FSM to FINALIZED.
- Human/operational determinism — hash-chained operator action log.
- Implementation verification — static compliance scan.
- IRL — sensor interface + normalization + noise filter + confidence.
- L1o — certainty tiers T0–T4; MPG multi-path reasoning; MPG+EPE advisory; ICL ambiguity/normalization; Void Architect/recall/auto-learn ecosystem.
- Lifecycle — sovereign lifecycle; app lifecycle; spec mutation requires rebuild/new spec_hash.
- Lo2 — verified-input-only learning; Logic Quantum provenance; governed law synthesis/evolution; USL hash-chained ledger; signed federation law distribution/dry-run.
- Lo3 — swarm governor macro pipeline; trust ledger; Cage sandbox; prompt-law filter.
- Memory model — task/session/project scoped state; persistent Vault distinction; provenance-aware durable truth.
- Named product surfaces — NEXY::FRONT/VIEW/RUN/FORGE; NEXY::PULSE; NEXY::DIALOG; NEXY::GUARD.
- Node security — HSM/TPM/boot attestation authority.
- Public mode — Private / Invite / Public / Marketplace lifecycle.
- Robotics — Fast Brain; Safe Brain; sensor fusion; perception/planner; safety verifier; arbitration; actuator bridge; CAN zero-trust; ROS2; STM32 watchdog/SIGSAFE/reflex; independent safety MCU/kill switch; FreeRTOS integration; Python L1o prototype.
- RSEL — Risk = Impact × Probability × Uncertainty.
- Runtime determinism — non-determinism scan + replay verification.
- Runtime integrity — canonical state hashing + freeze callback.
- Sandbox — depth/tier guard; deterministic WASM; Firecracker/Kata/runc/gVisor/WASM routing; escape detection.
- Sovereign continuity — Vault/audit/ledger continuity; partition / 3-of-5 unreachable degradation law.
- Storage containment — hash-chained WAL gateway.
- Trinity — L1o + Lo3 + Lo2 binding.
- Universe — capability registry; user-tier grants; cross-app typed channels; sandbox runtime/isolation selection.
- Universe isolation — container/namespace/syscall/memory/WASM isolation policy.
- Versioning law — proposal/ratify/deploy/revert lifecycle.

## SOURCE DETAIL RULE

The uploaded workbook contains 935 normalized requirement/system-feature records. This file is the system-level inventory. When exact feature-level wording, source location, dependency, validation evidence, or record ID is required, use the source workbook-derived detailed inventory rather than inventing missing detail.

No percentage values belong in this inventory.
