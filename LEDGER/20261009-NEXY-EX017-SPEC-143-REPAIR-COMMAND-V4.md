# LEDGER 20261009-NEXY-EX017-SPEC-143-REPAIR-COMMAND-V4
TASK_ID: 20261009-NEXY-EX017-SPEC-143-REPAIR-COMMAND-V4
MODE: ตรวจ / COMMAND_DESIGN_ONLY, NOT PRODUCT BUILDER EXECUTION
SOURCE_DOCX: Actual user-uploaded แอป [NEXY-IGNIS] ที่กำลังพัฒนา(20261008-072414).docx, SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7, 12537 paragraphs; byte-equal to earlier original.
SOURCE_PRODUCT: goif74945-crypto/NEXY.AI-, branch NEXY.ai, fresh queried HEAD 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992 at this task.
SOURCE_REGISTER: EX016 local 143 JSON and prior direct GitHub product source/source-only observation; register is discovery not authoritative proof.
NEW_COMMAND: COMMANDS/20261009-NEXY-GPT6-SOL-143-FIX-UNTIL-VERIFIED-V4.md, blob eb550b1a276e8e4cc67f8ecb709cecb788237b30.
NEW_143_GATE_REGISTER: COMMANDS/20261009-NEXY-GPT6-SOL-143-ACCEPTANCE-REGISTER-V4.md, blob 1bab7b766a3ac80ea99c195d6c63fed0089cb805, exactly 143 unique source checks.
SECURITY: no production DB mutation, no forced ref update, no fake human signoff/CI results, scope is DOC-C build vs DOC-E release.
PRODUCT_MUTATION_THIS_TASK: NONE.
RUNTIME_TEST_THIS_TASK: NONE; uses earlier independently observed canonical RED result as historical prerequisite; builder must reproduce current HEAD.
VERSION: 4.
TIMESTAMP_SOURCE: 2026-10-09 user local date.

L01 FILE_HASH: both mounted DOCX copies had same SHA256, 12537 paragraphs -> ORIGINAL_BYTES_HASH_MATCH.
L02 MATRIX: 143 rows, categories 26 defaults/4 status/8 states/29 errors/19 FSM/12 routes/12 UI screens/14 UI components/7 storage/12 DOC-E. Past statuses 86 exact source match, 14 component files, 12 route exports, 12 UI screen candidate files, 6 storage literal matches, 1 storage semantic equiv unknown, 12 old blocked evidence. NONE imply all Product features done.
L03 ORIGINAL_DOCX P9837-P9845: build DOC-C, deployment DOC-E; P9889-P9899 mandatory and P9902-P9909 excluded categories; P10495-P10499 log+incident side-effects; P10925-P10948 E1-E12 actual receipts.
L04 CURRENT_CODE: NEXY.ai HEAD 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992; canonical-json.ts blob 3894381cc80648c31f38b7b88035a64ee1d9cde6 unchanged; tests/contract/canonical-json.test.ts blob 688d317063ec7201c1a2ee7815685d3caeb3de18; package.json SHA 972cd03ed7878ff6eb0cb4813e459cb0c29cd1e7.
L05 KNOWN_REPRO_OLDER_EX016: Node22 canonical JSON 10 tests, 4 pass/6 fail at old exact blob. NEW_CODE_TEST_THIS_TASK=NOT_RUN. Builder must reproduce, patch, test with dependents.
L06 NEW_GITHUB_V4: command Git blob eb550b1a276e8e4cc67f8ecb709cecb788237b30, 19322 characters; acceptance register Git blob 1bab7b766a3ac80ea99c195d6c63fed0089cb805, 39846 characters, 143 checked rows, readback success.
L07 VERIFIED_COMMAND_GATES: 11/11 structural command checks and 4/4 register checks. Product level tests/release not established.
L08 RISKS: unknown full DOC-C denominator, non-verified end-to-end tests, old stale DOC-E E11 signoff; cross-chat DOCX accessibility may differ. Explicitly distinguish scope-specific blocked from total stop.
VERDICT: COMMAND_VERIFIED_WITH_LIMITS, PRODUCT_PARTIAL.
