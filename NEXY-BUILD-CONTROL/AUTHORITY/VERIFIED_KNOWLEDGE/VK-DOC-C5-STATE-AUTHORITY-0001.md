KNOWLEDGE_ID: VK-DOC-C5-STATE-AUTHORITY-0001
CLAIM: For locked Spec SHA b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7, the final build-authority DOC-C executable matrix authorizes error->FREEZE only from RUNNING and VERIFYING; its ANY-except-STOP row applies to fatal->STOP, while owner hard-kill is a separate RUNNING/VERIFYING/CONSENSUS -> FREEZE action. The earlier ANY-except-STOP error table is pre-FINAL-VERDICT historical text and is not the active build oracle.
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
EVIDENCE:
- Primary spec P09834-P09845 establishes FINAL VERDICT and DOC-C-only build obligation.
- Primary spec P10353-P10452 contains only RUNNING/VERIFYING error->FREEZE and ANY-except-STOP fatal->STOP.
- Primary spec P10470-P10485 defines separate Owner Actions.
- Historical conflicting table is P08562-P08634 before FINAL VERDICT.
- Exact integration source shows TS 26 transitions vs Rust 21, with only five extra TS error edges.
VERIFIED_BY: C-6B8D31F5
VALID_FROM: 2026-10-05T17:14:00+07:00
INVALIDATED_BY: none
STATUS: VERIFIED
