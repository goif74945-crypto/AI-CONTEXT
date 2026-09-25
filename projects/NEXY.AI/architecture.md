# NEXY.AI — Architecture Context

## 1. Source and scope boundary

This file normalizes the uploaded design into architecture context. DOC-C is the current vNEXT build specification; DOC-D supplies product design where DOC-C supports it. The Final Architecture is a conceptual model, not a claim about the live code. Runtime and deployment claims require exact-head tests, logs or DOC-E evidence.

## 2. System shape

The source describes NEXY as a **Core AI Control Hub** with a small user-facing surface and a large controlled backbone. The architecture separates authority, reasoning, multi-agent work, safety, execution, persistence, interface and external integrations.

The final conceptual flow is:

```text
Input → IRL → CIRL → CLE → L1o → Lo3 → DSL → RSEL → ECL → one verified output or freeze
                                      ↑          ↑
                               Safety Kernel dominates execution
                                      ↑
                              Lo2 receives governed feedback only
```

The Safety Kernel is independent and dominant for safety-critical execution. Lo2 is a governed feedback/learning layer; it does not silently patch the current runtime law.

## 3. Canonical conceptual layers

### Input Reality Layer (IRL)

Converts raw real-world/input data into structured truth candidates. Components described include sensor interfaces, normalization, noise filtering and confidence estimation. Raw input should not enter reasoning unnormalized.

### Context & Intent Resolution Layer (CIRL)

Resolves the intended task and explicit constraints, with outputs such as intent, constraints and risk level. Ambiguity is a blocking condition when it affects correctness; missing material facts must not be guessed.

### Constraint Law Engine (CLE)

Converts intent/requirements into explicit constraints. Named law classes include Safety Law, Logical Law, Resource Law and Temporal Law.

### L1o — Sovereign / Deterministic Logic Core

The source uses L1o as the sovereign deterministic logic core. Its bounded truth tiers are T0 Unknown, T1 Heuristic, T2 Empirical, T3 Formally Verified and T4 Immutable Law. The source does not establish one universal numeric CTS threshold; numeric threshold conflicts remain unresolved and must not be invented here.

Later specifications add path reduction/Top-K collapse, time-bounded reasoning and state-transition graphs. A stricter later version uses normalized input, ambiguity checking, requirement parsing, deterministic reasoning, verification and bounded execution behavior. L1o is not the whole control stack: DSL, RSEL, ECL and the immutable Safety Kernel remain separate layers.

### Lo3 — Swarm Governor

Coordinates multiple agents/models. The source describes context sharding, parallel/concurrent agents, bounded adversarial loops, weighted proof consensus, trust/evaluation, conflict resolution, deterministic re-run and elimination of inconsistent results. Agents are intended to be isolated from each other's answers until the comparison stage in the stricter swarm model.

### DSL / Decision Synthesis Layer

Combines L1o + Lo3 into candidate action sets with scores/selection information. Internal Top-K or multiple candidates do not bypass the final release rule: release one legal verified output or freeze. The exact numeric scoring mechanism in the source is conceptual and must not be treated as a verified production algorithm.

### RSEL — Risk & Safety Evaluation Layer

The source represents risk conceptually as:

```text
Risk = Impact × Probability × Uncertainty
```

The stated hard rule is to block an action when risk exceeds a defined threshold. This is a design heuristic; the source does not provide a universally validated production calibration.

### ECL — Execution Control Layer

Converts a verified decision into an executable action. Named controls include Fast Path, Safe Path and timeout fallback.

### Safety Kernel

An immutable, independent safety layer that must not be overridden by the AI reasoning stack. Functions described include collision prevention, force limits, boundary enforcement and emergency stop.

### Lo2 — Singularity Core / Feedback & Learning Loop

The source uses Lo2 for a higher-level learning/synthesis layer. It is described as extracting logic quanta, synthesizing laws, evolving laws under verification, anti-poison filtering and maintaining a distributed/immutable knowledge structure. Later sections call it a Singularity Core and a machine that turns verified experience into laws. Current DOC-C does not authorize silent self-patching of the live runtime.

## 4. Authority model

The source distinguishes the human/user authority from system internals.

```text
USER LAW
   ↓
NEXY::LAW
   ↓
NEXY::CORE / L1o
   ↓
NEXY::JUDGE / DSL
   ↓
NEXY::SWARM / Lo3
   ↓
ECL, subject to RSEL and Safety Kernel
```

When LAW says stop, downstream execution stops. The UI may expose control surfaces but should not redefine core authority or silently change core naming/semantics.

## 5. Truth and uncertainty model

The final architecture repeatedly emphasizes:

- Never output unverified action.
- Quantify uncertainty.
- Propagate uncertainty through input → reasoning → decision → action.
- Bound reasoning to the domain and time budget.
- Do not assume perfect knowledge, zero error or infinite reasoning.
- Prefer bounded intelligence + verified outputs + adaptive learning.

The risk/intelligence states in the conceptual architecture are:

```text
NORMAL → CAUTION → UNCERTAIN → CRITICAL → FAILSAFE
```

