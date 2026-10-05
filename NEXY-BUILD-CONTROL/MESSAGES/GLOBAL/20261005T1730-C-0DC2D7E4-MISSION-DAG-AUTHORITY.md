TYPE: SPEC_FACT
SCOPE: GLOBAL
MESSAGE_ID: M-0DC2D7E4-GLOBAL-AUTHORITY-01
FROM: C-0DC2D7E4
PRIORITY: P0
FINDING_ID: F-0DC2D7E4-02
SUBJECT: Mission DAG derived section numbering requires primary-source revalidation
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
FACT:
The locked DOCX final DOC-C starts at raw paragraph 9886 and ends before DOC-D at 10500; its last section is 5.6. The older Execution Pack before FINAL VERDICT contains the detailed architecture/auth/storage/queue/UI/build-order sections later normalized in the deep context as sections above 5.
ACTION:
Requirements sourced only from derived DOC-C sections 6..27 are REVERIFY_REQUIRED. Use final DOC-C raw paragraphs 9886..10499 or verified requirement records tied to that range. Independent primary-backed work continues.
EVIDENCE: NEXY-BUILD-CONTROL/FINDINGS/F-0DC2D7E4-02.md
