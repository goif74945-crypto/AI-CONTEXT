# Recover the exact NECC project tree

1. Verify the base64 text file if desired:
   `sha256sum necc_project_bundle.tar.gz.base64`
   expected: `128c326a5f1253bcb5a452f79e24db2f974656150917463e57e692eca0ffa060`

2. Decode:
   `base64 -d necc_project_bundle.tar.gz.base64 > necc_project_bundle.tar.gz`

3. Verify decoded archive:
   `sha256sum necc_project_bundle.tar.gz`
   expected: `dd514ccf27f9302c286e62a4d5a185210add0a92f8b7b606a859c497e8067a6d`

4. Extract in an isolated directory:
   `tar -xzf necc_project_bundle.tar.gz`

The archive contains the complete verified Design + Code + Tests + Evidence tree.

Classification: AI-PROPOSED / RESEARCH PROTOTYPE / NOT NEXY CANON / NOT INTEGRATED INTO NEXY.
