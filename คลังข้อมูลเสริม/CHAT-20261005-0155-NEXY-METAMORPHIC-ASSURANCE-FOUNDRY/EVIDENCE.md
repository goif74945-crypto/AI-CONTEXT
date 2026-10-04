# Evidence Record

Chat reference: `CHAT-20261005-0155-NEXY-METAMORPHIC-ASSURANCE-FOUNDRY`
Local verification session: 2026-10-05 +07:00.

## Executed evidence
- E1 `python -m py_compile nmaf.py test_nmaf.py demo.py` -> PASS.
- E1 AST boundary scan of `nmaf.py` -> PASS, zero forbidden imports/calls.
- E2 `python -m unittest -v test_nmaf.py` -> PASS, 22/22 tests.
- E2 second unit run -> PASS.
- E2 `python demo.py` -> PASS; relation passed, failing fixture minimized to `{"trigger":"FREEZE"}`, mandatory/optional schedule fit budget without freeze.

## Repository evidence
- AI-CONTEXT PR: #49.
- Merge commit: `17392b601d487fc51c6a621486677a22db690b6a`.
- PR diff at merge preparation: 14 files, +733 lines, 0 deletions.
- Repository blob identity matched the local tested artifact for `nmaf.py`, `test_nmaf.py`, `demo.py`, and raw evidence files.
- Post-write audit detected Markdown backslash-escaping drift in documentation only; those docs were repaired in-place within this task folder and are subject to a final re-fetch audit.
- Local pre-merge manifest: `evidence/local-manifest.json`.

## Not proven
NEXY runtime integration; deployment; E3/E4/E5/E6; external-executor sandbox security; mathematical global minimality; globally optimal scheduling; promotion into current DOC-C.
