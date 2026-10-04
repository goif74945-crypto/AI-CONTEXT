from __future__ import annotations

from dataclasses import dataclass

from .model import Locale, ReasonCode, RecoveryIntent


@dataclass(frozen=True, slots=True)
class ReasonPolicy:
    title_en: str
    title_th: str
    summary_en: str
    summary_th: str
    allowed_intents: frozenset[RecoveryIntent]
    suppress_evidence_when_restricted: bool = False
    force_dependency_recheck_unsafe: bool = False

    def title(self, locale: Locale) -> str:
        return self.title_th if locale is Locale.TH else self.title_en

    def summary(self, locale: Locale) -> str:
        return self.summary_th if locale is Locale.TH else self.summary_en


INTENT_PRIORITY: tuple[RecoveryIntent, ...] = (
    RecoveryIntent.PROVIDE_REQUIRED_INPUT,
    RecoveryIntent.RESOLVE_AUTHORITY_CONFLICT,
    RecoveryIntent.REFRESH_EVIDENCE,
    RecoveryIntent.REQUEST_AUTHORITY_REVIEW,
    RecoveryIntent.RECHECK_DEPENDENCY,
    RecoveryIntent.ADJUST_SCOPE,
    RecoveryIntent.ESCALATE_OPERATOR,
    RecoveryIntent.ACKNOWLEDGE_STATE,
)


