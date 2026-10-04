# Observability & Incident Knowledge

## Observability Contract
ทุก critical flow ควรตอบได้ว่า request เริ่มไหน, ผ่าน component ใด, ใช้ dependency อะไร, เปลี่ยน state อะไร, จบแบบใด และใช้เวลาเท่าไร.

## Signals
Metrics: aggregate behavior/trends.
Logs: discrete events พร้อม context.
Traces: causal path ข้าม boundaries.
Audit events: security/administrative mutation history.

## Correlation
ใช้ correlation/trace ID ข้าม async boundaries เมื่อเป็นไปได้. หลีกเลี่ยง PII/secrets ใน telemetry.

## Golden Failure Signals
error rate; latency; saturation; queue depth/age; dependency failure; retry rate; timeout rate; data validation rejection; authorization denial anomalies.

## SLO Reasoning
กำหนด user-visible success ก่อน metric. SLI ต้องวัดสิ่งที่ผู้ใช้ได้รับจริง. Error budget ใช้เป็นกลไก trade-off reliability กับ change velocity.

## Incident Record
impact, start/detection/containment/recovery times, affected scope, trigger, contributing factors, detection gap, response gap, root causes, corrective actions, evidence, regression prevention.

## Postmortem Rule
หลีกเลี่ยงสรุปว่า "human error" เป็น root cause สุดท้าย. ถามว่าระบบอนุญาต ตรวจไม่พบ หรือกู้คืนยากเพราะอะไร.

## Alert Quality
alert ต้อง actionable, มี owner, severity, runbook/context และหลีกเลี่ยง duplicate noise. Alert ที่ไม่มี action มักกลายเป็น wallpaper.
