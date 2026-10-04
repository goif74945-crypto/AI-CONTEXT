from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conformance" / "truth_surface_checker.py"
SPEC = importlib.util.spec_from_file_location("truth_surface_checker", PATH)
assert SPEC and SPEC.loader
m = importlib.util.module_from_spec(SPEC)
sys.modules["truth_surface_checker"] = m
SPEC.loader.exec_module(m)

ROLES = ["OWNER", "OPERATOR", "AUDITOR", "SYSTEM", "PUBLIC_USER"]
CASES = [
    ("INIT", "OK"), ("READY", "OK"), ("RUNNING", "OK"), ("VERIFYING", "OK"),
    ("CONSENSUS", "OK"), ("STABLE", "OK"), ("STABLE", "DEGRADED"),
    ("FREEZE", "FREEZE"), ("STOP", "STOP")
]


def backend(state, status):
    b = {"status": status, "state": state, "request_id": "req", "trace_id": "trace", "data": {}}
    if state == "STABLE": b["data"] = {"accepted": True, "releaseable": True, "integrity_hash": "hash"}
    if state == "FREEZE": b["freeze"] = {"recoverable": True}
    return b


def clean_surface(state, status, role):
    s = {
        "displayed_status": status, "displayed_state": state, "headline": state.title(),
        "summary": "Authoritative state.", "result_visible": False, "result": None,
        "actions": [], "request_id": "req", "trace_id": "trace"
    }
    if state == "STABLE": s.update(result_visible=True, result={"ok": True}, headline="Verified result")
    if state == "FREEZE" and role == "OWNER":
        s["actions"] = [{"id":"recover","kind":"MUTATION_REQUEST","requires_backend_authorization":True,"requires_confirmation":True}]
    if state == "READY" and role in {"OWNER","OPERATOR"}:
        s["actions"] = [{"id":"new_directive","kind":"MUTATION_REQUEST","requires_backend_authorization":True}]
    return s


def main():
    clean = 0
    injected = 0
    caught = 0
    failures = []
    for state, status in CASES:
        for role in ROLES:
            b = backend(state, status)
            s = clean_surface(state, status, role)
            r = m.audit_surface(b, s, role)
            if not r.conformant:
                failures.append(("clean", state, status, role, [v.code for v in r.violations]))
            else:
                clean += 1

            mutations = []
            x = dict(s); x["trace_id"] = "wrong"; mutations.append(("trace", x, "TRACE_ID_MISMATCH"))
            x = dict(s); x["displayed_state"] = "READY" if state != "READY" else "RUNNING"; mutations.append(("state", x, "STATE_MISMATCH"))
            if state in m.PENDING_STATES:
                x = dict(s); x["result_visible"] = True; x["result"] = {"leak": 1}; mutations.append(("pending_result", x, "PENDING_RESULT_LEAK"))
                x = dict(s); x["headline"] = "Completed successfully"; mutations.append(("pending_copy", x, "PENDING_SUCCESS_COPY"))
            if state == "FREEZE":
                x = dict(s); x["result_visible"] = True; x["result"] = {"leak":1}; mutations.append(("freeze_result", x, "FREEZE_RESULT_LEAK"))
            if state == "STOP":
                x = dict(s); x["actions"] = [{"id":"recover","kind":"MUTATION_REQUEST","requires_backend_authorization":True,"requires_confirmation":True}]; mutations.append(("stop_mutation", x, "STOP_MUTATION_ACTION"))
            if state == "STABLE":
                b2 = dict(b); b2["data"] = {}; x = dict(s); mutations.append(("stable_no_proof", (b2, x), "RELEASE_PROOF_MISSING"))

            for name, specimen, expected in mutations:
                injected += 1
                if isinstance(specimen, tuple): bx, sx = specimen
                else: bx, sx = b, specimen
                report = m.audit_surface(bx, sx, role)
                got = {v.code for v in report.violations}
                if expected in got: caught += 1
                else: failures.append((name, state, status, role, expected, sorted(got)))

    print({"clean_cases": clean, "injected_defects": injected, "caught": caught, "failures": len(failures)})
    if failures:
        for f in failures[:20]: print(f)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
