from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from lo4q64 import Q64, SPECS, evaluate  # noqa: E402


def main() -> None:
    out = []
    for idx, cid in enumerate(sorted(SPECS), start=1):
        spec = SPECS[cid]
        values = {k: Q64.from_basis_points(((idx * 997) + i * 613) % 10001) for i, k in enumerate(spec.required_inputs)}
        out.append(evaluate(cid, values).as_dict())
    print(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