REASON_POLICIES: dict[ReasonCode, ReasonPolicy] = {
    ReasonCode.MISSING_REQUIRED_INPUT: ReasonPolicy(
        title_en="Input required before execution can continue",
        title_th="ต้องมีข้อมูลเพิ่มก่อนจึงจะทำงานต่อได้",
        summary_en="Required input is missing. NEXY stopped instead of guessing.",
        summary_th="ข้อมูลที่จำเป็นยังไม่ครบ NEXY จึงหยุดแทนการเดา",
        allowed_intents=frozenset({
            RecoveryIntent.PROVIDE_REQUIRED_INPUT,
            RecoveryIntent.ADJUST_SCOPE,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
    ),
    ReasonCode.AUTHORITY_CONFLICT: ReasonPolicy(
        title_en="Authority conflict requires resolution",
        title_th="พบความขัดแย้งด้านอำนาจที่ต้องแก้ก่อน",
        summary_en="Two or more authoritative instructions conflict. No side was selected automatically.",
        summary_th="คำสั่งที่มีอำนาจมากกว่าหนึ่งชุดขัดแย้งกัน ระบบไม่ได้เลือกฝ่ายใดเอง",
        allowed_intents=frozenset({
            RecoveryIntent.RESOLVE_AUTHORITY_CONFLICT,
            RecoveryIntent.REQUEST_AUTHORITY_REVIEW,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
        force_dependency_recheck_unsafe=True,
    ),
    ReasonCode.POLICY_CONFLICT: ReasonPolicy(
        title_en="Policy conflict blocks the requested operation",
        title_th="ข้อขัดแย้งด้านนโยบายทำให้การทำงานนี้ถูกบล็อก",
        summary_en="The requested operation conflicts with an active policy or law boundary.",
        summary_th="การทำงานที่ร้องขอขัดกับนโยบายหรือขอบเขตกฎที่มีผลอยู่",
        allowed_intents=frozenset({
            RecoveryIntent.REQUEST_AUTHORITY_REVIEW,
            RecoveryIntent.ADJUST_SCOPE,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
        force_dependency_recheck_unsafe=True,
    ),
    ReasonCode.INSUFFICIENT_EVIDENCE: ReasonPolicy(
        title_en="More evidence is required",
        title_th="ต้องมีหลักฐานเพิ่ม",
        summary_en="The available evidence does not support a safe verified result.",
        summary_th="หลักฐานที่มีอยู่ยังไม่เพียงพอสำหรับผลลัพธ์ที่ตรวจสอบได้อย่างปลอดภัย",
        allowed_intents=frozenset({
            RecoveryIntent.REFRESH_EVIDENCE,
            RecoveryIntent.PROVIDE_REQUIRED_INPUT,
            RecoveryIntent.ADJUST_SCOPE,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
    ),
    ReasonCode.DEPENDENCY_UNAVAILABLE: ReasonPolicy(
        title_en="A required dependency is unavailable",
        title_th="บริการหรือองค์ประกอบที่จำเป็นยังไม่พร้อมใช้งาน",
        summary_en="Execution is blocked by a dependency. State was preserved instead of fabricating a result.",
        summary_th="การทำงานติดที่องค์ประกอบภายนอก ระบบจึงรักษาสถานะไว้แทนการสร้างผลลัพธ์เทียม",
        allowed_intents=frozenset({
            RecoveryIntent.RECHECK_DEPENDENCY,
            RecoveryIntent.ADJUST_SCOPE,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
    ),
    ReasonCode.SECURITY_INTEGRITY: ReasonPolicy(
        title_en="Execution frozen for security or integrity",
        title_th="ระบบถูกแช่แข็งเพื่อความปลอดภัยหรือความถูกต้อง",
        summary_en="A security or integrity condition requires containment. Sensitive details are intentionally limited.",
        summary_th="พบเงื่อนไขด้านความปลอดภัยหรือความถูกต้องที่ต้องควบคุม รายละเอียดที่อ่อนไหวถูกจำกัดโดยตั้งใจ",
        allowed_intents=frozenset({
            RecoveryIntent.ESCALATE_OPERATOR,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
        suppress_evidence_when_restricted=True,
        force_dependency_recheck_unsafe=True,
    ),
    ReasonCode.INVALID_STATE_TRANSITION: ReasonPolicy(
        title_en="The requested state transition is not legal",
        title_th="การเปลี่ยนสถานะที่ร้องขอไม่ถูกต้องตามกฎ",
        summary_en="The requested transition is not permitted from the current state.",
        summary_th="สถานะปัจจุบันไม่อนุญาตให้เปลี่ยนไปยังสถานะที่ร้องขอ",
        allowed_intents=frozenset({
            RecoveryIntent.REQUEST_AUTHORITY_REVIEW,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
        force_dependency_recheck_unsafe=True,
    ),
    ReasonCode.STALE_EVIDENCE: ReasonPolicy(
        title_en="Evidence is stale for the current target",
        title_th="หลักฐานเก่าเกินไปสำหรับเป้าหมายปัจจุบัน",
        summary_en="Existing proof does not match the current version or target and must be refreshed.",
        summary_th="หลักฐานเดิมไม่ตรงกับเวอร์ชันหรือเป้าหมายปัจจุบัน จึงต้องตรวจใหม่",
        allowed_intents=frozenset({
            RecoveryIntent.REFRESH_EVIDENCE,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
    ),
    ReasonCode.PERMISSION_DENIED: ReasonPolicy(
        title_en="Current authority does not permit the operation",
        title_th="อำนาจปัจจุบันไม่อนุญาตการทำงานนี้",
        summary_en="The current authority scope does not permit the requested operation.",
        summary_th="ขอบเขตอำนาจปัจจุบันไม่อนุญาตการทำงานที่ร้องขอ",
        allowed_intents=frozenset({
            RecoveryIntent.REQUEST_AUTHORITY_REVIEW,
            RecoveryIntent.ESCALATE_OPERATOR,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
        force_dependency_recheck_unsafe=True,
    ),
    ReasonCode.INTERNAL_INVARIANT: ReasonPolicy(
        title_en="An internal invariant was violated",
        title_th="เงื่อนไขคงที่ภายในระบบถูกละเมิด",
        summary_en="NEXY detected a state that violates an internal invariant and stopped safely.",
        summary_th="NEXY พบสถานะที่ละเมิดเงื่อนไขคงที่ภายใน จึงหยุดอย่างปลอดภัย",
        allowed_intents=frozenset({
            RecoveryIntent.ESCALATE_OPERATOR,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
        force_dependency_recheck_unsafe=True,
    ),
    ReasonCode.UNKNOWN_REASON: ReasonPolicy(
        title_en="Execution is frozen",
        title_th="การทำงานถูกแช่แข็ง",
        summary_en="The system cannot safely classify the blocking reason. No additional cause was inferred.",
        summary_th="ระบบไม่สามารถจำแนกสาเหตุที่บล็อกได้อย่างปลอดภัย และไม่ได้เดาสาเหตุเพิ่มเติม",
        allowed_intents=frozenset({
            RecoveryIntent.ESCALATE_OPERATOR,
            RecoveryIntent.ACKNOWLEDGE_STATE,
        }),
        force_dependency_recheck_unsafe=True,
    ),
}
