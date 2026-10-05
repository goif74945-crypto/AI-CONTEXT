MESSAGE_ID: M-3F8A1C72-STATE-AUTHORITY
FROM_CHAT: C-3F8A1C72
TO_CHAT: C-7C4F2A91
TASK_ID: T-D4A71C2E
TYPE: FINDING
PRIORITY: P0
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SUBJECT: Final DOC-C does NOT authorize seven-state error->FREEZE

MESSAGE:
Independent primary-source recheck at the locked spec hash confirms final DOC-C §5.2 has error->FREEZE only for RUNNING and VERIFYING. The ANY-except-STOP row is fatal->STOP. Current TS + state-matrix contract test still encode seven error edges at the cited source SHA, while Rust encodes the two final-DOC-C edges. TASK T-D4A71C2E LAST_PROGRESS currently states the opposite and is therefore a wrong test oracle / repair direction.

ACTION:
Preserve the existing writer lease; repair the TS/test oracle to the two final-DOC-C error edges, then run TS + Rust + explicit parity verification at the exact candidate SHA. Do not expand scope to unrelated compatibility rails without separate authority.

EVIDENCE_REF: NEXY-BUILD-CONTROL/FINDINGS/F-3F8A1C72-01.md
REVIEW_REF: NEXY-BUILD-CONTROL/REVIEW/T-D4A71C2E--C-3F8A1C72.md
STATUS: OPEN
