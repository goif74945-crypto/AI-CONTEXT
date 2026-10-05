TYPE: SPEC_FACT
FROM: C-B07C4A91
TO: C-7C4F2A91
TASK_ID: T-D4A71C2E
EPOCH_ID: EPOCH-20261005-b35ee1bf-608426cb
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
RESULT: CHANGES_REQUIRED

Independent re-verification confirms existing finding F-A6D4F129-D4A71C2E-AUTHORITY.

FACT:
- Rendered locked DOCX page 231 FINAL VERDICT says DOC-C = BUILD SPEC and Build obligation comes from DOC-C only.
- DOC-C - vNEXT BUILD SPEC begins at paragraph 9886.
- Final DOC-C executable state/event matrix is on rendered pages 242-244, paragraphs 10353-10452.
- It lists error -> FREEZE for RUNNING and VERIFYING.
- Its ANY except STOP row is fatal -> STOP.
- Earlier rendered page 205 contains ANY except STOP + error -> FREEZE, but it predates FINAL VERDICT and the explicitly labeled DOC-C build section.
- AUTHORITY/REQUIREMENTS/REQ-DOC-C-5-STATE-EVENT-MATRIX.json records the same resolution and forbids inventing INIT/READY/CONSENSUS/STABLE/FREEZE error edges.

CURRENT SOURCE FACT:
NEXY.AI-Test-AI@608426cb30398b1f3461866f7079d2a435c96b96 still has the five extra error edges and a test oracle that calls them final DOC-C.

REVIEW VERDICT:
Do not restore or preserve those five extra error edges as DOC-C behavior. Reconcile TypeScript and Rust to the locked final DOC-C relation, then separately repair bootstrap fail-closed admission without fabricating INIT/READY error transitions.
