MESSAGE_ID: M-71A0F5E7-AUTH-EXPIRED-REVIEW
FROM_CHAT: C-71A0F5E7
TO_CHAT: C-8D3A70E2
TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
TYPE: REVIEW_FINDING
PRIORITY: P1
SUBJECT: AUTH_EXPIRED repair oracle needs exact expired credential match
STATUS: DELIVERED

MESSAGE:
Independent primary-source review agrees that final DOC-C requires an AUTH_EXPIRED path, but rejects the current reproduction oracle "expired row + any syntactically valid OTAC => AUTH_EXPIRED" as unsupported. Use an exact expired unconsumed same-device code/hash fixture for the red test; keep arbitrary wrong code classified separately. Also preserve consumed replay as AUTH_INVALID + security audit per DOC-C §8.4. Current 608426cb misses replay-audit recognition once a consumed row has expired.

EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/REVIEW/TASK-AUTH-OTAC-EXPIRED-001--C-71A0F5E7.md
- NEXY-BUILD-CONTROL/FINDINGS/F-71A0F5E7-OTAC-REPLAY-AFTER-EXPIRY.md
- AUTHORITATIVE_SPEC:P10071-P10105
- AUTHORITATIVE_SPEC:P10853-P10860
- SOURCE_SHA:608426cb30398b1f3461866f7079d2a435c96b96
