# คลังข้อมูลเสริม — NEXY.AI Future Knowledge Pack

Status: ACTIVE / additive-only knowledge
Created: 2026-10-05
Target project: goif74945-crypto/NEXY.AI- (READ-ONLY evidence source)
Storage repo: goif74945-crypto/AI-CONTEXT
Chat reference: current ChatGPT conversation, 2026-10-05T01:09+07:00

## Purpose
คลังนี้เก็บความรู้เสริมที่ไม่ควรแก้ source-of-truth ของ NEXY.AI โดยตรง แต่ช่วยการออกแบบ ตรวจสอบ วิจัย red-team และตัดสินใจในอนาคต

## Observed project invariants
FACT — จาก branch NEXY.ai:
- package.json ระบุหลัก “One Output. One Truth. Or Freeze. Silence is better than a wrong answer.”
- มี contract/integration/coverage/typecheck/boundary/static-determinism/six-system/canon-source gates
- มี evidence sealing และ historical verification scripts
- NX Language v0.1 กำหนด deterministic parsing/compilation, explicit failure, no hidden authority
- NX UI event เป็น request envelope เท่านั้น ไม่ใช่ authority
- NX v0.1 ห้าม clock/randomness/filesystem/network/database/process/env/hidden I/O ใน core
- Docker validation ผูก exact source identity และ rerun nonce เพื่อบังคับ rerun proof gates
- Rust authority path และ Node/Next product path ถูก validate ใน image เดียวกัน

## Knowledge packs
1. 01_EVIDENCE_ARCHITECTURE.md — evidence graph และ proof lifecycle
2. 02_CONTEXT_ENGINE.md — retrieval/context architecture
3. 03_AGENTIC_SECURITY.md — threat model สำหรับ agent/tool/memory
4. 04_FAILURE_TAXONOMY.md — failure classes + FREEZE policy
5. 05_EVALS_AND_REGRESSION.md — eval architecture
6. 06_FUTURE_RESEARCH_BACKLOG.md — งานวิจัยต่อยอดที่ไม่แตะ NEXY source

## Authority rule
เอกสารในโฟลเดอร์นี้เป็น SECONDARY / ADVISORY CONTEXT เท่านั้น
ห้าม override authoritative specification, sealed evidence, project source, explicit user directive หรือ deterministic contract ของ NEXY.AI

## Trust labels
ทุกข้อควรตีความเป็นหนึ่งใน:
- FACT_PROJECT: ตรวจจาก NEXY.AI โดยตรง
- FACT_EXTERNAL: ตรวจจากแหล่งภายนอกที่ระบุ
- PROPOSAL: แนวทางเสนอ ยังไม่ใช่ requirement
- HYPOTHESIS: ต้องทดสอบ
- UNKNOWN: หลักฐานไม่พอ

## Stop rule
ถ้า context ขัดกับ project authority ให้ FREEZE การสรุป ไม่เลือกข้างด้วยการเดา
