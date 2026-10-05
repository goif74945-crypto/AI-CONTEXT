FINDING_ID: F-71A0F5E7-OTAC-REPLAY-AFTER-EXPIRY
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P2_HARDENING
STATUS: NON_REQUIRED_HARDENING
TYPE: AUDIT_TELEMETRY_HARDENING

OBSERVED:
The current verify path recognizes consumed-code reuse only while the stored row is still live. After expiry the same stored row is rejected through the generic invalid path.

AUTHORITY:
The previous record cited paragraph 10863 replay-prevention text as final DOC-C. That is incorrect because locked final DOC-C ends at 10499. Final DOC-C does not explicitly require special audit telemetry for reuse after expiry.

CLASSIFICATION:
This behavior may be useful hardening but it does not block required DOC-C closure unless another active authority is bound. Rejection of expired or consumed credentials must remain intact.

SOURCE_MUTATION: NONE
