# NEXY.AI — Architecture Context

## 1. System shape

The source describes NEXY as a **Core AI Control Hub** with a small user-facing surface and a large controlled backbone. The architecture separates authority, reasoning, multi-agent work, safety, execution, persistence, interface and external integrations.

Conceptual top-level flow:

```text
User Input
  ↓
Input / Intent Resolution
  ↓
USER LAW + Constraint / Policy Gate
  ↓
L1o Deterministic Logic Core
  ↓
Lo3 Swarm Governor / Multi-Agent Debate
  ↓
Cross-Verification / Adversarial Review
  ↓
JUDGE / Decision Synthesis
  ↓
Risk + Safety Evaluation
  ↓
Execution Control
  ↓
Verified Output
  ↓
Vault / Audit / Feedback
```

The source also describes an even stricter runtime stack for embodied systems, where a dedicated Safety Kernel dominates any AI decision.

## 2. Canonical conceptual layers

### Input Reality Layer (IRL)
Converts raw real-world/input data into structured truth candidates. Components described include sensor interfaces, normalization, noise filtering and confidence estimation. Raw input should not enter reasoning unnormalized.

### Context & Intent Resolution Layer (CIRL)
Resolves the intended task and explicit constraints, with outputs such as intent, constraints and risk level. Ambiguity is a blocking condition when it affects correctness.

### Constraint Law Engine (CLE)
Converts intent/requirements into explicit constraints. Named law classes include Safety Law, Logical Law, Resource Law and Temporal Law.

### L1o — Deterministic Logic Core
The source describes L1o as the sovereign deterministic reasoning core. Later specifications add bounded truth tiers (T0–T4), path reduction/Top-K collapse, time-bounded reasoning and state-transition graphs. A stricter later version uses a seven-layer architecture with normalized input, ambiguity checking, requirement parsing, deterministic reasoning, verification and bounded execution behavior.

### Lo3 — Swarm Governor
Coordinates multiple agents/models. The source describes context sharding, parallel/concurrent agents, adversarial loops, weighted proof consensus, trust/evaluation, conflict resolution, deterministic re-run and elimination of inconsistent results. Agents are intended to be isolated from seeing each other's answers until the comparison stage in the stricter swarm model.

### DSL / Decision Synthesis Layer
Combines L1o + Lo3 into candidate action sets with scores/selection information. The exact numeric scoring mechanism in the source is conceptual and must not be treated as a verified production algorithm.

### RSEL — Risk & Safety Evaluation Layer
Computes/uses a risk model represented in the source as:

```text
Risk = Impact × Probability × Uncertainty
```

The stated hard rule is to block an action when risk exceeds a defined threshold.

### ECL — Execution Control Layer
Converts a verified decision into an executable action. Named controls include Fast Path, Safe Path and timeout fallback.

### Safety Kernel
An immutable, independent safety layer that must not be overridden by the AI reasoning stack. Functions described include collision prevention, force limits, boundary enforcement and emergency stop.

### Lo2 — Feedback / Learning / Singularity Core
The source uses Lo2 for a higher-level learning/synthesis layer. It is described as extracting logic quanta, synthesizing laws, evolving laws under verification, anti-poison filtering and maintaining a distributed/immutable knowledge structure. Later sections call it a Singularity Core and a machine that turns verified experience into laws.

## 3. Authority model

The source distinguishes the human/user authority from system internals.

```text
USER LAW
   ↓
NEXY::LAW
   ↓
NEXY::CORE
   ↓
NEXY::JUDGE
   ↓
NEXY::SWARM / agents
   ↓
execution
```

The intended rule is: when LAW says stop, downstream execution stops. The UI may expose control surfaces but should not redefine core authority or silently change core naming/semantics.

## 4. Truth and uncertainty model

The final architecture repeatedly emphasizes:

- Never output unverified action.
- Quantify uncertainty.
- Propagate uncertainty through input → reasoning → decision → action.
- Bound reasoning to the domain and time budget.
- Do not assume perfect knowledge, zero error or infinite reasoning.
- Prefer bounded intelligence + verified outputs + adaptive learning.

Defined runtime states in the later architecture are:

```text
NORMAL
CAUTION
UNCERTAIN
CRITICAL
FAILSAFE
```

Example transitions described by the source:

```text
uncertainty ↑ → CAUTION
risk ↑        → CRITICAL
failure       → FAILSAFE
```

## 5. Determinism

The design goal is deterministic execution and repeatability. The broader project constraints require avoiding hidden randomness, time/environment-dependent core behavior, uncontrolled shared mutable state and unspecified ordering. Any future implementation must prove the actual deterministic contract with tests rather than inherit the claim from design prose.

## 6. Freeze model

