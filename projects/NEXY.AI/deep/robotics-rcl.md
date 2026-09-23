# NEXY.AI — Robotics / Robot Control Layer (RCL-L600) Deep Context

## Status
SOURCE-DESIGN / HARDWARE DIRECTION. NOT VERIFIED RUNTIME OR PHYSICAL SYSTEM.

This file distinguishes:
- conceptual robotics architecture;
- RCL-L600 control semantics;
- suggested prototype hardware/software;
- claims that require real physical evidence.

No source prose here should be interpreted as proof of a functioning robot, certified safety system, medical/autonomous-vehicle readiness or real-time guarantee.

# 1. Why L1o + Lo3 cannot simply be placed directly into a robot

The source explicitly identifies a mismatch between deep verified reasoning and physical real-time control.

Naive behavior:
`Sense → Analyze → Verify → Attack → Re-check → Act`

Advantages:
- deeper verification;
- self-check before actuation;
- lower willingness to guess.

Risks:
- latency;
- indecision/freeze when information is incomplete;
- sensor ambiguity;
- over-verification;
- physical consequences of software failure.

Examples in the source illustrate:
- surgery: deep simulation/verification helps precision but adds latency;
- autonomous driving: waiting for full verification can be unsafe in an immediate hazard;
- factory robotics: constrained/predictable environments fit the architecture better.

These are design examples, not domain-safety claims.

# 2. Required adaptation for embodied systems

Four problems are called out before using L1o/Lo3 physically:

1. **Latency**
   - full reasoning is slower;
   - requires Fast Path vs Safe Path.

2. **Sensor uncertainty**
   - the real world is noisy;
   - requires probabilistic/confidence wrapper and sensor fusion before deterministic reasoning.

3. **Over-verification**
   - adversarial loops can delay action;
   - requires time-bounded reasoning and bounded swarm size/rounds.

4. **Physical risk**
   - a wrong software action can injure people/damage hardware;
   - requires independent hardware failsafe and emergency-stop authority.

# 3. RCL-L600 goal

The Robot Control Layer is designed to make decisions that are:
- fast enough for real-time use;
- safe enough for the physical world;
- verifiable under explicit constraints.

Top-level flow:
`Sensors → Perception → Decision (L1o + Lo3 hybrid) → Control → Actuators`

But the actual architecture adds:
**Fast Brain + Safe Brain + independent Kill/Safety system.**

# 4. Dual-Brain architecture

## 4.1 Fast Path / Reflex System
Target in the design:
- <10 ms class behavior for immediate reflex rules.

Used for:
- obstacle avoidance;
- balance;
- emergency stop;
- other precomputed time-critical actions.

Uses:
- heuristic/precomputed deterministic safety rules;
- no full L1o/Lo3 cycle.

Example:
`if distance < threshold → STOP immediately`

Reason:
some physical hazards cannot wait for multi-agent reasoning.

## 4.2 Safe Path
Design range:
- approximately 50–500 ms for deeper decisions depending on task;
- a separate later critical-loop target is <100 ms total for the safety-critical control path, creating a design tension that must be resolved through profiling and domain-specific budgets.

Used for:
- planning;
- important multi-step decisions;
- non-reflex action selection.

Runs:
- L1o reasoning;
- bounded Lo3 adversarial verification;
- simulations/constraints.

Dispatch concept:
`if time_critical → FAST PATH; else → SAFE PATH`

The source presents this split as the mechanism preventing deep-verification behavior from freezing real-time survival actions.

# 5. Perception Layer

Raw sensors are not passed directly into reasoning.

Sensor Fusion example:
`camera + lidar + IMU → unified state`

State carries:
- semantic object;
- position;
- confidence/uncertainty.

Low-confidence state is explicitly marked uncertain before downstream reasoning.

This fits the later Final Architecture rule:
**No raw input enters reasoning.**

# 6. Hybrid Decision Layer

