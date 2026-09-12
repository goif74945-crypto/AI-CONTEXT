# NEXY.AI — Project Overview

## Provenance

This context is derived from the uploaded project document **แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx** and from the existing `AI-CONTEXT` repository structure. It is a project-context record, not proof that the described system has been implemented or verified.

## Identity

NEXY is described as a deterministic AI control system / Core AI Control Hub, not a presentation-only website and not AGI. The central idea is architect-first, zero-guess, verify-only execution: external AI models may generate candidate work, but NEXY remains the authority that scopes, checks, routes, verifies, freezes, and exposes outputs.

A repeated canonical identity in the source is: **NEXY = a deterministic AI control system that produces a single verified result under explicit law/constraints.**

The source also uses the conceptual expansion **NEXY = Nexus of Execution** and defines the human-facing role as the interface between a human authority and AI while preserving human authority.

## Core principles

- Never output an unverified action.
- Never guess when required information is ambiguous or missing.
- User Law is the highest user-defined authority and must not be violated.
- Safety dominates decision, and decision dominates intelligence.
- When an error, contradiction, unsafe state, policy conflict, or insufficient evidence is detected, the system freezes rather than silently patching, guessing, or continuing.
- Deterministic behavior is a design target: the same relevant input, state, policy and constraints should produce the same structural result.
- The user should see the useful result, not the hidden core machinery.
- Complexity should scale behind a small user-facing surface.

## Intended role of the product

NEXY is intended as a controllable AI orchestration/control hub that can analyze, write, verify, route tasks, coordinate multiple AI agents, enforce laws/constraints, store project truth in a Vault, and expose controlled outputs. It is intended to automate knowledge/engineering work while keeping authority, proof, security, and rollback mechanisms explicit.

## Major named concepts

- **NEXY::CORE** — deterministic core authority; no guessing or uncontrolled creativity.
- **NEXY::LAW** — authority and rules, including User Law and system rules.
- **NEXY::JUDGE** — final deterministic adjudication layer.
- **NEXY::SWARM** — multi-agent labor/debate/orchestration layer.
- **NEXY::VIEW** — user-facing representation of trusted results.
- **NEXY::RUN** — execution control concept.
- **NEXY::FORGE** — build/generation concept.
- **NEXY::FRONT** — front/user entry surface.
- **NEXY::PULSE** — system/status feedback surface.
- **NEXY::DIALOG** — conversational/sandbox interaction surface.
- **NEXY::GUARD** — human safety / protective interaction layer.
- **VAULT** — project/file/timeline based persistent source of truth.
- **AGENT** — an individual AI worker/model slot.
- **SWARM** — multiple agents working with conflict resolution and verification.
- **USER LAW** — user authority that downstream behavior must obey.

## UX language and tone

The design favors a minimal, premium, information-dense, adaptive control-room experience. The source repeatedly distinguishes UI, GUI, and the hidden core. The user should not need to understand internal terminology to operate the product. The product language is intended to be human, concise, non-therapist, and non-patronizing.

The source explicitly rejects a therapist-style interaction pattern as the identity of the product. NEXY can communicate clearly and naturally, but its role is control, verification and execution rather than emotional counseling.

## Memory model

The project describes task/session/project-scoped memory and a Vault as the persistent source of truth. It rejects uncontrolled long-term memory. In later design material the memory model expands into working/verified/experimental or immutable/experimental tiers, with conflict handling, provenance, and verification before durable commitment.

## AI integration philosophy

AI models are treated as generators/workers rather than the authority of the system. The source describes hot-swapping across GPT, Gemini, Claude, local/custom/new/legacy/experimental and specialized models. The intended pipeline is:

**Decompose → parallel debate → adversarial review → cross-verify → consensus → final judge/output.**

AI may assist during build/generation, but the core system is intended to remain the source of operational truth; the project also describes both build-time AI assistance and runtime multi-AI orchestration, so those contexts must be kept distinct.

## Security direction

The design calls for zero-trust input handling, server-side secrets, API gateways, rate limiting, immutable audit logs, prompt-injection resistance, sandboxing, RCE blocking, access control, isolation, encryption, secret scanning, and freeze-on-breach behavior. API keys are explicitly server-only and should be injected at runtime rather than hardcoded.

## Auth direction

The initial auth model in the source is intentionally described as a temporary/simple V0 mechanism: email + one-time alphanumeric code, roughly 10 characters, TTL around 10–15 minutes, single-use, hash storage, limited guessing attempts and temporary sessions. The source explicitly says this is not MFA and not a full zero-trust identity system; later hardening is expected.

## Backend and data direction

The preferred backend direction is serverless and database-agnostic, with a temporary session store, persistent Vault store, policy separation and immutable audit logging. API architecture is described as Frontend → API Gateway → Core Logic → External APIs, with real provider details and keys hidden from the frontend.

## Deployment direction

The source mentions web/PWA/mobile delivery, edge rendering, low-resource safety, one-click deployment concepts, container/cloud options, monitoring, rollback and recovery. These are design targets, not implementation evidence.

## Robotics extension

A major later section extends NEXY into robotics. It maps:

- L1o → deterministic logic engine / ROS2 node.
- Lo3 → swarm governor / swarm controller node.
- Fast Path → MCU firmware.
- Safety Kernel → dedicated independent safety MCU.

The hardware direction includes a main AI computer such as Jetson Orin NX/AGX Orin, a real-time MCU such as STM32/Pico, a separate safety MCU, camera/depth sensing, LiDAR, IMU, ultrasonic/force sensing, motor/servo actuation, Ubuntu + ROS2, FreeRTOS, ONNX Runtime/TensorRT, Gazebo and RViz. The source emphasizes that AI must not be the only safety mechanism.

## Current interpretation

This repository entry should be treated as a structured, source-derived project context. Claims about implementation, production readiness, security, performance, deterministic guarantees, or deployment remain unverified until supported by repository artifacts, tests, logs, and reproducible evidence.