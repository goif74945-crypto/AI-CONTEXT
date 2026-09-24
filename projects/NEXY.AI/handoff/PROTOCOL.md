# NEXY Cross-Chat Handoff Protocol

Every handoff package must contain:

- CHAT_ID
- ROLE
- TASK
- exact repository / branch / HEAD
- SCOPE
- INPUT
- OUTPUT
- CLAIMS
- PROOF
- TESTS
- CHANGES
- FINDINGS
- UNRESOLVED
- NEXT_ACTION

## Rules
1. Refresh HEAD before resuming.
2. If HEAD changed, previous implementation/test/evidence claims become historical until refreshed.
3. A claim must state its proof class: source / implementation presence / executed test / runtime / deployment / physical.
4. No “another chat said it was done” claim is authoritative without artifact/proof references.
5. Preserve unresolved items; do not silently convert them to assumptions.
6. The receiver should load the Context Router pack for the next task rather than the whole project.
