# NEXY.AI — Project Overview

## Provenance and authority boundary

This context is derived from the uploaded project document **แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx** and from the existing `AI-CONTEXT` repository structure.

- Source document SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- DOC-B is current system law; DOC-C is the current vNEXT build specification; DOC-D is current product design only where DOC-C supports it.
- The Final Architecture is conceptual architecture; DOC-E is deployment/runtime evidence only.
- Design, implementation, runtime behavior and deployment evidence are separate truth domains. A design statement is not proof that the NEXY implementation has that behavior.

## Identity

NEXY is described as a deterministic AI control system / Core AI Control Hub, not a presentation-only website and not AGI. The central idea is architect-first, zero-guess, verify-only execution: external AI models may generate candidate work, but NEXY remains the authority that scopes, checks, routes, verifies, freezes, and exposes outputs.

The source's stable behavioral rule is: **one legal, verified output or freeze/silence**. This is a release boundary, not a guarantee that every request will produce a result.

The source also uses the conceptual expansion **NEXY = Nexus of Execution** and defines the human-facing role as the interface between a human authority and AI while preserving human authority.

## Core principles

- Never output an unverified action.
- Never guess when required information is ambiguous or missing.
- User Law is the highest user-defined authority and must not be violated.
- Safety dominates decision, and decision dominates intelligence.
- When an error, contradiction, unsafe state, policy conflict, or insufficient evidence is detected, the system freezes rather than silently patching, guessing, or continuing.
- Deterministic behavior is a design target: the same relevant input, state, policy and constraints should produce the same structural result.
- The user should see the useful result or an explicit freeze state, not the hidden core machinery.
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

The source contains an early V0 direction of roughly a 10-character one-time code with a TTL around 10–15 minutes. That value is historical and must not be used as the current build contract.

The current DOC-C canonical auth defaults are:

- OTAC length: `10` characters.
- OTAC TTL: `5 minutes` / `300000 ms`.
- Maximum verification attempts: `5`.
- Resend cooldown: `60 seconds`.
- Lock window: `15 minutes`.
- Session TTL: `6 hours` / `21600000 ms`.
- Concurrent sessions: `5` per user.

The design explicitly says this is not MFA and not a complete zero-trust identity system; later hardening remains a design direction.

## Backend and data direction

The general source direction favors serverless and database-agnostic deployment, with a temporary session store, persistent Vault store, policy separation and immutable audit logging. The current DOC-C reference implementation target is more specific: Next.js + TypeScript, Next.js Route Handlers or a Node API, Zod, PostgreSQL, Prisma, BullMQ + Redis, email OTAC with secure cookies, blob/object storage, structured JSON logs with trace IDs, and Vitest/Playwright/Prisma integration testing.

The API architecture is Frontend → API Gateway → Core Logic → External APIs, with real provider details and keys hidden from the frontend. These are build targets, not proof of the live implementation.

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

This repository entry is a structured, source-derived project context. It is aligned to the recorded design hierarchy, but it does not establish implementation, runtime, deployment, physical robotics, performance, security or deterministic guarantees. The latest read-only observation of the separate NEXY implementation repository is tracked in the project snapshot; it is not treated as current proof until exact-head validation and DOC-E evidence exist.
