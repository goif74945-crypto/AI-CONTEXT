# Publication Evidence Seal

Status: `Lo4_AI_PROPOSAL_ONLY`
Mission code: `CHAT-20261005-0222-NEXY-LO4-PROOF-COMPILER-LAB`
Evidence target branch before this seal: `lo4-proof-compiler-lab-0222@46a4035f6eacc1c171d5a3049a619f4f3470aa47`

## Runtime evidence bound to exact source/test bytes

The local verification copy was byte-aligned to the GitHub branch blobs listed below before the final execution.

Final execution:
- `PYTHONPATH=src python -m compileall -q src tests` -> PASS
- `PYTHONPATH=src python -m unittest discover -s tests -v` -> 50 tests, 0 failures, 0 errors, OK
- `PYTHONPATH=src python run_reference.py` -> PASS

Reference integration output:
- authority digest: `36e26b6928893c6511f3750d19b977469b7c201824c08383714a1839a60ff46d`
- proof probes: `unit-check`
- witness kinds: `positive,negative,missing`
- compile status: `PASS`
- compile digest: `91ca5b1b7633caddd7af880c647c47107906961016f1c05174584fe5f28128d2`

## Git blob identity manifest

```text
7a5d5946421572b793a5e504e42419e0a59e78db  README.md
47a33512af1d74c931bbecaab792268822e5a2b8  01_ARCHITECTURE.md
9505d4ebbc4af8ff4ed8bd617d1b675f675dfd3f  02_REQUIREMENT_LEDGER.md
e8d0cfa216d056f3c5b3d886449c1ba46be2d092  03_INTEGRATION_CONTRACT.md
e4d45c643c3f3d5f598902a897e60f7a57d1ab15  04_NOVELTY_MATRIX.md
0505529e2bb6c830c33c2a34da4b0e48df218de7  EVIDENCE.md
05ac31be85f9f1755d476cad325bac656a2bf4ff  FINAL_AUDIT.md
606430514ba19d11e3195aa03e076a53c7856cf9  run_reference.py
8f99c82ee748783837c62594e122ceef966095b2  src/nexy_lo4_lab/__init__.py
f371f4bdd62f660b945f65550375280857bdea7a  src/nexy_lo4_lab/authority.py
6046fa51b240f341c67e50f53fef390826845bee  src/nexy_lo4_lab/integration.py
294f41cb2c1944bb01f4fe8a58eff55405076653  src/nexy_lo4_lab/output_compiler.py
e2337a67e7e7b053c071e6c0d3c18491043b3ee7  src/nexy_lo4_lab/planner.py
b8e67f4fbaa3f07dedd70575bea73ace9ec6a8cc  src/nexy_lo4_lab/uncertainty.py
f197be955b7df35648801198f305126b6f60ca42  src/nexy_lo4_lab/witness.py
45b40003c49d43309bd834dc11e8ad5cd972c52a  tests/test_adversarial.py
394465b6667c20e56fd0dca488b936772feefe92  tests/test_authority.py
aa309e2fc98bf37157c8b1f7e3920a21bc87e0a4  tests/test_integration.py
9c9e79b4b1cbdc40bd4cf14bfbbeaa0233cc9c0d  tests/test_output_compiler.py
5eda07a35f04a11e35efd312851a5ade1dc292b0  tests/test_planner.py
82fceee7c87b0d65e39d3bacbf4a6d334a846d50  tests/test_uncertainty.py
01630e8c3000437509fb79e8993a9bd7564a7a8e  tests/test_witness.py
```

## Boundary
This seal proves the isolated branch bytes and local execution above correspond for the listed source/test artifacts. It does not prove NEXY.AI integration, production deployment, or Canon promotion.
