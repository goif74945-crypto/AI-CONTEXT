# Evidence Record

Local verification session: 2026-10-05 +07:00.

- E1 \`python -m py_compile nmaf.py test_nmaf.py demo.py\` -> PASS.
- E1 AST boundary scan of \`nmaf.py\` -> PASS, zero forbidden imports/calls.
- E2 \`python -m unittest -v test_nmaf.py\` -> PASS, 22/22 tests.
- E2 second unit run -> PASS.
- E2 \`python demo.py\` -> PASS; relation passed, failing fixture minimized to \`{"trigger":"FREEZE"}\`, mandatory/optional schedule fit budget without freeze.
- Local exact-content manifest is in \`evidence/local-manifest.json\` with SHA-256, Git blob SHA-1 and byte length.

Not proven: NEXY runtime integration; deployment; E3/E4/E5/E6; external-executor sandbox security; mathematical global minimality; globally optimal scheduling; promotion into current DOC-C.
