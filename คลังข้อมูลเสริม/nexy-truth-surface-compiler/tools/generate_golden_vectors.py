from __future__ import annotations

import json
from pathlib import Path

from nxts import compile_payload

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ["release.json", "freeze-unknown.json", "freeze-conflict.json"]

vectors = []
for name in FIXTURES:
    payload = json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))
    result = compile_payload(payload)
    vectors.append({
        "fixture": name,
        "input_sha256": result["receipt"]["input_sha256"],
        "output_sha256": result["receipt"]["output_sha256"],
        "decision": result["decision"],
        "freeze_codes": [x["code"] for x in result["freeze_reasons"]],
        "canonical_output": result,
    })

out = ROOT / "fixtures" / "golden-vectors.json"
out.write_text(json.dumps({"schema": "nxts.golden-vectors.v0", "vectors": vectors}, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
print(out)
