import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
py_raw = subprocess.check_output(["python", str(root / "interop/python_wire.py")], text=True).strip()
js_raw = subprocess.check_output(["node", str(root / "interop/node_wire.mjs")], text=True).strip()
py = json.loads(py_raw)
js = json.loads(js_raw)
if py != js:
    raise SystemExit(
        "PARITY FAIL\n"
        + "PY=" + json.dumps(py, sort_keys=True, separators=(",", ":")) + "\n"
        + "JS=" + json.dumps(js, sort_keys=True, separators=(",", ":"))
    )
print("PARITY PASS")
print(json.dumps(py, sort_keys=True, separators=(",", ":")))
