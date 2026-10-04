# LICPL Bundle Restore & Verification

This file documents how to reconstruct the exact standalone NEXY Lo4 Innovation Containment Lab payload preserved in this folder.

## Transport boundary

The `bundle/*.b64` files are transport fragments only. Their contents must be concatenated **without separators or added newlines** in this exact order:

1. `bundle/BUNDLE.part00.b64`
2. `bundle/BUNDLE.part01.b64`
3. `bundle/BUNDLE.part02.b64`
4. `bundle/BUNDLE.part03.b64`
5. `bundle/BUNDLE.part04a.b64`
6. `bundle/BUNDLE.part04b.b64`
7. `bundle/BUNDLE.part04c.b64`
8. `bundle/BUNDLE.part05.b64`

The split into 04a/04b/04c is transport-only. It reconstructs the original part04 bytes exactly.

## Reconstruct

Example on a POSIX shell:

```bash
cat \
  bundle/BUNDLE.part00.b64 \
  bundle/BUNDLE.part01.b64 \
  bundle/BUNDLE.part02.b64 \
  bundle/BUNDLE.part03.b64 \
  bundle/BUNDLE.part04a.b64 \
  bundle/BUNDLE.part04b.b64 \
  bundle/BUNDLE.part04c.b64 \
  bundle/BUNDLE.part05.b64 \
  > BUNDLE.full.b64

base64 -d BUNDLE.full.b64 > NEXY-LO4-INNOVATION-CONTAINMENT-LAB.tar.gz
sha256sum NEXY-LO4-INNOVATION-CONTAINMENT-LAB.tar.gz
```

Required decoded archive SHA-256:

`c592552347f3a8f69b4c80b64748ae244651d221834d702173afa0c7eda48498`

Expected decoded archive size: **38,462 bytes**.

Expected concatenated base64 size: **51,284 characters**.

## Extract

```bash
mkdir restored
tar -xzf NEXY-LO4-INNOVATION-CONTAINMENT-LAB.tar.gz -C restored
cd restored
```

The archive contains the standalone project files including:
- Design and architecture documents
- five concept specifications
- Python reference implementation
- unit/adversarial/integration tests
- stress/property harnesses
- policy/secret verification scripts
- raw evidence outputs
- failure/fix audit
- final audit
- `PROJECT_MANIFEST.json`
- `MANIFEST.sha256`

The internal project manifest identity captured at seal time is:

`843c4f7a2618aa980e911e541c72093a83c301a9e61267e97eb7df3bc861eb31`

Manifest inventory: **49 entries / 135,611 bytes**.

## Re-run standalone verification

```bash
python3 -m compileall -q nexy_lo4_lab tests scripts
PYTHONHASHSEED=1 python3 run_tests.py
PYTHONHASHSEED=777 python3 run_tests.py
STRESS_SEED=1 python3 scripts/stress_properties.py
STRESS_SEED=777 python3 scripts/stress_properties.py
python3 scripts/verify_policy.py
python3 demo.py
```

Expected captured results:
- 48/48 tests PASS under hash seed 1
- 48/48 tests PASS under hash seed 777
- 1,203 stress/property checks PASS at seed 1
- 1,203 stress/property checks PASS at seed 777
- policy audit: 7 core files, 0 violations
- schema parse: PASS
- demo composition: PASS

## Authority warning

Successful reconstruction or successful local tests **do not promote these ideas into NEXY Canon**. The highest state produced by this Lo4 research artifact is `ELIGIBLE_FOR_HUMAN_REVIEW`.

NEXY integration/runtime/deployment remains `NOT_VERIFIED`.
