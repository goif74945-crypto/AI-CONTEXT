from __future__ import annotations

from dataclasses import dataclass

from .model import ActionCode, Locale, ReasonCode


@dataclass(frozen=True, slots=True)
class ReasonPolicy:
    title_en: str
    title_th: str
    summary_en: str
    summary_th: str
    allowed_actions: frozenset[ActionCode]
    suppress_evidence_when_restricted: bool = False
    force_non_retryable: bool = False

    def title(self, locale: Locale) -> str:
        return self.title_th if locale is Locale.TH else self.title_en

    def summary(self, locale: Locale) -> str:
        return self.summary_th if locale is Locale.TH else self.summary_en


ACTION_PRIORITY: tuple[ActionCode, ...] = (
    ActionCode.PROVIDE_MISSING_INPUT,
    ActionCode.REVIEW_CONFLICT,
    ActionCode.OPEN_EVIDENCE,
    ActionCode.REQUEST_AUTHORITY_REVIEW,
    ActionCode.RETRY_AFTER_DEPENDENCY,
    ActionCode.WAIT_FOR_SYSTEM,
    ActionCode.CHANGE_SCOPE,
    ActionCode.CONTACT_OPERATOR,
    ActionCode.ACKNOWLEDGE,
)


REASON_POLICIES: dict[ReasonCode, ReasonPolicy] = {
    ReasonCode.MISSING_REQUIRED_INPUT: ReasonPolicy(
        title_en="Input required before execution can continue",
        title_th="ต้องมีข้อมูลเพิ่มก่อนจึงจะทำงานต่อได้",
        summary_en="Required input is missing. NEXY stopped instead of guessing.",
        summary_th="ข้อมูลที่จำเป็นยังไม่ครบ NEXY จึงหยุดแทนการเดา",
        allowed_actions=frozenset({ActionCode.PROVIDE_MISSING_INPUT, ActionCode.CHANGE_SCOPE, ActionCode.ACKNOWLEDGE}),
    ),
    ReasonCode.AUTHORITY_CONFLICT: ReasonPolicy(
        title_en="Authority conflict requires resolution",
        title_th="พบความขัดแย้งด้านอำนาจที่ต้องแก้ก่อน",
        summary_en="Two or more authoritative instructions conflict. No side was selected automatically.",
        summary_th="คำสั่งที่มีอำนาจมากกว่าหนึ่งชุดขัดแย้งกัน ระบบไม่ได้เลือกฝ่ายใดเอง",
        allowed_actions=frozenset({ActionCode.REVIEW_CONFLICT, ActionCode.REQUEST_AUTHORITY_REVIEW, ActionCode.OPEN_EVIDENCE, ActionCode.ACKNOWLEDGE}),
        force_non_retryable=True,
    ),
    ReasonCode.POLICY_CONFLICT: ReasonPolicy(
        title_en="Policy conflict blocks the requested action",
        title_th="ข้อขัดแย้งด้านนโยบายทำให้คำสั่งนี้ถูกบล็อก",
        summary_en="The requested action conflicts with an active policy or law boundary.",
        summary_th="การกระทำที่ร้องขอขัดกับนโยบายหรือขอบเขตกฎที่มีผลอยู่",
        allowed_actions=frozenset({ActionCode.REVIEW_CONFLICT, ActionCode.REQUEST_AUTHORITY_REVIEW, ActionCode.CHANGE_SCOPE, ActionCode.ACKNOWLEDGE}),
        force_non_retryable=True,
    ),
    ReasonCode.INSUFFICIENT_EVIDENCE: ReasonPolicy(
        title_en="More evidence is required",
        title_th="ต้องมีหลักฐานเพิ่ม",
        summary_en="The available evidence does not support a safe verified result.",
        summary_th="หลักฐานที่มีอยู่ยังไม่เพียงพอสำหรับผลลัพธ์ที่ตรวจสอบได้อย่างปลอดภัย",
        allowed_actions=frozenset({ActionCode.OPEN_EVIDENCE, ActionCode.PROVIDE_MISSING_INPUT, ActionCode.CHANGE_SCOPE, ActionCode.ACKNOWLEDGE}),
    ),
    ReasonCode.DEPENDENCY_UNAVAILABLE: ReasonPolicy(
        title_en="A required dependency is unavailable",
        title_th="บริการหรือองค์ประกอบที่จำเป็นยังไม่พร้อมใช้งาน",
        summary_en="Execution is blocked by a dependency. NEXY preserved state instead of fabricating a result.",
        summary_th="การทำงานติดที่องค์ประกอบภายนอก NEXY จึงรักษาสถานะไว้แทนการสร้างผลลัพธ์เทียม",
        allowed_actions=frozenset({ActionCode.RETRY_AFTER_DEPENDENCY, ActionCode.WAIT_FOR_SYSTEM, ActionCode.CHANGE_SCOPE, ActionCode.ACKNOWLEDGE}),
    ),
    ReasonCode.SECURITY_INTEGRITY: ReasonPolicy(
        title_en="Execution frozen for security or integrity",
        title_th="ระบบถูกแช่แข็งเพื่อความปลอดภัยหรือความถูกต้อง",
        summary_en="A security or integrity condition requires containment. Sensitive details are intentionally limited.",
        summary_th="พบเงื่อนไขด้านความปลอดภัยหรือความถูกต้องที่ต้องควบคุม รายละเอียดที่อ่อนไหวถูกจำกัดโดยตั้งใจ",
        allowed_actions=frozenset({ActionCode.CONTACT_OPERATOR, ActionCode.ACKNOWLEDGE}),
        suppress_evidence_when_restricted=True,
        force_non_retryable=True,
    ),
    ReasonCode.INVALID_STATE_TRANSITION: ReasonPolicy(
        title_en="The requested state transition is not legal",
        title_th="การเปลี่ยนสถานะที่ร้องขอไม่ถูกต้องตามกฎ",
        summary_en="The requested transition is not permitted from the current state.",
        summary_th="สถานะปัจจุบันไม่อนุญาตให้เปลี่ยนไปยังสถานะที่ร้องขอ",
        allowed_actions=frozenset({ActionCode.OPEN_EVIDENCE, ActionCode.REQUEST_AUTHORITY_REVIEW, ActionCode.ACKNOWLEDGE}),
        force_non_retryable=True,
    ),
    ReasonCode.STALE_EVIDENCE: ReasonPolicy(
        title_en="Evidence is stale for the current target",
        title_th="หลักฐานเก่าเกินไปสำหรับเป้าหมายปัจจุบัน",
        summary_en="Existing proof does not match the current version or target and must be refreshed.",
        summary_th="หลักฐานเดิมไม่ตรงกับเวอร์ชันหรือเป้าหมายปัจจุบัน จึงต้องตรวจใหม่",
        allowed_actions=frozenset({ActionCode.OPEN_EVIDENCE, ActionCode.RETRY_AFTER_DEPENDENCY, ActionCode.ACKNOWLEDGE}),
    ),
    ReasonCode.PERMISSION_DENIED: ReasonPolicy(
        title_en="Permission does not allow this action",
        title_th="สิทธิ์ปัจจุบันไม่อนุญาตการกระทำนี้",
        summary_en="The current authority scope does not permit the requested action.",
        summary_th="ขอบเขตอำนาจปัจจุบันไม่อนุญาตการกระทำที่ร้องขอ",
        allowed_actions=frozenset({ActionCode.REQUEST_AUTHORITY_REVIEW, ActionCode.CONTACT_OPERATOR, ActionCode.ACKNOWLEDGE}),
        force_non_retryable=True,
    ),
    ReasonCode.INTERNAL_INVARIANT: ReasonPolicy(
        title_en="An internal invariant was violated",
        title_th="เงื่อนไขคงที่ภายในระบบถูกละเมิด",
        summary_en="NEXY detected a state that violates an internal invariant and stopped safely.",
        summary_th="NEXY พบสถานะที่ละเมิดเงื่อนไขคงที่ภายใน จึงหยุดอย่างปลอดภัย",
        allowed_actions=frozenset({ActionCode.CONTACT_OPERATOR, ActionCode.OPEN_EVIDENCE, ActionCode.ACKNOWLEDGE}),
        force_non_retryable=True,
    ),
    ReasonCode.UNKNOWN_REASON: ReasonPolicy(
        title_en="Execution is frozen",
        title_th="การทำงานถูกแช่แข็ง",
        summary_en="The system cannot safely classify the blocking reason. No additional cause was inferred.",
        summary_th="ระบบไม่สามารถจำแนกสาเหตุที่บล็อกได้อย่างปลอดภัย และไม่ได้เดาสาเหตุเพิ่มเติม",
        allowed_actions=frozenset({ActionCode.CONTACT_OPERATOR, ActionCode.ACKNOWLEDGE}),
        force_non_retryable=True,
    ),
}