Decision sequence:
1. generate candidate actions;
2. simulate outcomes;
3. apply constraints;
4. run bounded Lo3 attack;
5. select a safe candidate.

Action model includes:
- action identifier;
- risk;
- confidence.

Deadline rule:
`if decision_time > deadline → fallback to Fast Path/safe default`

Important: fallback behavior must itself be predeclared and safety-validated. “Fallback” cannot become an implicit guess.

# 7. Control Layer

Converts abstract action → actuator commands.

Example:
`move_forward → motor_left / motor_right command`

Closed-loop behavior:
`action → sensor feedback → correction`

The control layer is lower-level than cognition and must remain bounded by safety authority.

# 8. Immutable / independent Safety Kernel

The source repeatedly states that AI must not be the sole physical safety authority.

Safety Kernel is separate from normal AI reasoning and dominates it.

Named safety functions:
- Collision Prevention;
- Force Limit;
- Boundary Constraint;
- Emergency Stop.

Examples:
- distance below minimum → override STOP;
- force above safe limit → actuator shutdown;
- out-of-zone → safe-area behavior.

RCL ordering given in source:
`Safety Kernel > L1o > Lo3`

The broader final architecture phrases the invariant:
**Safety > Decision > Intelligence.**

Important: “Safety Kernel must never fail” is a requirement/aspiration, not a physically provable absolute. Real implementation needs redundant hardware, hazard analysis and validation.

# 9. Real-Time Lo3 / Mini-Swarm

Full Lo3 is intentionally reduced for robotics.

Design recommendation:
- use only critical/non-reflex decisions;
- approximately 2–3 agents;
- approximately 2–3 attack rounds.

Purpose:
preserve adversarial checking without allowing the swarm to violate the real-time budget.

Potential uses:
- route planning;
- multi-agent planning;
- high-consequence multi-step decision critique.

# 10. Failure Handling

### Sensor failure
Loss of a sensor → switch to predefined backup path if available.

### Decision timeout
Timeout → safe default / Fast Path behavior, not endless reasoning.

### No safe action
Conflict with no safe candidate → STOP + alert.

This is a physical-world interpretation of fail-safe dominance.

# 11. Performance model

Source budget examples:
- sensor stage ~5 ms;
- Fast Path ~5 ms;
- Safe Path ~50–200 ms in one table;
- control ~5 ms;
- target critical loop <100 ms.

Another source passage allows Safe Path ~50–500 ms.

Therefore exact latency is **UNRESOLVED / DOMAIN-DEPENDENT**. The source contains multiple conceptual budgets and real hardware tests must set the actual contract.

RCL flow:
`Sensors → Fusion → Critical? → Fast Path OR L1o+Lo3 → Safety Kernel → Execute → Feedback`

# 12. Physical architecture

Suggested source topology:
`Sensors → Edge Compute/Fast Brain → Main Compute/L1o+Lo3 → Control Board → Actuators`

## Main AI computer
Source suggests:
- NVIDIA Jetson Orin NX;
- AGX Orin when higher budget is available.

Intended workloads:
- L1o engine;
- Lo3 mini-swarm;
- simulation;
- local AI models.

This is a hardware recommendation from design prose, not a locked hardware requirement.

## Fast Brain MCU
Source suggestions:
- STM32;
- Raspberry Pi Pico for simpler prototype.

Runs:
- Fast Path;
- reflex logic;
- emergency handling.

## Dedicated Safety MCU
Must be separate from the AI path in the design.

Suggestions:
- second STM32;
- Arduino-class controller for prototype.

Functions:
- kill switch;
- force limit;
- collision override.

The intended property is that AI failure does not disable the safety controller.

# 13. Sensor stack

Source examples:
### Vision/depth
- Intel RealSense;
- ZED camera.

### Distance/mapping
- RPLidar A2/A3 example.

### Motion
- MPU6050 / BNO055 IMU examples.

### Contact/safety
- ultrasonic sensors;
- force sensors.

