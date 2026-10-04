from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _shape(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _shape(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        kinds = sorted({_canon(_shape(v)) for v in value})
        return {"type": "list", "item_shapes": kinds}
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    return type(value).__name__


@dataclass(frozen=True)
class Probe:
    probe_id: str
    critical: bool = False


@dataclass(frozen=True)
class Observation:
    probe_id: str
    status: str
    output: Any

    def signature(self) -> str:
        normalized = {"status": self.status, "shape": _shape(self.output)}
        return sha256(_canon(normalized).encode("utf-8")).hexdigest()


def evaluate(probes: Iterable[Probe], baseline: Iterable[Observation], candidate: Iterable[Observation]) -> dict[str, Any]:
    probe_map: dict[str, Probe] = {}
    for p in probes:
        if not p.probe_id or p.probe_id in probe_map:
            raise ValueError("probe IDs must be non-empty and unique")
        probe_map[p.probe_id] = p

    def index(items: Iterable[Observation]) -> dict[str, Observation]:
        out: dict[str, Observation] = {}
        for item in items:
            if item.probe_id in out:
                raise ValueError(f"duplicate observation: {item.probe_id}")
            out[item.probe_id] = item
        return out

    b, c = index(baseline), index(candidate)
    diffs: list[dict[str, Any]] = []
    critical_failure = False

    for pid in sorted(probe_map):
        p = probe_map[pid]
        bo, co = b.get(pid), c.get(pid)
        if bo is None:
            raise ValueError(f"trusted baseline missing probe {pid}")
        if co is None:
            diffs.append({"probe_id": pid, "kind": "missing_candidate", "critical": p.critical})
            critical_failure |= p.critical
            continue
        if bo.signature() != co.signature():
            diffs.append({
                "probe_id": pid,
                "kind": "behavior_drift",
                "critical": p.critical,
                "baseline_signature": bo.signature(),
                "candidate_signature": co.signature(),
            })
            critical_failure |= p.critical

    extras = sorted(set(c) - set(probe_map))
    for pid in extras:
        diffs.append({"probe_id": pid, "kind": "unknown_candidate_probe", "critical": False})

    status = "FREEZE" if critical_failure else ("DRIFT" if diffs else "PASS")
    baseline_fp = sha256(_canon({k: b[k].signature() for k in sorted(probe_map)}).encode()).hexdigest()
    candidate_known = {k: c[k].signature() for k in sorted(c) if k in probe_map}
    candidate_fp = sha256(_canon(candidate_known).encode()).hexdigest()
    return {"status": status, "differences": diffs, "baseline_fingerprint": baseline_fp, "candidate_fingerprint": candidate_fp}