Freeze is a first-class state, not an error message decoration. The source names freeze triggers including agent disagreement, policy conflict, ambiguous/insufficient input, unsafe states and detected integrity/security failures. The architecture explicitly rejects silently patching, forcing through contradictions or continuing after a critical integrity failure.

## 7. Multi-AI orchestration

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

## 8. Memory and Vault architecture

The Vault is described as file-based, project-based and timeline-based. It is the persistent project source of truth. It supports pin/unpin, deletion policy, restore/permanent erase and minimal output views.

Memory concepts across the source include:

- Task Memory.
- Session Memory.
- Working Memory.
- Verified/Immutable Memory.
- Experimental Memory.
- Quanta Memory.
- Law Memory.
- Deprecated Memory.
- Memory conflict resolution via fork/simulation/selection.

Important constraint: uncontrolled/mushy core memory is rejected; durable knowledge should be explicit, scoped and provenance-aware.

## 9. API and backend architecture

The source defines:

```text
Frontend → API Gateway → Core Logic → External APIs
```

The API Gateway is expected to provide authentication, rate limiting and logging. Frontend code should not expose real provider APIs or API keys. Secrets are server-side and injected at runtime. Secret manager use is preferred; no hardcoded keys and no pasting secrets into source.

Backend direction: serverless preferred, database-agnostic, temporary session store, persistent Vault store, policy separation and immutable audit logging.

## 10. UI / UX architecture

The source distinguishes:

- UI — what the user sees and interacts with.
- GUI / control panel — richer control surfaces for an architect/power user.
- Core — hidden system authority.

Named surfaces include NEXY::FRONT, NEXY::PULSE, NEXY::DIALOG, NEXY::GUARD, NEXY::VIEW, NEXY::RUN and NEXY::FORGE.

The UI DNA is minimal, premium, information-dense, adaptive, chat-centric and low-RAM safe. It may include command bars, dashboards, agent monitors, theme adaptation, multilingual support and output views. The user-facing layer should not make policy decisions that belong to LAW/CORE/JUDGE.

## 11. Security architecture

Design claims/targets in the source include:

- Zero-trust input validation.
- Prompt-injection resistance.
- Model boundaries.
- RCE blocking.
- Execution sandboxing.
- Immutable auditing.
- Authentication and access controls.
- Session isolation.
- Encryption / key management.
- Rate limiting and abuse controls.
- Breach isolation and freeze-on-anomaly.
- Secret scanning and server-only API credentials.

These are architecture requirements/aspirations until backed by implemented controls and reproducible tests.

## 12. Robotics architecture

Physical mapping described by the source:

```text
Sensors
  ↓
Edge Compute / Fast Brain
  ↓
Main Compute / L1o + Lo3
  ↓
Control Board
  ↓
Actuators
```

Main compute: Jetson Orin NX or AGX Orin is suggested.

Fast real-time layer: STM32 or Raspberry Pi Pico is suggested.

Safety MCU: a dedicated independent STM32/Arduino-class controller is suggested for prototype safety functions.

Sensor examples: depth/vision camera, LiDAR, IMU, ultrasonic and force sensors.

Actuators: DC motors + encoder, servo/stepper and motor drivers such as L298N/BTS7960 for prototypes.

Software examples: Ubuntu + ROS2, FreeRTOS, ONNX Runtime/TensorRT, Gazebo and RViz.

NEXY software mapping:

```text
L1o → ROS2 logic_engine node
Lo3 → ROS2 swarm_governor node
Fast Path → MCU firmware
Safety Kernel → independent MCU loop
```

Communication examples: ROS2 DDS for the main system and UART/CAN between MCU and main computer.

Real-time model described:

```text
~10 ms fast loop: sensor → MCU → reflex action
~100 ms slower loop: sensor → L1o → Lo3 → decision
```

A hardware kill switch and redundant stopping paths are emphasized.

## 13. Robotics safety principle

The source's strongest robotics insight is the separation of:

**Fast Brain (survival/reflex) + Safe Brain (reasoning) + Safety Kernel (independent protection).**

AI must not be the sole safety authority.

## 14. Build-phase direction for robotics

- Phase 1: prototype with Jetson + one MCU + camera/ultrasonic for simple obstacle avoidance.
- Phase 2: add L1o logic and a simple two-agent Lo3.
- Phase 3: dual MCU, full safety kernel and swarm optimization.

The source explicitly notes this is not AGI robotics and that reasoning remains bounded.

## 15. Canonical formula / design summary

The source presents a conceptual equation:

```text
Intelligence = Verified Logic
            × Constraint Integrity
            × Safety Enforcement
            × Learning Efficiency
```

This should be treated as a design principle, not a mathematically validated production metric.