Sensor fusion creates the world model.

These are prototype examples and may be outdated/inappropriate for a specific safety domain; do not treat them as certified components.

# 14. Actuation

Examples:
- DC motors + encoders;
- servo/stepper for arms;
- L298N as simple prototype driver;
- BTS7960 as a stronger example.

Again: prototype guidance only.

# 15. Software stack

Suggested source stack:
- Ubuntu;
- ROS2 (Humble/Iron named in source);
- FreeRTOS on STM32;
- C++ for ROS2/performance;
- Python for L1o prototyping;
- ONNX Runtime / TensorRT;
- quantized local LLM;
- Gazebo simulation;
- RViz visualization.

Version names are source-era examples, not evergreen current requirements.

# 16. NEXY software mapping to robotics

Source mapping:
- L1o → ROS2 node `logic_engine`
- Lo3 → ROS2 node `swarm_governor`
- Fast Path → MCU firmware in embedded C/C++
- Safety Kernel → independent MCU loop, explicitly **no ROS dependency**

This keeps the safety path outside the high-level AI runtime.

# 17. Communications

Main system:
- ROS2 DDS.

MCU ↔ main computer:
- UART / CAN Bus.

Authority flow:
`AI proposes command → control MCU executes → Safety MCU may override`

The exact bus/topology/redundancy contract remains implementation-specific.

# 18. Real-time loops

Conceptual source loops:
### Fast loop
~10 ms:
`sensor → MCU → reflex action`

### Slow/deep loop
~100 ms class:
`sensor → L1o → Lo3 → decision`

Actual deterministic real-time requirements must be measured on target hardware.

# 19. Physical safety mechanisms

Named mechanisms:
- physical hardware kill switch;
- software watchdog;
- redundant stop capability through control MCU + safety MCU.

Example watchdog:
`if no signal → shutdown`

The architecture requires safety to remain functional when AI or ROS fails.

# 20. Build phases

### Phase 1 — Prototype
- Jetson Orin NX class main compute;
- one MCU;
- camera + ultrasonic;
- simple obstacle avoidance.

### Phase 2 — Add Intelligence
- L1o logic;
- simple Lo3, around two agents.

### Phase 3 — Full NEXY robotics direction
- dual MCU;
- independent/full safety kernel;
- bounded swarm optimization.

The source gives a rough historical prototype estimate around USD 500–1500; this is not a current price quote and should not be used for procurement without current research.

# 21. Deterministic Action Engine

The source wants:
same sufficiently equivalent physical state + same governed inputs → same bounded action.

However real sensors are noisy, so the deterministic contract applies **after perception normalization/confidence quantization**, not to raw analog reality itself.

This is why IRL/perception exists ahead of L1o.

# 22. Self-Debugging / Zero-Trust action concepts

Robotics extensions include:
- continuous self-diagnosis;
- distrust raw sensor/model/user input until it passes the appropriate checks;
- explicit action verification;
- evidence around why an action was selected.

These are design goals. “Zero Trust” does not mean zero uncertainty.

# 23. Important physical-proof boundary

The following cannot be established from source code/design text alone:
- physical Safety MCU correctness;
- actuator stop distance;
- sensor accuracy;
- real watchdog independence;
- bus timing;
- thermal/power behavior;
- electromagnetic/mechanical faults;
- real-time latency under load;
- human-safety certification;
- surgical/automotive suitability.

Required evidence classes would include:
- simulation;
- hardware-in-the-loop tests;
- fault injection;
- timing traces;
- independent safety-controller tests;
- power-loss tests;
- physical emergency-stop tests;
- domain-specific hazard/safety certification where applicable.

# 24. Core robotics insight

The source’s strongest robotics invariant is:

**Fast Brain = survive now.  
Safe Brain = reason carefully.  
Safety Kernel = independent authority that can stop both.**

The architecture intentionally refuses to let “more intelligence” replace physical safety engineering.