These are not the same as the current DOC-C execution FSM. The current build-oriented execution states are `INIT → READY → RUNNING → VERIFYING → CONSENSUS → STABLE`, with `FREEZE` and `STOP` side paths. A context reader must not merge the two state machines.

## 6. Determinism

The design goal is deterministic execution and repeatability. The broader project constraints require avoiding hidden randomness, time/environment-dependent core behavior, uncontrolled shared mutable state and unspecified ordering. Any future implementation must prove the actual deterministic contract with tests rather than inherit the claim from design prose.

## 7. Freeze model

Freeze is a first-class state, not an error message decoration. The source names freeze triggers including agent disagreement, policy conflict, ambiguous/insufficient input, unsafe states and detected integrity/security failures. The architecture explicitly rejects silently patching, forcing through contradictions or continuing after a critical integrity failure.

## 8. Multi-AI orchestration

The intended orchestration pipeline is:

1. Decompose the task.
2. Route/select agents.
3. Run parallel debate/work.
4. Perform adversarial review.
5. Cross-verify independent outputs.
6. Reach proof-weighted consensus.
7. Judge/adjudicate.
8. Release only the verified result.

The source treats GPT, Gemini, Claude, local/custom, legacy/new and specialized models as interchangeable workers behind the control layer rather than authorities over NEXY.

## 9. Memory and Vault architecture

The Vault is described as file-based, project-based and timeline-based. It is the persistent project source of truth. It supports pin/unpin, deletion policy, restore/permanent erase and minimal output views.

Memory concepts across the source include Task Memory, Session Memory, Working Memory, Verified/Immutable Memory, Experimental Memory, Quanta Memory, Law Memory and Deprecated Memory. Durable knowledge should be explicit, scoped and provenance-aware; uncontrolled/mushy core memory is rejected.

## 10. API and backend architecture

The source defines:

```text
Frontend → API Gateway → Core Logic → External APIs
```

The general direction favors serverless and database-agnostic deployment. The current DOC-C reference implementation target is Next.js + TypeScript, Route Handlers or a Node API, Zod, PostgreSQL, Prisma, BullMQ + Redis, email OTAC with secure cookies, blob/object storage, structured JSON logs with trace IDs, and Vitest/Playwright/Prisma integration tests. Frontend code should not expose real provider APIs or API keys. Secrets are server-side and injected at runtime.

## 11. UI / UX architecture

The source distinguishes UI, GUI/control panel and hidden Core authority. Named surfaces include NEXY::FRONT, NEXY::PULSE, NEXY::DIALOG, NEXY::GUARD, NEXY::VIEW, NEXY::RUN and NEXY::FORGE.

The UI DNA is minimal, premium, information-dense, adaptive, chat-centric and low-RAM safe. The user-facing layer should not make policy decisions that belong to LAW/CORE/JUDGE.

## 12. Security architecture

Design claims/targets include zero-trust input validation, prompt-injection resistance, model boundaries, RCE blocking, execution sandboxing, immutable auditing, authentication and access controls, session isolation, encryption/key management, rate limiting, breach isolation, freeze-on-anomaly, secret scanning and server-only API credentials. These remain architecture requirements until backed by implemented controls and reproducible tests.

## 13. Robotics architecture

Physical mapping described by the source:

```text
Sensors → Edge Compute / Fast Brain → Main Compute / L1o + Lo3 → Control Board → Actuators
```

Main compute: Jetson Orin NX or AGX Orin is suggested. Fast real-time layer: STM32 or Raspberry Pi Pico is suggested. A dedicated independent safety MCU is suggested for prototype safety functions. Sensor examples include depth/vision camera, LiDAR, IMU, ultrasonic and force sensors. Software examples include Ubuntu + ROS2, FreeRTOS, ONNX Runtime/TensorRT, Gazebo and RViz.

NEXY software mapping:

```text
L1o → ROS2 logic_engine node
Lo3 → ROS2 swarm_governor node
Fast Path → MCU firmware
Safety Kernel → independent MCU loop
```

The source gives example loops of about 10 ms for fast reflex control and about 100 ms for the slower AI loop. It also contains conflicting Safe Path budgets of about 50–200 ms and 50–500 ms, plus a critical target under 100 ms. These are source examples, not one canonical physical budget; the exact budget is unresolved and requires hardware/domain profiling before implementation claims.

A hardware kill switch and redundant stopping paths are emphasized.

## 14. Robotics safety principle

The source's strongest robotics insight is the separation of **Fast Brain (survival/reflex) + Safe Brain (reasoning) + Safety Kernel (independent protection)**. AI must not be the sole safety authority.

## 15. Build-phase direction for robotics

- Phase 1: prototype with Jetson + one MCU + camera/ultrasonic for simple obstacle avoidance.
- Phase 2: add L1o logic and a simple two-agent Lo3.
- Phase 3: dual MCU, full safety kernel and swarm optimization.

This is not AGI robotics and reasoning remains bounded.

## 16. Canonical formula / design summary

The source presents a conceptual equation:

```text
Intelligence = Verified Logic
            × Constraint Integrity
            × Safety Enforcement
            × Learning Efficiency
```

This is a design principle, not a mathematically validated production metric.
