# Working Memory — NEXY Decision Capsule & Replay Lab

Status: IN_PROGRESS
Classification: AI PROPOSAL / SECONDARY ADVISORY CONTEXT
Started: 2026-10-05T01:21+07:00
Target storage: goif74945-crypto/AI-CONTEXT
Protected target: goif74945-crypto/NEXY.AI- — READ ONLY / NO MUTATION

## Objective
สร้าง reference/prototype แบบ standalone สำหรับบันทึก ตรวจสอบ และ replay provenance ของ decision/output หนึ่งรายการ โดยไม่ยก proposal ให้เป็น NEXY requirement อัตโนมัติ

## Non-goals
- ไม่แก้ source code ใน NEXY.AI
- ไม่อ้างว่า prototype นี้เป็น current NEXY implementation
- ไม่ override DOC-B / DOC-C / DOC-D / DOC-E
- ไม่แทนที่ evidence architecture, context engine, security, failure taxonomy หรือ eval packs ที่มีอยู่แล้ว

## Distinct gap
Existing supplemental packs cover release evidence, retrieval context, agentic security, failure taxonomy, evals, and research backlog.
This lab focuses on per-decision deterministic capsules:
- canonical structural identity
- tamper-evident event chain
- replayable state machine
- authority fingerprint capture
- tool side-effect pairing
- terminal-state proof rules
- structural diff for counterfactual inspection

## Current execution state
CURRENT STATE: DESIGN + LOCAL IMPLEMENTATION
COMPLETED:
- Read AI-CONTEXT bootstrap/index/kernel/router.
- Read NEXY.AI overview/deep index/current 837-row matrix summary.
- Read all existing files in คลังข้อมูลเสริม.
- Confirmed this work is additive and distinct from the six existing packs.
- Selected Python stdlib-only prototype.
IN PROGRESS:
- implementation
- local unit tests
BLOCKED:
- none
NEXT ACTION:
- implement code, run tests, repair failures, then commit verified artifacts.
VERIFICATION STATUS: NOT_VERIFIED

## Authority anchors
- AI-CONTEXT/AI-EXECUTION-KERNEL.md
- AI-CONTEXT/projects/NEXY.AI/overview.md
- AI-CONTEXT/projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md
- explicit current user directive

## Stop conditions
Freeze mutation if:
- requested path collides with another chat's work,
- task would require modifying NEXY.AI,
- proposal would be represented as canonical/current NEXY law,
- verification cannot distinguish design from implementation truth.