ACTION_TEXT: dict[Locale, dict[ActionCode, tuple[str, str]]] = {
    Locale.EN: {
        ActionCode.PROVIDE_MISSING_INPUT: ("Provide required input", "Supply only the missing fields listed below."),
        ActionCode.REVIEW_CONFLICT: ("Review the conflict", "Inspect the conflicting authorities before any mutation."),
        ActionCode.RETRY_AFTER_DEPENDENCY: ("Retry after recovery", "Retry only after the required dependency is healthy."),
        ActionCode.OPEN_EVIDENCE: ("Inspect evidence", "Open the evidence references associated with this freeze."),
        ActionCode.REQUEST_AUTHORITY_REVIEW: ("Request authority review", "Route this case to the authorized reviewer."),
        ActionCode.CONTACT_OPERATOR: ("Contact an operator", "Escalate to an authorized operator without bypassing the freeze."),
        ActionCode.ACKNOWLEDGE: ("Acknowledge", "Acknowledge the freeze without changing system state."),
        ActionCode.CHANGE_SCOPE: ("Change scope", "Submit a narrower or different scope that remains within policy."),
        ActionCode.WAIT_FOR_SYSTEM: ("Wait for system recovery", "Preserve the task state until the dependency recovers."),
    },
    Locale.TH: {
        ActionCode.PROVIDE_MISSING_INPUT: ("เพิ่มข้อมูลที่จำเป็น", "ส่งเฉพาะข้อมูลที่ขาดตามรายการด้านล่าง"),
        ActionCode.REVIEW_CONFLICT: ("ตรวจความขัดแย้ง", "ตรวจแหล่งอำนาจที่ขัดกันก่อนมีการเปลี่ยนแปลงใด ๆ"),
        ActionCode.RETRY_AFTER_DEPENDENCY: ("ลองใหม่หลังระบบต้นทางฟื้น", "ลองใหม่เมื่อองค์ประกอบที่จำเป็นกลับมาพร้อมแล้วเท่านั้น"),
        ActionCode.OPEN_EVIDENCE: ("ตรวจหลักฐาน", "เปิดรายการหลักฐานที่เชื่อมกับเหตุการณ์ FREEZE นี้"),
        ActionCode.REQUEST_AUTHORITY_REVIEW: ("ขอการตรวจจากผู้มีอำนาจ", "ส่งกรณีนี้ไปยังผู้ตรวจที่ได้รับสิทธิ์"),
        ActionCode.CONTACT_OPERATOR: ("ติดต่อผู้ควบคุมระบบ", "ยกระดับไปยังผู้ควบคุมที่มีสิทธิ์โดยไม่ข้าม FREEZE"),
        ActionCode.ACKNOWLEDGE: ("รับทราบ", "รับทราบสถานะโดยไม่เปลี่ยนสถานะระบบ"),
        ActionCode.CHANGE_SCOPE: ("ปรับขอบเขตงาน", "ส่งขอบเขตใหม่ที่แคบลงหรือแตกต่างแต่ยังอยู่ในนโยบาย"),
        ActionCode.WAIT_FOR_SYSTEM: ("รอระบบฟื้น", "รักษาสถานะงานไว้จนกว่าองค์ประกอบที่จำเป็นจะกลับมาพร้อม"),
    },
}
