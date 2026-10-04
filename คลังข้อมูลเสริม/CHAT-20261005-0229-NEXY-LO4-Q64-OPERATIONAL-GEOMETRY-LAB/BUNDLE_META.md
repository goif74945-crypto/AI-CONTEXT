# Verified Bundle Metadata

Work code: `CHAT-20261005-0229-NEXY-LO4-Q64-OPERATIONAL-GEOMETRY-LAB`
Classification: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANON`
Target repository: `goif74945-crypto/AI-CONTEXT`
Protected repositories: every repository whose name contains `NEXY.AI` remained read-only.

## Canonical part order

1. `BUNDLE.part01.b64` — 6000 chars
2. `BUNDLE.part02a.b64` — 2000 chars
3. `BUNDLE.part02b.b64` — 2000 chars
4. `BUNDLE.part02c.b64` — 2000 chars
5. `BUNDLE.part03.b64` — 6000 chars
6. `BUNDLE.part04.b64` — 6000 chars
7. `BUNDLE.part05.b64` — 4760 chars

Concatenated encoded length: **28760 characters**.

## Integrity chain

- Concatenated base64 SHA-256: `577617449397dab131e2bc5e25b48699f1e009546936fa8796d67ddba2b78905`
- gzip byte length before base64: **21568 bytes**
- gzip SHA-256: `0622746009200d56cfb38ab464583cea26804ac5794e3053678d5f37198fc96c`
- Uncompressed `bundle.json` byte length: **78100 bytes**
- Uncompressed `bundle.json` SHA-256: `319aac10e8060387ced22614c305a2b3ec38a1a3831e37aa910e180c9e32d1ac`
- Bundle entry count: **19**

GitHub readback of all seven physical part files was concatenated after publication. The remote concatenation had length 28760 and SHA-256 `577617449397dab131e2bc5e25b48699f1e009546936fa8796d67ddba2b78905`, exactly matching the locally verified snapshot.

## Deterministic restore

```python
from pathlib import Path
import base64
import gzip
import json
import hashlib

names = [
    "BUNDLE.part01.b64",
    "BUNDLE.part02a.b64",
    "BUNDLE.part02b.b64",
    "BUNDLE.part02c.b64",
    "BUNDLE.part03.b64",
    "BUNDLE.part04.b64",
    "BUNDLE.part05.b64",
]

encoded = "".join(Path(name).read_text(encoding="ascii") for name in names)
assert len(encoded) == 28760
assert hashlib.sha256(encoded.encode("ascii")).hexdigest() == "577617449397dab131e2bc5e25b48699f1e009546936fa8796d67ddba2b78905"

compressed = base64.b64decode(encoded, validate=True)
assert len(compressed) == 21568
assert hashlib.sha256(compressed).hexdigest() == "0622746009200d56cfb38ab464583cea26804ac5794e3053678d5f37198fc96c"

raw = gzip.decompress(compressed)
assert len(raw) == 78100
assert hashlib.sha256(raw).hexdigest() == "319aac10e8060387ced22614c305a2b3ec38a1a3831e37aa910e180c9e32d1ac"

items = json.loads(raw.decode("utf-8"))
assert len(items) == 19
for item in items:
    path = Path(item["path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(item["content"], encoding="utf-8")
```

## Snapshot note

The bundle intentionally captures the exact locally tested Design + Code + Tests + Evidence snapshot. Its bundled `FINAL_AUDIT.md` is a **pre-persistence snapshot** and is superseded by the top-level `FINAL_AUDIT.md` beside this metadata file, which records GitHub publication/readback results and the later read-only NEXY compatibility review.
