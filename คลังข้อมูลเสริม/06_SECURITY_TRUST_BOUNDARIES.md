# Security & Trust Boundaries

## Core Rule
ทุก external/user/model/tool input เป็น untrusted จนผ่าน validation ตาม boundary.

## Checklist
identity; authentication; authorization; input validation; output encoding; secret handling; tenant isolation; data classification; auditability; rate/resource limits; replay protection; dependency trust.

## Authorization
ตรวจสิทธิ์ที่ server-side enforcement point. แยก authentication จาก authorization. Object-level access ต้องตรวจ object จริง ไม่ใช่เพียง role.

## Secret Rules
ห้ามเก็บ secret ใน context knowledge files. ห้าม log credential/token. ใช้ least privilege. ต้อง rotate/revoke ได้. secret absence ต้อง fail ชัด.

## AI-specific Threats
prompt injection; tool privilege escalation; data exfiltration; cross-context contamination; untrusted retrieved instructions; indirect prompt injection; model-generated unsafe parameters.

Defense: authority hierarchy, allowlisted tool scope, parameter validation, read/write separation, confirmation gates สำหรับ destructive action, output provenance, post-action verification.

## Fail-Closed Candidates
authorization; signature verification; tenant boundary; critical schema validation; destructive target resolution.

## Evidence
security claim ต้องผูกกับ test/evidence เช่น denied request, audit event, isolation test ไม่ใช่แค่มี component ชื่อ security.
